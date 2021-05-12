import Models.Account_Type_Initialization as ati
import Models.Asset_Class_Properties as acp
import Models.Mortality as mort
import Models.Account as act
import SocialSecurity.SocialSecurity as ss
# import Models.Social_Security as ss
# import Error_Obj as e
import Models.Earnings_Curve as ec
import Models.Account_Contribution_Limit_Initialization as acli
import Models.RMD as rmd
import os


class Initialization_Parameters(object):
    def __init__(self, file_path):
        self.chr_dir = os.getcwd()
        # self.error_init = e.Error_Obj()
        self.error_init = ''
        self.mortality_init = mort.Mortality(file_path, 0, self.error_init)
        self.account_type_init = ati.Account_Type_Initalization(
            file_path, 2, self.error_init)
        # self.social_security_init = ss.Social_Security(file_path,4, self.error_init)
        self.asset_class_properties_init = acp.Asset_Class_Properties(
            file_path, 5, self.error_init)
        self.earnings_growth_init = ec.Earnings_Curves(
            file_path, 1, self.error_init)
        self.account_contribution_limit_init = acli.Account_Contribution_Limit_Initalization(file_path, 3,
                                                                                             self.error_init)
        self.rmd_init = rmd.RMD(file_path, 6, self.error_init)
        self.number_of_runs = 1000
        self.negative_balance_return = 0
        self.retirement_need_adjustment_after_death = .8
        self.default_output_location = os.path.join(self.chr_dir, "output")

# ip = Initialization_Parameters("C:/Users/bcosm/Google Drive/Macbook/Documents/Monte_carlo/setup_files/Initialization_Parameters.xlsx",0,2,4,5,1,3)
