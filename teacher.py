from flask import Blueprint, render_template,session,request,redirect,url_for

teacher = Blueprint('teacher', __name__,static_folder='static')


@teacher.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('teacher.index'))
    username= session['username']
    return render_template('teacher-details.html',username=username)

@teacher.route('/stulist',methods=['GET','POST'])
def stulist():
    if request.method == 'POST':
        value = request.form.get('row_id')
        if value:
            print(value)
    username= session['username']
    return render_template('students.html',username=username)
@teacher.route('/titlist',methods=['GET','POST'])
def titlist():
    if request.method == 'POST':
        value = request.form.get('row_id')
        if value:
            print(value)
    username= session['username']
    return render_template('tea_subjects.html', username=username)
@teacher.route('/stuapp')
def stuapp():
    value = request.args.get('stuid', None)
    st = request.args.get('st', None)
    if value:
        print(value,st)
        return redirect(url_for('teacher.stuapp'))
    else:
        username= session['username']
        return render_template('add-student.html',username=username)


@teacher.route('/titapp',methods=['GET','POST'])
def titapp():
    username= session['username']
    value = request.args.get('titid', None)
    if value:
        print(value)
        if(username[0]=='2'):
            return redirect(url_for('teacher.titapp'))
        return redirect(url_for('teacher.titapp'))
    else:
        if request.method == 'POST':
            #写入数据库
            if username[0]=='3':
                name=request.form['name']
                direct=request.form['direct']
                information=request.form['information']
                print(name,direct,information)
                return redirect(url_for('teacher.index'))

    return render_template('add-subject.html',username=username)
@teacher.route('/edittit',methods=['GET','POST'])
def edittit():
    if request.method == 'POST':
        value = request.form.get('rowId')
        if value:
            print(value)
    return redirect(url_for('teacher.titlist'))



