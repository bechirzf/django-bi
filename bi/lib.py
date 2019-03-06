import glob
import hashlib
import importlib
import os
from typing import List, Tuple, Type

from django.conf import settings
from django.core.cache import cache
from django.http import QueryDict

from bi.models.report import BaseReport


def transform_python_list_to_list_for_echarts(l: list) -> str:
    """Преобразует питоновский лист в строку вида '['abc', 'efg']' для echarts.

    :param l: список, который нужно преобразовать
    :return: строка для echarts
    """
    return '[\'' + '\', \''.join([str(i) for i in l]) + '\']'


def get_entity_by_path(path: str, class_name: str, class_params: dict = None):
    """Returns class instance.

    Args:
        class_params: Parameters of class (e.g. dashboard or report).
        path: File path (e.g. dashboards/dummy1/dummy3.py).
        class_name: Class name (e.g. Dashboard).`

    Returns:
        Dashboard or Report.
    """

    cls = get_class_by_path(path, class_name)
    if cls:
        return cls(class_params)
    else:
        return None


def get_class_by_path(path: str, class_name: str):
    """Returns class definition.

    Args:
        path: File path (e.g. dashboards/dummy1/dummy3.py).
        class_name: Class name (e.g. Dashboard).`

    Returns:
        Dashboard or Report.
    """

    try:
        splitted_path = path[:-3].split('/')
        cls_path = '.'.join(splitted_path)
        spec = importlib.util.spec_from_file_location(cls_path, settings.OBJECTS_PATH + '/' + path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        cls = getattr(module, class_name)

        return cls
    except FileNotFoundError:
        return None


def get_reports_list() -> List[Type[BaseReport]]:
    """Возвращает список экземпляров отчётов.
    """
    reports_list = []
    files = glob.iglob(os.path.join(settings.OBJECTS_PATH, 'reports', '**', '[!_]*.py'), recursive=True)
    files = list(files)
    for file in sorted(files):
        file = os.path.relpath(file, settings.OBJECTS_PATH + '/')
        print(file)
        report = get_entity_by_path(file, 'Report')
        print(report)
        reports_list.append(report)
    return reports_list


def get_dashboards_hierarchy():
    """Возвращает иерархию классов дашбордов.
    """
    dashboards_hierarchy = {}
    files = glob.iglob(os.path.join(settings.OBJECTS_PATH, 'dashboards', '**', '[!_]*.py'), recursive=True)
    files = list(files)
    for file in sorted(files):
        file = os.path.relpath(file, settings.OBJECTS_PATH + '/')
        cls = get_class_by_path(file, 'Dashboard')
        if str(cls) not in [str(key) for key in dashboards_hierarchy.keys()] and len(file.split('/')) == 2:
            dashboards_hierarchy[cls] = []
        if len(file.split('/')) == 3:
            if str(cls.get_parent_dashboard_class()) not in [str(key) for key in dashboards_hierarchy.keys()]:
                dashboards_hierarchy[cls.get_parent_dashboard_class()] = [cls]
            else:
                for key in dashboards_hierarchy.keys():
                    if str(key) == str(cls.get_parent_dashboard_class()):
                        dashboards_hierarchy[key].append(cls)

    return dashboards_hierarchy


def convert_dashboard_class_to_tuple(dashboard_class) -> Tuple:
    """Преобразует класс дашборда в тупл для использования в шаблонах.

    :param dashboard_class:
    :return:
    """
    board = dashboard_class(QueryDict())
    result = [board.id,
              board.title,
              board.icon,
              dashboard_class.get_parent_dashboard_id()]
    return tuple(result)


def get_dashboards_hierarchy_for_template() -> dict:
    """Возвращает иерархию дашбордов в виде словаря туплов.
    Для чего это ... сделано: в темплейтах классы автоматически инстанцируются, поэтому сделано на туплах

    :param path_to_objects:
    :return:
    """
    dashboards_hierarchy_class = get_dashboards_hierarchy()
    dashboards_hierarchy_for_template = {}

    for dashboards_hierarchy_class_key in dashboards_hierarchy_class.keys():
        temp_key = convert_dashboard_class_to_tuple(dashboards_hierarchy_class_key)
        dashboards_hierarchy_for_template[temp_key] = []
        for dashboards_hierarchy_class_value in dashboards_hierarchy_class[dashboards_hierarchy_class_key]:
            dashboards_hierarchy_for_template[temp_key].append(
                convert_dashboard_class_to_tuple(dashboards_hierarchy_class_value))
    return dashboards_hierarchy_for_template


def cache_dataframe(fn):
    """
    Декоратор для кеширования датафрейма в методе get_dataframe датасета.

    :param fn:
    :return:
    """
    CACHE_TIMOUT = 1 * 7 * 24 * 60 * 60  # неделя

    def cache_get_key(*args):
        serialise = []
        for arg in args:
            serialise.append(str(arg))

        full_str = ''.join(serialise).encode('utf-8')
        key = hashlib.md5(full_str).hexdigest()
        return key

    def memoized_func(dataset, params=None):
        _cache_key = cache_get_key(fn.__name__, type(dataset), params)
        result = cache.get(_cache_key)
        if result is None:
            result = fn(dataset, params)
            cache.set(_cache_key, result, CACHE_TIMOUT)
        return result

    return memoized_func
