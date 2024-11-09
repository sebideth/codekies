from sqlalchemy import create_engine


# TODO: add config file
collation = "utf8mb4_general_ci"
username = "root"
password = "change_me"
host = "localhost:3306"
database = "codekis"
connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}?collation={collation}"
engine = create_engine(connection_string, echo=True)
