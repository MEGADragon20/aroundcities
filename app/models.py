from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ARRAY, JSON

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    adress = db.Column(JSON, nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self): # actually default
        return str(self.id)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(ARRAY(db.String(256)), nullable=False)
    price = db.Column(db.String(30), nullable=False)
    stock = db.Column(JSON(), default={
        "XS": 0,
        "S": 0,
        "M": 0,
        "L": 0,
        "XL": 0,
        "XXL": 0
    })
    image = db.Column(ARRAY(db.String(64)), nullable=False)
    collections = db.Column(ARRAY(db.String(64)), nullable=False)
    modifications = db.Column(ARRAY(db.String(64)), nullable=False)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    products = db.Column(JSON(), nullable=False) # JSON first unique identification code then count
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    address = db.Column(JSON(), nullable= False)
    email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, default=db.func.now())

class Waitlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())