import numpy as np
import Sim_Household_Cashflows as shhc
import tensorflow as tf
import time
import Sim_Helper as simulation_helper


# IMPROVE, add bequest support
# IMPROVE, tax taxable account by adjusting the sim file
# IMPROVE, calculate taxable income
def run_simulation(household, init_params):
    max_contribution_period = 0

    temp_hhc = shhc.Sim_Household_Cashflows(household, init_params)
    min_cashflow_period = min(household.get_min_rmd_period(), temp_hhc.get_min_cashflow_period())

    flat_contribution_array = simulation_helper.get_flat_contribution_array(household, temp_hhc,
                                                                            max_contribution_period)
    flat_account_array = simulation_helper.get_flat_account_array(household)

    # throw an error if there is no default account, accounts obj should have always created one
    default_account_location = simulation_helper.get_default_account_position(flat_account_array)
    num_account_and_money_source = int(np.shape(flat_account_array)[0])
    max_periods_alive = household.max_periods_alive

    # Initialize output arrays
    balance_output = np.zeros([init_params.number_of_runs, num_account_and_money_source], dtype=int)
    net_cashflow_output = np.zeros([init_params.number_of_runs, num_account_and_money_source], dtype=int)
    total_balance_output = np.zeros([init_params.number_of_runs, max_periods_alive], dtype=int)
    net_cashflow_output_total = np.zeros([init_params.number_of_runs, max_periods_alive])

    balance_tf = np.empty([init_params.number_of_runs, max_periods_alive + 1, num_account_and_money_source])
    sim_file_tf = np.empty([init_params.number_of_runs, max_periods_alive, num_account_and_money_source])
    contributions_tf = np.empty([max_contribution_period, num_account_and_money_source])
    net_cashflow_tf = np.zeros([init_params.number_of_runs, num_account_and_money_source])

    for acct_iter in range(num_account_and_money_source):
        balance_tf[:, 0, acct_iter] = float(flat_account_array[acct_iter].start_balance)
        sim_file_tf[:, :, acct_iter] = flat_account_array[acct_iter].sim_file[:, :max_periods_alive]
        contributions_tf[:, acct_iter] = flat_contribution_array[acct_iter].flat_contri_array[:max_contribution_period]

    tensorflow_placeholders = simulation_helper.get_tensorflow_placeholders(init_params.number_of_runs, num_account_and_money_source)
    tensorflow_functions = simulation_helper.get_tensorflow_functions(tensorflow_placeholders)

    start_time = time.clock()
    with tf.Session() as sess:

        for year_iter in range(max_periods_alive):
            # check to see if need to calculate RMD, should save some time
            rmd_tf = np.zeros([init_params.number_of_runs, num_account_and_money_source])
            for each_hoh in household.head_of_household_array:
                rmd_tf = simulation_helper.set_rmd(rmd_tf, each_hoh, balance_tf, flat_account_array, init_params, year_iter)

            # process the RMDs so the account balances are adjusted before you staett cashflows, if not accounts can go negative to fast
            feed_dict = {
                tensorflow_placeholders['previous_balance']: balance_tf[:, year_iter, :],
                tensorflow_placeholders['current_period_rmd']: rmd_tf,
            }
            balance_tf[:, year_iter + 1, :] = sess.run(tensorflow_functions['calculate_portfolio_value_post_rmd'], feed_dict=feed_dict)

            rmd_net_cashflow = np.sum((rmd_tf), axis=1)
            # net cashflow will be number of runs long, it contains the total amount of money needed to be put in or taken out of accounts
            # the next section will spread the cashflow over all accounts creating a runs X acct_money_source_matrix
            net_cashflow_temp = np.rint(np.sum(temp_hhc.include_in_annual_net_numpy[:, year_iter]) + rmd_net_cashflow)

            # a bit hacky, assuming all RMDs are taxable, should hold true in the US
            # I don't think taxable_cashflows works, may need to do it later
            # taxable_cashflows = np.sum(temp_hhc.taxable_cashflows_numpy[:,year_iter]) + rmd_net_cashflow

            # positive cashflows, if they exist, are directed to the default account
            temp_locations = np.where(net_cashflow_temp > 0)
            net_cashflow_tf = np.zeros([init_params.number_of_runs, num_account_and_money_source])
            if np.shape(temp_locations)[1] > 0:
                net_cashflow_tf[temp_locations, default_account_location] = net_cashflow_temp[temp_locations]
                net_cashflow_temp[temp_locations] = 0

            # take out negative cashflows before further processing
            net_cashflow_tf = simulation_helper.take_out_negative_cashflows(rmd_tf, temp_hhc, year_iter,
                                                                            flat_account_array, balance_tf,
                                                                            net_cashflow_tf)
            # process the cashflows first so you can see negative account balances and adjsut returns
            # don't want to have market return on a negative balance
            feed_dict = {
                tensorflow_placeholders['previous_balance']: balance_tf[:, year_iter + 1, :],
                tensorflow_placeholders['current_period_cashflow']: net_cashflow_tf,
            }
            balance_tf[:, year_iter + 1, :] = sess.run(tensorflow_functions['calculate_portfolio_value_post_cashflow'], feed_dict=feed_dict)

            temp_locations = np.where(balance_tf[:, year_iter + 1, :] < 0)
            if np.shape(temp_locations)[1] > 0:
                sim_file_tf[temp_locations[0], :, temp_locations[1]] = 0

            if year_iter < max_contribution_period:
                feed_dict = {
                    tensorflow_placeholders['previous_balance']: balance_tf[:, year_iter + 1, :],
                    tensorflow_placeholders['current_period_return']: sim_file_tf[:, year_iter, :],
                    tensorflow_placeholders['current_period_contributions']: contributions_tf[year_iter, :]
                }
                balance_tf[:, year_iter + 1, :] = sess.run(tensorflow_functions['calculate_portfolio_value_contributions'], feed_dict=feed_dict)
            else:
                feed_dict = {
                    tensorflow_placeholders['previous_balance']: balance_tf[:, year_iter + 1, :],
                    tensorflow_placeholders['current_period_return']: sim_file_tf[:, year_iter, :],
                }
                balance_tf[:, year_iter + 1, :] = sess.run(tensorflow_functions['calculate_portfolio_value_no_contributions'], feed_dict=feed_dict)

            balance_output = np.hstack((balance_output, balance_tf[:, year_iter, :]))
            net_cashflow_output = np.hstack((net_cashflow_output, np.rint(net_cashflow_tf)))
            total_balance_output[:, year_iter] = np.sum(balance_tf[:, year_iter, :], axis=1)
            net_cashflow_output_total[:, year_iter] = np.sum(net_cashflow_tf, axis=1)

        return total_balance_output[:, -1]
