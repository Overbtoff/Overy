from flask import Flask,render_template,redirect
from admin import admin
from teacher import teacher
from student import student

app = Flask(__name__)

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(teacher, url_prefix='/teacher')
app.register_blueprint(student, url_prefix='/student')
# 404错误处理器
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error-404.html'), 404


@app.route('/')
def index():  # put application's code here
    return render_template("students.html")
@app.route('/login')
def login():
    return redirect('/student')

if __name__ == '__main__':
    app.run(debug=True)
