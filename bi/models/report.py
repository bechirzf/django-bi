import urllib
from abc import ABC, abstractmethod
from typing import Dict, Type, Text, Union, Optional

from django.forms import Form
from django.http import QueryDict
from django.urls import reverse


class BaseReport(ABC):
    """Base abstract class for all reports.

    Attributes:
        _params: Report parameters.
    """
    # TODO: make abstract method get_data
    _params: Dict

    def __init__(self, params: Dict) -> None:
        """Inits Report.

        Args:
            params: Report parameters.
        """
        self._params = params

    @property
    def id(self) -> Text:
        """Returns id of report.

        Returns:
            A string with id of report.
        """
        return str(self.__class__.__module__).split('.')[-1]

    @property
    @abstractmethod
    def title(self) -> Text:
        """Returns title of report.

        Returns:
            A string with title of report.
        """
        pass

    @property
    def form_class(self) -> Union[Type[Form], None]:
        """Returns report's form class.
        """
        return None

    @property
    def form_defaults(self) -> Dict:
        """Returns report's default form inputs values.
        """
        return {}

    @property
    @abstractmethod
    def description(self) -> Text:
        """Returns report description.

        Returns:
            A string with report description.
        """
        pass

    @property
    def template(self) -> Text:
        """Returns path to report template.

        Returns:
            A string with path to report template.
        """
        # TODO: rework!!11111
        return '/'.join(self.__module__.split('.')[self.__module__.split('.').index('reports'):]) + '.html'

    @property
    def container_id(self) -> Text:
        """Returns graphic container id.

        Returns:
            A string with graphic container id.
        """
        return '{}_report'.format(self.id)

    def get_form(self) -> Optional[Type[Form]]:
        """Returns form instance.

        Returns:
            Form instance.
        """
        if self.has_form():
            params = QueryDict(mutable=True)
            params.update(self.form_defaults)
            params.update(self._params)

            form = self.form_class(params)
            form.is_valid()

            return form

    def has_form(self) -> bool:
        """Returns True if report has form.

        Returns:
            True or False.
        """
        return self.form_class is not None

    def get_raw_view_url(self) -> Text:
        """Returns URL for raw entry point.

        Returns:
            A string with url.
        """
        # TODO: improve with format
        return reverse('bi:report-detail-raw', args=[self.id]) + '?' + urllib.parse.urlencode(self._params)
