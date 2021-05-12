import Common.utils as utils
import Simulation.Sim_Account_Flat as saf

import numpy as np


def flatten_accounts(account, owner_age, flat_account_array):
    for each_balance in account.balance_array:
        flat_account_array.append(saf.Sim_Account_Flat(account.name,
                                                       each_balance[0], each_balance[1], account.sim_file,
                                                       account.early_penality_withdrawal_age,
                                                       account.early_penality_withdrawal_percent, account.rmd_applies,
                                                       account.default_cashflow_status,
                                                       owner_age))
    return flat_account_array


def limit_ee_contributions(flat_contri_array):
    # first cycle through all of the contributions and the limits that apply to them
    # group the contributions that share a limit (e.g. all money sources for a plan limint, all pretax and roth contributions that apply to 402g, ira limits)
    # the group is stored in an array that has the limit_id, limit_amount, if it is a govt limit and then as many contribution objects that apply
    temp_limit_array = []  # will have limit id, limit acount, if it is a govt limit (boolean), and each flat contribuion object that is subject to the limit, contri1, contri2...
    for each_contri in flat_contri_array:
        for each_limit in each_contri.account.applicable_limits_array:
            if each_limit.is_employee and each_contri.money_type in each_limit.money_type_array:
                temp_index = utils.find_row_in_list(temp_limit_array, each_limit.limit_id)
                if temp_index is None:
                    order_id = 1
                    if not each_limit.is_govt:
                        order_id = 0
                    temp_limit_array.append(
                        [each_limit.limit_id, each_limit.limit_amount, each_limit.is_govt, order_id, each_contri])
                else:
                    temp_limit_array[temp_index].append(each_contri)

    # order the array so plan limits are first, if you do govt first you may reduce limits to far
    temp_limit_array = sorted(temp_limit_array, key=lambda x: x[4])
    print(temp_limit_array)

    # now that you have your contribuitons group by the limits that apply you need to check them
    temp_contri_obj_array = []
    temp_annual_contri_array = np.empty((100))
    for each_row in temp_limit_array:

        temp_limit_amount = each_row[1]  # this is the 402g or 415 or plan or whatever dollar limit amount

        for each_contri in range(4, len(each_row)):
            temp_annual_contri_array = np.vstack(temp_annual_contri_array, each_contri.flat_contribution_array)
            temp_contri_obj_array.append(each_contri)

        # you now have all your contributions stacked in a numpy array for 100 years
        # you have a corresponding array of contri objects
        # check to see if any contribuitons applly to the limit (not sure this is necessary but safer to leave in)
        if np.shape(temp_annual_contri_array)[0] > 0:
            temp_annual_contri_array = temp_annual_contri_array[1:]
            num_rows = np.shape(temp_annual_contri_array)[0]
            # for each year, check to see if the contribuiton is above the limit
            for year_iter in range(100):
                uncapped_contri = np.sum(temp_annual_contri_array[:, year_iter])
                # if contribution is above the limit figure out how much you have to reduce it by
                if uncapped_contri > temp_limit_amount:
                    reduce_amount = (uncapped_contri - temp_limit_amount)
                # reduce logic is pretty stupid, just prorates it across all contributions
                # this reset the sim_contribution_Flat contribution amount to the new amount
                for each_contr_obj in temp_contri_obj_array:
                    current_year_contri = each_contr_obj.get_contribution_for_year(year_iter)
                    each_contr_obj.set_contribution_by_year(year_iter,
                                                            reduce_amount * (current_year_contri / uncapped_contri))

    def calculate_match(flat_contri_array):
        pass
