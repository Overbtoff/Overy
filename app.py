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
    # if 'logged_in' in session:
    #     username = session['username']
    #     role = session['role']
    #     if role == 'admin':
    #         return redirect(url_for('admin.index'))
    #     return render_template('students.html', username=username)
    # else:
    #     if request.method == 'POST':
    #         username = request.form['username']
    #     password = request.form['password']
    #     sql=f"insert into login(username,password) values({username},{password})"
    #     cursor.execute(sql)
    #     conn.commit()
    #     return redirect(url_for('login'))
    # return render_template('register.html')
    return render_template("index.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
