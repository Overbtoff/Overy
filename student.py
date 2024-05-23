from flask import Blueprint, render_template

student = Blueprint('student', __name__,static_folder='static')

@student.route('/')
def index():
    return render_template('index.html')

@student.route('/about')
def about():
    return render_template('about.html')
