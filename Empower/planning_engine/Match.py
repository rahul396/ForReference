import numpy as np

class Match(object):

    def __init__(self, match_array, applicable_money_type_array = []):
        self.match_stucture = match_array
        self.total_tiers = np.shape(match_array)[0]
        self.match_amount_array = match_array[:,0]
        self.match_limit_array = match_array[:,1]
        self.match_amount_is_percent = match_array[:,2]
        self.match_limit_is_percent = match_array[:,3]
        self.applicable_money_types = applicable_money_type_array


    def get_employer_match_received(self, dollar_contribution):

        total_match_limit= 0
        total_match= 0

        for match_iter in range(np.shape(self.match_limit_array)[0]):
            if contribution > total_match_limit:
                total_match += self.match_amount_array[match_iter] * min(self.match_limit_array[match_iter],contribution)
            else:
                total_match += self.match_amount_array[match_iter] * max(contribution-total_match_limit,0)

            total_match_limit += self.match_limit_array[match_iter]

        return total_match


    def get_match_missed(self, contribution):
        return max(self.total_possible_match - self.get_employer_match(contribution),0)
