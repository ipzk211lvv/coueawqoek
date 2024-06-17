from init import db
from datetime import datetime

from flask_login import current_user

from flask_admin.contrib.sqla import ModelView


class Reports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(71), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    problem = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text)
    date = db.Column(db.String(30), nullable=False, default=datetime.now().strftime("%d.%m.%Y %H:%M"))


class AdminModelReports(ModelView):
    column_list = ('user', 'title', 'problem', 'answer', 'date')
    column_filters = ['user', 'title', 'problem', 'answer', 'date']
    page_size = 10

    def is_accessible(self):
        if current_user.is_authenticated and not current_user.is_anonymous:
            return current_user.admin
        return False

