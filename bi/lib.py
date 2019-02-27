import glob
import hashlib
import os
import sys
from typing import Union, Dict, List, Tuple, Type

from django.conf import settings
from django.core.cache import cache
from django.http import Http404, QueryDict

from bi.models.dashboard import BaseDashboard
from bi.models.report import BaseReport


def transform_python_list_to_list_for_echarts(l: list) -> str:
    """Преобразует питоновский лист в строку вида '['abc', 'efg']' для echarts.

    :param l: список, который нужно преобразовать
    :return: строка для echarts
    """
    return '[\'' + '\', \''.join([str(i) for i in l]) + '\']'


def get_entity_by_class(path: str, class_name: str, class_params: dict = None) -> Union[
    BaseReport, BaseDashboard]:
    """Возвращает экземпляр класса по пути до файла и имени класса.

    :param class_params: параметры класса отчёта
    :param path: путь до файла класса (например, objects.dashboards.dummydashboard.dashboard
    :param class_name: название класса
    :return:
    """

    splitted_objects_path = settings.OBJECTS_PATH.split('/')
    splitted_objects_path = splitted_objects_path[:-1]

    if len(splitted_objects_path):
        path = '.'.join(splitted_objects_path) + '.' + path

    try:
        module = __import__(path, globals(), locals(), ['*'])

        entity_class = getattr(module, class_name)
        return entity_class(params=class_params)
    except ModuleNotFoundError:
        # если такой репорт не найден
        # TODO: not good that there are 404
        raise Http404()


def get_class_by_class_path(path: str, class_name: str, class_params: dict = None):
    try:
        module = __import__(path, globals(), locals(), ['*'])

        entity_class = getattr(module, class_name)
        return entity_class
    except ModuleNotFoundError:
        # если такой репорт не найден
        # TODO: not good that there are 404
        raise Http404()


def get_reports_list(path_to_objects='') -> List[Type[BaseReport]]:
    """Возвращает список экземпляров отчётов.

    :param path_to_objects:
    :return:
    """
    reports_list = []
    files = glob.iglob(os.path.join(path_to_objects, 'objects', 'reports', '**', 'report.py'), recursive=True)
    files = list(files)
    for file in sorted(files):
        paths = file.split('/')
        paths[-1] = paths[-1][0:-3]
        module_name = '.'.join(paths)

        __import__(module_name, globals(), locals(), ['*'])
        cls = getattr(sys.modules[module_name], 'Report')

        reports_list.append(cls(QueryDict()))
    return reports_list


def get_dashboards_hierarchy(path_to_objects='') -> Dict[Type[BaseDashboard], List[Type[BaseDashboard]]]:
    """Возвращает иерархию классов дашбордов.

    :param path_to_objects: путь до директории с объектами (по умолчанию - пустая строка, директория в корне проекта)
    :return:
    """

    def get_len_of_path_to_objects(path_to_objects_dir=''):
        return len(path_to_objects_dir.split('/')) - 1

    dashboards_hierarchy = {}
    files = glob.iglob(os.path.join(path_to_objects, 'objects', 'dashboards', '**', 'dashboard.py'), recursive=True)
    files = list(files)
    for file in sorted(files):
        paths = file.split('/')
        paths[-1] = paths[-1][0:-3]
        module_name = '.'.join(paths)

        __import__(module_name, globals(), locals(), ['*'])
        cls = getattr(sys.modules[module_name], 'Dashboard')

        if cls not in dashboards_hierarchy and len(paths) == get_len_of_path_to_objects(path_to_objects) + 4:
            dashboards_hierarchy[cls] = []
        if len(paths) == get_len_of_path_to_objects(path_to_objects) + 5:
            if cls.get_parent_dashboard_class() not in dashboards_hierarchy.keys():
                dashboards_hierarchy[cls.get_parent_dashboard_class()] = [cls]
            else:
                dashboards_hierarchy[cls.get_parent_dashboard_class()].append(cls)

    return dashboards_hierarchy


def convert_dashboard_class_to_tuple(dashboard_class: Type[BaseDashboard]) -> Tuple:
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


def get_dashboards_hierarchy_for_template(path_to_objects='') -> dict:
    """Возвращает иерархию дашбордов в виде словаря туплов.
    Для чего это ... сделано: в темплейтах классы автоматически инстанцируются, поэтому сделано на туплах

    :param path_to_objects:
    :return:
    """
    dashboards_hierarchy_class = get_dashboards_hierarchy(path_to_objects)
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
