import ast

from cloudipsp import Api, Checkout
from flask import render_template, request, redirect, flash, url_for
from flask_login import current_user
from sqlalchemy import or_

from init import app, db
from models.cart import Cart
from models.jewelry import Jewelry
from models.orders import Orders

import matplotlib.pyplot as plt
import numpy as np

import datetime


@app.route('/buy/<string:jewelry_info>')
def buy_order(jewelry_info):
    jw = jewelry_info.split('&')
    jewelry_dict = {}
    for i in jw:
        jewelry_item = i.split('+')
        jewelry_dict[int(jewelry_item[0])] = int(jewelry_item[1])
    jewelry = Jewelry.query.filter(or_(Jewelry.id == i for i in jewelry_dict))

    price = 0  # Ціна в замовленні
    for i in jewelry_dict:
        item = Jewelry.query.get(i)
        price += item.price * int(jewelry_dict[i])

    for i in jewelry:
        if i.count == 0:
            flash(f'Даний товар закінчився', 'cart')
            return redirect(url_for('cart'))
        elif i.count-jewelry_dict[i.id] < 0:
            flash(f'Не вистачає товару. Ви намагаєтеся придбати {jewelry_dict[i.id]} екземплярів з доступних'
                  f' {i.count} ', 'cart')
            return redirect(url_for('cart'))
    return render_template('buy.html', price=price)


@app.route('/buy-jewelry', methods=['GET', 'POST'])
def buy():
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        telephone = request.form['telephone']
        address = request.form['address']
        jewelry = request.form['jewelry']

        jewelry_ = [i for i in jewelry.split('&')]
        jewelry_id = [i.split('+') for i in jewelry_]

        jewelry = Jewelry.query.filter(or_(Jewelry.id == i[0] for i in jewelry_id)).all()
        cart = Cart.query.get(current_user.id)
        cart_ = ast.literal_eval(cart.array_cart)

        j = 0   # Видалення придбаних елементів з кошику
        for i in jewelry:
            i.count -= int(jewelry_id[j][1])
            try:
                del cart_[i.id]
            except:
                pass
            j += 1
        cart.array_cart = str(cart_)

        price = 0   # Ціна в замовленні
        for i in jewelry_id:
            item = Jewelry.query.get(i[0])
            price += item.price*int(i[1])

        fig, ax = plt.subplots()
        orders = Orders.query.all()
        sum = []
        dat = []
        temp = ''
        for i in orders:
            if datetime.datetime.strptime(i.date_reg, "%d.%m.%Y %H:%M") >= datetime.datetime.now() - datetime.timedelta(
                    days=30):
                for j in eval(i.jewelry):
                    if i.date_reg[:-6] == temp:
                        sum[len(sum) - 1] += int(j[1])
                    else:
                        temp = i.date_reg[:-6]
                        sum.append(int(j[1]))
                        dat.append(i.date_reg[:-6])

        xpoints = np.array(dat)
        ypoints = np.array(sum)

        plt.bar(xpoints, ypoints)
        ax.set_title('Замовлення за місяць', loc='left')
        ax.set_ylabel('Кількість замовлень')
        plt.savefig('./static/img/matplotlib.png')

        plt.close()

        fig, ax = plt.subplots()
        sum = []
        dat = []
        temp = ''
        for i in orders:
            for j in eval(i.jewelry):
                if i.date_reg[:-6] == temp:
                    sum[len(sum) - 1] += int(j[1])
                else:
                    temp = i.date_reg[:-6]
                    sum.append(int(j[1]))
                    dat.append(i.date_reg[:-6])

        xpoints = np.array(dat)
        ypoints = np.array(sum)
        ax.set_title('Замовлення за весь час', loc='left')
        ax.set_ylabel('Кількість замовлень')
        plt.bar(xpoints, ypoints)
        plt.savefig('./static/img/matplotlib2.png')

        vals = []
        labels = []
        temp = ''
        for i in orders:
            for j in eval(i.jewelry):
                jew = Jewelry.query.get(int(j[0]))
                jew = f'({jew.id}){jew.type}'
                if labels.count(jew) == 0:
                    labels.append(jew)
                    vals.append(int(j[1]))
                else:
                    vals[labels.index(jew)] += int(j[1])

        explode = list([0.1 if vals[i] == max(vals) else 0 for i in range(len(vals))])
        fig, ax = plt.subplots()
        ax.pie(vals, labels=labels, autopct='%1.1f%%', shadow=True, explode=explode,
               wedgeprops={'lw': 0.3, 'ls': '--', 'edgecolor': "k"}, rotatelabels=True)
        ax.axis("equal")
        plt.savefig('./static/img/matplotlib3.png')

        try:
            orders = Orders(jewelry=str(jewelry_id), name=name, surname=surname,
                            email=email, address=address, telephone=telephone, price=price)
            db.session.add(orders)
            db.session.commit()
        except:
            flash('Невідома помилка', 'cart')
            return redirect('cart')

        api = Api(
            merchant_id=1396424,
            secret_key='test'
        )
        checkout = Checkout(api=api)
        data = {
            'currency': 'UAH',
            'amount': str(price) + '00',
        }
        url = checkout.url(data).get('checkout_url')
        return redirect(url)
    else:
        return redirect('cart')