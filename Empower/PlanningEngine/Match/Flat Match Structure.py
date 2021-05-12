import pandas as pd
import numpy as np


class Flat_Match_Structure(object):
    def __init__(self, match_amount, match_limit, match_type, account_type, contribution_limit, earnings="",
                 job_name="", owner_name=""):
        self.fms_df = pd.DataFrame(columns=['match_amount', 'match_limit', 'match_type', 'account_type',
                                            'contribution_limit', 'earnings', 'job_name', 'owner_name'])
        self.append_row(match_amount, match_limit, match_type, account_type, contribution_limit, earnings, job_name,
                        owner_name)

    def append_row(self, match_amount, match_limit, match_type, account_type, contribution_limit, earnings="",
                   job_name="", owner_name=""):
        self.fms_df.loc[np.shape(self.fms_df)[0]] = [match_amount, match_limit, match_type, account_type,
                                                     contribution_limit, earnings, job_name, owner_name]

    def sort_by_column(self, column_name, in_ascending_order=True):
        return self.fms_df.sort_values(by=column_name, ascending=in_ascending_order).reset_index(drop=True)

    def adjust_match_for_salary_and_limit(self):
        sorted_fms = self.sort_by_column(['owner_name', 'job_name', 'account_type', 'match_amount'], False)

        num_rows = np.shape(sorted_fms)[0]

        for row_iter in range(num_rows):
            running_total = 0
            limit_reached = False
            salary_or_plan_limit = min(sorted_fms.loc[row_iter, "contribution_limit"],
                                       sorted_fms.loc[row_iter, "earnings"])
            temp_id = sorted_fms.loc[row_iter, "owner_name"] + sorted_fms.loc[row_iter, "job_name"] + sorted_fms.loc[
                row_iter, "account_type"]

            while temp_id == sorted_fms.loc[row_iter, "owner_name"] + sorted_fms.loc[row_iter, "job_name"] + \
                    sorted_fms.loc[row_iter, "account_type"]:
                if limit_reached:
                    sorted_fms.set_value(row_iter, "match_limit", 0)

                elif running_total + sorted_fms.loc[row_iter, "match_limit"] > salary_or_plan_limit:
                    sorted_fms.set_value(row_iter, "match_limit", salary_or_plan_limit - running_total)
                    limit_reached = True

                running_total += sorted_fms.loc[row_iter, "match_limit"]
                row_iter += 1
                if row_iter == num_rows:
                    break
            else:
                continue
            break

        print(sorted_fms)

    def convert_match_to_dollar(self):
        if self.match_type == 'dollar':
            pass
        else:
            self.match_amount = self.match_amount / self.earnings
            self.match_limit = self.match_limit / self.earnings

        if contribution_limit <= 2:
            self.contribution_limit = self.contribution_limit * self.earnings


fms = Flat_Match_Structure(1, 1000, 'dollar', '401k', 3000, 50000, 'c', 'hh1')
fms.append_row(.75, 1000, 'dollar', '401k', 3000, 500, 'a', 'hh1')
fms.append_row(1, 1000, 'dollar', '401k', 3000, 500, 'a', 'hh1')
fms.adjust_match_for_salary_and_limit()
# temp_fms = fms.sort_by_column('match_amount',False)
# print(temp_fms)
