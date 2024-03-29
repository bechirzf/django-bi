from django.http import JsonResponse

from bi.lib import transform_python_list_to_list_for_echarts
from bi.models.report import BaseReport
from tests.fixtures.objects.datasets.dummy import Dataset


class Report(BaseReport):
    """
    Пример отчёта для тестов и образца. Не менять!
    """
    title = 'Dummy report 1'
    description = 'Dummy report 1 для примера и тестов'

    def get_data(self) -> JsonResponse:
        dataset = Dataset()
        data = dataset.get_dataframe()

        x_axis = data['x_axis'].values.tolist()
        y_axis_all = data['y_axis_all'].values.tolist()
        y_axis_desktop = data['y_axis_desktop'].values.tolist()
        y_axis_mobile = data['y_axis_mobile'].values.tolist()
        y_axis_app = data['y_axis_app'].values.tolist()

        x_axis = transform_python_list_to_list_for_echarts(x_axis)
        y_axis_all = transform_python_list_to_list_for_echarts(y_axis_all)
        y_axis_desktop = transform_python_list_to_list_for_echarts(
            y_axis_desktop)
        y_axis_mobile = transform_python_list_to_list_for_echarts(y_axis_mobile)
        y_axis_app = transform_python_list_to_list_for_echarts(y_axis_app)
        return JsonResponse({
            'x_axis': x_axis,
            'y_axis_all': y_axis_all,
            'y_axis_desktop': y_axis_desktop,
            'y_axis_mobile': y_axis_mobile,
            'y_axis_app': y_axis_app
        })
