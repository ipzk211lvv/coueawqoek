from datetime import datetime

from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from flask_login import current_user

from init import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    surname = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String(254), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text, default='')
    admin = db.Column(db.BOOLEAN, nullable=False, default=False)
    date_reg = db.Column(db.String(30), nullable=False, default=datetime.now().strftime("%d.%m.%Y %H:%M"))



    def __init__(self, name, surname, email, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.id


class AdminModelUser(ModelView):
    column_list = ('name', 'surname', 'email', 'address', 'admin', 'date_reg')
    column_filters = ['name', 'surname', 'email', 'date_reg']
    page_size = 25

    def is_accessible(self):
        if current_user.is_authenticated and not current_user.is_anonymous:
            return current_user.admin
        return False
