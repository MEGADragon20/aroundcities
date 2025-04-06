from app2 import app
from app.models import db, Order, Waitlist

with app.app_context():
    Order.__table__.drop(db.engine)
    Waitlist.__table__.drop(db.engine)

with app.app_context():
    Order.__table__.create(db.engine)
    Waitlist.__table__.create(db.engine)

