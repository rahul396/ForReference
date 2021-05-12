import numpy as np


# This it the logic that puts an order to the account withdrawal squence
# You can never have a tie, it will break the code that takes money out of accounts
# Tie break is the sum of balances for a given account, the idea is to take money out of accounts with smallest balance
# first so number of accounts with a balance decrease as fast as possible
# that said, it is the sum of the balance across all runs, not each run, not going to have a different order for each sim run
def order_accounts_for_withdrawal(flat_account_array, sim_period, balance_total_array, num_account_and_money_source,
                                  order_type='default'):
    mapping_array = np.transpose(np.vstack((np.empty([num_account_and_money_source]), balance_total_array)))

    # then order by order type and balacne in that order
    # then set withdrawal sequence by iterating in the sorted order referencing the original order

    for acct_iter in range(num_account_and_money_source):
        if sim_period > flat_account_array[acct_iter].locked_for_withdrawal_period:
            if order_type == 'default':
                # Prorated takes from all accounts equally while trying to aviovd any early withdrawal penalities
                if sim_period > flat_account_array[acct_iter].penality_age:
                    mapping_array[acct_iter, 1] = 0
                else:
                    mapping_array[acct_iter, 1] = 1
            elif order_type == 'by_tax_type':
                # by tax type should be more tax efficient than prorated, sequence is least tax deferral to most tax deferral
                if sim_period > flat_account_array[acct_iter].penality_age:
                    if flat_account_array[acct_iter, 1].money_type == 'taxable':
                        mapping_array[acct_iter, 0] = 0
                    elif flat_account_array[acct_iter].money_type == 'pretax':
                        mapping_array[acct_iter, 0] = 1
                    elif flat_account_array[acct_iter, 1].money_type == 'post_tax':
                        mapping_array[acct_iter, 0] = 2
                    elif flat_account_array[acct_iter].money_type == 'roth':
                        mapping_array[acct_iter, 0] = 3
                else:
                    if flat_account_array[acct_iter].money_type == 'pretax':
                        mapping_array[acct_iter, 0] = 4
                    elif flat_account_array[acct_iter].money_type == 'post_tax':
                        mapping_array[acct_iter, 0] = 5
                    elif flat_account_array[acct_iter].money_type == 'roth':
                        mapping_array[acct_iter, 0] = 6
            else:
                print("account order type " + str(order_type) + " not supported")

    # mapping array can now be sorted by column 1 which is money type order, then column two, balance
    return np.lexsort((mapping_array[:, 0], mapping_array[:, 1]))
