from abc import ABC, abstractmethod
from typing import Dict, Type

from django.forms import Form
from django.http import QueryDict
from django.urls import reverse


class BaseReport(ABC):
    """Абстрактный класс для всех классов отчётов (они должны быть от него отнаследованы).

        form_class  Определеине класса формы
        form_defaults   Значения полей формы по умолчанию
    """

    _params: QueryDict = None

    form_class: Type[Form] = None
    form_defaults: Dict = {}

    def __init__(self, params: QueryDict) -> None:
        """Констурктор.

        :param params: параметры отчета
        """
        self._params = params

    @property
    def id(self) -> str:
        """Возвращает идентификатор отчёта.

        :return:
        """
        return str(self.__class__.__module__).split('.')[-2]

    @property
    @abstractmethod
    def title(self) -> str:
        """заголовок отчёта

        :return:
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """описание отчёта

        :return:
        """
        pass

    @property
    def template(self) -> str:
        """возвращает путь до темплейта отчёта

        :return:
        """
        return 'reports/{}/template.html'.format(self.id)

    @property
    def container_id(self) -> str:
        """возвращает идентификатор div, в котором будет отрисован график

        :return:
        """
        return '{}_report'.format(self.id)

    def get_form(self) -> Form:
        """Возвращате экземпляр формы отчета

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
        """Сущесвование формы

        :return:
        """
        return self.form_class is not None

    def get_raw_view_url(self) -> str:
        """URL до raw entry point

        :return:
        """
        return reverse('bi:report-detail-raw', args=[self.id]) + '?' + self._params.urlencode()
