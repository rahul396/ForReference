import numpy as np

class Account_Contribution_Limit(object):

    def __init__(self, init_params, limit_id):

        temp_matirx = init_params.Account_Contribution_Limit_Initalization.limit_matrix
        temp_index = np.where(temp_matix[:,0] == limit_id)
        if temp_index == None:
            print("error: limit_id not found - ", limit_id)
        else:
            self.limit_id = temp_matrix[temp_index,0]
            self.limit_amount = temp_matrix[temp_index,1]
            self.limit_is_percent =temp_matrix[temp_index,2]
            self.is_ee_only_limit = temp_matrix[temp_index,3]
            self.is_govt_limit = temp_matrix[temp_index,4]
            self.money_type_array = temp_matrix[temp_index,5].split(',')
