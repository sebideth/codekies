from flask import Flask

from commands.database import database_cli

app = Flask(__name__)

app.cli.add_command(database_cli)

if __name__ == "__main__":
    app.run("127.0.0.1", port="5001", debug=True)

