from flask import Flask,render_template
from admin import admin
from teacher import teacher
from student import student

app = Flask(__name__)

app.register_blueprint(admin, url_prefix='/')
app.register_blueprint(teacher, url_prefix='/')
app.register_blueprint(student, url_prefix='/')
# 404错误处理器
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error-404.html'), 404


@app.route('/')
def index():  # put application's code here
    return render_template("login.html")


if __name__ == '__main__':
    app.run()
