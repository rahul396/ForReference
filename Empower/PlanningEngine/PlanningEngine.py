from Common.config import logging
from Common import utils
from Common.context import Context
from Common.aop import after, before
from Simulation.Simulation import Simulation
from Models.Portfolio import Portfolio
from Models.Contribution import Contribution
from Models.SmartSchedule import SmartSchedule
from Models.Account import Account
from Models.Pension import Pension
from Models.Job import Job
from Models.Individual import Individual
from Models.Household import Household
from Models.Cashflow import Cashflow
from Models.Glidepath import Glidepath
import Simulation.Simulation_File as sf
import traceback
import time
import json


class PlanningEngine:
    def __init__(self):
        self.LOG = logging.getLogger(self.__class__.__name__)
        self.context = Context()

    @before()
    @after
    def validateHouseHold(self, request):
        try:
            json_data = request
            user_Data = json_data['personDetails']
            temp_household = self.create_household(self.context, user_Data)

            if temp_household.is_valid:
                result_dict = json.dumps(temp_household, default=utils.complex_encoder,
                                         sort_keys=True)
                return json.loads(result_dict)

            else:
                exceptions = temp_household.exception_list
                return "Process failed due to following errors: %s" % exceptions

        except Exception as e:
            return "Error Occurred %s" % e

    def runSimulation(self, request):
        try:
            simulation = Simulation()
            start_time = time.clock()
            utils.print_time_difference(start_time, time.clock())
            json_data = request
            user_Data = json_data['personDetails']
            temp_household = self.create_household(self.context, user_Data)
            result = simulation.run_simulation(temp_household, self.context)
            utils.print_time_difference(start_time, time.clock())
            result = result.tolist()
            data = json.dumps(result)
            return {'Simulation': data}

        except Exception as e:
            traceback.print_exc()
            return "Error Occurred %s " % e

    def create_household(self, context, data):
        equity_asset_class = "Emerging Market Equity"
        fixed_income_asset_class = "Cash"
        temp_asset_classes = [equity_asset_class, fixed_income_asset_class]
        # temp_weights = [[1, 0], [.5, .5], [0, 1], [1, 0], [.5, .5], [0, 1]]
        temp_weights = [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1]]
        household_array = []
        person_index = 0
        index = 0
        state_code = ''
        cashflow_array_obj = None

        for person_data in data:
            account_array = []
            rk_account_array = []
            person = utils.obj_dict(person_data)

            for account in person.account:
                try:
                    account_obj = self.create_rk_account(account, temp_asset_classes,
                                                         weight=temp_weights[index])
                    index += 1
                    rk_account_array.append(account_obj)

                except Exception:
                    self.LOG.exception("Exception occurred while creating Account object")

            for account in person.otherAssetDetails:
                try:
                    account_obj = self.create_external_account(account, temp_asset_classes,
                                                               weight=temp_weights[index])
                    index += 1
                    account_array.append(account_obj)

                except Exception:
                    self.LOG.exception(
                        "Exception occurred while creating account object from Other Assets")

            job_obj = self.create_obj(Job, person.employment, account_array=rk_account_array,
                                      context=context)
            job_array = [job_obj]

            participant_data = getattr(person, 'participantData', None)

            if participant_data is not None and participant_data.userCaseType.investor.pension:
                pension_array = [self.create_obj(Pension, person)]
            else:
                pension_array = []

            individual_obj = self.create_obj(Individual, person, retirement_need_type='dollar',
                                             context=context,
                                             health_state='cancer',
                                             account_array=account_array, job_array=job_array,
                                             pension_array=pension_array)

            if person_index == 0:
                cashflow_obj = self.create_cashflow(participant_data)
                cashflow_array_obj = [cashflow_obj]
                state_code = person.stateCode
                person_index += 1
            household_array.append(individual_obj)

        household_obj = self.create_obj(Household, person, household_array, state_code, context, [],
                                        cashflow_array_obj)
        return household_obj

    def create_obj(self, class_name, data, *args, **kwargs):
        if args is not None and len(args) > 0:
            obj = class_name(*args)
        elif kwargs is not None and len(kwargs) > 0:
            obj = class_name(**kwargs)
        else:
            obj = class_name()

        if data is not None:
            obj.set_values(data)

        is_valid = obj.validate()
        if is_valid:
            try:
                obj.set_additional_parameters()
                obj.validate_additional_parameters()
            except Exception as ex:
                self.LOG.exception("Error Occurred %s " % ex)

        return obj

    def create_rk_account(self, account, asset_classes, weight):
        account_name = getattr(account, "accountDefinitionName", None)
        combined_id = getattr(account, "id", None)
        holding_balance = getattr(account, "holdingsBalance", None)
        start_year = getattr(account, "startYear", None)

        portfolio_obj = self.create_obj(Portfolio, None, self.context, asset_classes,
                                        weight)
        portfolio_array = [portfolio_obj] * 100
        temp_glidepath = self.create_obj(Glidepath, None, portfolio_array)
        sim_file = sf.Monte_Carlo_Returns_All_Years(temp_glidepath, self.context)

        money_type, account_type = self.get_money_and_account_type(combined_id)
        contribution_array = self.create_contribution_array(account)
        smart_schedule_obj = self.create_obj(SmartSchedule, account)

        account_obj = self.create_obj(Account, None, account_name, account_type,
                                      [[money_type, holding_balance]], temp_glidepath, sim_file,
                                      self.context,
                                      contribution_array, start_year, smart_schedule_obj)
        return account_obj

    def create_external_account(self, account, asset_classes, weight):
        contribution_array = []
        account_name = account.accountTypeName
        portfolio_obj = self.create_obj(Portfolio, None, self.context, asset_classes,
                                        weight)
        portfolio_array = [portfolio_obj] * 100
        temp_glidepath = self.create_obj(Glidepath, None, portfolio_array)
        sim_file = sf.Monte_Carlo_Returns_All_Years(temp_glidepath, self.context)
        for contribution in account.currentContribution.contributionDetail:
            contribution.accountTypeName = account_name
            contribution_array.append(self.create_obj(Contribution, contribution))

        # Need to check below mapping
        balance_array = [[account.accountTypeCode, account.accountBalance]]
        account_obj = self.create_obj(Account, account, balance_array=balance_array,
                                      glidepath=temp_glidepath, sim_file=sim_file,
                                      context=self.context,
                                      contribution_array=contribution_array)
        return account_obj

    def get_money_and_account_type(self, combined_id):
        money_type = None
        account_type = None
        combined_id = combined_id.lower().split("~")[1]
        money_types = ['pretax', 'roth', 'mix', 'posttax']
        for data in money_types:
            if data in combined_id:
                money_type = data
                account_type = combined_id.replace(data, '')
        return (money_type, account_type)

    def create_contribution_array(self, account):
        account_name = getattr(account, "accountDefinitionName", None)
        combined_id = getattr(account, "id", None)
        money_type, account_type = self.get_money_and_account_type(combined_id)
        savings_plan = getattr(account, "savingsPlan", None)
        amount = None
        percent = None
        is_percent = False
        if savings_plan is not None:
            amount = getattr(savings_plan, "amount", None)
            if amount is not None:
                value = getattr(amount, "value", None)
            percent = getattr(savings_plan, "percentage", None)
            if value is not None:
                is_percent = False
                contribution_array = [self.create_obj(Contribution, None, value,
                                                      money_type, is_percent, account_name)]
            elif percent is not None:
                is_percent = True
                contribution_array = [self.create_obj(Contribution, None, percent,
                                                      money_type, is_percent, account_name)]
            else:
                contribution_array = [self.create_obj(Contribution, None)]

        return contribution_array

    def create_cashflow(self, participant_data):
        cashflow_data = None
        generic_cashflow = None
        try:
            if participant_data is not None:
                generic_cashflow = getattr(participant_data.userCaseType, 'genericCashflow', None)
        except Exception as ex:
            self.LOG.exception("Error Occurred %s " % ex)

        if generic_cashflow is not None:
            for cashflow in generic_cashflow:
                cashflow_data = cashflow

        cashflow_obj = self.create_obj(Cashflow, cashflow_data,
                                       context=self.context,
                                       inflate_to_start=True, inflate_to_end=True,
                                       inflation_override_amount=.01, is_taxable=False)

        return cashflow_obj
