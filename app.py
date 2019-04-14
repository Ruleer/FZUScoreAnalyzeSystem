from flask import Flask
from flask import render_template,request
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("test.html", comment="testaaa")

if __name__ == '__main__':
    app.run()