import numpy as np
import Asset_Class_Properties as acp


class Portfolio(object):

    def __init__(self, asset_class_names, asset_class_weights, init_params):
        self.asset_class_names = asset_class_names
        self.asset_class_weights = np.array(asset_class_weights)
        self.acp = init_params.asset_class_properties_init
        self.expected_return = self.portfolio_er_calc()
        self.standard_deviation = self.portfolio_stdev_calc()


    def check_portfolio_integrity (self):
        is_error = False
        error_code = []

        sum_portfolio= np.sum(self.asset_class_weights)
        if sum_portfolio != 1:
            error_code.append("Sum of portfolio weights <> 1: %f" % sum_portfolio)
            is_error = True

        if is_error:
            return (error_code)


    def portfolio_er_calc(self):
        return np.dot(self.asset_class_weights,self.acp.get_asset_class_expected_return(self.asset_class_names))

    def portfolio_stdev_calc(self):

        return np.sqrt((np.dot(self.asset_class_weights.T,
            np.dot(self.acp.get_covariance_matrix(self.asset_class_names),self.asset_class_weights))))

    def portfolio_equity_alloc_calc(self):
        return np.dot(self.asset_class_weights,self.acp.get_asset_class_equity_indicator(self.asset_class_names))

    def get_asset_allocation(self):
        return np.vstack((self.asset_class_names, self.asset_class_weights))



'''
us_asset_classes = acp.Asset_Class_Properties("/Users/briancosmano/Documents/monte_carlo/setup_files/2018 GWI CMAs.xlsx")
#temp_name = us_asset_classes.get_supported_asset_class_names()
temp_name = ['Large Cap Equity', 'Bond']

temp_weight = [.5,.5]
#start_time = time.clock()

my_port = Portfolio(us_asset_classes, temp_name, temp_weight)
print(my_port.portfolio_stdev_calc())
'''
