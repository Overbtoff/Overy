from flask import Blueprint, render_template,session,request,redirect,url_for

admin = Blueprint('admin', __name__,static_folder='static')

@admin.route('/')
def index():
    username= session['username']
    return render_template('ad_students.html',username=username)
@admin.route('/stulist',methods=['GET','POST'])
def stulist():
    username= session['username']
    return render_template('ad_students.html',username=username)
@admin.route('/tealist',methods=['GET','POST'])
def tealist():
    username= session['username']
    return render_template('ad_teachers.html',username=username)
@admin.route('/titlist',methods=['GET','POST'])
def titlist():
    if request.method == 'POST':
        row_id = request.form.get('rowId')
        print(row_id)
        return redirect(url_for('admin.titlist'))
    username= session['username']
    return render_template('ad_subjects.html', username=username)
@admin.route('/mdperson',methods=['GET','POST'])
def mdperson():
    username= session['username']
    return render_template('ad_person_details.html', username=username)

