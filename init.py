import datetime

from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)
app.secret_key = 'n`i#$n_^j*~a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/cover'
db = SQLAlchemy(app)
manager = LoginManager(app)


from models.user import User, AdminModelUser
from models.jewelry import Jewelry, AdminModelJewelry
from models.orders import Orders, AdminModelOrders
from models.reports import Reports, AdminModelReports


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='Admin', template_mode='bootstrap4')

admin.add_view(AdminModelUser(User, db.session))
admin.add_view(AdminModelJewelry(Jewelry, db.session))
admin.add_view(AdminModelOrders(Orders, db.session))
admin.add_view(AdminModelReports(Reports, db.session))

db.create_all()


fig, ax = plt.subplots()
orders = Orders.query.all()
sum = []
dat = []
temp = ''
for i in orders:
    if datetime.datetime.strptime(i.date_reg, "%d.%m.%Y %H:%M") >= datetime.datetime.now() - datetime.timedelta(days=30):
        for j in eval(i.jewelry):
                sum.append(i.date_reg[:-6])
                dat.append(int(i.price))

xpoints = np.array(sum)
ypoints = np.array(dat)

plt.bar(xpoints, ypoints)
ax.set_title('Замовлення за місяць', loc='left')
ax.set_ylabel('Гривень')
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
ax.pie(vals, labels=labels, autopct='%1.1f%%', shadow=True, explode=explode, wedgeprops={'lw':0.3, 'ls':'--','edgecolor':"k"}, rotatelabels=True)
ax.axis("equal")
plt.savefig('./static/img/matplotlib3.png')