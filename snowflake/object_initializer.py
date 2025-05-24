import os

def init_snowflake_object(session):
    db = os.environ["SNOWFLAKE_DATABASE"]
    schema = os.environ["SNOWFLAKE_SCHEMA"]
    stage = os.environ["SNOWFLAKE_STAGE"]
    wh = os.environ["SNOWFLAKE_WAREHOUSE"]
    
    sql_statements = [
        f"CREATE OR REPLACE DATABASE {db};",
        f"CREATE OR REPLACE SCHEMA {db}.{schema};",
        f"CREATE OR REPLACE WAREHOUSE {wh};",
        f"USE DATABASE {db};",
        f"USE SCHEMA {schema};",
        f"USE WAREHOUSE {wh};",
        f"""
            CREATE OR REPLACE STAGE {stage}
                DIRECTORY = ( ENABLE = true )
                ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE' );
        """
    ]
    for sql in sql_statements:
        session.sql(sql).collect()