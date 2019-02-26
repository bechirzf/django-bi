from typing import Dict

import pandas as pd

from bi.models.dataset import BaseDataset


class DummyDataset(BaseDataset):
    def get_dataframe(self, params: Dict = None) -> pd.DataFrame:
        data = dict([('x_axis',
                      ['2019-01-12', '2019-01-13', '2019-01-14', '2019-01-15', '2019-01-16', '2019-01-17', '2019-01-18',
                       '2019-01-19', '2019-01-20', '2019-01-21', '2019-01-22']),
                     ('y_axis_all',
                      [413033, 416167, 486315, 481322, 540052, 557697, 520895, 451806, 488078, 600682, 125374]),
                     ('y_axis_desktop',
                      [169551, 152731, 208275, 240521, 233834, 231331, 208510, 161870, 180588, 242976, 41173]),
                     ('y_axis_mobile',
                      [206050, 227782, 240046, 204529, 268750, 289747, 276107, 254239, 268735, 287234, 72589]),
                     ('y_axis_app',
                      [43656, 45167, 47099, 47766, 48462, 47916, 45739, 43639, 48061, 81745, 13876]),
                     ])
        df = pd.DataFrame.from_dict(data)
        return df
