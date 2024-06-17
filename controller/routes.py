import datetime
import shutil

from flask import render_template, request, redirect, url_for
from flask_login import current_user

from init import app, db
from models.jewelry import Jewelry
from models.orders import Orders

import matplotlib.pyplot as plt
import numpy as np

@app.route('/')
@app.route('/home')
def index():
    jewelry = Jewelry.query.filter(Jewelry.count > 0).order_by(Jewelry.date_create.desc()).all()
    return render_template('/index.html', jewelry=jewelry[:5])


@app.route('/order/<int:id>', methods=['POST', 'GET'])
def order(id):
    rep = Orders.query.get(id)
    if request.method == "POST":
        rep.status = True
        db.session.commit()
    return redirect(f'/user/{current_user.id}')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return redirect('/')

@app.route('/backup', methods=['POST', 'GET'])
def backup():
    shutil.copyfile('./shop.db', f'./backup/ShopDB-{datetime.datetime.now().strftime("%d.%m.%Y(%H-%S)")}.db')
    return redirect(f'/admin')


