from Common.config import LOG
from Common.aop import after, before


class EmployerContribution(object):
    salary_limit = 280000
    salary = 0
    employee_contribution = 0
    employer_match_tier_match_list = []

    @before()
    @after
    def employer_contribution_initialization(self, salary, employee_contribution, employer_match_tier_match_list):
        """
        initialize parameters to calculate employer contribution.

        :param salary: salary of employee
        :param employee_contribution: employee contribution
        :param employer_match_tier_match_list: list of tuples of employer match percentage and tier match percentage
        :return:
        """
        self.salary = salary
        self.employee_contribution = employee_contribution
        self.employer_match_tier_match_list = employer_match_tier_match_list
        self.limit_salary()

    def limit_salary(self):
        if self.salary > self.salary_limit:
            self.salary = self.salary_limit

    @before()
    @after
    def calculate_employer_contribution(self):
        """
        calculate the contribution by employer
        :return: employer contribution
        """
        employer_contribution = 0
        for employer_match, tier_match in self.employer_match_tier_match_list:
            employer_contribution += (self.salary * employer_match * tier_match)
        return employer_contribution
