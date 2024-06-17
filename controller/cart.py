import ast

from flask import render_template, request, redirect, flash, url_for

from init import app, db
from models.cart import Cart
from models.jewelry import Jewelry


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    jewelry = Jewelry.query.all()
    cart = Cart.query.all()
    if request.method == "POST":
        array_cart = request.form['array_cart']
        user_id = request.form['user_id']
        cart = Cart.query.get(user_id)
        cart.array_cart = array_cart
        try:
            db.session.commit()
            return redirect('/cart')
        except:
            return 'Error'
    else:
        cart_user = []
        for i in cart:
            cart_user.append([i.id, [key for key in ast.literal_eval(i.array_cart).items()]])
        return render_template('cart.html', jewelry=jewelry, cart=cart_user)


@app.route('/cart/<int:user_id>/<int:jewelry_id>', methods=['GET', 'POST'])
def add_cart(user_id, jewelry_id):
    user_cart = Cart.query.get(user_id)
    if user_cart:
        array_cart = ast.literal_eval(user_cart.array_cart)
        if list(array_cart.keys()).count(f'{jewelry_id}') == 0:
            array_cart.update({jewelry_id: 1})
            user_cart.array_cart = str(array_cart)
        db.session.commit()
        flash('good')
        return redirect(f'/jewelry/{jewelry_id}')
    else:
        new_cart = Cart(id=user_id, array_cart=str({jewelry_id: 1}))
        try:
            db.session.add(new_cart)
            db.session.commit()
            return redirect(f'/jewelry/{jewelry_id}')
        except:
            return "Error"