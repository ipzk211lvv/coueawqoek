from flask import render_template, request, redirect, url_for
from flask_login import current_user

from init import app, db
from models.reports import Reports
from models.user import User


@app.route('/error-report/<string:error>', methods=['POST', 'GET'])
def error_rport(error):
    url, code = error.split('+')

    report_ = Reports(user='ERROR', title=code, problem=f'Cторінку не знайдено — {url.replace("$", "/")}', answer='error')
    db.session.add(report_)
    db.session.commit()
    return redirect('/')


@app.route('/report', methods=['POST', 'GET'])
def reports():
    user = User.query.get(current_user.id)
    if request.method == "POST":
        title = request.form['title']
        problem = request.form['problem']

        report = Reports(user=current_user.email, title=title, problem=problem, answer='')
        db.session.add(report)
        db.session.commit()
        return redirect(f'user/{current_user.id}')
    else:
        return render_template('report.html')


@app.route('/report/<int:id>', methods=['POST', 'GET'])
def report(id):
    report = Reports.query.get(id)
    if request.method == "POST":
        report.answer = request.form['answer']
        try:
            db.session.commit()
            return render_template('reports.html', report=report)
        except:
            return render_template('reports.html', report=report)
    else:
        return render_template('reports.html', report=report)


@app.route('/report/del/<int:id>')
def report_del(id):
    Reports.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(f'/user/{current_user.id}')