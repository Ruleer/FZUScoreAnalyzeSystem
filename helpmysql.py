import pymysql
import json
import numpy as np
class MysqlHelper():
    def __init__(self,host='localhost',port=3306,user='root',password='Fxn03166',charset='utf8',db='user'):
        self.conn = pymysql.connect(host=host,port=port,user=user,password=password,charset=charset,db=db)
        self.date = ['大一上','大一下','大二上','大二下']
        self.table = ['score1','score2','score3','score4']

    def sentence_term(self,study_number):  #根据学号返回学期数
        curse = self.conn.cursor()
        sql = "select 学期 from student where  学号='%s'" % (str(study_number+' '))
        curse.execute(sql)
        num = curse.fetchone()
        num = int(num)
        curse.close()
        self.conn.close()
        return num

    def pget_all_message(self,study_number):   #返回个人信息
        curse = self.conn.cursor()
        sql = "select 学号,名字,学院 from student where s='%s'" % (str(study_number))
        curse.execute(sql)
        message = curse.fetchall()
        message = list(message)
        jmesssge = {
            "name":["学号","姓名","学院"],
            "message":message
        }
        jsonmessage = json.dumps(jmesssge)
        curse.close()
        self.conn.close()
        return jsonmesssge


    def pget_data(self,study_number):  #返回当前学期的科目和分数
        term = self.sentence_term(study_number)
        curse1=self.conn.cursor()
        curse2=self.conn.cursor()
        sql="select * from '%s' where study_number='%s'" % (str(self.table[self.date.index(term)],study_number))
        curse1.execute(sql)
        data=curse1.fetchall()
        data = list(data)
        data_new = data[4:]
        sql="select COLUMN_NAME from information_schema.COLUMNS where TABLE_SCHEMA = mysql and TABLE_NAME ='%s' " % (str(self.table[self.date.index(term)]))
        curse2.execute(sql)
        namelist = curse2.fetchall()
        namelist = list(namelist)
        namelist_new = namelist[4:]
        namelist_new.append("平均分")
        dataj = {
            "name":namelist_new,
            "score":data_new
        }
        datajson = json.dumps(dataj)
        curse1.close()
        curse2.close()
        self.conn.close()
        return datajson

    def prank_num(self,study_number):   #返回排名和总人数
        term = self.sentence_term(study_number)
        curse = self.conn.cursor()
        sql = "select 总分 from '%s'" % (str(self.table[self.date.index(term)]))
        curse.execute(sql)
        data = curse.fetchall()
        data = list(data)
        sorted(data,reverse=True)
        curse1 = self.conn.cursor()
        sql = "select 总分 from '%s' where 学号='%s'" % (str(self.table[self.date.index(term)]),str(study_number))
        curse1.execute(sql)
        num = curse1.fetchone()
        num = int(num)
        for i in range(len(data)):
            if data[i-1] == num:
                j=i
                break
        jdata = {
            "nums":len(data),
            "rank":j
        }
        jsondata = json.dumps(jdata)
        curse.close()
        curse1.close()
        self.conn.close()
        return jsondata

    def pget_process_line(self,study_number):    #返回各个学期的排名构造曲线图
        curse = self.conn.cursor()
        sql = "select 学期 from student where 学号='%s'" % (str(study_number))
        curse.execute(sql)
        num = curse.fetchone()
        num = int(num)
        rank = []
        for i in range(num):
            p = self.prank_num(study_number,i)
            rank[i-1] = p["rank"]
        linej = {
            "term":self.date[0:num],
            "rank":rank
        }
        linejson = json.dumps(linej)
        curse.close()
        self.conn.close()
        return linejson

    def is_minitor(self,study_number):
        curse = self.conn.cursor()
        sql = "select 班长 from student where 学号='%s'" % (str(study_number))
        curse.execute(sql)
        num = curse.fetchone()
        curse.close()
        self.conn.close()
        num = int(num)
        if num == 0:
            return False
        else:
            return True
    def sentence_class(self,study_number):
        curse = self.conn.cursor()
        sql = "select 班级 from student where 学号='%s'" % (str(study_number))
        curse.execute(sql)
        num = curse.fetchone()
        num = int(num)
        curse.close()
        self.conn.close()
        return num
    def num_of_subject(self,study_number):
        curse = self.conn.cursor()
        term = self.sentence_term(study_number)
        sql = "select COLUMN_NAME from information_schema.COLUMNS where TABLE_SCHEMA = mysql and TABLE_NAME ='%s' " % (str(self.table[self.date.index(term)]))
        curse.execute(sql)
        namelist = curse.fetchall()
        namelist = list(namelist)
        namelist_new = namelist[4:]
        curse.close()
        self.conn.close()
        return len(namelist_new)
    def detail_of_subject(self,study_number):
        curse = self.conn.cursor()
        term = self.sentence_term(study_number)
        sql = "select COLUMN_NAME from information_schema.COLUMNS where TABLE_SCHEMA = mysql and TABLE_NAME ='%s' " % (str(self.table[self.date.index(term)]))
        curse.execute(sql)
        namelist = curse.fetchall()
        namelist = list(namelist)
        namelist_new = namelist[4:]
        curse.close()
        self.conn.close()
        return namelist_new
    def num_of_people(self,study_number):
        class_num = self.sentence_class(study_number)
        curse = self.conn.cursor()
        sql = "select 班长 from student where 学号='%s'" % (str(class_num))
        curse.execute(sql)
        num_list = curse.fetchall()
        num = len(num_list)
        curse.close()
        self.conn.close()
        return num

    def class_case(self,study_number,subject):  #班长查看班级优秀率，及格率，最高最低分，平均分
        excel = 80
        passi = 60
        term = self.sentence_term(study_number)
        num_class = self.sentence_class(study_number)
        num_people = self.num_of_people(study_number)
        curse = self.conn.cursor()
        sql = "select '%s' from '%s' where 班级='%s'" % (str(subject),str(self.table[self.date.index(term)]),str(num_class))
        curse.execute(sql)
        points = curse.fetchall()
        pointslist = list(points)
        max_num = max(pointslist)
        min_num = min(pointslist)
        average = np.mean(pointslist)
        excellent = 0.0
        passing = 0.0
        for i in pointslist:
            if i > 60 or i == 60:
                passing += 1
                if i > 80 or i == 80:
                    excellent += 1
        rate_ofexcellent = excellent / num_people
        rate_ofpassing = passing / num_people
        data = {
            "rate_of_excellent":excellent,
            "rate_of_passing":passing,
            "average":average,
            "max":max_num,
            "min":min_num
        }
        jsondata = json.dumps(data)
        curse.close()
        self.conn.close()
        return jsondata

    def all_stu_scores_in_calss(self,study_number):     #展示班级所有学生成绩
        term = self.sentence_term(study_number)
        class_num = self.sentence_class(study_number)
        curse = self.conn.cursor()
        sql = "select 学号,名字,总分 from '%s' where 班级='%s'" % (str(self.table[self.date.index(term)]),str(class_num))
        curse.execute(sql)
        results = curse.fetchall()
        results = list(results)
        sorted(results,key=lambda x:x[2],reverse=True)
        #转化成json格式

    def all_stu_score_along(self,study_number,subject):
        term = self.sentence_term(study_number)
        class_num = self.sentence_class(study_number)
        curse = self.conn.cursor()
        sql = "select "+"学号"",姓名,"+str(subject)+"from "+self.table[self.date.index(term)]+ "where 班级='%s'" % (str(class_num))
        curse.execute(sql)
        scorelist = list(curse.fetchall())
        sorted(scorelist,key=lambda x:x[2],reverse=True)
        #转化成json格式

    def test_data(self,study_number,subject):
        term = self.sentence_term(study_number)
        class_num = self.sentence_class(study_number)
        curse = self.conn.cursor()
        sql = "select " + "学号"",姓名," + str(subject) + "from " + self.table[self.date.index(term)] + "where 班级='%s'" % (str(class_num))
        curse.execute(sql)
        scorelist = list(curse.fetchall())
        sorted(scorelist, key=lambda x: x[2], reverse=True)
        curse.close()
        self.conn.close()
        return scorelist

    def password_change(self,password):
        curse = self.conn.cursor()
        sql = "update student set 密码='%s'" % (str(password))
        curse.execute(sql)
        curse.close()
        self.conn.close()

    def password_and_username(self,password,username):
        curse = self.conn.cursor()
        sql = "select * from student where 密码='%s' and 账号='%s'" % (str(password),str(username))
        curse.execute(sql)
        k = curse.fetchall()
        if k == None:
            return False
        else:
            return True

if __name__ == '__main__':
    a = MysqlHelper()
    print(a.test_data("031799101","认知实习"))






