from flask import Flask, render_template

from functions.initial.initial_script import initial_script

app = Flask(__name__)



initial_script()


@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
