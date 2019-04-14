from flask import Flask,url_for,render_template,jsonify,request,redirect
from Mysqlhelper import Mysqlhelper


app = Flask(_name_)
app.config["DEBUG"]=True

@app.route("/",methods=["GET","POST"])
def main_page():
    if request.method == "GET":
        return render_template("login.html",error=False)
    if 账号密码匹配:
        return redirect(url_for('index'))

@app.route("/index")
def index():


@app.route("/logout")
def logout:


if __name__ == '__main__':
    app.run()
