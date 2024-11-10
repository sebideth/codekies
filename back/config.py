import os

from dotenv import load_dotenv

load_dotenv()

debug = True if os.getenv("debug") in ["True", "true"] else False

# Database config
db_username = os.getenv("db_username")
db_password = os.getenv("db_password")
db_name = os.getenv("db_name")
db_host = os.getenv("db_host")
db_collation = os.getenv("db_collation")
