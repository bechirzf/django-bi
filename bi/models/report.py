from abc import ABC, abstractmethod
from typing import Dict, Type, Text

from django.forms import Form
from django.http import QueryDict
from django.urls import reverse


class BaseReport(ABC):
    """Base abstract class for all reports.

    Attributes:
        _params: Report parameters.
        form_class: Report form class.
        form_defaults: Default form inputs values.
    """
    _params: QueryDict
    form_class: Type[Form]
    form_defaults: Dict

    def __init__(self, params: QueryDict) -> None:
        """Inits Report.

        Args:
            params: Report parameters.
        """
        self._params = params
        self.form_class = None
        self.form_defaults = {}

    @property
    def id(self) -> Text:
        """Returns id of report.

        Returns:
            A string with id of report.
        """
        return str(self.__class__.__module__).split('.')[-2]

    @property
    @abstractmethod
    def title(self) -> Text:
        """Returns title of report.

        Returns:
            A string with title of report.
        """
        pass

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
        return 'reports/{}/template.html'.format(self.id)

    @property
    def container_id(self) -> Text:
        """Returns graphic container id.

        Returns:
            A string with graphic container id.
        """
        return '{}_report'.format(self.id)

    def get_form(self) -> Form:
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
        return reverse('bi:report-detail-raw', args=[self.id]) + '?' + self._params.urlencode()
