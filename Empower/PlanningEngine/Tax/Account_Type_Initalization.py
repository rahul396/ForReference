import pandas as pd
import numpy as np


class Account_Type_Initalization(object):
    def __init__(self, file_path_and_name_with_ext, error_init):

        self.error_init = error_init
        try:
            xlfile = pd.ExcelFile(file_path_and_name_with_ext)
        except FileNotFoundError:
            error_init.add_error('critical', "Accounts Type Initilization",
                                 "Invalid file path for accounts file: %s" % file_path_and_name_with_ext)

        xlsheet = xlfile.parse(0)
        self.atp = np.array(xlsheet.iloc[:, 0:14])

    def get_supported_account_types(self):
        return self.atp[:, 0]

    def is_supported_account(self, account_type_name):
        return account_type_name in self.atp[:, 0]

    def get_ee_contribuiton_limit(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 1][0][0]

    def get_combined_contribution_limit(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 2][0][0]

    def get_tax_treatment_growth(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 3][0][0]

    def get_tax_treatment_withdrawals(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 4][0][0]

    def get_tax_treatment_contributions(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 5][0][0]

    def get_contributions_subject_to_fica(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 6][0][0]

    def get_early_penality_withdrawal_age(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 7][0][0]

    def get_early_penality_withdrawal_percent(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 8][0][0]

    def get_loan_limit(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 9][0][0]

    def get_pretax_support(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 10][0][0]

    def get_roth_support(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 11][0][0]

    def get_after_tax_support(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 12][0][0]

    def get_taxable_support(self, account_type_name):
        return self.atp[np.where(self.atp[:, 0] == account_type_name), 13][0][0]
