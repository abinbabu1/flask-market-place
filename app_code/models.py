from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from app_code import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password_hash = db.Column(db.String(128))
    budget = db.Column(db.Integer, nullable=False, default=1000)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)

    user_items = db.relationship('Item', backref='owner', lazy=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Item(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(30), nullable=False)
    barcode = db.Column(db.String(12), unique=True)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __init__(self, name, barcode, price, description, owner_id):
        self.name = name
        self.barcode = barcode
        self.price = price
        self.description = description
        self.owner_id = owner_id


# db.create_all()
