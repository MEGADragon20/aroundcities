from app2 import app
from app.models import db, User, Order, Waitlist
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from os import environ
import os


load_dotenv()  #Load .env


def create_admin():
    admin_pw = os.getenv('ADMIN_PW')
    if admin_pw is not None:
        default_admin = User(username="admin", email="admin@example.com", password_hash=generate_password_hash(admin_pw), is_admin=True, address="-None")
        db.session.add(default_admin)
        db.session.commit()

with app.app_context():
    #Waitlist.__table__.drop(db.engine)
    #Order.__table__.drop(db.engine)
    User.__table__.drop(db.engine)


with app.app_context():
    #User.__table__.create(db.engine)
    create_admin()
    #Waitlist.__table__.create(db.engine)
    Order.__table__.create(db.engine)
    

    # idk
