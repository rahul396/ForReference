import numpy as np


def create_cashflow_array( amount, start_period, end_period, end_simulation, init_params, inflate_to_start = False,
    inflate_to_end = False, inflation_override = ''):

    #print (owner, id, amount, start_period, end_period, end_simulation, inflate_to_start, inflate_to_end, inflation_override)
    if inflation_override != '':
        inflation =  inflation_override
    else:
        inflation = init_params.asset_class_properties_init.inflation

    end_period = int(end_period)
    start_period = int(start_period)
    #Check if end_period is greater than start_period or not
    if end_period < start_period:
        end_period = start_period

    end_simulation = int(end_simulation)
    start_cashflow = amount

    if inflate_to_start:
        start_cashflow  = np.fv(inflation,start_period,0,amount *-1)

    if inflate_to_end:
        temp_cashflow_array = np.fv(inflation,np.arange(end_period-start_period),0,start_cashflow*-1)

    else:
        temp_cashflow_array = np.full((end_period - start_period),start_cashflow)

    return  np.hstack((np.zeros(start_period),temp_cashflow_array,np.zeros(end_simulation - end_period)))
