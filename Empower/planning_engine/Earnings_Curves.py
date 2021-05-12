import pandas as pd
import numpy as np

#used to adjust future earnigns based on growth assumptions by age and earnigns ID
#requries an external data sources, currently excel file based
class Earnings_Curves(object):

    def __init__(self, file_name_with_ext, ip_sheet_num, error_init):
        # read in a data source that has age in the first column, different growth curves in the following columns
        self.xlfile = pd.ExcelFile(file_name_with_ext)
        self.earnings_df = self.xlfile.parse(ip_sheet_num, header = 0)#Always reads in teh first tab of the excel file, could change by chaging first zero
        self.min_supported_age = self.earnings_df.iloc[:,0].min()# minimum age in the data source
        self.max_supported_age = self.earnings_df.iloc[:,0].max()#maximum age in the data source
        self.error_init = error_init


    #get the growth rates for a given growth curve identifier
    #retuns a np matrix: age, growth percentage
    #optionally can specify a start and end age
    #Note this is just the growth rate, not the earnings over time, see get_real_earnings for earnings over time
    def get_earnings_growth_curve(self, earnings_curve_id = 'default', start_age = '', end_age = ''):
        #check if th growth curve id is in the file, if not throw a warning but continue processing with the default
        try:
            column_index = self.earnings_df.columns.get_loc(earnings_curve_id)
        except:
            column_index = self.earnings_df.columns.get_loc('default')
            self.error_init.add_error('warning',"Earnings Curve - get_earnigns_growth_curve","could not find earnings growth curve " + earnings_curve_id + ", used default instead")

        #assume the starting point is the frist row, ending point is the last end_row
        start_row = 0
        end_row = self.earnings_df.shape[0]
        #if start age is passed, override the start row
        if start_age != '':
            #if start age is less than supported start age stop processing
            #IMPORVE consider a warning and override to min supported age
            if start_age < self.min_supported_age:
                    self.error_init.add_error('critical', 'Earnings_Curves - get_earnings_curve', 'start age requested,  ' , start_age,', is less then min age supported, ', self.min_supported_age)

            start_row = np.where(self.earnings_df.iloc[:,0]==start_age)[0][0]

        #if end age is passed, override the end row
        if end_age != '':
            #if end age is greater than supported start age stop processing
            #IMPORVE consider a warning and override to max supported age
            if end_age > self.max_supported_age:
                    self.error_init.add_error('critical', 'Earnings_Curves - get_earnings_curve', 'end age requested,  ' , max_age,', is greater then max age supported, ', self.max_supported_age)

            end_row = np.where(self.earnings_df.iloc[:,0]==end_age)[0][0]

        return np.transpose(np.vstack((self.earnings_df.iloc[start_row:end_row, 0],self.earnings_df.iloc[start_row:end_row,column_index])))

    #returns earnings adjusted for an assumed growth rate and start age
    #returns a np matrix: age, real earnings
    #optionally can specifiy end age, if no growth curve is identified the default curve is used
    def get_real_earnings(self, start_age, current_earnings, earnings_curve_id = 'default', end_age = ''):
        #get the appropriate earnigns growth curve
        earnings_growth_array = self.get_earnings_growth_curve( earnings_curve_id, start_age, end_age)
        #create a numpy matrix to store your results
        real_earnings_array = np.empty((np.shape(earnings_growth_array)[0]))
        #set year 0 to current earnings
        real_earnings_array[0] = current_earnings
        #calculate future year earnigns with growth curve and previous year earnings
        #e.g. earnings(t+1) = earnings(t) * (1 + growth rate)
        for age_index in range(1, np.shape(earnings_growth_array)[0]):
            real_earnings_array[age_index] = real_earnings_array[age_index - 1] * (1 + earnings_growth_array[age_index-1,1])

        return real_earnings_array
