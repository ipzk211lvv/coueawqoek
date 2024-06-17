from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from init import app, db, manager
from models.jewelry import Jewelry
from models.orders import Orders
from models.reports import Reports
from models.user import User


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if request.method == "POST":
        if login and password:
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect("/")
            else:
                flash('Email чи пароль невірний!', 'log')
                return redirect('/')
        else:
            flash('Всі поля повинні бути заповнені!', 'log')
            return redirect('/')
    else:
        return render_template('index.html')


@app.route("/register", methods=['POST', 'GET'])
def register():
    name = request.form.get('name')
    surname = request.form.get('surname')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == "POST":
        if not (name and surname and email and password and password2):
            flash('Всі поля повинні бути заповнені!', 'reg')
            return redirect('/')
        elif password != password2:
            flash('Паролі не співпадають!', 'reg')
            return redirect('/')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(name=name, surname=surname, email=email, password=hash_pwd)
            try:
                db.session.add(new_user)
                db.session.commit()
            except:
                return 'Error'
            login_user(new_user)
            return redirect('/')
    else:
        return redirect('/')


@app.route('/user/<int:id>')
def user_info(id):
    user = User.query.get(id)
    report = Reports.query.order_by("answer").all()
    orders = Orders.query.all()
    jewelry = Jewelry.query.all()
    jw = {}
    for i in orders:
        a = {}
        for j in eval(i.jewelry):
            a[int(j[0])] = int(j[1])
        jw[i.id] = a
    return render_template("user_info.html", user=user, report=report, orders=orders, jewelry=jewelry, jw=jw)


@app.route('/user/<int:id>/update', methods=['POST', 'GET'])
def user_update(id):
    user = User.query.get(id)
    if request.method == "POST":
        user.name = request.form["name"]
        user.surname = request.form["surname"]
        user.email = request.form["email"]
        # user.password = request.form["password"]
        user.address = request.form["address"]
        try:
            db.session.commit()
            return redirect(f"/user/{id}")
        except:
            return "Error"
    else:
        return render_template('user_update.html', user=user)


@app.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')