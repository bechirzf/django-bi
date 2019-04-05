import glob
import hashlib
import os.path
from importlib.util import spec_from_file_location, module_from_spec
from typing import List, Tuple, Type, Union, Dict, Text, Callable, TYPE_CHECKING

from django.conf import settings
from django.core.cache import cache
from django.http import QueryDict
from pandas import DataFrame

from bi.models.dataset import BaseDataset
from bi.models.report import BaseReport

if TYPE_CHECKING:
    from bi.models.dashboard import BaseDashboard


def transform_python_list_to_list_for_echarts(l: List) -> Text:
    """Transform python list to string for echarts e.g. '['abc', 'efg']'.

    Args:
        l: list to transform.

    Returns:
        String for echarts.
    """
    return '[\'' + '\', \''.join([str(i) for i in l]) + '\']'


def get_entity_by_path(path: Text, class_name: Text, class_params: Dict = None) \
        -> Union[BaseReport, 'BaseDashboard', None]:
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


def get_class_by_path(path: Text, class_name: Text
                      ) -> Union[Type[BaseReport], Type['BaseDashboard'], None]:
    """Get class definition by path to file.

    Args:
        path: File path (e.g. dashboards/dummy1/dummy3.py).
        class_name: Class name (e.g. Dashboard).`

    Returns:
        Dashboard or Report.
    """
    try:
        cls_path = '.'.join(
            os.path.splitext(os.path.normcase(path))[0].split(os.sep))
        spec = spec_from_file_location(
            cls_path, os.path.join(settings.OBJECTS_PATH, path))
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        cls = getattr(module, class_name)

        return cls
    except FileNotFoundError:
        return None


def get_reports_list() -> List[Union[BaseReport, None]]:
    """Get list of reports instances.

    Returns:
        List of reports instances.
    """
    reports_list = []
    files = glob.iglob(
        os.path.join(settings.OBJECTS_PATH, 'reports', '**', '[!_]*.py'),
        recursive=True)
    files = list(files)
    for file in sorted(files):
        file = os.path.relpath(file, settings.OBJECTS_PATH + os.sep)
        report = get_entity_by_path(file, 'Report')
        reports_list.append(report)
    return reports_list


def get_datasets_list() -> List[Union[BaseDataset, None]]:
    """Get list of datasets instances.

    Returns:
        List of datasets instances.
    """
    datasets_list = []
    files = glob.iglob(
        os.path.join(settings.OBJECTS_PATH, 'datasets', '**', '[!_]*.py'),
        recursive=True)
    files = list(files)
    for file in sorted(files):
        file = os.path.relpath(file, settings.OBJECTS_PATH + os.sep)
        report = get_entity_by_path(file, 'Dataset')
        datasets_list.append(report)
    return datasets_list


def get_dashboards_hierarchy(
) -> Dict[Type['BaseDashboard'], List[Type['BaseDashboard']]]:
    """Get hierarchy of dashboards classes.

    Returns:
        Dict of dashboards classes.
    """
    dashboards_hierarchy = {}
    files = glob.iglob(
        os.path.join(settings.OBJECTS_PATH, 'dashboards', '**', '[!_]*.py'),
        recursive=True)
    files = list(files)
    for file in sorted(files):
        file = os.path.relpath(file, settings.OBJECTS_PATH + os.sep)
        cls = get_class_by_path(file, 'Dashboard')
        if str(cls) not in [str(key) for key in dashboards_hierarchy.keys()
                            ] and len(file.split(os.sep)) == 2:
            dashboards_hierarchy[cls] = []
        if len(file.split(os.sep)) == 3:
            if str(cls.get_parent_dashboard_class()) not in [
                str(key) for key in dashboards_hierarchy.keys()
            ]:
                dashboards_hierarchy[cls.get_parent_dashboard_class()] = [cls]
            else:
                for key in dashboards_hierarchy.keys():
                    if str(key) == str(cls.get_parent_dashboard_class()):
                        dashboards_hierarchy[key].append(cls)

    return dashboards_hierarchy


def convert_dashboard_class_to_tuple(
        dashboard_class: Type['BaseDashboard']) -> Tuple:
    """Transforms dashboard to tuple for template.

    Args:
        Dashboard to transform.

    Returns:
        Tuple with dashboard info.
    """
    board = dashboard_class(QueryDict())
    result = [
        board.id, board.title, board.icon,
        dashboard_class.get_parent_dashboard_id()
    ]
    return tuple(result)


def get_dashboards_hierarchy_for_template() -> Dict:
    """Get dashboard hierarchy for using in template.

    Returns:
         Dictionary with dashboard hierarchy.
    """
    dashboards_hierarchy_class = get_dashboards_hierarchy()
    dashboards_hierarchy_for_template = {}

    for dashboards_hierarchy_class_key in dashboards_hierarchy_class.keys():
        temp_key = convert_dashboard_class_to_tuple(
            dashboards_hierarchy_class_key)
        dashboards_hierarchy_for_template[temp_key] = []
        for dashboards_hierarchy_class_value in dashboards_hierarchy_class[
            dashboards_hierarchy_class_key]:
            dashboards_hierarchy_for_template[temp_key].append(
                convert_dashboard_class_to_tuple(
                    dashboards_hierarchy_class_value))
    return dashboards_hierarchy_for_template


def cache_dataframe(timeout: int = 1 * 7 * 24 * 60 * 60) -> Callable:
    """Decorator for caching dataframe in dataset's get_dataframe method.

    Args:
        timeout: the default timeout, in seconds, to use for the cache.

    Returns:
        Cached dataset's get_dataframe method result.
    """

    def cache_dataframe_inner(fn):

        def cache_get_key(*args) -> Text:
            serialise = []
            for arg in args:
                serialise.append(str(arg))
            full_str = '.'.join(serialise).encode('utf-8')
            key = hashlib.md5(full_str).hexdigest()
            # TODO: remove md5, return in format <dataset_name>.md5(params)
            return key

        def memoized_func(*args) -> DataFrame:
            # getting string for dataset's module name relative objects/datasets
            splitted_module_name = str(type(args[0])).split('.')
            if 'objects' in splitted_module_name:
                splitted_module_name = splitted_module_name[
                                       splitted_module_name.index('datasets') + 1:-1]
            else:
                splitted_module_name = splitted_module_name[1:-1]
            module_name = '.'.join(splitted_module_name)
            _cache_key = cache_get_key(module_name, fn.__name__, args[1:])
            result = cache.get(_cache_key)
            if result is None:
                result = fn(*args)
                cache.set(_cache_key, result, timeout)
            return result

        return memoized_func

    return cache_dataframe_inner
