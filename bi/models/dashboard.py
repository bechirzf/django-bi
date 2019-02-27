from abc import ABC, abstractmethod
from typing import Union, Dict, Type, Text

from django.forms import Form
from django.http import QueryDict


# TODO: make BaseObject class

class BaseDashboard(ABC):
    """
    Базовый класс для всех классов дашбордов (они должны быть от него отнаследованы).

        form_class  Определеине класса формы
        form_defaults   Значения полей формы по умолчанию
    """

    _params: QueryDict = None
    form_class: Type[Form] = None
    form_defaults: Dict = {}

    # TODO: check params necessity
    def __init__(self, params: QueryDict):
        """
        Констурктор.

        :param params: параметры отчета
        """
        self._params = params
        pass

    @property
    def id(self) -> Text:
        """
        Идентификатор дашборда.

        :return:
        """
        return str(self.__module__).split('.')[-2]

    @property
    def icon(self) -> Text:
        return "fa fa-pie-chart"

    @property
    @abstractmethod
    def title(self) -> Text:
        """
        Заголовок дашборда.

        :return:
        """
        pass

    @property
    def template(self) -> Text:
        """
        Путь до темплейта дашборда.

        :return:
        """
        if self.get_parent_dashboard_id():
            return 'dashboards/{}/{}/template.html'.format(self.get_parent_dashboard_id(), self.id)
        else:
            return 'dashboards/{}/template.html'.format(self.id)

    @classmethod
    def get_parent_dashboard_id(cls) -> Union[Text, None]:
        module_splitted = cls.__module__.split('.')
        if module_splitted[-3] == 'dashboards':
            return None
        else:
            return module_splitted[-3]

    @classmethod
    def get_parent_dashboard_class(cls):
        module_splitted = cls.__module__.split('.')
        module = __import__('.'.join(module_splitted[:-2]) + '.dashboard', globals(), locals(), ['*'])

        entity_class = getattr(module, 'Dashboard')
        return entity_class

    def get_form(self) -> Form:
        """
        Возвращате экземпляр формы отчета.

        :return:
        """
        if self.has_form():
            params = QueryDict(mutable=True)
            params.update(self.form_defaults)
            params.update(self._params)

            form = self.form_class(params)
            form.is_valid()

            return form

    def has_form(self) -> bool:
        """
        Сущесвование формы.

        :return:
        """
        return self.form_class is not None
