import logging.config, yaml

# Logging section
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# streamHandler = logging.StreamHandler()
# streamHandler.setFormatter(formatter)
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[logging.FileHandler("PlanningEngine.log"),
#
#               logging.StreamHandler()]
# )
def load_logging_config():
    with open('./Common/LogConfig.yaml', 'rt') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

# Various configurations related to Social Security Benefit calculation
youngest_claim_age = 62
oldest_claim_age = 70
current_year = 2018

# Temporarily Hardcoded, but have to extract from environment variable
context_file_name = "C:\\Users\\rku172\\Documents\\PythonPractice\\Empower\\PlanningEngine\\Resources\\Initialization_Parameters.xlsx"
# context_file_name = "C:\\Initialization_Parameters.xlsx"

birthyear_retire_age_dict = [(1937, 65), (1954, 66)]
default_retire_age = 67

retirement_need_adjustment_after_death = .8
