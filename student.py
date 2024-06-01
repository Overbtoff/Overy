from flask import Blueprint, render_template,session,redirect,url_for,request

student = Blueprint('student', __name__,static_folder='static')

@student.route('/')
def index():
    username= session['username']
    return render_template('student-details.html',username=username)
@student.route('/info')
def info():
    username= session['username']
    return render_template('student-details.html',username=username)
@student.route('/titlist')
def titlist():
    value = request.args.get('teaid', None)
    username= session['username']
    return render_template('stu_subjects.html',username=username)
@student.route('/tealist')
def tealist():
    username= session['username']
    return render_template('stu_teachers.html',username=username)

@student.route('/app')
def app():
    #写入数据库
    return redirect(url_for('student.index'))

