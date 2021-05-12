import pandas as pd
from Common.config import LOG
from copy import deepcopy
from Common.aop import after, before


class EmployeeContribution(object):
    contributionList = []
    salary = 0
    contribution_per_accountType = {}
    employee_contributionDf = pd.DataFrame(columns=['Account Type', 'Intended Contribution', 'Actual Contribution'])

    def __init__(self, contribution_limitDf):
        """
        Create Employee contribution instance and initialize the contribution limit

        :param contribution_limitDf: Dataframe object who has defined limit per account type
        """
        self.contribution_LimitDf = contribution_limitDf
        self.extrapolate_limits()

    @before()
    @after
    def extrapolate_limits(self):
        tempDf = deepcopy(self.contribution_LimitDf[self.contribution_LimitDf['Limit Name'] == '402g'])
        if '401k' not in self.contribution_LimitDf['Limit Name'].tolist():
            tempDf['Limit Name'] = '401k'
            self.contribution_LimitDf = self.contribution_LimitDf.append(tempDf, ignore_index=True)

        if '403b' not in self.contribution_LimitDf['Limit Name'].tolist():
            tempDf['Limit Name'] = '403b'
            self.contribution_LimitDf = self.contribution_LimitDf.append(tempDf, ignore_index=True)

    @before()
    @after
    def employee_contribution_initialization(self, salary, contribution_per_accountType):
        """
        Initialize the Employee data to calculate the contribution against each account type.

        :param salary: employee salary
        :param contribution_per_accountType: Dictionary object who has accounttype as key and tuple of contribution and contributiontype as value
        """
        self.salary = salary
        self.contribution_per_accountType = contribution_per_accountType
        self.validate_input_values()
        self.employee_contributionDf['Account Type'] = list(self.contribution_per_accountType.keys())
        self.employee_contributionDf['Intended Contribution'] = self.contributionList
        self.employee_contributionDf = self.employee_contributionDf.set_index('Account Type').join(
            self.contribution_LimitDf[['Limit Name', 'Limit Amount']].set_index('Limit Name'))

    @before()
    @after
    def validate_input_values(self):
        total_contribution = self.get_total_contribution()
        LOG.info(
            'Total Contribution and Employee Salary is {} and {} respectively.'.format(total_contribution, self.salary))
        if sum(self.contributionList) > self.salary:
            raise ValueError('Total Contribution cannot be greater than the employee salary.')

    @before()
    @after
    def get_total_contribution(self):
        total_contribution = 0

        for value, valuetype in self.contribution_per_accountType.values():
            contribution = self.get_contribution(value, valuetype)
            total_contribution += contribution
            self.contributionList.append(contribution)
        return total_contribution

    @before()
    @after
    def get_contribution(self, contribution_value, type_of_contribution):
        contribution = 0
        if type_of_contribution.lower().strip() in 'percentage':
            contribution = self.salary * contribution_value
            LOG.info('value , contribution {}/{}'.format(contribution_value, contribution))
        else:
            contribution = contribution_value
            LOG.info('value , contribution {}/{}'.format(contribution_value, contribution))
        return contribution

    @before()
    @after
    def get_employee_contribution_per_accountType_limit(self):
        """
        Calculate the contribution based on the limit defined
        :return: dictionary object where accounttype is key and the actual contribution in dollar is value
        """
        intendedContribution = self.employee_contributionDf['Intended Contribution'].tolist()
        limit = self.employee_contributionDf['Limit Amount'].tolist()
        self.employee_contributionDf['Actual Contribution'] = list(
            map(lambda x, y: x if x < y else y, intendedContribution, limit))
        return self.employee_contributionDf
