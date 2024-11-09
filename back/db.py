from sqlalchemy import create_engine
from config import username, password, host, collation, database

connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}/{database}?collation={collation}"

engine = create_engine(connection_string, echo=False)


def engine_with_no_database():
    connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}?collation={collation}"
    return create_engine(connection_string, echo=False)
