from flask import Blueprint, render_template,session

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
    return render_template('stu_subjects.html')
@student.route('/tealist')
def tealist():
    return render_template('teachers.html')

