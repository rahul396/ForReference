import pandas as pd
import numpy as np
import argparse


column_names_str = "(display_name,datasource_id,report_id,field_id,field_type,field_name,tooltip_description,placeholder_text,csv_header_name,db_column_name,data_type,csv_sequence,sort_key,dist_key,created_at,updated_at,is_request,is_db,db_data_size,db_data_type,is_visible,is_primary)"
values_str = "('{display_name}',{datasource_id},{report_id},1,'{field_type}','{field_name}','','','{csv_header_name}','{db_column_name}','{data_type}',2,0,0,NULL,NULL,{is_request},{is_db},{db_data_size},'{db_data_type}',1,NULL)"
base_query_staging = "INSERT INTO dc_admin_staging.report_form_fields {column_names_str} VALUES {values_str};"
child_query_staging = "INSERT INTO dc_admin_staging.child_report_form_fields {column_names_str} VALUES {values_str};"

DATA_TYPE_MAPPINGS = {
		'varchar':'string',
		'float':'numeric',
		'array': 'child',
		'list': 'child'
	} 

def create_sql_query(df_row, datasource_id, report_id, is_child_report=False):
	""" 
	Construct a query based on the dataframe row 
	"""
	
	csv_header_name = df_row.csv_header_name if 'csv_header_name' in df_row else df_row.field_name
	db_column_name = df_row.db_column_name.replace('.','_') if 'db_column_name' in df_row else df_row.field_name

	# db_data_type column is of varchar type. So if the value is NULL then single quotes should NOT be applied
	if df_row.db_data_size == 'NULL':
		db_data_size = df_row.db_data_size
	elif df_row.data_type == 'string':
		db_data_size = "'" + str(int(df_row.db_data_size))+ "'"
	else:
		db_data_size = "'" + str(df_row.db_data_size)+ "'"

	is_request = 1
	is_db = 1
	if df_row.data_type in ("child","complex"):
		is_request = 1
		is_db = 0
		
	values = values_str.format(
					display_name = get_display_name(df_row.field_name, convert_to_proper_case),
					datasource_id = datasource_id,
					report_id = report_id,
					field_name = df_row.field_name.lstrip().rstrip(),
					field_type = df_row.field_type.lstrip().rstrip(),
					csv_header_name = csv_header_name.lstrip().rstrip(),
					db_column_name = db_column_name.lstrip().rstrip(),
					data_type = df_row.data_type,
					db_data_size = db_data_size,
					db_data_type = df_row.data_type,
					is_request = is_request,
					is_db = is_db
				)

	if is_child_report:
		query = child_query_staging.format(
						column_names_str = column_names_str,
							values_str = values
						)
	else:
		query = base_query_staging.format(
						column_names_str = column_names_str,
						values_str = values
						)
	
	return query

def convert_to_proper_case(field):
	"""
	Convert names like sample_field --> SampleField to be used in display_name column
	"""
	field = field.lstrip().rstrip()
	field = field[0].upper() + field[1:]
	while True:
		try:
			i = field.index('_')
			field = field[:i] + field[i+1].upper() + field[i+2:]
		except:
			break
	return field

def dot_to_underscore(field):
	"""
	Convert names like this.that into this_that
	"""
	field = field.lstrip().rstrip()
	while True:
		try:
			i = field.index('.')
			field = '_'.join([field[:i],field[i+1:]])
		except:
			break
	return field
			

def get_display_name(field, *steps):
	"""
	Get the field display name based the sequence of methods applied on it. The sequence should be
	a list of methods that defines how should the field display name created based on the field_name. 
	One such example is convert_to_proper_case(field) method. Write your own criteria function
	if the available functions are not sufficients
	"""
	for criteria_function in steps:
		field =  criteria_function(field)
	
	return field

								
	
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--datasource_id", help="Pass the datasource id of the connector", type=int)
	parser.add_argument("--report_id", help="Report id as defined in the reports table",type=int)
	parser.add_argument("--is_child_report",help="Optional. If passed, then the query is prepared for child_report_form_fields table", type=bool, default=False)
	parser.add_argument("--include_headers", help="Options. If passed, then the first line of the csv will be considered as headers", type=bool, default=False)
	
	args = parser.parse_args()
	datasource_id = args.datasource_id
	report_id = args.report_id
	is_child_report = args.is_child_report
	filename = input('Enter csv filename with path: ')

	if filename.split('.')[-1] == 'xlsx':
		df = pd.read_excel(filename)
	elif filename.split('.')[-1] == 'csv':	
		if args.include_headers:
			df = pd.read_csv(filename)
		else:
			df = pd.read_csv(filename, names=('field_name','data_type','db_data_size'))
	
	df = df.replace(np.nan, 'NULL', regex=True)
	
	# Some data_types have different names in schema vs database. E.g varchar in schema is string in our database.
	for data_type in DATA_TYPE_MAPPINGS:
		df.loc[df.data_type==data_type, 'data_type'] = DATA_TYPE_MAPPINGS[data_type]
	
	# If the field names have '.' in them, replace them with '_' as it is not advisable to use a column with '.'
	# df.field_name = df.field_name.str.replace('.','_')

	queries = []
	for index, df_row in df.iterrows():
		# if df_row.field_name in to_add:
			query = create_sql_query(df_row, datasource_id, report_id, is_child_report)
			queries.append(query)
	
	with open('./output.sql','w+') as f:
		for q in queries:
			print(q)
			f.write(q + '\n')
	
	print('*******************Queries created successfully***************************')
	
	
	
					
					
	
