import pandas as pd
import numpy as np


class Account_Contribution_Limit_Initalization(object):
    def __init__(self, file_path, ip_sheet_num, error_init):

        self.error_init = error_init
        try:
            xlfile = pd.ExcelFile(file_path)
        except FileNotFoundError:
            error_init.add_error('critical', "Account Contribution Limit",
                                 "Invalid file path for account limits file: %s" % file_path)

        xlsheet = xlfile.parse(ip_sheet_num)
        self.atp = np.array(xlsheet.iloc[:, 0:5])

    def get_limit_properties(self):
        pass
