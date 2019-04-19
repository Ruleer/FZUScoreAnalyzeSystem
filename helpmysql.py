import pymysql
import json
import numpy as np

class MysqlHelper():
    def __init__(self,host='localhost',port=3306,user='root',password='Acer3101',charset='utf8',db='user'):
        self.conn = pymysql.connect(host=host,port=port,user=user,password=password,charset=charset,db=db)
        self.table = ['score1','score2','score3','score4']

    def pget_all_message(self,study_number):   #返回个人信息
        curse = self.conn.cursor()
        self.conn.ping(reconnect=True)
        sql = "select 学号,姓名,学院 from student where 学号='%s'" % (str(study_number))
        curse.execute(sql)
        message = curse.fetchall()
        message = list(message)
        n = self.get_term(study_number=study_number)
        jmesssge = {
            "name":["学号","姓名","学院"],
            "message":message,
            "now_term":n
        }
        curse.close()
        self.conn.close()
        return jmesssge

    def get_institute(self,study_number):
        curse = self.conn.cursor()
        self.conn.ping(reconnect=True)
        sql = "select 学院 from student where 学号='%s'" % (str(study_number))
        curse.execute(sql)
        data = curse.fetchall()
        institute = data[0][0]
        return institute

    def pget_data(self,study_number,term):       #返回当前学期的科目和分数
        institute = self.get_institute(study_number=study_number)
        curse1 = self.conn.cursor()
        curse2 = self.conn.cursor()
        curse3 = self.conn.cursor()
        self.conn.ping(reconnect=True)
        sql = "select * from subjects where 学期='%s' and 学院='%s'" %(str(term),str(institute))
        curse2.execute(sql)
        dsubjects = curse2.fetchall()
        dsubjects = list(dsubjects)
        subjects = {}
        for i in range(len(dsubjects[0])-2):
            subjects[i] = dsubjects[0][i+2]
        subject = ""
        for j in range(len(dsubjects[0])-2):
            if j != (len(dsubjects[0])-3):
                subject = subject + str(dsubjects[0][j+2]) + ","
            else:
                subject = subject + str(dsubjects[0][j+2])
        sql="select "+subject+" from "+str(self.table[term-1])+" where 学号='%s'" % (str(study_number))
        curse1.execute(sql)
        data=curse1.fetchall()
        data_new = list(data[0])
        sql = "select 总分,平均分 from "+str(self.table[term-1])+" where 学号='%s'" % (str(study_number))
        curse3.execute(sql)
        total = curse3.fetchall()
        total_data = list(total[0])
        dataj = {
            "subjects":subjects,
            "report":data_new
        }
        datak = {
            "total":["总分","平均分"],
            "total_data":total_data
        }
        datajson = {
            "datadetail":dataj,
            "datatotal":datak
        }
        curse1.close()
        curse2.close()
        curse3.close()
        self.conn.close()
        return datajson

    def prank_num(self,study_number,term):             #返回排名和总人数班级
        class_num = self.sentence_class(study_number=study_number)
        curse = self.conn.cursor()
        self.conn.ping(reconnect=True)
        sql = "select 总分 from "+str(self.table[term-1])+" where 班级='%s'" % (str(class_num))
        curse.execute(sql)
        data = curse.fetchall()
        data = list(data)
        data = sorted(data,reverse=True)
        curse1 = self.conn.cursor()
        self.conn.ping(reconnect=True)
        sql = "select 总分 from "+str(self.table[term-1])+" where 学号='%s'" % (str(study_number))
        curse1.execute(sql)
        nums = curse1.fetchone()
        num = nums[0]
        num = int(num)
        for i in range(len(data)):
            if data[i-1][0] == num:
                break
        jdata = {
            "class_nums":len(data),
            "class_rank":i
        }
        curse.close()
        curse1.close()
        self.conn.close()
        return jdata

    def pget_weak_best(self,study_number,term):         #优势和弱势学科
        class_nums = self.num_of_people(study_number=study_number)
        jdata = self.pget_data(study_number=study_number,term=term)
        scores = jdata['datadetail']['report']
        subjects = jdata['datadetail']['subjects']
        subject_num = len(subjects)
        rank = {}
        for i in range(subject_num):
            subject = subjects[i]
            all_data = self.all_stu_score_along(study_number=study_number,subject=subject,term=term)
            for j in range(class_nums):
                if scores[i] == all_data[j][2]:
                    rank[str(subject)] = j+1
                    break
        rank = sorted(rank.items(),key=lambda x:x[1],reverse=True)
        weak = rank[0:2]
        best = rank[-2:]
        datal = {
            "weak":weak,
            "best":best
        }
        data2 = self.pget_data(study_number=study_number,term=term)
        data2 = data2['datadetail']
        data3 = {
            "weak_best":datal,
            "datadetail":data2
        }
        return data3

    def get_term(self,study_number):  #获得学期
        curse = self.conn.cursor()
        self.conn.ping(reconnect=True)
        sql = "select 学期 from student where 学号='%s'" % (str(study_number))
        curse.execute(sql)
        num = curse.fetchall()
        n = num[0][0]
        n = int(n)
        return n

    def pget_process_line(self,study_number):        #返回各个学期的排名构造曲线图年级排名
        term = self.get_term(study_number=study_number)
        curse = self.conn.cursor()
        self.conn.ping(reconnect=True)
        rank = {}
        for i in range(term):
            p = self.prank_num(study_number=study_number,term=(i+1))
            rank[i+1] = int(p["class_rank"])
        linej = {
            "class_rank":rank
        }
        curse.close()
        return linej
    def is_minitor(self,study_number):
        curse = self.conn.cursor()
        self.conn.ping(reconnect=True)
        sql = "select 班长 from student where 学号='%s'" % (str(study_number))
        curse.execute(sql)
        nums = curse.fetchone()
        curse.close()
        self.conn.close()
        num = int(nums[0])
        if num == 0:
            return 0
        else:
            return 1

    def sentence_class(self,study_number):     #判断班级
        curse = self.conn.cursor()
        sql = "select 班级 from student where 学号='%s'" % (str(study_number))
        self.conn.ping(reconnect=True)
        curse.execute(sql)
        nums = curse.fetchone()
        num = nums[0]
        num = int(num)
        curse.close()
        self.conn.close()
        return num

    def num_of_subject(self,study_number,term):     #判断学科数
        return len(self.detail_of_subject(study_number=study_number,term=term))

    def detail_of_subject(self,study_number,term):        #给出学科详情
        curse = self.conn.cursor()
        institute = self.get_institute(study_number=study_number)
        self.conn.ping(reconnect=True)
        sql = "select * from subjects where 学期='%s' and 学院='%s'" % (str(term),str(institute))
        curse.execute(sql)
        namelist = curse.fetchall()
        namelist = list(namelist)
        subjects = {}
        for i in range(len(namelist[0])-2):
            subjects[i] = namelist[0][i+2]
        curse.close()
        self.conn.close()
        return subjects

    def num_of_people(self,study_number):            #班级人数
        class_num = self.sentence_class(study_number)
        curse = self.conn.cursor()
        self.conn.ping(reconnect=True)
        sql = "select 班长 from student where 班级='%s'" % (str(class_num))
        curse.execute(sql)
        num_list = curse.fetchall()
        num_class = len(num_list)
        curse.close()
        self.conn.close()
        return num_class

    def class_case(self,study_number,subject,term):    #班长查看班级优秀率，及格率，最高最低分，平均分
        excel = 85
        passi = 60
        num_class = self.sentence_class(study_number)
        num_people = self.num_of_people(study_number)
        curse = self.conn.cursor()
        self.conn.ping(reconnect=True)
        sql = "select "+str(subject)+" from "+str(self.table[term-1])+" where 班级='%s'" % (str(num_class))
        curse.execute(sql)
        points = curse.fetchall()
        pointslist = list(points)
        max_num = max(pointslist)[0]
        min_num = min(pointslist)[0]
        average = np.mean(pointslist)
        excellent = 0.0
        passing = 0.0
        for i in range(len(pointslist)):
            if pointslist[i][0] > passi or pointslist[i][0] == passi:
                passing += 1
                if pointslist[i][0] > excel or pointslist[i][0] == excel:
                    excellent += 1
        rate_ofexcellent = round(excellent / num_people,2)
        rate_ofpassing = round(passing / num_people,2)
        data = {
            "rate_of_excellent":rate_ofexcellent,
            "rate_of_passing":rate_ofpassing,
            "average":round(average,2),
            "max":int(max_num),
            "min":int(min_num)
        }
        curse.close()
        self.conn.close()
        return data

    def all_stu_scores_in_calss(self,study_number,term):     #展示班级所有学生成绩
        class_num = self.sentence_class(study_number)
        curse = self.conn.cursor()
        self.conn.ping(reconnect=True)
        sql = "select 学号,名字,总分 from "+str(self.table[term-1])+" where 班级='%s'" % (str(class_num))
        curse.execute(sql)
        results = curse.fetchall()
        results = list(results)
        results = sorted(results,key=lambda x:x[2],reverse=True)
        return results


    def all_stu_score_along(self,study_number,subject,term):    #单科班级学生成绩传入班长学号和科目
        class_num = self.sentence_class(study_number)
        curse = self.conn.cursor()
        self.conn.ping(reconnect=True)
        sql = "select "+"学号,名字,"+str(subject)+" from "+str(self.table[term-1])+ " where 班级='%s' " % (str(class_num))
        curse.execute(sql)
        scorelist = list(curse.fetchall())
        scorelist = sorted(scorelist,key=lambda x:x[2],reverse=True)
        return scorelist


    def password_change(self,password,username):    #更改密码
        curse = self.conn.cursor()
        self.conn.ping(reconnect=True)
        sql = "update student set 密码='%s' where 学号='%s'" % (str(password),str(username))
        curse.execute(sql)
        self.conn.commit()
        curse.close()
        self.conn.close()
        return "success"

    def password_and_username(self, password, username):  # 验证密码和账号
        curse = self.conn.cursor()
        self.conn.ping(reconnect=True)
        sql = "select * from student where 密码='%s' and 学号='%s'" % (str(password), str(username))
        curse.execute(sql)
        k = curse.fetchall()
        k = list(k)
        n = len(k)
        curse.close()
        self.conn.close()
        if n == 0:
            return False
        else:
            return True

    def get_status_login(self,username):            #登录时更改状态
        curse = self.conn.cursor()
        self.conn.ping(reconnect=True)
        sql = "update student set 状态='%s' where 学号='%s'" % (str(200),str(username))
        curse.execute(sql)
        self.conn.commit()
        curse.close()
        self.conn.close()
        return "success"

    def get_status_logout(self,username):                  #退出时更改状态
        curse = self.conn.cursor()
        self.conn.ping(reconnect=True)
        sql = "update student set 状态='%s' where 学号='%s'" % (str(201),str(username))
        curse.execute(sql)
        self.conn.commit()
        curse.close()
        self.conn.close()
        return "success"

    def class_subject_analyse(self,study_number,subject,term):         #每科的各分数段人数
        nums = self.num_of_people(study_number=study_number)
        all_scores = self.all_stu_score_along(study_number=study_number,subject=subject,term=term)
        scores = {}
        for i in range(len(all_scores)):
            scores[i] = all_scores[i-1][2]
        excellent = 0
        good = 0
        passing = 0
        for j in range(len(all_scores)):
            score = int(scores[j])
            if score > 85 or score == 85:
                excellent += 1
            if score > 75 or score == 75:
                good += 1
            if score > 60 or score == 60:
                passing += 1
        no_passing = nums - passing
        data1 = {
            "subject":subject,
            "num_of_class":nums,
            "excellent":excellent,
            "good":good,
            "passing":passing,
            "no_passing":no_passing
        }
        data2 = self.class_case(study_number=study_number,subject=subject,term=term)
        data = {
            "class_detail_case":data2,
            "subject_score_line":data1
        }
        return data

if __name__ == '__main__':
    a = MysqlHelper()
    gdata = a.all_stu_score_along('031799101','线性代数',1)
    print(gdata)














