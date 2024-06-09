from flask import Flask,render_template,redirect,request,url_for,session
from admin import admin
from teacher import teacher
from student import student

from dbconn import conn,cursor

app = Flask(__name__)
app.secret_key = '6ragonPa5ace1n'
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(teacher, url_prefix='/teacher')
app.register_blueprint(student, url_prefix='/student')

# 404错误处理器
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error-404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'logged_in' in session:
        role = session['role']
        if role == '管理员':
            return redirect(url_for('admin.index'))
        if role == '老师' or role == '系主任':
            return redirect(url_for('teacher.index'))
        if role == '学生':
            return redirect(url_for('student.index'))
        return redirect(url_for('logout'))
        #return render_template('students.html', username=username)
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if len(username) == 0 or len(password) == 0:
                return render_template('login.html',error='用户名或密码不能为空')
            if username[0]=='3':
                sql="SELECT USER_STUDENT_ID,USER_STUDENT_PASSWORDHASH FROM USER_STUDENT WHERE USER_STUDENT_ID=:username"
                cursor.execute(sql,username=username)
                data = cursor.fetchall()
                name=''
                print(data)
                print(1)
                for i in data:
                    print(i[0],i[1])
                    if i[0]==username and i[1]==password:
                        session['logged_in'] = True
                        sql="SELECT STUDENT_NAME FROM STUDENT WHERE STUDENT_ID=:username"
                        cursor.execute(sql,username=username)
                        data = cursor.fetchall()
                        for j in data:
                            name = j[0]
                        session['username'] = name
                        session['role'] = '学生'
                        session['id'] = username
                        return redirect(url_for('student.index'))
            if username[0]=='1':
                sql="SELECT USER_TEACHER_ID,USER_TEACHER_PASSWORDHASH FROM USER_TEACHER WHERE USER_TEACHER_ID=:username"
                cursor.execute(sql,username=username)
                data = cursor.fetchall()
                name=''
                for i in data:
                    if i[0]==username and i[1]==password:
                        session['logged_in'] = True
                        sql="SELECT TEACHER_NAME FROM TEACHER WHERE TEACHER_ID=:username"
                        cursor.execute(sql,username=username)
                        data = cursor.fetchall()
                        for j in data:
                            name = j[0]
                        session['username'] = name
                        session['role'] = '老师'
                        session['id'] = username
                        return redirect(url_for('teacher.index'))
            if username[0]=='0':
                sql="SELECT USER_ADMIN_ID,USER_ADMIN_PASSWORDHASH,USER_ADMIN_NAME FROM USER_ADMIN WHERE USER_ADMIN_ID=:username"
                cursor.execute(sql,username=username)
                data = cursor.fetchall()
                for i in data:
                    if i[0]==username and i[1]==password:
                        session['logged_in'] = True
                        session['username'] = i[2]
                        session['role'] = '管理员'
                        session['id'] = username
                        return redirect(url_for('admin.index'))
            if username[0]=='2':
                sql="SELECT USER_TEACHER_ID,USER_TEACHER_PASSWORDHASH FROM USER_TEACHER WHERE USER_TEACHER_ID=:username"
                cursor.execute(sql,username=username)
                data = cursor.fetchall()
                name=''
                for i in data:
                    if i[0]==username and i[1]==password:
                        session['logged_in'] = True
                        sql="SELECT TEACHER_NAME FROM TEACHER WHERE TEACHER_ID=:username"
                        cursor.execute(sql,username=username)
                        data = cursor.fetchall()
                        for j in data:
                            name = j[0]
                        session['username'] = name
                        session['role'] = '系主任'
                        session['id'] = username
                        return redirect(url_for('teacher.index'))
            return render_template('login.html',error='用户名或密码错误')
        else:
            return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('role', None)
    session.pop('id',None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    app.config['PERMANENT_SESSION_LIFETIME'] = 1
