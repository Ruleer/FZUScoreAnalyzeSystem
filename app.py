from flask import Flask,url_for,render_template,jsonify,request,redirect
from helpmysql import *
import json
import sys

app = Flask(__name__)
app.config["DEBUG"]=True
a = MysqlHelper()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login",methods=["GET","POST"])
def main_page():
    if request.method == "GET":
        return render_template("once.html",error=False)     #发送get请求则返回登录页面
    data = request.form
    password = data.get('password')
    username = data.get('username')
    print(password)
    print(username)
    if a.password_and_username(password=password,username=username):
        a.get_status_login(username=username)
        return username #登陆成功则返回个人信息
    else:
        return "202"

@app.route("/enterSelf")
def enterSelf_page():
    return render_template('studenReport.html')

@app.route("/enterMointer")
def enterMointer_page():
    return render_template('mointor.html')

@app.route("/studentself",methods=["GET","POST"])
def student():
    data = request.args
    username = data.get('username')
    return jsonify(a.is_minitor(study_number=username),a.pget_all_message(study_number=username),a.get_term(study_number=username))

@app.route("/self")    #进入个人首页
def self_page():
    data = request.args
    username = data.get('username')
    if data.get('status') == str(201):
        a.get_status_logout(username=username)
        return "success"                 #状态码为退出则返回主页面
    parameter = data.get('parameter')
    term = data.get('term')
    term = int(term)
    print(parameter)
    print(term)
    if parameter == "report_card":
        data1 = a.pget_data(study_number=username, term=term)
        data2 = a.prank_num(study_number=username, term=term)
        return jsonify(data1, data2)
    if parameter == "weak_and_best" :
        print("aaa")
        return jsonify(a.pget_weak_best(study_number=username,term=term))
    if parameter == "progress" :
        return jsonify(a.pget_process_line(study_number=username))
    if a.is_minitor(study_number=username) == 1:                #班长操作面
        subject = data.get('subject')
        if parameter == "detail_of_subject":  #获取科目名
            return jsonify(a.detail_of_subject(study_number=username,term=term))
        if parameter == "class_total_case":    #查看班级所有学生成绩
            return jsonify(a.all_stu_scores_in_calss(study_number=username,term=term))
        if parameter == "subject_score_line":      #班级成绩段划分
            return jsonify(a.class_subject_analyse(study_number=username,subject=subject,term=term))
        if parameter == "single_score_class":     #单科学生成绩
            return jsonify(a.all_stu_score_along(study_number=username,subject=subject,term=term))



if __name__ == '__main__':
    app.run()