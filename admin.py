from flask import Blueprint, render_template,session,request,redirect,url_for,send_file
import io
admin = Blueprint('admin', __name__,static_folder='static')

@admin.route('/')
def index():
    username= session['username']
    return render_template('ad_students.html',username=username)

@admin.route('/stulist',methods=['GET','POST'])
def stulist():
    username= session['username']
    if request.method == 'GET':
        check1=request.args.get('select1')
        check2=request.args.get('select2')
        return render_template('ad_students.html',username=username)
    return render_template('ad_students.html',username=username)

@admin.route('/tealist',methods=['GET','POST'])
def tealist():
    username= session['username']
    if request.method == 'GET':
        check1=request.args.get('select1')
        check2=request.args.get('select2')
        return render_template('ad_students.html',username=username)
    return render_template('ad_teachers.html',username=username)

@admin.route('/titlist',methods=['GET','POST'])
def titlist():
    username= session['username']
    if request.method == 'GET':
        check1=request.args.get('select1')
        check2=request.args.get('select2')
        return render_template('ad_students.html',username=username)
    if request.method == 'POST':
        row_id = request.form.get('rowId')
        print(row_id)
        return redirect(url_for('admin.titlist'))
    return render_template('ad_subjects.html', username=username)

@admin.route('/addstu',methods=['GET','POST'])
def addstu():
    if request.method == 'POST':

        return redirect(url_for('admin.stulist'))

@admin.route('/addtea',methods=['GET','POST'])
def addtea():
    if request.method == 'POST':
        return redirect(url_for('admin.tealist'))

@admin.route('/addtit',methods=['GET','POST'])
def addtit():
    if request.method == 'POST':
        return redirect(url_for('admin.titlist'))

