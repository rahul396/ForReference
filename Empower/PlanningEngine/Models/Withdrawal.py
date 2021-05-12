import numpy as np
import Account_Flat as af


# This it the logic that puts an order to the account withdrawal squence
def order_accounts_for_withdrawal(flat_account_array, sim_period, order_type='prorated'):
    for each_account in flat_account_array:
        if sim_period > each_account.locked_for_withdrawal_period:
            if order_type == 'prorated':
                # Prorated takes from all accounts equally while trying to avoid any early withdrawal penalities
                if sim_period <= each_account.penality_age:
                    each_account.set_withdrawal_sequence(1)
                else:
                    each_account.set_withdrawal_sequence(0)
            if order_type == 'by_tax_type':
                # by tax type should be more tax efficient than prorated, sequence is least tax deferral to most tax deferral
                if sim_period > each_account.penality_age:
                    if each_account.money_type == 'pretax':
                        each_account.set_withdrawal_sequence(0)
                    elif each_account.money_type == 'post_tax':
                        each_account.set_withdrawal_sequence(1)
                    elif each_account.money_type == 'roth':
                        each_account.set_withdrawal_sequence(2)
                else:
                    if each_account.money_type == 'taxable':
                        each_account.set_withdrawal_sequence(3)
                    elif each_account.money_type == 'pretax':
                        each_account.set_withdrawal_sequence(4)
                    elif each_account.money_type == 'post_tax':
                        each_account.set_withdrawal_sequence(5)
                    elif each_account.money_type == 'roth':
                        each_account.set_withdrawal_sequence(6)
            # may add some additinal accounts here
            # flaw in this approach is the assumed money types.  I think it is ok for US, maybe this is rewritten for other countries
            # or just jam their money type into one of the four
            else:
                print("account order type " + order_type + "not supported")

    return flat_account_array


def withdrawal_from_ordered_accounts(withdrawal_amount_array, flat_account_array):
    max_withdrawal_sequence = 0
    for each_account in flat_account_array:
        if each_account.withdrawal_sequence > max_withdrawal_sequence:
            max_withdrawal_sequence = each_account.withdrawal_sequence

    for withdrawal_iter in range(max_withdrawal_sequence):
        temp_account_array = np.empty((0))
        for each_account in flat_account_array:
            if each_account.withdrawal_sequence == withdrawal_iter:
                temp_account_array = np.vstack(
                    temp_account_array, each_account.balance_array)

            total_balance_array = np.sum(temp_account_array)
            weighted_balance_array = np.divide(
                temp_account_array, total_balance_array)

            if total_balance_array >= withdrawal_amount_array:
                temp_account_array = temp_account_array - \
                                     (withdrawal_amount_array * weighted_balance_array)
                withdrawal_amount_array = 0
            else:
                withdrawal_acount_array = withdrawal_amount_array - \
                                          np.sum(total_balance_array)
                temp_account_array = 0

            if np.sum(withdrawal_amount_array) == 0:
                break


# don't forget about penalities
# what are you going to do with negative
# should I just say f it, cycle through them all
# or make sure you only withdrawal from one account at a time (lowest balance)
# if you do this, if balance > withdrawal, withdrawal and stop, else withdrawal balance and continue


'''
temp = [None] * 3
temp[0] = af.Account_Flat(1, 'pretax', 100000)
temp[1] = af.Account_Flat(2,'roth',100000)
temp[2]  =af.Account_Flat(3,'pretax',100000,50,.10)
output = withdrawal_from_acconts(temp, 500000,0)
print (np.around(output[:,1]))
'''

# this isn't done, need to address the withdrawal perid and age issue, I hard coded with withdrawal penality
# need to reorder the account and I have two extra accounts
# but I am close, could just do these later to make sure the simulatin is running first since I should be a few steps aways
