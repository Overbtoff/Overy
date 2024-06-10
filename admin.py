from flask import Blueprint, render_template,session,request,redirect,url_for,send_file
import io
from dbconn import conn,cursor
from datetime import datetime
admin = Blueprint('admin', __name__,static_folder='static')


@admin.route('/',methods=['GET','POST'])
def index():
    username= session['username']
    role = session['role']
    stuid=request.args.get('stuid')
    st=request.args.get('st')
    if stuid:
        print(1, stuid)#delete
        return redirect(url_for('admin.index'))
    if request.method == 'GET':
        check1=request.args.get('select1')
        if check1=="1":
            sql="""SELECT student_id,Student_name,Student_sex,department_name,Student_subject,Student_class,Student_number,Student_email,USER_STUDENT_PASSWORDHASH
                FROM STUDENT,DEPARTMENT,USER_STUDENT
                WHERE DEPARTMENT_ID = Student_department_id
                AND department_name='计算机学院'
                AND USER_STUDENT_ID = student_id"""
        elif check1=="2":
            sql="""SELECT student_id,Student_name,Student_sex,department_name,Student_subject,Student_class,Student_number,Student_email,USER_STUDENT_PASSWORDHASH
                FROM STUDENT,DEPARTMENT,USER_STUDENT
                WHERE DEPARTMENT_ID = Student_department_id
                AND department_name='汉语言与新闻传播学院'
                AND USER_STUDENT_ID = student_id"""
        else:
            sql="""SELECT student_id,Student_name,Student_sex,department_name,Student_subject,Student_class,Student_number,Student_email,USER_STUDENT_PASSWORDHASH
                FROM STUDENT,DEPARTMENT,USER_STUDENT
                WHERE DEPARTMENT_ID = Student_department_id
                AND USER_STUDENT_ID = student_id"""
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template('ad_students.html',username=username,role=role,data=data)


@admin.route('/tealist',methods=['GET','POST'])
def tealist():
    username= session['username']
    role = session['role']
    teaid=request.args.get('teaid')
    st=request.args.get('st')
    if teaid:
        print(1, teaid)#delete
        return redirect(url_for('admin.tealist'))
    if request.method == 'GET':
        check1=request.args.get('select1')
        if check1=="1":
            sql="""SELECT teacher_id,teacher_name,teacher_sex,Teacher_title,department_name,teacher_number,teacher_email,Teacher_gradnumber,user_teacher_passwordhash
                FROM TEACHER,DEPARTMENT,user_teacher
                where Teacher_department_id = DEPARTMENT_ID
                AND department_name='计算机学院'
                AND USER_TEACHER_ID = teacher_id"""
        elif check1=="2":
            sql="""SELECT teacher_id,teacher_name,teacher_sex,Teacher_title,department_name,teacher_number,teacher_email,Teacher_gradnumber,user_teacher_passwordhash
                FROM TEACHER,DEPARTMENT,user_teacher
                where Teacher_department_id = DEPARTMENT_ID
                AND department_name='汉语言与新闻传播学院'
                AND USER_TEACHER_ID = teacher_id"""
        else:
            sql="""SELECT teacher_id,teacher_name,teacher_sex,Teacher_title,department_name,teacher_number,teacher_email,Teacher_gradnumber,user_teacher_passwordhash
                FROM TEACHER,DEPARTMENT,user_teacher
                where Teacher_department_id = DEPARTMENT_ID
                AND USER_TEACHER_ID = teacher_id"""
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template('ad_teachers.html',username=username,role=role,data=data)

@admin.route('/titlist',methods=['GET','POST'])
def titlist():
    username= session['username']
    role = session['role']
    if request.method == 'GET':
        check1=request.args.get('select1')
        if check1=="1":
            sql="""SELECT Theme_id,Graduation_topic,Teacher_name,Graduation_introduction,Theme_Deadline
                FROM GRADUATION,THEME,TEACHER
                WHERE Theme_id = Graduation_id
                AND Theme_teacher = Teacher_id
                AND Teacher_name ='teacher1'
                """
        elif check1=="2":
            sql="""SELECT Theme_id,Graduation_topic,Teacher_name,Graduation_introduction,Theme_Deadline
                FROM GRADUATION,THEME,TEACHER
                WHERE Theme_id = Graduation_id
                AND Theme_teacher = Teacher_id
                AND Teacher_name ='teacher2'
                """
        else:
            sql="""SELECT Theme_id,Graduation_topic,Teacher_name,Graduation_introduction,Theme_Deadline
                FROM GRADUATION,THEME,TEACHER
                WHERE Theme_id = Graduation_id
                AND Theme_teacher = Teacher_id"""
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template('ad_subjects.html',username=username,role=role,data=data)
    if request.method == 'POST':
        row_id = request.form.get('rowId')
        print(row_id)
        return redirect(url_for('admin.titlist'))
    return render_template('ad_subjects.html', username=username)

@admin.route('/addstu',methods=['GET','POST'])
def addstu():
    if request.method == 'POST':
        id=request.form.get('id')
        name=request.form.get('name')
        sex=request.form.get('sex')
        department=request.form.get('department')
        subject=request.form.get('subject')
        clas=request.form.get('class')
        phone=request.form.get('number')
        email=request.form.get('email')
        password=request.form.get('password')
        print(request.form)
        print(id,name,sex,department,subject,clas,phone,email,password)
        sql="""SELECT DEPARTMENT_ID FROM DEPARTMENT WHERE DEPARTMENT_NAME=:department"""
        cursor.execute(sql,department=department)
        department=cursor.fetchall()
        print(department)
        department=department[0][0]
        sql="""INSERT INTO STUDENT(student_id,Student_name,Student_sex,STUDENT_DEPARTMENT_ID,Student_subject,Student_class,Student_number,Student_email) 
        VALUES(:id,:name,:sex,:department,:subject,:clas,:phone,:email)"""
        cursor.execute(sql,id=id,name=name,sex=sex,department=department,subject=subject,clas=clas,phone=phone,email=email)
        conn.commit()
        sql="""INSERT INTO USER_STUDENT(USER_STUDENT_ID,USER_STUDENT_PASSWORDHASH) VALUES(:id,:password)"""
        cursor.execute(sql,id=id,password=password)
        conn.commit()
        return redirect(url_for('admin.index'))

@admin.route('/addtea',methods=['GET','POST'])
def addtea():
    if request.method == 'POST':
        id=request.form.get('id')
        name=request.form.get('name')
        sex=request.form.get('sex')
        title=request.form.get('level')
        department=request.form.get('department')
        phone=request.form.get('phone')
        email=request.form.get('email')
        num=request.form.get('number')
        password=request.form.get('password')
        sql="""SELECT DEPARTMENT_ID FROM DEPARTMENT WHERE DEPARTMENT_NAME=:department"""
        cursor.execute(sql,department=department)
        department=cursor.fetchall()
        print(department)
        department=department[0][0]
        print(id,name,sex,title,department,phone,email,num,password)
        sql="""INSERT INTO TEACHER(TEACHER_ID,TEACHER_NAME,TEACHER_SEX,TEACHER_TITLE,TEACHER_DEPARTMENT_ID,TEACHER_number,TEACHER_email,TEACHER_GRADNUMBER) 
        VALUES(:id,:name,:sex,:title,:department,:phone,:email,:num)"""
        cursor.execute(sql,id=id,name=name,sex=sex,title=title,department=department,phone=phone,email=email,num=num)
        conn.commit()
        sql="""INSERT INTO USER_TEACHER(USER_TEACHER_ID,USER_TEACHER_PASSWORDHASH) VALUES(:id,:password)"""
        cursor.execute(sql,id=id,password=password)
        conn.commit()
        return redirect(url_for('admin.tealist'))

@admin.route('/addtit',methods=['GET','POST'])
def addtit():
    if request.method == 'POST':
        id=request.form.get('id')
        name=request.form.get('name')
        info=request.form.get('info')
        deadline=request.form.get('date')
        deadline=datetime.strptime(deadline, '%Y-%m-%d')
        teacher=request.form.get('teacher')
        sql="""SELECT TEACHER_ID FROM TEACHER WHERE TEACHER_NAME=:teacher"""
        cursor.execute(sql,teacher=teacher)
        teacher=cursor.fetchall()
        teacher=teacher[0][0]
        print(teacher)
        sql="""INSERT INTO GRADUATION(Graduation_id,Graduation_topic,GRADUATION_KIND,Graduation_introduction,Graduation_teacher_id,GRADUATION_SUBDATE,Graduation_state,GRADUATION_APPDATE)
        VALUES(:id,:name,:info,'生科',:teacher,sysdate,'未审核',:deadline)"""
        cursor.execute(sql,id=id,name=name,info=info,teacher=teacher,deadline=deadline)
        conn.commit()
        return redirect(url_for('admin.titlist'))

