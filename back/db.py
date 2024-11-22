from sqlalchemy import create_engine, text
from config import db_username, db_password, db_host, db_collation, db_name

def engine_with_no_database():
    return create_engine(f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}?collation={db_collation}", echo=False)

def engine():
    connection_string = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}/{db_name}?collation={db_collation}"
    return create_engine(connection_string, echo=False)

def run_query(connection, query, parameters=None):
    result = connection.execute(text(query), parameters)
    connection.commit()
    return result
