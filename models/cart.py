from init import db

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    array_cart = db.Column(db.Text)

    def __repr__(self):
        return '<Cart %r>' % self.id
