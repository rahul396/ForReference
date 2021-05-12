import Models.Glidepath as gp


def static_glidepath_creator(starting_portfolio, num_periods):
    """temp_glidepath =[None]*num_periods

    for period_iter in range(num_periods):
        temp_glidepath[period_iter] = starting_portfolio
    """
    temp_glidepath = [starting_portfolio] * num_periods

    return gp.Glidepath(temp_glidepath)


def td_glidepath_creator(asset_class_names_array, start_equity, end_equity, num_periods):
    pass


def random_glidepth_creator(asset_class_names_array, num_periods):
    pass
