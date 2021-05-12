import numpy as np
#import Portfolio as port
#import Asset_Class_Properties as acp

class Glidepath(object):

    def __init__ (self,portfolio_array):
        self.gp = portfolio_array
        self.num_years = len(portfolio_array)
        self.expected_return = self.get_expected_return_glidepath()
        self.stdev = self.get_stdev_glidepath()


    def get_equity_allocation_glidepath(self):
        equity_alloc_array = np.empty(self.num_years)
        for period_iter in range(self.num_years):
            equity_alloc_array[period_iter] = self.gp[period_iter].portfolio_equity_alloc_calc()

        return equity_alloc_array

    def get_expected_return_glidepath(self):
        expected_return_array = np.empty(self.num_years)
        for period_iter in range(self.num_years):
            expected_return_array[period_iter] = self.gp[period_iter].portfolio_er_calc()

        return expected_return_array

    def get_stdev_glidepath(self):
        stdev_array = np.empty(self.num_years)
        for period_iter in range(self.num_years):
            stdev_array[period_iter] = self.gp[period_iter].portfolio_stdev_calc()

        return stdev_array

'''
us_asset_classes = acp.Asset_Class_Properties("/Users/briancosmano/Documents/monte_carlo/setup_files/2018 GWI CMAs.xlsx")
temp_array = [None] *10
for i in range(10):
    temp_array[i]=  port.Portfolio(us_asset_classes,['Large Cap Equity','Bond'],[.4,.6])

my_gp = Glidepath(temp_array)
print(my_gp.expected_return_glidepath_calc())
'''
