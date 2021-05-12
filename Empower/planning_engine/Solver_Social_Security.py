import numpy as np
import Run_Simulation as rs
import Solver_Retirement_Income as sri
class Solver_Social_Security(object):

    def __init__(self, household, init_params, solve_for_hoh_1 , solve_for_hoh_2 = False):
        self.household = household
        self.init_params = init_params
        self.solve_for_hoh_1 = solve_for_hoh_1
        self.solve_for_hoh_2 = solve_for_hoh_2
        self.hoh_1_age = self.household.head_of_household_array[0].age
        self.hoh_1_total_comp = self.household.head_of_household_array[0].total_comp
        if self.household.number_of_hohs ==2:
            self.hoh_2_age = self.household.head_of_household_array[1].age
            self.hoh_2_total_comp = self.household.head_of_household_array[1].total_comp


    def optimize_ss_no_gap(self):
        ri_solver = sri.Solver_Retirement_Income(self.household, self.init_params, True, True)
        all_claiming_array = self.init_params.social_security_init.get_benefit_for_all_household_claiming_ages(self.hoh_1_age, self.hoh_1_total_comp, self.hoh_2_age, self.hoh_2_total_comp)
        all_claiming_array =  all_claiming_array[all_claiming_array[:,-1].argsort()][::-1]

        max_income = -1000000000
        self.household.head_of_household_array[1].life_expectancy =95
        for row_iter in all_claiming_array:

            self.household.head_of_household_array[0].set_ss_start_age(row_iter[0], True)
            if self.solve_for_hoh_2:
                self.household.head_of_household_array[1].set_ss_start_age(row_iter[2], True)

            if (self.household.head_of_household_array[0].life_expectancy > self.household.head_of_household_array[0].ss_start_age and
                self.household.head_of_household_array[1].life_expectancy > self.household.head_of_household_array[1].ss_start_age):
                ri_solver.household = self.household
                temp_income =  ri_solver.solve_for_income()
                if temp_income > max_income:
                    print (row_iter, "   " , int(temp_income), "  ", int(max_income))
                    max_income = temp_income
                    best_row = row_iter
                else:
                    print ("passing on ", row_iter, "  income ", int(temp_income))


        print ("best", best_row)
