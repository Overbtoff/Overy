from flask import Blueprint, render_template,session

teacher = Blueprint('teacher', __name__,static_folder='static')

@teacher.route('/')
def index():
    username= session['username']
    return render_template('teacher.html',username=username)
@teacher.route('/stulist')
def stulist():
    username= session['username']
    return render_template('students.html',username=username)
@teacher.route('/titlist')
def titlist():
    username= session['username']
    return render_template('subjects.html',username=username)
@teacher.route('/info')
def info():
    username= session['username']
    return render_template('teacher-details.html',username=username)
@teacher.route('/stuapp')
def stuapp():
    return render_template('add-student.html')
@teacher.route('/titapp')
def titapp():
    return render_template('add-subject.html')
