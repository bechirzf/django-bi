from abc import ABC, abstractmethod
from typing import Dict

import pandas as pd

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
    def get_dataframe(self, params: Dict = None) -> pd.DataFrame:
        """Returns x and y axes data (maybe several).

        Returns:
            Pandas dataframe.
        """
        pass
