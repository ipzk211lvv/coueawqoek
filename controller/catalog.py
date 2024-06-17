import os

from sqlalchemy import or_, and_
from flask import render_template, request, redirect, flash, url_for, session
from werkzeug.utils import secure_filename

from init import app, db
from models.jewelry import Jewelry
from models.cart import Cart


@app.route('/catalog')
def catalog():
    jewelry = Jewelry.query.filter().order_by(Jewelry.count.desc()).all()

    return render_template('catalog.html', jewelry=jewelry)


@app.route('/catalog/<string:filters>')
def catalogs(filters):
    filter_ = [i for i in filters.split('&')]

    type_ = [i for i in filter_[0].split('+')]
    metal = [i for i in filter_[1].split('+')]
    color = [i for i in filter_[2].split('+')]
    gender = [i for i in filter_[3].split('+')]
    price = [i for i in filter_[4].split('+')]
    stone = [i for i in filter_[5].split('+')]

    jewelry = Jewelry.query.filter(
        Jewelry.type.in_(type_),
        Jewelry.metal.in_(metal),
        Jewelry.metal_color.in_(color),
        Jewelry.gender.in_(gender),
        and_(Jewelry.price >= int(price[0]), Jewelry.price <= int(price[1])),
        or_(Jewelry.stones.like('%'+stone[i]+'%') for i in range(len(stone)) if stone[0] != '')
    ).order_by(Jewelry.count.desc()).all()

    return render_template('catalog.html', jewelry=jewelry)


@app.route('/jewelry/<int:id>')
def jewelry_info(id):
    jewelry = Jewelry.query.get(id)
    cart = Cart.query.all()
    return render_template('jewerly_info.html', jewelry=jewelry, cart=cart)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == "POST":  # TODO Добавить сохранение картинки и ее названия
        type = request.form['type']
        title = request.form['title']
        metal = request.form['metal']
        proba = request.form['proba']
        metal_color = request.form['metal_color']
        stones = request.form['stone']
        gender = request.form['gender']
        price = request.form['price']
        count = request.form['count']
        if 'image' not in request.files:
            flash('Під час завантаження фото виникла помилка. Спробуйте ще раз', 'add')
            return render_template("add.html")
        file = request.files['image']
        if file.filename == '':
            flash('Фото не завантажене', 'add')
            return render_template("add.html")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                newfilename = str(Jewelry.query.all()[-1].id + 1) + '.jpg'
            except IndexError:
                newfilename = '1.jpg'

            os.rename(
                os.path.join(app.config['UPLOAD_FOLDER'], filename),
                os.path.join(app.config['UPLOAD_FOLDER'], newfilename)
            )

        jewelry = Jewelry(
            type=type, image=newfilename, title=title,
            metal=metal, proba=proba, metal_color=metal_color,
            stones=stones, gender=gender, price=price, count=count
        )
        try:
            db.session.add(jewelry)
            db.session.commit()
            return redirect('/add')
        except:
            flash('При добавлении произошла ошибка', 'add')
            return render_template("add.html")
    else:
        return render_template("add.html")


@app.route('/jewelry-update/<int:id>', methods=['POST', 'GET'])
def jewelry_update(id):
    jewelry = Jewelry.query.get(id)
    if request.method == "POST":
        print(3)
        jewelry.type = request.form['type']
        print(3.1)
        jewelry.title = request.form['title']
        jewelry.metal = request.form['metal']
        jewelry.proba = request.form['proba']
        print(3.2)
        jewelry.metal_color = request.form['metal_color']
        print(3.3)
        jewelry.stones = request.form['stone']
        jewelry.gender = request.form['gender']
        jewelry.price = request.form['price']
        jewelry.count = request.form['count']
        print(4)
        try:
            db.session.commit()
            return redirect(f'/jewelry/{id}')
        except:
            flash('При добавлении произошла ошибка', 'add')
            return render_template("jewelry_update.html", jewelry=jewelry)
    else:
        return render_template("jewelry_update.html", jewelry=jewelry)


@app.route('/delete/<int:id>')
def jewelry_del(id):
    jewelry = Jewelry.query.get_or_404(id)
    try:
        db.session.delete(jewelry)
        os.remove(os.path.join(f'static/cover', f'{id}.jpg'))
        db.session.commit()
    except:
        flash('При удалении произошла ошибка', 'add')
        return redirect(f'/jewelry/{id}')
    return redirect(f'/catalog')