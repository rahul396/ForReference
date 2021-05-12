import numpy as np
import pandas as pd

asset_class_name_col = 0
expected_return_col = 1
stdev_col = 2
is_equity_col = 3
start_covar_col = 4


class Asset_Class_Properties(object):
    def __init__(self, file_path_and_name_with_ext, ip_sheet_num, error_init):

        # open excel file, get first sheet and parse columns
        xlfile = pd.ExcelFile(file_path_and_name_with_ext)
        xlsheet = xlfile.parse(ip_sheet_num)

        self.acp = np.array(xlsheet.iloc[:, 0:start_covar_col])

        # no additional data is expected in the first column
        self.num_assets = self.acp.shape[0]
        self.end_covar_col = start_covar_col + self.num_assets
        self.acp = np.hstack(
            (self.acp, np.array(xlsheet.iloc[:, start_covar_col:self.end_covar_col])))
        self.error_init = error_init
        # Imporve should be read from file
        self.inflation = .03
        self.real_inflation = 0

    def __get_multiple_rows(self, asset_class_name_array, return_col):
        temp = self.acp[np.where(
            self.acp[:, 0] == asset_class_name_array[0]), return_col]
        for ac_iter in range(1, np.shape(asset_class_name_array)[0]):
            temp = np.vstack((temp, self.acp[np.where(
                self.acp[:, 0] == asset_class_name_array[ac_iter]), return_col]))
        return temp

    def get_lowest_risk_asset_class(self):
        return self.acp[np.where(self.acp[:, stdev_col] == (np.min(self.acp[:, stdev_col]))), asset_class_name_col][0][
            0]

    def get_supported_asset_class_names(self):
        return np.reshape(self.acp[:, asset_class_name_col:asset_class_name_col + 1], self.num_assets)

    def get_asset_class_expected_return(self, asset_class_name_array=[]):
        if asset_class_name_array == []:
            return self.acp[:, expected_return_col:expected_return_col + 1]
        else:
            return self.__get_multiple_rows(asset_class_name_array, expected_return_col)

    def get_asset_class_stdev(self, asset_class_name_array=[]):
        if asset_class_name_array == []:
            return self.acp[:, stdev_col:stdev_col + 1]
        else:
            return self.__get_multiple_rows(asset_class_name_array, stdev_col)

    def get_asset_class_equity_indicator(self, asset_class_name_array=[]):
        if asset_class_name_array == []:
            return self.acp[:, is_equity_col:is_equity_col + 1]
        else:
            return self.__get_multiple_rows(asset_class_name_array, is_equity_col)

    def get_covariance_matrix(self, asset_class_name_array=[]):
        if asset_class_name_array == []:
            return self.acp[:, start_covar_col:self.end_covar_col]
        else:
            num_requested_assets = np.shape(asset_class_name_array)[0]
            cov_index_array = np.empty((num_requested_assets))
            for ac_iter in range(num_requested_assets):
                cov_index_array[ac_iter] = np.where(
                    self.acp[:, 0] == asset_class_name_array[ac_iter])[0]

            final_cov_array = np.empty(
                [num_requested_assets, num_requested_assets])

            for x in range(num_requested_assets):
                for y in range(num_requested_assets):
                    final_cov_array[x, y] = self.acp[int(cov_index_array[x]), int(
                        cov_index_array[y] + start_covar_col)]

            return final_cov_array

# acp = Asset_Class_Properties("/Users/briancosmano/Documents/monte_carlo/setup_files/2018 GWI CMAs.xlsx")
# print(acp.get_supported_asset_class_names())
# print(acp.get_covariance_matrix([]).shape)
