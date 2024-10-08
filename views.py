from flask import render_template, request, redirect, url_for
from testapp import app

from testapp import db
from testapp.models.employee import Employee


@app.route('/')
def index():
    my_dict = {
        'insert_something1': 'views.pyのinsert_something1部分です。',
        'insert_something2': 'views.pyのinsert_something2部分です。',
        'test_titles': ['title1', 'title2', 'title3']
    }
    return render_template('testapp/index.html', my_dict=my_dict)


@app.route('/test')
def other1():
    return render_template('testapp/sampleform.html')


@app.route('/sampleform', methods=['GET', 'POST'])
def sample_form():
    if request.method == 'GET':
        return render_template('testapp/sampleform.html')
    if request.method == 'POST':
        print('POSTデータ受け取ったので処理します。')
        req1 = request.form['data1']
        return f'POST受け取ったよ: {req1}'

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'GET':
        return render_template('testapp/add_employee.html')
    if request.method == 'POST':
        form_name = request.form.get('name')  # str
        form_mail = request.form.get('mail')  # str
        # チェックなしならFalse。str -> bool型に変換
        form_is_remote = request.form.get('is_remote', default=False, type=bool)
        form_department = request.form.get('department')  # str
        # int, データないとき０
        form_year = request.form.get('year', default=0, type=int)

        employee = Employee(
            name=form_name,
            mail=form_mail,
            is_remote=form_is_remote,
            department=form_department,
            year=form_year
        )
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/employees')
def employee_list():
    # 一覧ページ（全件）
    employees = Employee.query.all()
    return render_template('testapp/employee_list.html', employees=employees)

@app.route('/employees/<int:id>')
def employee_detail(id):
    # 詳細ページ
    employee = Employee.query.get_or_404(id)
    return render_template('testapp/employee_detail.html', employee=employee)

@app.route('/employee/<int:id>/edit', methods=['GET'])
def employee_edit(id):
    # 編集ページ表示用
    employee = Employee.query.get(id)
    return render_template('testapp/employee_edit.html', employee=employee)

@app.route('/employees/<int:id>/update', methods=['POST'])
def employee_update(id):
    employee = Employee.query.get(id)  # 更新するデータをDBから取得
    employee.name = request.form.get('name')
    employee.mail = request.form.get('mail')
    employee.is_remote = request.form.get('is_remote', default=False, type=bool)
    employee.department = request.form.get('department')
    employee.year = request.form.get('year', default=0, type=int)

    db.session.merge(employee)
    db.session.commit()
    return redirect(url_for('employee_list'))

@app.route('/employees/<int:id>/delete', methods=['POST'])  
def employee_delete(id):  
    employee = Employee.query.get(id)   
    db.session.delete(employee)  
    db.session.commit()  
    return redirect(url_for('employee_list'))
