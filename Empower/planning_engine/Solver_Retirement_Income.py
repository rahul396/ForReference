import numpy as np
import Run_Simulation as rs


class Solver_Retirement_Income(object):

    def __init__(self, household,init_params, solve_for_hoh_1, solve_for_hoh_2 = False, target_percentile = 90):
        self.household = household
        self.init_params = init_params
        self.solve_for_hoh_1 = solve_for_hoh_1
        self.solve_for_hoh_2 = solve_for_hoh_2
        self.target_percentile = target_percentile



    def solve_for_income(self):

        prob_of_success = -1
        if self.solve_for_hoh_1:
            spend_split_for_hoh_1 = 1
        if self.solve_for_hoh_2:
            spend_split_for_hoh_1 = 0
        if self.solve_for_hoh_1 and self.solve_for_hoh_2:
            spend_split_for_hoh_1=  self.household.head_of_household_array[0].retirement_need/(self.household.head_of_household_array[0].retirement_need + self.household.head_of_household_array[1].retirement_need)

        num_guess = -1
        while prob_of_success != self.target_percentile:
            current_spending = 0
            if self.solve_for_hoh_1:
                current_spending += self.household.head_of_household_array[0].retirement_need
            if self.solve_for_hoh_2:
                current_spending += self.household.head_of_household_array[1].retirement_need

            ending_wealth = rs.run_simulation(self.household, self.init_params)
            prob_of_success = int(round(np.shape(np.where(ending_wealth>0))[1]/self.init_params.number_of_runs*100))
            ending_wealth_at_target = np.percentile(ending_wealth, 100-self.target_percentile)
            #bigger step size for smaller expected return seems better (.045 for all cash, .033 for all equity)
            new_spend = current_spending + ending_wealth_at_target * .045
            #print ("ending wealth at target ", ending_wealth_at_target, " current spend ", int(current_spending)," new spend", int(new_spend), " spend split ", spend_split_for_hoh_1)
            if self.solve_for_hoh_1:
                self.household.head_of_household_array[0].retirement_need = new_spend * spend_split_for_hoh_1
            if self.solve_for_hoh_2:
                self.household.head_of_household_array[1].retirement_need = new_spend * (1-spend_split_for_hoh_1)

            num_guess +=1

            #print (ending_wealth_at_target, "prob ", prob_of_success, "rn1 = ", self.household.head_of_household_array[0].retirement_need, " rn2 = ", self.household.head_of_household_array[1].retirement_need )

        print ("number of guesses required for solver = " ,num_guess)
        return self.household.head_of_household_array[0].retirement_need +self.household.head_of_household_array[1].retirement_need
