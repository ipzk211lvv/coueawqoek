from init import db
from datetime import datetime

from flask_login import current_user

from flask_admin.contrib.sqla import ModelView

from models.orders import Orders

class Jewelry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(10), nullable=False)
    title = db.Column(db.Text, nullable=False)
    metal = db.Column(db.String(40), nullable=False)
    proba = db.Column(db.Integer, nullable=False)
    metal_color = db.Column(db.String(30), nullable=False)
    stones = db.Column(db.Text)
    gender = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    date_create = db.Column(db.String(30), nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return '<Jewelry %r>' % self.id


class AdminModelJewelry(ModelView):
    column_list = ('type', 'title', 'metal', 'proba', 'metal_color', 'gender', 'stones', 'price', 'count', 'date_create')
    column_filters = ['type', 'title', 'metal', 'proba', 'metal_color', 'gender', 'stones', 'price', 'count' , 'date_create']
    page_size = 25

    def is_accessible(self):
        if current_user.is_authenticated and not current_user.is_anonymous:
            return current_user.admin
        return False