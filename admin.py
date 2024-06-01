from flask import Blueprint, render_template,session

admin = Blueprint('admin', __name__,static_folder='static')

@admin.route('/')
def index():
    username= session['username']
    return render_template('admin.html',username=username)
@admin.route('/stulist')
def stulist():
    username= session['username']
    return render_template('students.html',username=username)
@admin.route('/tealist')
def tealist():
    username= session['username']
    return render_template('teachers.html',username=username)
@admin.route('/titlist')
def titlist():
    username= session['username']
    return render_template('stu_subjects.html', username=username)
