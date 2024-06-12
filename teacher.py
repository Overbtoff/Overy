from flask import Blueprint, render_template, session, request, redirect, url_for, send_file
from dbconn import conn, cursor
import io
from datetime import datetime
from refreshid import newid

teacher = Blueprint('teacher', __name__, static_folder='static')


@teacher.route('/', methods=['GET', 'POST'])
def index():
    username = session['username']
    id = session['id']
    role = session['role']
    sql = """SELECT T.Teacher_id,T.Teacher_name,T.Teacher_sex,D.DEPARTMENT_NAME,T.Teacher_research,Teacher_title,T.Teacher_number,T.Teacher_email,T.Teacher_gradnumber
            FROM TEACHER T,DEPARTMENT D
            WHERE Teacher_department_id = DEPARTMENT_ID AND Teacher_id=:username"""
    cursor.execute(sql, username=id)
    data = cursor.fetchall()
    return render_template('teacher-details.html', username=username, role=role, data=data)


@teacher.route('/stulist', methods=['GET', 'POST'])
def stulist():
    if request.method == 'POST':
        value = request.form.get('row_id')
        score = request.form.get('score')
        print(value, score)
        sql="""UPDATE SCORE set Score_=:score where Score_student_id=:value"""
        cursor.execute(sql,score=score,value=value)
        conn.commit()
        return redirect(url_for('teacher.stulist'))
    username = session['username']
    role = session['role']
    id = session['id']
    if request.method == 'GET':
        check1 = request.args.get('select1')
        print(check1)
        if check1 == "1":
            sql = """SELECT DISTINCT Theme_student 学生学号,Student_name 学生姓名,Student_sex 学生性别,Student_subject 学生专业,Student_class 学生班级,Student_number 学生电话号码,Student_email 学生邮箱
                FROM THEME,STUDENT,TEACHER
                WHERE Theme_student = student_id
                AND Theme_teacher=:username
                AND Theme_State = '同意'
        """
            cursor.execute(sql, username=1000000001)
            data = cursor.fetchall()
            return render_template('stu_subjects.html', username=username, role=role, data=data)

        sql = """SELECT DISTINCT Theme_student 学生学号,Student_name 学生姓名,Student_sex 学生性别,Student_subject 学生专业,Student_class 学生班级,Student_number 学生电话号码,Student_email 学生邮箱
                FROM THEME,STUDENT,TEACHER
                WHERE Theme_student = student_id
                AND Theme_teacher=:username
                AND Theme_State = '同意'
            """
        cursor.execute(sql, username=id)
        data = cursor.fetchall()
        return render_template('students.html', username=username, role=role, data=data)


@teacher.route('/titlist', methods=['GET', 'POST'])
def titlist():
    if request.method == 'POST':  # tui
        value = request.form.get('rowid')
        if value:
            sql="""DELETE FROM SCORE WHERE SCORE_GRADUATION_ID=:value"""
            cursor.execute(sql,value=value)
            sql= """DELETE FROM Theme WHERE THEME_ID=:value"""
            cursor.execute(sql, value=value)
            sql = """DELETE FROM GRADUATION WHERE GRADUATION_ID=:value"""
            cursor.execute(sql, value=value)
            sql="""UPDATE TEACHER set Teacher_gradnumber=Teacher_gradnumber-1 where Teacher_id=:id"""
            cursor.execute(sql,id=session['id'])
            conn.commit()
        return redirect(url_for('teacher.titlist'))
    username = session['username']
    role = session['role']
    id = session['id']
    if request.method == 'GET':
        sql = """SELECT DISTINCT GRADUATION_id,Graduation_topic 题目名称,Graduation_introduction 相关介绍,GRADUATION_DEADLINE,Graduation_subdate ,Graduation_appdate ,Graduation_state 
                FROM GRADUATION ,TEACHER
                WHERE teacher_id = Graduation_Teacher_id
                AND teacher_id = :username
            """
        cursor.execute(sql,username=id)
        data = cursor.fetchall()
        return render_template('tea_subjects.html', username=username, role=role, data=data)


@teacher.route('/stuapp')
def stuapp():
    stuid = request.args.get('stuid', None)
    titid = request.args.get('titid', None)
    st = request.args.get('st', None)
    if stuid:
        sql="""SELECT STUDENT_ID FROM STUDENT WHERE STUDENT_NAME=:value"""
        cursor.execute(sql,value=stuid)
        stuid = cursor.fetchall()
        stuid = stuid[0][0]
        print(stuid)
        if st == '1':
            sql = """UPDATE THEME set Theme_State='同意' where Theme_student = :value"""
            cursor.execute(sql, value=stuid)
            sql = """INSERT INTO Score(Score_student_id,Score_teacher_id,Score_graduation_id,Score_) 
            VALUES (:stuid,:taeid,:titid,'') """
            cursor.execute(sql,stuid=stuid,taeid=session['id'],titid=titid)
            conn.commit()
        else:
            sql = """UPDATE THEME set Theme_State='拒绝' where Theme_student = :value"""
            cursor.execute(sql, value=stuid)
            sql="""DELETE from SCORE where Score_student_id = :id"""
            cursor.execute(sql,id=stuid)
            conn.commit()
        return redirect(url_for('teacher.stuapp'))
    else:
        username = session['username']
        role = session['role']
        id = session['id']
        sql = """SELECT DISTINCT Theme_id 编号,Graduation_topic 题目名称,Student_name 申请学生姓名,Student_number 申请学生电话,Student_email, Theme_State 申请状态
                FROM GRADUATION,THEME,TEACHER,STUDENT
                WHERE Theme_id = Graduation_id
                AND Theme_student = student_id
                AND Theme_teacher = :username
            """
        cursor.execute(sql, username=id)
        data = cursor.fetchall()
        print(data)
        return render_template('add-student.html', username=username, role=role, data=data)


@teacher.route('/titapp', methods=['GET', 'POST'])
def titapp():
    username = session['username']
    role = session['role']
    id = session['id']
    value = request.args.get('titid', None)
    st = request.args.get('st', None)
    if value:
        print(value,st)
        if st == '1':
            sql="""UPDATE GRADUATION set Graduation_state='通过' where GRADUATION_ID = :value"""
            cursor.execute(sql,value=value)
            sql="""UPDATE GRADUATION set Graduation_subdate=sysdate where GRADUATION_ID = :value"""
            cursor.execute(sql,value=value)
            conn.commit()
        else:
            sql="""UPDATE GRADUATION set Graduation_state='拒绝' where GRADUATION_ID = :value """
            cursor.execute(sql,value=value)
            conn.commit()
        return redirect(url_for('teacher.titapp'))
    else:
        if request.method == 'POST':
            # 写入数据库
            name = request.form['name']
            direct = request.form['direct']
            information = request.form['information']
            file=request.files['file']
            deadline = request.form['deadline']
            deadline=datetime.strptime(deadline,'%Y-%m-%d')
            blob_data = file.read()
            sql="""INSERT INTO GRADUATION(Graduation_id,Graduation_topic,Graduation_Teacher_id,Graduation_kind,Graduation_introduction,Graduation_subdate,Graduation_state,Graduation_appdate,GRADUATION_DEADLINE,GRADUATION_WORD) 
VALUES(:newid,:name,:id,:direct,:information,SYSDATE,'未审核','',:deadline,:blob)"""
            cursor.execute(sql,newid=newid(),name=name,id=id,information=information,direct=direct,blob=blob_data,deadline=deadline)
            conn.commit()
            return redirect(url_for('teacher.index'))
        else:
            sql="""SELECT Graduation_id 题目编号,Graduation_topic 题目名称,Teacher_name,Graduation_introduction 相关介绍,Graduation_State 申请状态
                    FROM GRADUATION,TEACHER
                    WHERE Graduation_Teacher_id = Teacher_id 
                """
            cursor.execute(sql)
            data = cursor.fetchall()
            return render_template('add-subject.html', username=username,role=role,data=data)


@teacher.route('/edittit', methods=['GET', 'POST'])
def edittit():
    if request.method == 'POST':
        value = request.form.get('rowId')
        print(value)
        if value:
            name=request.form.get('name')
            info=request.form.get('info')
            deadline=request.form.get('deadline')
            deadline=deadline[0:10]
            deadline=datetime.strptime(deadline,'%Y-%m-%d')
            sql="""UPDATE GRADUATION set Graduation_topic=:name,Graduation_introduction=:info,GRADUATION_DEADLINE=:deadline where GRADUATION_ID=:value"""
            cursor.execute(sql,name=name,info=info,deadline=deadline,value=value)
            conn.commit()
    return redirect(url_for('teacher.titlist'))


@teacher.route('/down/<stu>', methods=['GET', 'POST'])
def down(stu):
    sql = "SELECT THEME_WORD FROM Theme WHERE THEME_STUDENT = :stu"
    cursor.execute(sql, stu=stu)
    row = cursor.fetchone()
    blob_data = row[0].read()
    # 创建一个BytesIO对象
    file_io = io.BytesIO(blob_data)
    # 使用send_file函数发送文件
    return send_file(file_io, as_attachment=True, mimetype='application/octet-stream', download_name='file.docx')

@teacher.route('/titdown/<tit>', methods=['GET', 'POST'])
def titdown(tit):
    sql = "SELECT GRADUATION_WORD FROM Graduation WHERE GRADUATION_ID = :tit"
    cursor.execute(sql, tit=tit)
    row = cursor.fetchone()
    blob_data = row[0].read()
    # 创建一个BytesIO对象
    file_io = io.BytesIO(blob_data)
    # 使用send_file函数发送文件
    return send_file(file_io, as_attachment=True, mimetype='application/octet-stream', download_name='file.docx')

@teacher.route('/modify',methods=['GET','POST'])
def modify():
    if request.method == 'POST':
        name=request.form.get('name')
        sex=request.form.get('sex')
        department=request.form.get('department')
        research=request.form.get('research')
        tit=request.form.get('tit')
        number=request.form.get('number')
        email=request.form.get('email')
        password=request.form.get('password')
        sql="""select DEPARTMENT_ID from department where department_name=:name"""
        cursor.execute(sql,name=department)
        department=cursor.fetchall()
        department=department[0][0]
        sql="""UPDATE TEACHER SET TEACHER_NAME=:name,TEACHER_sex=:sex,TEACHER_DEPARTMENT_ID=:department,TEACHER_RESEARCH=:research,TEACHER_TITLE=:tit,TEACHER_NUMBER=:phone,TEACHER_EMAIL=:email WHERE TEACHER_ID=:id"""
        cursor.execute(sql,name=name,sex=sex,department=department,research=research,tit=tit,phone=number,email=email,id=session['id'])
        sql="""UPDATE USER_TEACHER SET USER_TEACHER_PASSWORDHASH=:password WHERE USER_TEACHER_ID=:id"""
        cursor.execute(sql,password=password,id=session['id'])
        conn.commit()
        return redirect(url_for('teacher.index'))