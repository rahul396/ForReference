from Common import utils, config
from Tax import TaxCalculator
import Models.Asset_Class_Properties as acp
import Models.Account_Contribution_Limit_Initialization as acli
import Models.Account_Type_Initialization as ati
import Models.Mortality as mort
import Models.Error_Obj as e
import Models.Earnings_Curve as ec
import os
import Models.RMD as rmd


class Context(object):
    def __init__(self):
        Context.get_instance(self, config.context_file_name, 0, 2, 4, 5, 1, 3, 6, 7, 8, 4)

    def get_instance(self, file_path, mortality_sn, account_sn, ss_table_sn, cma_sn, earnings_sn, acct_limit_sn,
                     standard_deduction_sn, tax_bracket_sn, state_tax_rates_sn, social_security_benefit_sn):
        self.number_of_runs = 1000
        self.standardDeductionDf = utils.get_dataframe(file_path, standard_deduction_sn)
        self.traxBracketDf = utils.get_dataframe(file_path, tax_bracket_sn)
        self.stateTaxRateDf = utils.get_dataframe(file_path, state_tax_rates_sn)
        self.income_tax_init = TaxCalculator.Tax_Calculator(self.standardDeductionDf, self.traxBracketDf,
                                                            self.stateTaxRateDf)
        self.social_security_df = utils.get_dataframe(file_path, social_security_benefit_sn)
        self.error_init = e.Error_Obj()
        self.asset_class_properties_init = acp.Asset_Class_Properties(file_path, 5, self.error_init)
        self.mortality_init = mort.Mortality(file_path, 0, self.error_init)
        self.account_type_init = ati.Account_Type_Initalization(file_path, 2, self.error_init)
        self.account_contribution_limit_init = acli.Account_Contribution_Limit_Initalization(file_path, 3,
                                                                                             self.error_init)
        self.earnings_growth_init = ec.Earnings_Curves(file_path, 1, self.error_init)
        self.chr_dir = os.getcwd()
        self.default_output_location = os.path.join(self.chr_dir, "output")
        self.rmd_init = rmd.RMD(file_path, 9, self.error_init)

# def singleton(class_):
#     instances = {}
#     def getinstance(*args, **kwargs):
#         if class_ not in instances:
#             instances[class_] = class_(*args, **kwargs)
#         return instances[class_]
#     return getinstance
# 
# @singleton
# class MyClass(BaseClass):
#     pass
