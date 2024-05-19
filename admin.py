from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)

@admin.route('/')
def index():
    return render_template('index.html')

@admin.route('/about')
def about():
    return render_template('about.html')
