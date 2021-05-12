import pandas as pd
import numpy as np


class RMD(object):
    def __init__(self, file_path_and_name_with_ext, ip_sheet_num, error_init):

        self.error_init = error_init
        try:
            xlfile = pd.ExcelFile(file_path_and_name_with_ext)
        except FileNotFoundError:
            error_init.add_error('critical', "RMD",
                                 "Invalid file path for RMD file: %s" % file_path_and_name_with_ext)

        xlsheet = xlfile.parse(ip_sheet_num)
        self.rmd_table = np.array(xlsheet.iloc[:, 0:2])
        is_nan = pd.isnull(self.rmd_table).any(axis=1)
        self.rmd_table = self.rmd_table[~is_nan]
        self.min_rmd_age = np.min(self.rmd_table[:, 0])
        self.max_supported_age = np.max(self.rmd_table[:, 0])

    def get_rmd_amount(self, balance_array, age):
        age = min(age, self.max_supported_age)
        rmd_value = self.rmd_table[np.where(
            self.rmd_table[:, 0] == age), 1][0][0]
        balance_array[balance_array < 0] = 0
        return np.rint(balance_array / rmd_value)
