from flask import Blueprint, render_template,session,redirect,url_for,request
from dbconn import conn,cursor
student = Blueprint('student', __name__,static_folder='static')

@student.route('/',methods=['GET','POST'])
def index():
    username= session['username']
    id=session['id']
    role = session['role']
    sql="SELECT STUDENT_ID,STUDENT_NAME,STUDENT_SEX,STUDENT_DEPARTMENT_ID,STUDENT_SUBJECT,STUDENT_CLASS,STUDENT_NUMBER,STUDENT_EMAIL FROM STUDENT WHERE STUDENT_ID=:username"
    cursor.execute(sql,username=id)
    data1 = cursor.fetchall()
    sql="""SELECT DISTINCT TH.Theme_id,G.Graduation_topic,TEA.Teacher_name,G.Graduation_introduction,TH.Theme_Deadline,TH.Theme_State,S.Score_
            FROM GRADUATION G,THEME TH,TEACHER TEA,SCORE S
            WHERE Theme_id = Graduation_id
            AND Theme_teacher = Teacher_id 
            AND Graduation_id = Score_graduation_id(+)
            AND Theme_student=:id
        """
    cursor.execute(sql,id=id)
    data2 = cursor.fetchall()
    return render_template('student-details.html',username=username,role=role,data1=data1,data2=data2)

@student.route('/titlist',methods=['GET','POST'])
def titlist():
    username= session['username']
    role = session['role']
    value = request.args.get('teaid', None)
    if value:
        print(value)
        #sql="SELECT THEME_ID,TEACHER_NAME,TEACHER_SEX,TEACHER_SUBJECT,TEACHER_NUMBER,TEACHER_EMAIL FROM TEACHER WHERE TEACHER_ID=:username"
        sql="""SELECT  GRADUATION_id 编号,Graduation_topic 题目名称,Teacher_name 负责老师,Graduation_introduction 相关介绍,Graduation_deadline 截止日期
                FROM GRADUATION,TEACHER 
                WHERE Graduation_Teacher_id = Teacher_id 
                AND Teacher_id =:username
                AND Graduation_state='通过'
        """
        cursor.execute(sql,username=value)
        data = cursor.fetchall()
        return render_template('stu_subjects.html',username=username,role=role,data=data)
    else:
        if request.method == 'GET':
            check1=request.args.get('select1')
            print(check1)
            if check1=="1":
                sql="""SELECT  GRADUATION_id 编号,Graduation_topic 题目名称,Teacher_name 负责老师,Graduation_introduction 相关介绍,Graduation_deadline 截止日期
                FROM GRADUATION,TEACHER 
                WHERE Graduation_Teacher_id = Teacher_id 
                AND Graduation_state='通过'
                AND Theme_teacher=:username
        """
                cursor.execute(sql,username=1000000001)
                data = cursor.fetchall()
                return render_template('stu_subjects.html',username=username,role=role,data=data)
            elif check1=="2":
                sql="""SELECT  GRADUATION_id 编号,Graduation_topic 题目名称,Teacher_name 负责老师,Graduation_introduction 相关介绍,Graduation_deadline 截止日期
                FROM GRADUATION,TEACHER 
                WHERE Graduation_Teacher_id = Teacher_id 
                AND Graduation_state='通过'
                AND Teacher_id=:username
        """
                cursor.execute(sql,username=1000000002)
                data = cursor.fetchall()
                return render_template('stu_subjects.html',username=username,role=role,data=data)
            else:
                sql="""SELECT  GRADUATION_id 编号,Graduation_topic 题目名称,Teacher_name 负责老师,Graduation_introduction 相关介绍,Graduation_deadline 截止日期
                FROM GRADUATION,TEACHER 
                WHERE Graduation_Teacher_id = Teacher_id 
                AND Graduation_state='通过'
        """
                cursor.execute(sql)
                data = cursor.fetchall()
                return render_template('stu_subjects.html',username=username,role=role,data=data)

@student.route('/tealist')
def tealist():
    username= session['username']
    role = session['role']
    check1=request.args.get('select1')
    print(check1)
    if check1=='1':
        sql="""SELECT T.Teacher_id,T.Teacher_name,T.Teacher_sex,D.DEPARTMENT_NAME,T.Teacher_research,Teacher_title,T.Teacher_number,T.Teacher_email
        FROM TEACHER T,DEPARTMENT D
        WHERE Teacher_department_id = DEPARTMENT_ID
        AND DEPARTMENT_NAME='计算机学院'
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        return render_template('stu_teachers.html',username=username,role=role,data=data)
    elif check1=='2':
        sql="""SELECT T.Teacher_id,T.Teacher_name,T.Teacher_sex,D.DEPARTMENT_NAME,T.Teacher_research,Teacher_title,T.Teacher_number,T.Teacher_email
        FROM TEACHER T,DEPARTMENT D
        WHERE Teacher_department_id = DEPARTMENT_ID
        AND DEPARTMENT_NAME='汉语言与新闻传播学院'
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        return render_template('stu_teachers.html',username=username,role=role,data=data)
    else:
        sql="""SELECT T.Teacher_id,T.Teacher_name,T.Teacher_sex,D.DEPARTMENT_NAME,T.Teacher_research,Teacher_title,T.Teacher_number,T.Teacher_email
        FROM TEACHER T,DEPARTMENT D
        WHERE Teacher_department_id = DEPARTMENT_ID
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        print(4113434)
        return render_template('stu_teachers.html',username=username,role=role,data=data)

@student.route('/app')
def app():
    stuid=session['id']
    id=request.args.get('titid')
    id=id.ljust(10, ' ')
    sql="""SELECT GRADUATION_TEACHER_ID FROM GRADUATION WHERE GRADUATION_ID=:id"""
    cursor.execute(sql,id=id)
    teaid = cursor.fetchall()

    teaid=teaid[0][0]
    sql="""INSERT INTO THEME(Theme_id,Theme_student,Theme_teacher,Theme_State) 
    VALUES (:id,:stuid,:teaid,'未审核')"""
    cursor.execute(sql,id=id,stuid=stuid,teaid=teaid)
    conn.commit()
    print(id)
    return redirect(url_for('student.index'))
@student.route('/resign')
def resign():
    #查询有啥
    return redirect(url_for('student.index'))
@student.route('/uploadf',methods=['GET','POST'])
def uploadf():
    id=session['id']
    if request.method == 'POST':
        file=request.files['file']
        print(1)
        print(request.form)
        if file:
            blob_data = file.read()
            sql="""UPDATE Theme SET THEME_WORD = :blob WHERE THEME_STUDENT = :id"""
            cursor.execute(sql,blob=blob_data,id=id)
            conn.commit()
    return redirect(url_for('student.index'))
@student.route('/modify',methods=['GET','POST'])
def modify():
    if request.method == 'POST':
        name=request.form.get('name')
        sex=request.form.get('sex')
        subject=request.form.get('subject')
        number=request.form.get('number')
        email=request.form.get('email')
        print(name,sex,subject,number,email)
        #modify db
        return redirect(url_for('student.index'))


