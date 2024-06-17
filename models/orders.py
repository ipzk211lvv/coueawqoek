from init import db
from datetime import datetime

from flask_login import current_user

from flask_admin.contrib.sqla import ModelView


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jewelry = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(35), nullable=False)
    surname = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    address = db.Column(db.Text, nullable=False)
    telephone = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    date_reg = db.Column(db.String(30), nullable=False, default=datetime.now().strftime("%d.%m.%Y %H:%M"))

    def __repr__(self):
        return '<Orders %r>' % self.id


class AdminModelOrders(ModelView):
    column_list = ('name', 'surname', 'email', 'address', 'telephone', 'price', 'status', 'date_reg')
    column_filters = ['name', 'surname', 'email', 'address', 'telephone', 'price', 'status', 'date_reg']
    page_size = 25

    def is_accessible(self):
        if current_user.is_authenticated and not current_user.is_anonymous:
            return current_user.admin
        return False
