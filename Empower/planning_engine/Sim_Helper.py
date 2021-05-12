import utils
import Sim_Account_Flat as saf
import Sim_Withdrawal_Order as swo
import Sim_Helper as sh
import Sim_Contribution_Flat as scf
import tensorflow as tf
import numpy as np


def flatten_accounts(account, owner_age, flat_account_array):

    for each_balance in account.balance_array:
        flat_account_array.append( saf.Sim_Account_Flat(account.id,
                                    each_balance[0],each_balance[1], account.sim_file, account.early_penality_withdrawal_age,
                                    account.early_penality_withdrawal_percent, account.rmd_applies, account.default_cashflow_status,
                                    owner_age))
    return flat_account_array

def limit_ee_contributions(flat_contri_array):
    #first cycle through all of the contributions and the limits that apply to them
    #group the contributions that share a limit (e.g. all money sources for a plan limint, all pretax and roth contributions that apply to 402g, ira limits)
    #the group is stored in an array that has the limit_id, limit_amount, if it is a govt limit and then as many contribution objects that apply
    temp_limit_array = []#will have limit id, limit acount, if it is a govt limit (boolean), and each flat contribuion object that is subject to the limit, contri1, contri2...
    for each_contri in flat_contri_array:
        for each_limit in each_contri.account.applicable_limits_array:
            if each_limit.is_employee == True  and each_contri.money_type in each_limit.money_type_array:
                temp_index = utils.find_row_in_list(temp_limit_array,each_limit.limit_id)
                if temp_index == None:
                    order_id = 1
                    if each_limit.is_govt == False:
                        order_id =0
                    temp_limit_array.append([each_limit.limit_id, each_limit.limit_amount, each_limit.is_govt, order_id, each_contri])
                else:
                    temp_limit_array[temp_index].append(each_contri)

    #order the array so plan limits are first, if you do govt first you may reduce limits to far
    temp_limit_array = sorted(temp_limit_array, key=lambda x:x[4])
    print (temp_limit_array)

    #now that you have your contribuitons group by the limits that apply you need to check them
    temp_contri_obj_array = []
    temp_annual_contri_array = np.empty((100))
    for each_row in temp_limit_array:

        temp_limit_amount = each_row[1]# this is the 402g or 415 or plan or whatever dollar limit amount

        for each_contri in range(4,len(each_row)):
            temp_annual_contri_array = np.vstack(temp_annual_contri_array,each_contri.flat_contribution_array)
            temp_contri_obj_array.append(each_contri)

        # you now have all your contributions stacked in a numpy array for 100 years
        # you have a corresponding array of contri objects
        #check to see if any contribuitons applly to the limit (not sure this is necessary but safer to leave in)
        if np.shape(temp_annual_contri_array)[0]>0:
            temp_annual_contri_array = temp_annual_contri_array[1:]
            num_rows = np.shape(temp_annual_contri_array)[0]
            #for each year, check to see if the contribuiton is above the limit
            for year_iter in range(100):
                uncapped_contri = np.sum(temp_annual_contri_array[:,year_iter])
                #if contribution is above the limit figure out how much you have to reduce it by
                if  uncapped_contri > temp_limit_amount:
                    reduce_amount = (uncapped_contri - temp_limit_amount)
                #reduce logic is pretty stupid, just prorates it across all contributions
                #this reset the sim_contribution_Flat contribution amount to the new amount
                for each_contr_obj in temp_contri_obj_array:
                    current_year_contri = each_contri_obj.get_contribution_for_year(year_iter)
                    each_contri_obj.set_contribution_by_year(year_iter, reduce_amount * (current_year_contri/uncapped_contri))

def calculate_match(flat_contri_array):
    pass


def get_flat_account_array(household):
    flat_account_array = []
    for each_account in household.account_array:
        flat_account_array = sh.flatten_accounts(each_account, 120, flat_account_array)

    # these are accounts that aren't tied to jobs but are associated with a head of houseold
    for each_hoh in household.head_of_household_array:
        for each_account in each_hoh.account_array:
            flat_account_array = sh.flatten_accounts(each_account, each_hoh.age, flat_account_array)

        for each_job in each_hoh.job_array:
            for each_account in each_job.account_array:
                flat_account_array = sh.flatten_accounts(each_account, each_hoh.age, flat_account_array)

    return flat_account_array


def get_flat_contribution_array(household, temp_hhc, max_contribution_period):
    flat_contribution_array = []
    for each_account in household.account_array:
        for each_contri in each_account.contribution_array:
            flat_contribution_array.append(scf.Sim_Contribution_Flat(temp_hhc.get_earnings(),
                                                                     10, "houeshold", each_account, each_contri))

    # these are accounts that aren't tied to jobs but are associated with a head of houseold
    for each_hoh in household.head_of_household_array:
        max_contribution_period = max(max_contribution_period, each_hoh.retire_age - each_hoh.age)
        for each_account in each_hoh.account_array:
            for each_contri in each_account.contribution_array:
                flat_contribution_array.append(scf.Sim_Contribution_Flat(temp_hhc.get_earnings(each_hoh.name),
                                                                         each_hoh.get_years_to_retirement(),
                                                                         each_hoh.name, each_account, each_contri))

        for each_job in each_hoh.job_array:
            for each_account in each_job.account_array:
                for each_contri in each_account.contribution_array:
                    flat_contribution_array.append(
                        scf.Sim_Contribution_Flat(temp_hhc.get_earnings(ind_name=each_hoh.name, job_name=each_job.name),
                                                  each_hoh.get_years_to_retirement(), each_hoh.name, each_account,
                                                  each_contri))

    return flat_contribution_array


def get_default_account_position(flat_account_array):
    num_account_and_money_source = int(np.shape(flat_account_array)[0])
    for acct_iter in range(num_account_and_money_source):
        if flat_account_array[acct_iter].default_cashflow_status == True:
            default_account_location = acct_iter
            break
    return default_account_location


def get_tensorflow_placeholders(number_of_runs, num_account_and_money_source):
    previous_balance = tf.placeholder(tf.float32, shape=(
        number_of_runs,
        num_account_and_money_source))  # year 0 = start balance, year n = result of calculation
    current_period_cashflow = tf.placeholder(tf.float32,
                                             shape=(number_of_runs, num_account_and_money_source))
    current_period_return = tf.placeholder(tf.float32, shape=(
        number_of_runs, num_account_and_money_source))  # one year of sim file
    current_period_contributions = tf.placeholder(tf.float32,
                                                  shape=(num_account_and_money_source))  # contribution to account
    current_period_rmd = tf.placeholder(tf.float32, shape=(number_of_runs, num_account_and_money_source))

    placeholders = {}
    placeholders['previous_balance'] = previous_balance
    placeholders['current_period_cashflow'] = current_period_cashflow
    placeholders['current_period_return'] = current_period_return
    placeholders['current_period_contributions'] = current_period_contributions
    placeholders['current_period_rmd'] = current_period_rmd

    return placeholders


def get_tensorflow_functions(placeholders):
    calculate_portfolio_value_post_rmd = (placeholders['previous_balance'] - placeholders['current_period_rmd'])
    calculate_portfolio_value_post_cashflow = (
        placeholders['previous_balance'] + placeholders['current_period_cashflow'])
    calculate_portfolio_value_contributions = (placeholders['previous_balance'] * (
        1 + placeholders['current_period_return'])) + placeholders['current_period_contributions']
    calculate_portfolio_value_no_contributions = (
        placeholders['previous_balance'] * (1 + placeholders['current_period_return']))

    tensorflow_function = {}
    tensorflow_function['calculate_portfolio_value_post_rmd'] = calculate_portfolio_value_post_rmd
    tensorflow_function['calculate_portfolio_value_post_cashflow'] = calculate_portfolio_value_post_cashflow
    tensorflow_function['calculate_portfolio_value_contributions'] = calculate_portfolio_value_contributions
    tensorflow_function['calculate_portfolio_value_no_contributions'] = calculate_portfolio_value_no_contributions

    return tensorflow_function


def set_rmd(rmd_tf, individual, balance_tf, flat_account_array, init_params, year):
    num_account_and_money_source = int(np.shape(flat_account_array)[0])

    if individual.age + year >= init_params.rmd_init.min_rmd_age:
        # if you find one person needs an rmd calc, just run trhough th process for all acounts
        for acct_iter in range(num_account_and_money_source):
            if flat_account_array[acct_iter].owner_age + year >= init_params.rmd_init.min_rmd_age and \
                    flat_account_array[acct_iter].rmd_applies:
                rmd_tf[:, acct_iter] = init_params.rmd_init.get_rmd_amount(
                    balance_tf[:, year, acct_iter],
                    flat_account_array[acct_iter].owner_age + year)

            else:
                rmd_tf[:, acct_iter] = 0

    return rmd_tf


def take_out_negative_cashflows(rmd_tf, temp_hhc, year_iter, flat_account_array, balance_tf, net_cashflow_tf):
    default_account_location = get_default_account_position(flat_account_array)

    rmd_net_cashflow = np.sum((rmd_tf), axis=1)
    # net cashflow will be number of runs long, it contains the total amount of money needed to be put in or taken out of accounts
    # the next section will spread the cashflow over all accounts creating a runs X acct_money_source_matrix
    net_cashflow_temp = np.rint(np.sum(temp_hhc.include_in_annual_net_numpy[:, year_iter]) + rmd_net_cashflow)
    # Negative cashflows mean we have to take money out of accounts, code below handles negative cashflows
    # note that it doesn't actually take mony out at this point, it just fugures how much to take out
    # actual reduction in balance will happen in the balance_tf tensorflow calculations below this section
    temp_locations = np.where(net_cashflow_temp < 0)
    # print (np.shape(temp_locations)[1])
    if np.shape(temp_locations)[1] > 0:
        withdrawal_balance_order = swo.order_accounts_for_withdrawal(
            flat_account_array, year_iter, np.average(balance_tf[:, year_iter, :], axis=0),
            len(flat_account_array)
        )

        for acct_iter in range(len(flat_account_array)):
            acct_withd_loc = withdrawal_balance_order[acct_iter]
            # find the row number where the balacne is large enough to supply the entire cash outflow
            temp_locations = np.where(balance_tf[:, year_iter + 1, acct_withd_loc] >= net_cashflow_temp * -1)
            # set that as the withdrawal from account in your final cashflow matrix
            net_cashflow_tf[temp_locations, acct_withd_loc] = net_cashflow_temp[temp_locations]
            # update the cashflow for those runs/row numbers to be zero since the cash outflow has been satisfied
            net_cashflow_temp[temp_locations] = 0
            # now look for any locations where there is a balance but it is not large enough to supply the entire cashflow
            temp_locations = np.intersect1d(np.where(balance_tf[:, year_iter + 1, acct_withd_loc] > 0),
                                            np.where(net_cashflow_temp < 0))
            # set the final cash outflow for the account equal to the account balance so it will go to zero when subtracted
            net_cashflow_tf[temp_locations, acct_withd_loc] = balance_tf[
                                                                  temp_locations, year_iter + 1, acct_withd_loc] * -1
            # adjust the cashflow by the amount of the balance
            net_cashflow_temp[temp_locations] = net_cashflow_temp[temp_locations] + balance_tf[
                temp_locations, year_iter + 1, acct_withd_loc]

            # check to see if all cashflows have been satisified, if so, you can break out of the loop, everything should be zero

            if np.all(np.isclose(net_cashflow_temp, 0)) == True:
                break
        # if there is a negative cashflow left, subtract the cashflow from the default location
        temp_locations = np.where(net_cashflow_temp < 0)
        if np.shape(temp_locations)[1] > 0:
            net_cashflow_tf[temp_locations, default_account_location] = net_cashflow_temp[temp_locations]
            net_cashflow_temp[temp_locations] = 0
        return net_cashflow_tf



