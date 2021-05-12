import numpy as np
import Flat_Match_Structure as fms


def get_optimized_match(fms_array, total_contribution, init_params):
    # sort fms array by first column
    sort_array = np.empty(([np.shape(fms_array)[0], 2]))
    i = 0
    for fms_item in fms_array:
        sort_array[i, 0] = fms_item.match_amount
        sort_array[i, 1] = i
        i = i + 1

    sort_array.view('i8,i8').sort(order=['f0'], axis=0)
    sorted_fms_array = []

    for sort_iter in reversed(sort_array):
        sorted_fms_array.append(fms_array[int(sort_iter[1])])

    running_contribution = 0
    temp_match_array = []
    for fms_item in sorted_fms_array:
        if running_contribution + fms_item.match_limit <= total_contribution:
            temp_match_array.append(
                [fms_item.match_limit, fms_item.account_type, fms_item.job_name, fms_item.owner_name,
                 fms_item.earnings])
            running_contribution += fms_item.match_limit
        elif running_contribution < total_contribution:
            temp_match_array.append(
                [total_contribution - running_contribution, fms_item.account_type, fms_item.job_name,
                 fms_item.owner_name, fms_item.earnings])
            running_contribution += (total_contribution - running_contribution)
        else:
            break

    return temp_match_array


temp_fms_array = []
temp_fms_array.append(fms.Flat_Match_Structure(1, 1000, 'dollar', '401k', 3000, 50000, 'j1', 'hh1'))
temp_fms_array.append(fms.Flat_Match_Structure(.5, 1000, 'dollar', '401k', 3000, 50000, 'j1', 'hh1'))
temp_fms_array.append(fms.Flat_Match_Structure(.25, 1000, 'dollar', '401k', 3000, 50000, 'j1', 'hh1'))
temp_fms_array.append(fms.Flat_Match_Structure(1, 1000, 'dollar', '401k', 1000, 10000, 'j2', 'hh1'))
temp_fms_array.append(fms.Flat_Match_Structure(.75, 5000, 'dollar', '401k', 18000, 4000, 'j1', 'hh2'))
temp_fms_array.append(fms.Flat_Match_Structure(.50, 1000, 'dollar', '401k', 18000, 100000, 'j2', 'hh2'))
temp_fms_array.append(fms.Flat_Match_Structure(.4, 1000, 'dollar', '401k', 18000, 50000, 'j2', 'hh2'))
temp_fms_array.append(fms.Flat_Match_Structure(.3, 1000, 'dollar', '401k', 18000, 50000, 'j2', 'hh2'))
# self,match_amount, match_limit, match_type, account_type, contribution_limit, earnings = "", job_name = "", owner_name = "")

print(get_optimized_match(temp_fms_array, 7500, "int"))
