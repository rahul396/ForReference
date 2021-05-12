import numpy as np

class Sovler_Reach_Goal(object):

    def __init__(self, household,init_params, adj_hoh1_ra, adj_hoh_2_ra, adj_hoh1_sr_array, adj_hoh_2_sr_array, target_percentile = 90):
        self.household = household
        self.init_params = init_params
        self.adj_hoh_1_ra = adj_hoh1_ra
        self.adj_hoh_2_ra = adj_hoh_2_ra
        self.adj_hoh_1_sr_array = adj_hoh_1_sr_array
        self.adj_hoh_2_sr_array = adj_hoh_2_sr_array
        self.target_percentile = target_percentile
