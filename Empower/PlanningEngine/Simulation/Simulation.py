import numpy as np
import Simulation.Sim_Household_Cashflows as shhc
import Simulation.Sim_Withdrawal_Order as swo
import Simulation.Sim_Helper as sh
import Simulation.Sim_Contribution_Flat as scf
import tensorflow as tf
import Common.utils as utils
import time


# IMPROVE, add bequest support
# IMPROVE, tax taxable account by adjusting the sim file
# IMPROVE, calculate taxable income

class Simulation:
    def run_simulation(self, household, context):

        max_contribution_period = 0

        temp_hhc = shhc.Sim_Household_Cashflows(household, context)
        min_cashflow_period = min(household.get_min_rmd_period(), temp_hhc.get_min_cashflow_period())

        flat_contribution_array = []
        flat_account_array = []
        # these are household accounts, they aren't related to a specific head of household
        for each_account in household.account_array:
            for each_contri in each_account.contribution_array:
                flat_contribution_array.append(scf.Sim_Contribution_Flat(temp_hhc.get_earnings(),
                                                                         10, "houeshold", each_account, each_contri))

            flat_account_array = sh.flatten_accounts(each_account, 120, flat_account_array)

        # these are accounts that aren't tied to jobs but are associated with a head of houseold
        for each_hoh in household.head_of_household_array:
            max_contribution_period = max(max_contribution_period, each_hoh.retire_age - each_hoh.age)
            for each_account in each_hoh.account_array:
                for each_contri in each_account.contribution_array:
                    flat_contribution_array.append(scf.Sim_Contribution_Flat(temp_hhc.get_earnings(each_hoh.name),
                                                                             each_hoh.get_years_to_retirement(),
                                                                             each_hoh.name, each_account, each_contri))

                flat_account_array = sh.flatten_accounts(each_account, each_hoh.age, flat_account_array)

            for each_job in each_hoh.job_array:
                for each_account in each_job.account_array:
                    for each_contri in each_account.contribution_array:
                        flat_contribution_array.append(scf.Sim_Contribution_Flat(
                            temp_hhc.get_earnings(ind_name=each_hoh.name, job_name=each_job.name),
                            each_hoh.get_years_to_retirement(), each_hoh.name, each_account, each_contri))

                    flat_account_array = sh.flatten_accounts(each_account, each_hoh.age, flat_account_array)

        '''
        for each_contri in flat_contribution_array:
            sh.limit_ee_contributions(flat_contribution_array)
            sh.calculate_match(flat_contribution_array[year_iter])
            sh.limit_er_contributions(flat_contribution_array)
        '''

        num_account_and_money_source = int(np.shape(flat_account_array)[0])
        max_periods_alive = household.max_periods_alive
        # min cashflow period is never set approptiratly, either set it properly or remove it

        # for each_account in flat_account_array:
        #    each_account.print_properties()
        for acct_iter in range(num_account_and_money_source):
            if flat_account_array[acct_iter].default_cashflow_status:
                default_account_location = acct_iter
                break
                # throw an error if there is no default account, accounts obj should have always created one

        balance_tf = np.empty([context.number_of_runs, max_periods_alive + 1, num_account_and_money_source])
        sim_file_tf = np.empty([context.number_of_runs, max_periods_alive, num_account_and_money_source])
        contributions_tf = np.empty([max_contribution_period, num_account_and_money_source])
        net_cashflow_tf = np.zeros([context.number_of_runs, num_account_and_money_source])

        for acct_iter in range(num_account_and_money_source):
            balance_tf[:, 0, acct_iter] = float(flat_account_array[acct_iter].start_balance)
            sim_file_tf[:, :, acct_iter] = flat_account_array[acct_iter].sim_file[:, :max_periods_alive]
            contributions_tf[:, acct_iter] = flat_contribution_array[acct_iter].flat_contri_array[:max_contribution_period]

        previous_balance = tf.placeholder(tf.float32, shape=(
            context.number_of_runs,
            num_account_and_money_source))  # year 0 = start balance, year n = result of calculation
        current_period_cashflow = tf.placeholder(tf.float32,
                                                 shape=(context.number_of_runs, num_account_and_money_source))
        current_period_return = tf.placeholder(tf.float32, shape=(
            context.number_of_runs, num_account_and_money_source))  # one year of sim file
        current_period_contributions = tf.placeholder(tf.float32,
                                                      shape=(num_account_and_money_source))  # contribution to account
        current_period_rmd = tf.placeholder(tf.float32, shape=(context.number_of_runs, num_account_and_money_source))

        calculate_portfolio_value_post_rmd = (previous_balance - current_period_rmd)
        calculate_portfolio_value_post_cashflow = (previous_balance + current_period_cashflow)
        calculate_portfolio_value_contributions = (previous_balance * (
            1 + current_period_return)) + current_period_contributions
        calculate_portfolio_value_no_contributions = (previous_balance * (1 + current_period_return))

        balance_output = np.zeros([context.number_of_runs, num_account_and_money_source], dtype=int)
        net_cashflow_output = np.zeros([context.number_of_runs, num_account_and_money_source], dtype=int)
        total_balance_output = np.zeros([context.number_of_runs, max_periods_alive], dtype=int)
        net_cashflow_output_total = np.zeros([context.number_of_runs, max_periods_alive])

        start_time = time.clock()
        with tf.Session() as sess:

            for year_iter in range(max_periods_alive):
                # check to see if need to calculate RMD, should save some time
                rmd_tf = np.zeros([context.number_of_runs, num_account_and_money_source])
                for each_hoh in household.head_of_household_array:
                    if each_hoh.age + year_iter >= context.rmd_init.min_rmd_age:
                        # if you find one person needs an rmd calc, just run trhough th process for all acounts
                        for acct_iter in range(num_account_and_money_source):
                            if flat_account_array[acct_iter].owner_age + year_iter >= context.rmd_init.min_rmd_age and \
                                    flat_account_array[acct_iter].rmd_applies:
                                rmd_tf[:, acct_iter] = context.rmd_init.get_rmd_amount(
                                    balance_tf[:, year_iter, acct_iter],
                                    flat_account_array[acct_iter].owner_age + year_iter)

                            else:
                                rmd_tf[:, acct_iter] = 0

                # process the RMDs so the account balances are adjusted before you start cashflows, if not accounts can go negative to fast
                balance_tf[:, year_iter + 1, :] = sess.run(calculate_portfolio_value_post_rmd,
                                                           feed_dict={previous_balance: balance_tf[:, year_iter, :],
                                                                      current_period_rmd: rmd_tf,
                                                                      })

                rmd_net_cashflow = np.sum((rmd_tf), axis=1)
                # net cashflow will be number of runs long, it contains the total amount of money needed to be put in or taken out of accounts
                # the next section will spread the cashflow over all accounts creating a runs X acct_money_source_matrix
                net_cashflow_temp = np.rint(
                    np.sum(temp_hhc.include_in_annual_net_numpy[:, year_iter]) + rmd_net_cashflow)

                # a bit hacky, assuming all RMDs are taxable, should hold true in the US
                # I don't think taxable_cashflows works, may need to do it later
                # taxable_cashflows = np.sum(temp_hhc.taxable_cashflows_numpy[:,year_iter]) + rmd_net_cashflow

                # positive cashflows, if they exist, are directed to the default account
                temp_locations = np.where(net_cashflow_temp > 0)
                net_cashflow_tf = np.zeros([context.number_of_runs, num_account_and_money_source])
                if np.shape(temp_locations)[1] > 0:
                    net_cashflow_tf[temp_locations, default_account_location] = net_cashflow_temp[temp_locations]
                    net_cashflow_temp[temp_locations] = 0

                # Negative cashflows mean we have to take money out of accounts, code below handles negative cashflows
                # note that it doesn't actually take mony out at this point, it just fugures how much to take out
                # actual reduction in balance will happen in the balance_tf tensorflow calculations below this section
                temp_locations = np.where(net_cashflow_temp < 0)
                # print (np.shape(temp_locations)[1])
                if np.shape(temp_locations)[1] > 0:
                    withdrawal_balance_order = swo.order_accounts_for_withdrawal(
                        flat_account_array, year_iter, np.average(balance_tf[:, year_iter, :], axis=0),
                        num_account_and_money_source
                    )

                    for acct_iter in range(num_account_and_money_source):
                        acct_withd_loc = withdrawal_balance_order[acct_iter]
                        # find the row number where the balacne is large enough to supply the entire cash outflow
                        temp_locations = np.where(
                            balance_tf[:, year_iter + 1, acct_withd_loc] >= net_cashflow_temp * -1)
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

                        if np.all(np.isclose(net_cashflow_temp, 0)):
                            break
                    # if there is a negative cashflow left, subtract the cashflow from the default location
                    temp_locations = np.where(net_cashflow_temp < 0)
                    if np.shape(temp_locations)[1] > 0:
                        net_cashflow_tf[temp_locations, default_account_location] = net_cashflow_temp[temp_locations]
                        net_cashflow_temp[temp_locations] = 0

                # process the cashflows first so you can see negative account balances and adjsut returns
                # don't want to have market return on a negative balance
                balance_tf[:, year_iter + 1, :] = sess.run(calculate_portfolio_value_post_cashflow,
                                                           feed_dict={previous_balance: balance_tf[:, year_iter + 1, :],
                                                                      current_period_cashflow: net_cashflow_tf,
                                                                      })

                temp_locations = np.where(balance_tf[:, year_iter + 1, :] < 0)
                if np.shape(temp_locations)[1] > 0:
                    # print (temp_locations)
                    sim_file_tf[temp_locations[0], :, temp_locations[1]] = 0

                if year_iter < max_contribution_period:
                    balance_tf[:, year_iter + 1, :] = sess.run(calculate_portfolio_value_contributions,
                                                               feed_dict={
                                                                   previous_balance: balance_tf[:, year_iter + 1, :],
                                                                   current_period_return: sim_file_tf[:, year_iter, :],
                                                                   current_period_contributions: contributions_tf[
                                                                                                 year_iter, :]})
                else:
                    balance_tf[:, year_iter + 1, :] = sess.run(calculate_portfolio_value_no_contributions,
                                                               feed_dict={
                                                                   previous_balance: balance_tf[:, year_iter + 1, :],
                                                                   current_period_return: sim_file_tf[:, year_iter, :],
                                                               })

                balance_output = np.hstack((balance_output, balance_tf[:, year_iter, :]))
                net_cashflow_output = np.hstack((net_cashflow_output, np.rint(net_cashflow_tf)))
                total_balance_output[:, year_iter] = np.sum(balance_tf[:, year_iter, :], axis=1)
                net_cashflow_output_total[:, year_iter] = np.sum(net_cashflow_tf, axis=1)

            # utils.output_to_excel(net_cashflow_output[1:], init_params, "all_cashflow_by_account.csv")
            # utils.output_to_excel(net_cashflow_output_total [1:], init_params, "all_cashflows_total.csv")
            # utils.output_to_excel(balance_output[1:], init_params, "balance_all_accounts.csv")
            # utils.output_to_excel(total_balance_output[1:], init_params, "balance_total.csv")
            print("90th percentile wealth", np.percentile(total_balance_output[:, -1], 10))
            print("50th percentile wealth", np.percentile(total_balance_output[:, -1], 50))
            print("percent of successful runs",
                  np.shape(np.where(total_balance_output[:, -1] > 0))[1] / context.number_of_runs * 100)
            print("time in session")
            utils.print_time_difference(start_time, time.clock())
            # return np.percentile(total_balance_output[:,-1],10)
            return total_balance_output[:, -1]
