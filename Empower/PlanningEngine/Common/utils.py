import json
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.parser import parse
from Common.config import logging

LOG = logging.getLogger(__name__)


def print_time_difference(start_time, end_time, term='ms'):
    if term == 'ms':
        print(np.around((end_time - start_time) * 1000, decimals=3), "ms")
    elif term == 's':
        print(np.around((end_time - start_time), decimals=2), "seconds")
    elif term == 'm':
        print(np.around((end_time - start_time) / 60, decimals=0), "minutes")


def calculate_date_dif(date1, date2=datetime.now(), return_type='years'):
    if return_type.strip().lower() == 'years':
        return date2.year - date1.year - ((date2.month, date2.day) < (date1.month, date1.day))


def interpolate_calculation(x_value, x_coords, y_coords):
    return np.interp(x_value, x_coords, y_coords)


def find_row_in_list(my_list, my_item):
    for r, c in enumerate(my_list):
        if my_item in c:
            return r


def get_dataframe(file_path_and_name_with_ext, ip_sheet_num):
    try:
        xlfile = pd.ExcelFile(file_path_and_name_with_ext)
    except FileNotFoundError as e:
        LOG.exception('File %s not found' % file_path_and_name_with_ext)
    xlsheet_df = xlfile.parse(ip_sheet_num)

    return xlsheet_df


def obj_dict(data):
    top = type('new', (object,), data)
    seqs = tuple, list, set, frozenset
    for i, j in data.items():
        if isinstance(j, dict):
            setattr(top, i, obj_dict(j))
        elif isinstance(j, seqs):
            setattr(top, i,
                    type(j)(obj_dict(sj) if isinstance(sj, dict) else sj for sj in j))
        else:
            if j is not None and type(j) is str:
                if is_parsable_to_int(j):
                    setattr(top, i, int(j))
                elif is_parsable_to_float(j):
                    setattr(top, i, float(j))
                elif j.lower() == 'true':
                    setattr(top, i, True)
                elif j.lower() == 'false':
                    setattr(top, i, False)
                elif j.lower() == 'null':
                    setattr(top, i, None)
                else:
                    setattr(top, i, j)
            else:
                setattr(top, i, j)
    return top


def age_calculator(birthDate):
    if birth_year_validator(birthDate):
        try:
            datetime_obj = parse(birthDate)
            birth_year = datetime_obj.year
            current_year = datetime.now().year
            today = datetime.now().date()
            birthday = datetime_obj.date()
            if birthday < today:
                return current_year - birth_year
            else:
                LOG.exception("BirthDate %s should be less than today" % birthDate)
                return None
        except Exception as e:
            LOG.exception(str(e))
            return None



def birth_year_validator(birthDate):
    try:
        parse(birthDate)
        return True
    except Exception:
        return False



def exception_logger(exception_list, LOG):
    for ex in exception_list:
        LOG.exception(ex)


def is_non_negative(num):
    if type(num).__name__ == 'int':
        if num >= 0:
            return True
        else:
            LOG.info("%s is negative" % num)
            return False
    else:
        LOG.error("%s is not an integer" % num)
        return False


def is_int(data):
    if type(data).__name__ == 'int':
        return True
    else:
        return False


def is_string(data):
    if type(data).__name__ == 'str':
        return True
    else:
        return False


def is_int_or_float(data):
    if type(data).__name__ == 'int' or type(data).__name__ == 'float':
        return True
    else:
        return False


def is_boolean(data):
    if type(data).__name__ == 'bool':
        return True
    else:
        return False


def is_parsable_to_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_parsable_to_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_jsonable(obj):
    try:
        json.dumps(obj)
        return True
    except Exception:
        return False


def complex_encoder(obj):
    to_remove = []
    attributes = obj.__dict__
    reserved_types = (list, tuple, dict, set)
    for key in attributes:
        if not is_jsonable(attributes[key]):
            attr_type = type(attributes[key])
            if not hasattr(attributes[key], 'is_valid') and attr_type not in reserved_types:
                to_remove.append(key)
    for k in to_remove:
        del attributes[k]
    return attributes

