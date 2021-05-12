import numpy as np
import pandas as pd

class Federal_Tax(object):

    #Static parameters
    standard_deductuion_joint = 0
    dependent_tax_incentive = 0 
    standard_deduction_single = 0
    
    #Dynamic parameters
    salary = 0
    bonus = 0
    incomeTaxableAccounts = 0
    Pension = 0   
    nonTaxable_interest = 0
    SSB = 0
    preTax_Contributions = 0
    HSA_Contributions = 0
    numDependents = 0
    
    #computed values
    grossIncome = 0
    childCredit = 0
    combinedIncome  = 0
    taxableSSB = 0
    taxable_income_pre_deduction = 0
    
    def __init__(self, file_path_and_name =-1, use_run_inflation = False, non_run_inflation_rate = .03):
        
        self.filepath = file_path_and_name
        if self.filepath != -1:
            "import file"
#$$$$$$$$$$Use 2018 tax law
#$$What about Alternative Minimum tax?
##Initialize standard deduction and child credit values######
            self.current_federal_tax_brackets = self.read_Tax_Bracket_File(self.filepath)
        else:
            self.current_federal_tax_brackets= np.array([[.10,.15, .25, .28,.33, .35,.396 ],
                                                    [9275,37650,91150,190150,413350, 415050,10**5],
                                                    [18550,75300, 151900, 231450, 413350, 466950, 10**5]],
                                                    dtype = float)
        
        self.dependent_tax_incentive = 1000
        #commenting out to make it equal to as given in excel sheet i.e 6300 : By Rahul
        #self.standard_deduction_single = 12000
        self.standard_deduction_single = 6300
        self.standard_deductuion_joint = 24000
        
        self.tax_inflation = non_run_inflation_rate
        self.num_row, self.number_of_brackets = self.current_federal_tax_brackets.shape

        self.federal_annual_tax_brackets = np.empty((self.number_of_brackets *3 ,100))

##Increasing the tax brackets by the inflation rate############
        if use_run_inflation == False:
            for i in range(100):
                self.federal_annual_tax_brackets[0:self.number_of_brackets,i] = self.current_federal_tax_brackets[0,:]

                self.federal_annual_tax_brackets[self.number_of_brackets:self.number_of_brackets*2,i] = np.multiply(self.current_federal_tax_brackets[1,:],
                                                            (1+self.tax_inflation)**i)

                self.federal_annual_tax_brackets[self.number_of_brackets*2:self.number_of_brackets*3,i] = np.multiply(self.current_federal_tax_brackets[2,:],(
                                                         1+self.tax_inflation)**i)
            print 'if user_run_inflation: '
            print self.federal_annual_tax_brackets[:,0:2]

    def read_Tax_Bracket_File(self,filename):
        taxBracketDf = pd.read_csv(filename)
        taxbracketArray = np.array(taxBracketDf)
        taxbracketArray = taxbracketArray.transpose()
        return taxbracketArray

    def calculate_essential_parameters(self):
        #Compute gross Income
        self.grossIncome = self.salary + self.bonus + self.incomeTaxableAccounts + self.Pension
        
        print 'gross income {}'.format(self.grossIncome)
        #Compute child credit
        if self.grossIncome < 110000:
            self.childCredit = self.numDependents * 1000
        
        #Compute Combined Income
        self.combinedIncome = self.grossIncome + self.nonTaxable_interest + (0.5 * self.SSB)
        
        #Compute taxable SSB
        if (self.combinedIncome > 32000 and self.combinedIncome <= 44000):
            self.taxableSSB = 0.5 * self.SSB
        elif (self.combinedIncome > 44000):
            self.taxableSSB = 0.85 * self.SSB            
            
    def calculate_taxable_income_pre_deduction(self):
        #commeting out: bY Rahul
        # self.taxable_income_pre_deduction = (self.grossIncome + self.taxableSSB) - (self.preTax_Contributions + self.HSA_Contributions)
        self.taxable_income_pre_deduction = 200000
        print 'prededuction income {}'.format(self.taxable_income_pre_deduction)

    def Federal_Tax_Initialization(self,salary, bonus, incomeTaxableAccounts, Pension, nonTaxable_interest, SSB, preTax_Contributions, HSA_Contributions, numDependents):
        self.salary = salary
        self.bonus = bonus
        self.incomeTaxableAccounts = incomeTaxableAccounts
        self.Pension = Pension
        self.nonTaxable_interest = nonTaxable_interest
        self.SSB = SSB
        self.preTax_Contributions = preTax_Contributions
        self.HSA_Contributions = HSA_Contributions
        self.numDependents = numDependents
        
        self.calculate_essential_parameters()
        self.calculate_taxable_income_pre_deduction()
       
##Defining tax status#########################################
    def convert_single_or_joint(self,single_or_joint):
        if single_or_joint.lower().strip() =="single":
            return self.number_of_brackets, self.number_of_brackets *2
        elif single_or_joint.lower().strip() =="joint":
            return self.number_of_brackets * 2, self.number_of_brackets * 3
        #this is currently useless, need to raise an error
        else:
            print("Error - please specify single or joint, you passed " , single_or_joint)

##Loading brackets (start taxable income and end taxable income##############################
    def get_federal_tax_brackets(self, single_or_joint, simulation_year_number = -1):
        bracket_start_position, bracket_end_position = self.convert_single_or_joint(single_or_joint)
        if simulation_year_number == -1:
            return np.vstack((self.federal_annual_tax_brackets[0:self.number_of_brackets,:],
            self.federal_annual_tax_brackets[bracket_start_position:bracket_end_position,:]))

        elif simulation_year_number >=0 and simulation_year_number <= 100:
            return np.vstack((self.federal_annual_tax_brackets[0:self.number_of_brackets,simulation_year_number],
            self.federal_annual_tax_brackets [bracket_start_position:bracket_end_position,simulation_year_number]))
        
    def calculate_federal_tax(self,single_or_joint, simulation_year_number =-1):
        #Ankur: Find taxable income as per the filing status
        taxable_income = 0
        if single_or_joint.lower().strip() == "single":
            taxable_income = self.taxable_income_pre_deduction - self.standard_deduction_single
        elif single_or_joint.lower().strip() == "joint":
            taxable_income = self.taxable_income_pre_deduction - self.standard_deductuion_joint

        if taxable_income < 0:
            taxable_income = 0

        print 'taxable_income {}'.format(taxable_income)
        temp_brackets = self.get_federal_tax_brackets(single_or_joint, simulation_year_number)

        computed_tax = 0
        
        if simulation_year_number == -1:
            computed_tax = "Not yet"
        else:
            last_income_bracket = 0
            maxrate = temp_brackets[0,:][len(temp_brackets[0,:])-1]
            
            for x, y in np.nditer([temp_brackets[0,:], temp_brackets[1,:]]):
                if x != maxrate:
                    if taxable_income > y:
                        computed_tax = computed_tax  + (x*(y-last_income_bracket))
                        last_income_bracket = y
                    else:
                        computed_tax = computed_tax + (x* (taxable_income - last_income_bracket))
                        break
                else:
                    print 'else else'
                    computed_tax = computed_tax + (x* (taxable_income - last_income_bracket))

        print computed_tax
        fedaral_tax = computed_tax - self.childCredit
        
        return fedaral_tax

#np.set_printoptions(suppress=True)
#a = Federal_Tax(file_path_and_name = 'TaxBracket2018.csv', non_run_inflation_rate =0)
# a.Federal_Tax_Initialization(25000,2000,5000,8000,2000,12000,1000,0,2)
# print(a.calculate_federal_tax("joint",0))

np.set_printoptions(suppress=True)
#a = Federal_Tax(file_path_and_name = 'TaxBracket2018.csv',non_run_inflation_rate =0)
a = Federal_Tax(non_run_inflation_rate =0)
a.Federal_Tax_Initialization(25000,2000,5000,8000,2000,12000,1000,0,2)
print(a.calculate_federal_tax("single",0))
