import os
from snowflake.snowpark import Session
from dotenv import load_dotenv
load_dotenv()

def get_snowpark_session():
    connection_parameters = {
    "account": os.environ["SNOWFLAKE_ACCOUNT"],
    "user": os.environ["SNOWFLAKE_USER"],
    "password": os.environ["SNOWFLAKE_PASSWORD"],
    }
    return Session.builder.configs(connection_parameters).create()
