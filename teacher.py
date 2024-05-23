from flask import Blueprint, render_template

teacher = Blueprint('teacher', __name__,static_folder='static')

@teacher.route('/')
def index():
    return render_template('index.html')

@teacher.route('/about')
def about():
    return render_template('about.html')