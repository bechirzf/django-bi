from abc import ABC, abstractmethod
from typing import Dict

import pandas as pd

from reporting.lib import cache_dataframe


class BaseDataset(ABC):
    """
    Абстрактный класс для всех классов датасетов (они должны быть от него отнаследованы).
    """

    @abstractmethod
    def get_dataframe(self, params: Dict = None) -> pd.DataFrame:
        """
        Возвращает данные по оси x и y (возможно несколько).

        :return:
        """
        pass

    @cache_dataframe
    def get_cached_dataframe(self, params: Dict = None) -> pd.DataFrame:
        """
        Возвращает закешированный датафрейм.

        :param params:
        :return:
        """
        # TODO: возможно лучше живьём обернуть, а не декоратором ... хз
        return self.get_dataframe(params)
