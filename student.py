from flask import Blueprint, render_template,session,redirect,url_for,request

student = Blueprint('student', __name__,static_folder='static')

@student.route('/',methods=['GET','POST'])
def index():
    username= session['username']
    return render_template('student-details.html',username=username)

@student.route('/titlist',methods=['GET','POST'])
def titlist():
    value = request.args.get('teaid', None)
    if value:
        print(value)
        return redirect(url_for('student.titlist'))
    else:
        username= session['username']
        if request.method == 'GET':
            check1=request.args.get('select1')
            check2=request.args.get('select2')
            print(check1,check2)
            if check1 or check2:
                #查询数据库
                return render_template('stu_subjects.html',username=username)
            return render_template('stu_subjects.html',username=username)
@student.route('/tealist')
def tealist():
    username= session['username']
    check1=request.args.get('select1')
    check2=request.args.get('select2')
    print(check1,check2)
    return render_template('stu_teachers.html',username=username)

@student.route('/app')
def app():
    #写入数据库
    return redirect(url_for('student.index'))
@student.route('/resign')
def resign():
    return redirect(url_for('student.index'))
@student.route('/uploadf',methods=['GET','POST'])
def uploadf():
    file=request.files['file']
    return redirect(url_for('student.index'))


