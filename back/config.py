import os

from dotenv import load_dotenv

load_dotenv()

username = os.getenv("username")
password = os.getenv("password")
database = os.getenv("database")
host = os.getenv("host")
collation = os.getenv("collation")
debug = True if os.getenv("debug") in ["True", "true"] else False
