import Flat_Match_Structure as fms


def flatten_match_household(houshehold, advisable_only=False):
    temp_flat_match_array = []
    for ind_iter in range(houshehold.number_of_hohs):
        temp_flattened_match.append(
            flatten_match_inidividual(household.head_of_household_array[ind_iter], advisable_only))

    return temp_flat_match_array


def flatten_match_individual(individual, advisable_only=False):
    temp_flat_match_array = []
    for job_iter in range(inidividual.number_of_jobs):
        temp_flattened_match.append(flatten_match_job(inidividual.job_array[job_iter], individual.name, advisable_only))

    return temp_flat_match_array


def flatten_match_job(job, owner_name="", advisable_only=False):
    temp_flat_match_array = []
    for account_iter in range(job.number_ofaccounts):
        temp_flat_match_array.append(
            flatten_match_account(job.account_array[account_iter], job.name, job.current_earnings,
                                  owner_name, advisable_only))

    return temp_flat_match_array


def flatten_match_account(account, job_name="", job_earnings="", owner_name="", advisable_only=False):
    temp_flat_match_array = []
    for match_row in range(account.total_tiers):
        temp_flat_match_array.append(fms.Flat_Match_Structure(account.match.match_amount[match_iter],
                                                              account.match.match_limit[match_iter],
                                                              account.account_type, account.contribution_limit,
                                                              job_name, job_earnings, owner_name))

    return temp_flat_match_array


def convert_to_dollar_match(flat_match_array):
    temp_flat_match_array = []
    for fmi in flat_match_array:
        temp_flattened_match.append(fmi.convert_to_dollar)
