import pandas as pd
import csv
import sys
import os

class SSBenefit:
    """
    Social Security Benefits
    """
    def __init__(self):
        self.ssb = self.set_monthly_ss_income()

    def set_monthly_ss_income(self):
        filename = 'SSTable.xlsx'
        try:
            df = pd.read_excel(filename)
        except:
            print ('File {} not found'.format(filename))

        new_df = df.filter(['VH_AGE','VH_RET_AGE','VH_ANN_SAL','VH_MTHLY_SS_INCOME'], axis=1)
        grp1 = new_df.groupby('VH_AGE')
        grp1 = dict(list(grp1))
        for key in grp1:
            grp1[key] = grp1[key].filter(['VH_RET_AGE','VH_ANN_SAL','VH_MTHLY_SS_INCOME'])
            grp1[key]=grp1[key].groupby('VH_RET_AGE')
            grp1[key] = dict(list(grp1[key]))
            for ret_age in grp1[key]:
                grp1[key][ret_age] = grp1[key][ret_age].filter(['VH_ANN_SAL','VH_MTHLY_SS_INCOME'])
                grp1[key][ret_age] = grp1[key][ret_age].groupby('VH_ANN_SAL')
                grp1[key][ret_age] = dict(list(grp1[key][ret_age]))
        return grp1


if __name__ == '__main__':

    ssbenefit = SSBenefit()
    print (ssbenefit.ssb[15][62][20000])
    # #Data is in a dictionary where the keys are the parameters
    # #So if you want the monthly social security for someone who started working at 15 and retired at 65 and made 20000
    # print(self.dic[15][65][20000].filter(['VH_MTHLY_SS_INCOME']).to_string(index = False))
    # #someone who started working at 15 and retired at 62 and made 80000
    # print(dic[15][62][80000].filter(['VH_MTHLY_SS_INCOME']).to_string(index = False))
    # #Or if you want to know all of the SS monthly income for people who worked 15 to 67
    #
    # for i in dic[15][67].keys():
    #     print(dic[15][67][i].to_string(index=False))

