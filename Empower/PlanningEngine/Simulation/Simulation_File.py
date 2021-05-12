from scipy.stats import norm
import numpy as np


def Monte_Carlo_Returns_One_Year(port_mean, port_stdev, seed_value, number_of_datapoints=10000):
    return norm.rvs(loc=port_mean, scale=port_stdev, size=number_of_datapoints, random_state=seed_value)


def Monte_Carlo_Returns_All_Years(glidepath, init_params, number_of_runs='', use_fixed_seed=True):
    if number_of_runs == '':
        number_of_runs = init_params.number_of_runs

    monte_carlo_returns = np.empty((number_of_runs), dtype=float)
    number_of_years = glidepath.num_years

    seed_value = 100
    for year_iter in range(number_of_years):
        port_mean = glidepath.expected_return[year_iter]
        port_stdev = glidepath.stdev[year_iter]

        if use_fixed_seed:
            seed_value = seed_value + 1
        else:
            seed_value = np.random.seed()

        monte_carlo_returns = np.vstack((monte_carlo_returns,
                                         Monte_Carlo_Returns_One_Year(port_mean, port_stdev, seed_value,
                                                                      number_of_runs)))
    return np.transpose(monte_carlo_returns[1:number_of_years + 1, :])
