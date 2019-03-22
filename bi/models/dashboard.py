from abc import ABC, abstractmethod
from typing import Union, Dict, Type, Text, Optional

from django.forms import Form
from django.http import QueryDict

from bi.lib import get_class_by_path


# TODO: make BaseObject class

class BaseDashboard(ABC):
    """Base abstract class for all dashboards.

    Attributes:
        params: Dashboard parameters.
    """

    _params: Dict

    # TODO: check params necessity
    def __init__(self, params: Dict):
        """Inits dashboard.

        Args:
            params: Dashboard parameters.
        """
        self._params = params

    @property
    def id(self) -> Text:
        """Returns id of dashboard.

        Returns:
            A string with id of dashboard.
        """
        return str(self.__module__).split('.')[-1]

    @property
    def icon(self) -> Text:
        """Returns icon of dashboard.

        Returns:
            A string with icon of dashboard.
        """
        return "fa fa-pie-chart"

    @property
    def form_class(self) -> Union[Type[Form], None]:
        """Returns dashboards's form class.
        """
        return None

    @property
    def form_defaults(self) -> Dict:
        """Returns dashboards's default form inputs values.
        """
        return {}

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
            return 'dashboards/{}/{}.html'.format(self.get_parent_dashboard_id(), self.id)
        else:
            return 'dashboards/{}.html'.format(self.id)

    @classmethod
    def get_parent_dashboard_id(cls) -> Union[Text, None]:
        """Returns id of dashboard's parent.

        Returns:
            ID of dashboard's parent.
        """
        module_splitted = cls.__module__.split('.')
        if module_splitted[-2] == 'dashboards':
            return None
        else:
            return module_splitted[-2]

    @classmethod
    def get_parent_dashboard_class(cls) -> Union[Text, None]:
        """Returns class of dashboard's parent.

        Returns:
            Class of dashboard's parent.
        """
        module_splitted = cls.__module__.split('.')
        temp_path = '/'.join(module_splitted[:-1]) + '.py'
        return get_class_by_path(temp_path, 'Dashboard')

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
        """Returns True if dashboard has form.

        Returns:
            True or False.
        """
        return self.form_class is not None
