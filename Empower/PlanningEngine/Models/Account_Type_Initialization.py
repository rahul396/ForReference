import pandas as pd
import numpy as np


class Account_Type_Initalization(object):
    def __init__(self, file_path_and_name_with_ext, ip_sheet_num, error_init):

        self.error_init = error_init
        try:
            xlfile = pd.ExcelFile(file_path_and_name_with_ext)
        except FileNotFoundError:
            error_init.add_error('critical', "Account Type Initilization",
                                 "Invalid file path for accounts file: %s" % file_path_and_name_with_ext)

        xlsheet = xlfile.parse(ip_sheet_num)
        self.atp = np.array(xlsheet.iloc[:, 0:12])

    def get_supported_account_types(self):
        return self.atp[:, 0]

    def is_supported_account(self, account_type_name):
        return account_type_name in self.atp[:, 0]

    def get_applicable_limits(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 1][0][0].split(',')

    def get_contributions_subject_to_fica(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 2][0][0]

    def get_early_penality_withdrawal_age(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 3][0][0]

    def get_early_penality_withdrawal_percent(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 4][0][0]

    def get_loan_limit(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 5][0][0]

    def get_pretax_support(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 6][0][0]

    def get_roth_support(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 7][0][0]

    def get_after_tax_support(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 8][0][0]

    def get_taxable_support(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 9][0][0]

    def get_default_account_support(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 10][0][0]

    def get_rmd_applies(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 11][0][0]
