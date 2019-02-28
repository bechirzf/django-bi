from abc import ABC, abstractmethod
from typing import Union, Dict, Type, Text

from django.forms import Form
from django.http import QueryDict


# TODO: make BaseObject class

class BaseDashboard(ABC):
    """Base abstract class for all dashboards.

    Attributes:
        params: Dashboard parameters.
        form_class: Report form class.
        form_defaults: Default form inputs values.
    """

    _params: QueryDict
    form_class: Type[Form]
    form_defaults: Dict

    # TODO: check params necessity
    def __init__(self, params: QueryDict):
        """Inits dashboard.

        Args:
            params: Dashboard parameters.
        """
        self._params = params
        self.form_class = None
        self.form_defaults = {}

    @property
    def id(self) -> Text:
        """Returns id of dashboard.

        Returns:
            A string with id of dashboard.
        """
        return str(self.__module__).split('.')[-2]

    @property
    def icon(self) -> Text:
        """Returns icon of dashboard.

        Returns:
            A string with icon of dashboard.
        """
        return "fa fa-pie-chart"

    @property
    @abstractmethod
    def title(self) -> Text:
        """Returns title of dashboard.

        Returns:
            A string with title of dashboard.
        """
        pass

    @property
    def template(self) -> Text:
        """Returns path to template of dashboard.

        Returns:
            A string with path to template of dashboard.
        """
        if self.get_parent_dashboard_id():
            return 'dashboards/{}/{}/template.html'.format(self.get_parent_dashboard_id(), self.id)
        else:
            return 'dashboards/{}/template.html'.format(self.id)

    @classmethod
    def get_parent_dashboard_id(cls) -> Union[Text, None]:
        """Returns id of dashboard's parent.

        Returns:
            ID of dashboard's parent.
        """
        module_splitted = cls.__module__.split('.')
        if module_splitted[-3] == 'dashboards':
            return None
        else:
            return module_splitted[-3]

    @classmethod
    def get_parent_dashboard_class(cls) -> Union[Text, None]:
        """Returns class of dashboard's parent.

        Returns:
            Class of dashboard's parent.
        """
        module_splitted = cls.__module__.split('.')
        module = __import__('.'.join(module_splitted[:-2]) + '.dashboard', globals(), locals(), ['*'])

        entity_class = getattr(module, 'Dashboard')
        return entity_class

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
        """Returns True if dashboard has form.

        Returns:
            True or False.
        """
        return self.form_class is not None
