import numpy as np
class Federal_Tax(object):


    def __init__(self, file_path_and_name =-1, use_run_inflation = False, non_run_inflation_rate = .03):
        self.filepath = file_path_and_name
        if self.filepath != -1:
            "import file"

        else:
            self.dependent_tax_incentive = 1000
            self.standard_deduction_single = 6300
            self.standard_deductuion_joint = 12600

            self.current_federal_tax_brackets= np.array([[.10,.15, .25, .28,.33, .35,.396 ],
                                                    [9275,37650,91150,190150,413350, 415050,10**5],
                                                    [18550,75300, 151900, 231450, 413350, 466950, 10**5]],
                                                    dtype = float)


            self.tax_inflation = non_run_inflation_rate
            self.num_row, self.number_of_brackets = self.current_federal_tax_brackets.shape

            self.federal_annual_tax_brackets = np.empty((self.number_of_brackets *3 ,100))

        if use_run_inflation == False:
            for i in range(100):
                self.federal_annual_tax_brackets[0:self.number_of_brackets,i] = self.current_federal_tax_brackets[0,:]

                self.federal_annual_tax_brackets[self.number_of_brackets:self.number_of_brackets*2,i] = np.multiply(self.current_federal_tax_brackets[1,:],
                                                            (1+self.tax_inflation)**i)

                self.federal_annual_tax_brackets[self.number_of_brackets*2:self.number_of_brackets*3,i] = np.multiply(self.current_federal_tax_brackets[2,:],(
                                                            1+self.tax_inflation)**i)

    def convert_single_or_joint(self,single_or_joint):
        if single_or_joint.lower().strip() =="single":
            return self.number_of_brackets, self.number_of_brackets *2
        elif single_or_joint.lower().strip() =="joint":
            return self.number_of_brackets * 2, self.number_of_brackets * 3
        #this is currently useless, need to raise an error
        else:
            print("Error - please specify single or joint, you passed " , single_or_joint)

    def get_federal_tax_brackets(self, single_or_joint, simulation_year_number = -1):
        bracket_start_position, bracket_end_position = self.convert_single_or_joint(single_or_joint)

        if simulation_year_number == -1:
            return np.vstack((self.federal_annual_tax_brackets[0:self.number_of_brackets,:],
            self.federal_annual_tax_brackets[bracket_start_position:bracket_end_position,:]))

        elif simulation_year_number >=0 and simulation_year_number <= 100:
            return np.vstack((self.federal_annual_tax_brackets[0:self.number_of_brackets,simulation_year_number],
            self.federal_annual_tax_brackets [bracket_start_position:bracket_end_position,simulation_year_number]))

    def calculate_federal_tax(self,single_or_joint,taxable_income_pre_deduction, simulation_year_number =-1):

        taxable_income = taxable_income_pre_deduction - self.standard_deductuion_joint
        if self.convert_single_or_joint(single_or_joint) =="single":
            taxable_income = taxable_income_pre_deduction - self.standard_deductuion_single

        if taxable_income < 0:
            taxable_income = 0

        temp_brackets = self.get_federal_tax_brackets(single_or_joint, simulation_year_number)
        temp = 0
        if simulation_year_number == -1:
            temp = "Not yet"
        else:
            last_income_bracket = 0
            for x, y in np.nditer([temp_brackets[0,:], temp_brackets[1,:]]):
                if taxable_income > y:
                    temp = temp  + (x*(y-last_income_bracket))
                    last_income_bracket = y
                else:
                    temp = temp + (x* (taxable_income - last_income_bracket))
                    break

        return temp

np.set_printoptions(suppress=True)
a = Federal_Tax(non_run_inflation_rate =0)
print(a.calculate_federal_tax("single",300000,0))
