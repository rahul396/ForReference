import numpy as np
import pandas as pd
import Individual as ind
import Initialization_Parameters as ip
import Contribution as contr
import Smart_Schedule as sm_sch
import Account as acct
import Pension as pension
import Job
import Portfolio as port
import Simulation_File as sf
import Asset_Class_Properties as ac_prop
import Glidepath_Creator as gpc
import Household as hh
import Cashflow as cf
import Simulation_File as sf
import os
import time
import utils

import Run_Simulation as rs
import Solver_Retirement_Income as sri
import Solver_Social_Security as sss

#Define Initialization parameters
chr_dir = os.getcwd()
initialization_file = os.path.join(chr_dir,'setup_files','Initialization_Parameters.xlsx')

init_params = ip.Initialization_Parameters(initialization_file)
#Create glidepath
start_time = time.clock()
equity_asset_class = "Emerging Market Equity"
fixed_income_asset_class = "Cash"
acp = init_params.asset_class_properties_init
temp_asset_classes = [equity_asset_class, fixed_income_asset_class]

#Improve you probalby need a set for glidepath so you can get the nubmers of years you want, only marginal improvement

temp_weights = [0,1]
temp_portfolio = port.Portfolio(temp_asset_classes,temp_weights, init_params)
temp_glidepath = gpc.static_glidepath_creator(temp_portfolio, 100)
temp_sim_file_1 = sf.Monte_Carlo_Returns_All_Years(temp_glidepath, init_params)

temp_weights = [0,1]
temp_portfolio = port.Portfolio(temp_asset_classes,temp_weights, init_params)
temp_glidepath = gpc.static_glidepath_creator(temp_portfolio, 100)
temp_sim_file_2 = sf.Monte_Carlo_Returns_All_Years(temp_glidepath, init_params)

temp_weights = [0,1]
temp_portfolio = port.Portfolio(temp_asset_classes,temp_weights, init_params)
temp_glidepath = gpc.static_glidepath_creator(temp_portfolio, 100)
temp_sim_file_3 = sf.Monte_Carlo_Returns_All_Years(temp_glidepath, init_params)

#Create Contribution
temp_contribution_array_hh1 = [contr.Contribution(.10,"pretax", True,"Empower Account")]
temp_contribution_array_hh2_ira = [contr.Contribution(1000,"pretax", False,"GWI Account")]
temp_contribution_array_hh2 = [contr.Contribution(1000,"pretax", False,"Monica IRA")]

temp_smart_schedule = sm_sch.Smart_Schedule(5,.01,'percent')


#Create Account
temp_account = acct.Account("Empower Account", "401k", [["pretax", 1000],["roth",2000]], temp_glidepath, temp_sim_file_1, init_params, temp_contribution_array_hh1, temp_smart_schedule)
temp_job_account_array_hh1 = [temp_account]

temp_account = acct.Account("Monica IRA", "Taxable", [["Taxable", 100000]], temp_glidepath, temp_sim_file_2,  init_params,temp_contribution_array_hh2_ira)
temp_hh_account_array_hh2 = [temp_account]

temp_account = acct.Account("GWI Account", "401k", [["roth",5000]], temp_glidepath, temp_sim_file_3,  init_params,temp_contribution_array_hh2)
temp_job_account_array_hh2 = [temp_account]


#Create Job
temp_job = Job.Job("Empower", 20000, temp_job_account_array_hh1, init_params, earnings_curve_id = 'technology')
temp_job_array_hh1 = [temp_job]
temp_job = Job.Job("GWI", 20000, temp_job_account_array_hh2, init_params)
temp_job_array_hh2 = [temp_job]

#Create Individual
temp_person_1 = ind.Individual("Chandler", "1982-4-2",65, "male", 200000,'dollar', init_params, "cancer",[], temp_job_array_hh1)
temp_person_2 = ind.Individual("Monica", "1982-4-2",65, "female", 10000,'dollar', init_params, "cancer",temp_hh_account_array_hh2, temp_job_array_hh2)

#Create pension
temp_pension_hh1 = pension.Pension('hh1_p1',temp_person_1.retire_age - temp_person_1.age, 5000, init_params)
temp_person_1.set_pension_array([temp_pension_hh1])

#Create a cashflow
temp_cashflow = [cf.Cashflow("hhc", 2020,2030,-2000, init_params, True, True, .01, False)]

#Create a houeshold
temp_hh_array = [temp_person_1, temp_person_2]

start_time = time.clock()
temp_household = hh.Household(temp_hh_array,"TX",init_params, cashflow_array = temp_cashflow)

utils.print_time_difference(start_time, time.clock())

result  = rs.run_simulation(temp_household, init_params)
print ("Printing first result")
print (result)
#temp_person_2.retirement_need = temp_person_2.retirement_need *.9
#temp_person_1.retirement_need = temp_person_1.retirement_need *.9

#ToDo: Improve, need to adjust pension start age if reitre age is updated
temp_person_2.set_ss_start_age(62, False)
temp_person_1.set_ss_start_age(62, False)
result = rs.run_simulation(temp_household, init_params)
print ("Printing 2nd result")
print (result)
utils.print_time_difference(start_time, time.clock())


# solver_ri = sri.Solver_Retirement_Income(temp_household, init_params, True, True)
# solver_ri.solve_for_income()



solver_ss = sss.Solver_Social_Security(temp_household,init_params, True, True)
solver_ss.optimize_ss_no_gap()
