from flask import Blueprint, render_template, session, request, redirect, url_for, send_file
from dbconn import conn, cursor
import io

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
        if value:
            print(value)
    username = session['username']
    role = session['role']
    id = session['id']
    if request.method == 'GET':
        check1 = request.args.get('select1')
        print(check1)
        if check1 == "1":
            sql = """SELECT TH.Theme_id,G.Graduation_topic,TEA.Teacher_name,G.Graduation_introduction,TH.Theme_Deadline,TH.Theme_State,S.Score_ 
        FROM GRADUATION G,THEME TH,TEACHER TEA,SCORE S WHERE Theme_id = Graduation_id
        AND Theme_teacher = Teacher_id
        AND Graduation_id = Score_graduation_id
        AND Theme_teacher=:username
        """
            cursor.execute(sql, username=1000000001)
            data = cursor.fetchall()
            return render_template('stu_subjects.html', username=username, role=role, data=data)

        sql = """SELECT Theme_student 学生学号,Student_name 学生姓名,Student_sex 学生性别,Student_subject 学生专业,Student_class 学生班级,Student_number 学生电话号码,Student_email 学生邮箱
                FROM THEME,STUDENT,TEACHER
                WHERE Theme_student = student_id
                AND Theme_teacher=:username
            """
        cursor.execute(sql, username=id)
        data = cursor.fetchall()
        print(data)
        return render_template('students.html', username=username, role=role, data=data)


@teacher.route('/titlist', methods=['GET', 'POST'])
def titlist():
    if request.method == 'POST':  # tui
        value = request.form.get('row_id')
        if value:
            print(value)
    username = session['username']
    role = session['role']
    id = session['id']
    if request.method == 'GET':
        sql = """SELECT TH.Theme_id 题目编号,G.Graduation_topic 题目名称,TEA.Teacher_name 负责老师,G.Graduation_introduction 相关介绍,TH.Theme_Deadline 截止日期
                FROM GRADUATION G,THEME TH,TEACHER TEA
                WHERE Theme_id = Graduation_id
                AND Theme_teacher = :username
            """
        cursor.execute(sql, username=id)
        data = cursor.fetchall()
        print(data)
        return render_template('tea_subjects.html', username=username, role=role, data=data)


@teacher.route('/stuapp')
def stuapp():
    value = request.args.get('stuid', None)
    st = request.args.get('st', None)
    if value:
        print(value, st)
        return redirect(url_for('teacher.stuapp'))
    else:
        username = session['username']
        role = session['role']
        id = session['id']
        sql = """SELECT DISTINCT Theme_id 编号,Graduation_topic 题目名称,Student_name 申请学生姓名,Student_number 申请学生电话,Student_email, Theme_State 申请状态
                FROM GRADUATION,THEME,TEACHER,STUDENT
                WHERE Theme_id = Graduation_id
                AND Theme_teacher = :username
                AND Theme_student = student_id
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
        return redirect(url_for('teacher.titapp'))
    else:
        if request.method == 'POST':
            # 写入数据库
            name = request.form['name']
            direct = request.form['direct']
            information = request.form['information']
            date = request.form['date']
            print(name, direct, information)
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
        if value:
            print(value)
    return redirect(url_for('teacher.titlist'))


@teacher.route('/down/<stu>', methods=['GET', 'POST'])
def down(stu):
    sql = "SELECT blob_data FROM blob_table WHERE STUDENT = :stu"
    cursor.execute(sql, stu=stu)
    row = cursor.fetchone()
    blob_data = row[0].read()
    # 创建一个BytesIO对象
    file_io = io.BytesIO(blob_data)
    # 使用send_file函数发送文件
    return send_file(file_io, as_attachment=True, mimetype='application/octet-stream')
