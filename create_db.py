from app2 import app
from app.models import db, User
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
    db.drop_all()

with app.app_context():
    db.create_all()
    create_admin()
