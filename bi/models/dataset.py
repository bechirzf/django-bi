from abc import ABC, abstractmethod
from typing import Dict, List, Text

from pandas import DataFrame

from bi.models.object import BaseObject


class BaseDataset(BaseObject, ABC):
    """Base abstract class for all datasets.

    Attributes:
        params: Dataset parameters.
    """

    params: Dict

    def __init__(self, params: Dict = {}) -> None:
        """Inits Dataset.

        Args:
            params: Dataset parameters.
        """
        super().__init__()
        self.params = params

    @abstractmethod
    def get_dataframe(self, params: Dict = None) -> DataFrame:
        """Returns x and y axes data (maybe several).

        Returns:
            Pandas dataframe.
        """
        pass

    @classmethod
    def get_cached_dataset_methods(cls) -> List[Text]:
        """Return all methods cached with cache_dataframe decorator.

        Returns:
            List of methods.
        """
        return [
            name for name, value in vars(cls).items()
            if 'cache_dataframe' in str(value)
        ]
