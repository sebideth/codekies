from flask import Flask, render_template

app = Flask(__name__)

if __name__ == "__main__":
    app.run("127.0.0.1", port="5001", debug=True)

