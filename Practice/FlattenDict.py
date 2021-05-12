# flatten dictionary

BASIC_TYPES = (int,float,str,bool,list,set,tuple,frozenset)
def get_value(obj, field_name, derived_field):
	value_obj = obj[field_name]
	if type(value_obj) in BASIC_TYPES or value_obj is None:
		value = {derived_field:value_obj}
	elif type(value_obj) == dict:
		value = {}
		for inner_field in value_obj:
			tmp_derived_name = derived_field + '_' + inner_field
			value.update(get_value(value_obj, inner_field, tmp_derived_name))
	return value


if __name__ == '__main__':
	obj = {
                'a':1,
                'b':{
                    'c':{
                        'd':4,
                        'e': {
								'x':24,
								'y':25
							}
                        },
                    'f':6
                    }
			}
	flattened = {}
	for field_name in ('a','b'):
		flattened.update(get_value(obj, field_name, field_name))
	print(flattened)
	

