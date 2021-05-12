import numpy as np
import pandas as pd
from Common.config import logging
from Common.aop import after, before
import traceback


class Tax_Calculator(object):
    # Static parameters
    standard_deductuion_joint = 0
    dependent_tax_incentive = 0
    standard_deduction_single = 0

    # Dynamic parameters
    salary = 0
    bonus = 0
    incomeTaxableAccounts = 0
    pension = 0
    nonTaxable_interest = 0
    SSB = 0
    preTax_Contributions = 0
    HSA_Contributions = 0
    # Once we will have number of house hold information, we can compute filing status. As of now we will get
    # as input initialization parameter
    filing_Status = ''
    numDependents = 0

    # computed values
    grossIncome = 0
    childCredit = 0
    combinedIncome = 0
    taxableSSB = 0
    taxable_income_pre_deduction = 0
    taxable_income = 0

    # Create empty DataFrame incase user will not supply the file
    state_tax_rate = pd.DataFrame(columns=['State', 'Average Effective Tax Rate'])

    def __init__(self, StandardDeductionDf, FederalTaxBracketDf, StateTaxRatesDf, error_init=False,
                 use_run_inflation=False, non_run_inflation_rate=.03):
        self.LOG = logging.getLogger(self.__class__.__name__)
        try:
            # Read tax bracket from the excel sheet
            taxbracketArray = np.array(FederalTaxBracketDf)
            self.current_tax_brackets = taxbracketArray.transpose()

            # Read State Tax Rate from excel sheet
            self.state_tax_rate = StateTaxRatesDf

            # Read Standard deduction values from excel sheet
            self.standard_tax_deduction = StandardDeductionDf

            # Defining standard Tax deduction values read from initialization paramters
            self.dependent_tax_incentive = self.standard_tax_deduction[
                self.standard_tax_deduction['Standard Deduction Type'] == 'Dependent Tax Incentive']['Amount'].iloc[
                0]  # 1000
            self.standard_deduction_single = self.standard_tax_deduction[
                self.standard_tax_deduction['Standard Deduction Type'] == 'Standard Deduction Single']['Amount'].iloc[
                0]  # 12000
            self.standard_deductuion_joint = self.standard_tax_deduction[
                self.standard_tax_deduction['Standard Deduction Type'] == 'Standard Deductuion Joint']['Amount'].iloc[
                0]  # 24000

            self.tax_inflation = non_run_inflation_rate
            self.num_row, self.number_of_brackets = self.current_tax_brackets.shape

            self.federal_annual_tax_brackets = np.empty((self.number_of_brackets * 3, 100))

            # Increasing the tax brackets by the inflation rate############
            if not use_run_inflation:
                for i in range(100):
                    self.federal_annual_tax_brackets[0:self.number_of_brackets, i] = self.current_tax_brackets[0, :]

                    self.federal_annual_tax_brackets[self.number_of_brackets:self.number_of_brackets * 2,
                    i] = np.multiply(self.current_tax_brackets[1, :],
                                     (1 + self.tax_inflation) ** i)

                    self.federal_annual_tax_brackets[self.number_of_brackets * 2:self.number_of_brackets * 3,
                    i] = np.multiply(self.current_tax_brackets[2, :], (
                        1 + self.tax_inflation) ** i)
        except Exception:
            self.LOG.exception('Exception occured while reading initialization parameters for Income_Tax class.')
            self.LOG.exception(traceback.format_exc())

    # Calculate essential parameters which are required to compute taxable income, fadaral tax and state tax
    @before()
    @after
    def calculate_essential_parameters(self):
        try:
            # Compute gross Income
            self.grossIncome = self.salary + self.bonus + self.incomeTaxableAccounts + self.pension

            self.LOG.info('gross income {}'.format(self.grossIncome))
            # Compute child credit
            if self.grossIncome < 110000:
                self.childCredit = self.numDependents * 1000

            # Compute Combined Income
            self.combinedIncome = self.grossIncome + self.nonTaxable_interest + (0.5 * self.SSB)

            # Compute taxable SSB
            if 32000 < self.combinedIncome <= 44000:
                self.taxableSSB = 0.5 * self.SSB
            elif self.combinedIncome > 44000:
                self.taxableSSB = 0.85 * self.SSB
        except Exception:
            self.LOG.exception('Exception occured while calculating essential parameters.')
            self.LOG.exception(traceback.format_exc())

    # Calculate the taxable income before deduction
    @before()
    @after
    def calculate_taxable_income_pre_deduction(self):
        try:
            self.taxable_income_pre_deduction = (self.grossIncome + self.taxableSSB) - (
                self.preTax_Contributions + self.HSA_Contributions)
            self.LOG.info('pre-deduction income {}'.format(self.taxable_income_pre_deduction))
        except Exception:
            self.LOG.exception('Exception occurred while calculating taxable income pre-deduction.')
            self.LOG.exception(traceback.format_exc())

    # Calculate the final taxable income
    @before()
    @after
    def calculate_taxable_income(self):
        try:
            if self.filing_Status.lower().strip() == 'single':
                self.taxable_income = self.taxable_income_pre_deduction - self.standard_deduction_single
            elif self.filing_Status.lower().strip() == 'joint':
                self.taxable_income = self.taxable_income_pre_deduction - self.standard_deductuion_joint

            if self.taxable_income < 0:
                self.taxable_income = 0

            self.LOG.info('taxable income {}'.format(self.taxable_income))
        except Exception:
            self.LOG.exception('Exception occurred while calculating taxable income.')
            self.LOG.exception(traceback.format_exc())

    # Calculate the tax
    @before()
    @after
    def Income_Tax_Initialization(self, salary, bonus, incomeTaxableAccounts, pension, nonTaxable_interest, SSB,
                                  preTax_Contributions, HSA_Contributions, filing_Status, numDependents):
        try:
            self.salary = salary
            self.bonus = bonus
            self.incomeTaxableAccounts = incomeTaxableAccounts
            self.pension = pension
            self.nonTaxable_interest = nonTaxable_interest
            self.SSB = SSB
            self.preTax_Contributions = preTax_Contributions
            self.HSA_Contributions = HSA_Contributions
            self.filing_Status = filing_Status
            self.numDependents = numDependents

            self.calculate_essential_parameters()
            self.calculate_taxable_income_pre_deduction()
            self.calculate_taxable_income()
        except Exception:
            self.LOG.exception('Exception occurred while initializing income tax parameters.')
            self.LOG.exception(traceback.format_exc())

    @before()
    @after
    def convert_single_or_joint(self, single_or_joint):
        if single_or_joint.lower().strip() == "single":
            return self.number_of_brackets, self.number_of_brackets * 2
        elif single_or_joint.lower().strip() == "joint":
            return self.number_of_brackets * 2, self.number_of_brackets * 3
        # this is currently useless, need to raise an error
        else:
            self.LOG.error("Error - please specify single or joint, you passed ", single_or_joint)

    # Loading brackets (start taxable income and end taxable income##############################
    @before()
    @after
    def get_federal_tax_brackets(self, simulation_year_number=-1):
        try:
            bracket_start_position, bracket_end_position = self.convert_single_or_joint(self.filing_Status)
            if simulation_year_number == -1:
                return np.vstack((self.federal_annual_tax_brackets[0:self.number_of_brackets, :],
                                  self.federal_annual_tax_brackets[bracket_start_position:bracket_end_position, :]))

            elif 0 <= simulation_year_number <= 100:
                return np.vstack((self.federal_annual_tax_brackets[0:self.number_of_brackets, simulation_year_number],
                                  self.federal_annual_tax_brackets[bracket_start_position:bracket_end_position,
                                  simulation_year_number]))
        except Exception:
            self.LOG.exception('Exception occurred while getting federal tax bracket.')
            self.LOG.exception(traceback.format_exc())

    @before()
    @after
    def calculate_federal_tax(self, simulation_year_number=-1):
        federal_tax = 0
        try:
            temp_brackets = self.get_federal_tax_brackets(simulation_year_number)

            computed_tax = 0

            # Need more information for calculating federal tax in case user supplies -1 as simulation year number.
            if simulation_year_number == -1:
                computed_tax = "Not yet"
            else:
                last_income_bracket = 0
                maxrate = temp_brackets[0, :][len(temp_brackets[0, :]) - 1]

                for x, y in np.nditer([temp_brackets[0, :], temp_brackets[1, :]]):
                    if x != maxrate:
                        if self.taxable_income > y:
                            computed_tax = computed_tax + (x * (y - last_income_bracket))
                            last_income_bracket = y
                        else:
                            computed_tax = computed_tax + (x * (self.taxable_income - last_income_bracket))
                            break
                    else:
                        computed_tax = computed_tax + (x * (self.taxable_income - last_income_bracket))

            self.LOG.info('computed tax = {}'.format(computed_tax))

            if simulation_year_number != -1:
                federal_tax = computed_tax - self.childCredit
        except Exception:
            self.LOG.exception('Exception occurred while calculating federal tax.')
            self.LOG.exception(traceback.format_exc())

        return federal_tax

    # Calculating state tax as per the state rates read from csv
    @before()
    @after
    def calculate_state_tax(self, state):
        state_tax = 0
        try:
            tax_rate = self.state_tax_rate[self.state_tax_rate['State'] == state]['Average Effective Tax Rate'].iloc[0]
            state_tax = self.taxable_income * tax_rate
        except Exception:
            self.LOG.exception('Exception occurred while calculating state tax.')
            self.LOG.exception(traceback.format_exc())
        return state_tax

# np.set_printoptions(suppress=True)
# a = Income_Tax(TaxBracket_file_path_and_name = os.getcwd() + r'\IncomeTaxFiles\TaxBracket2018.csv', StateTaxRates_file_path_and_name = os.getcwd() + r'\IncomeTaxFiles\StateTaxRates.csv',  non_run_inflation_rate =0)
# a.Income_Tax_Initialization(25000,2000,5000,8000,2000,12000,1000,0,'joint',2)
# print('Fedal tax = {}'.format(a.calculate_federal_tax(0)))
# print('State tax = {}'.format(a.calculate_state_tax('CA')))
