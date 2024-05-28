from flask import Flask,render_template,redirect,request,url_for,session
from admin import admin
from teacher import teacher
from student import student

# from dbconn import conn,cursor

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
        username = session['username']
        role = session['role']
        if role == 'admin':
            return redirect(url_for('admin.index'))
        if role == 'teacher':
            return redirect(url_for('teacher.index'))
        if role == 'student':
            return redirect(url_for('student.index'))
        #return render_template('students.html', username=username)
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if len(username) == 0 or len(password) == 0:
                return render_template('login.html',error='用户名或密码不能为空')
            # sql=f"insert into login(username,password) values({username},{password})"
            # cursor.execute(sql)
            # conn.commit()
            print(username,password)
            if username[0]=='1':
                session['logged_in'] = True
                session['username'] = username
                session['role'] = 'student'
                return redirect(url_for('student.index'))
            if username[0]=='3':
                session['logged_in'] = True
                session['username'] = username
                session['role'] = 'teacher'
                return redirect(url_for('teacher.index'))
            if username[0]=='0':
                session['logged_in'] = True
                session['username'] = username
                session['role'] = 'admin'
                return redirect(url_for('admin.index'))
        else:
            return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    app.config['PERMANENT_SESSION_LIFETIME'] = 1
