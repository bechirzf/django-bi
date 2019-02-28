from abc import ABC, abstractmethod
from typing import Dict

import pandas as pd

from bi.lib import cache_dataframe


class BaseDataset(ABC):
    """Base abstract class for all datasets.
    """

    @abstractmethod
    def get_dataframe(self, params: Dict = None) -> pd.DataFrame:
        """Returns x and y axes data (maybe several).

        Returns:
            Pandas dataframe.
        """
        pass

    @cache_dataframe
    def get_cached_dataframe(self, params: Dict = None) -> pd.DataFrame:
        """Returns cached x and y axes data (maybe several).

        Returns:
            Pandas dataframe.
        """
        # TODO: perhaps it is better to do not decorator
        return self.get_dataframe(params)
