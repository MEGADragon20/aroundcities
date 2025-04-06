from .models import Order, User, db
import datetime, json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()




def transform_in_euro(number: int) -> str:
    """
    Takes an int (cents) and transforms it into a string (euros)

    ________________________________________________________________
    by MD20
    """
    number /= 100
    number_str = str(number) + " €"
    return number_str

def transform_out_euro(number: str) -> int:
    """
    Takes a string (euros) and transforms it into an int (cents)

    ________________________________________________________________
    by MD20
    """
    only_float = number[:-1]
    return int(float(only_float) * 100)


def create_order(cart, price, usr_id, order_adress: None) -> Order:
    """
    Creates a new order with an ID, current date, and a list of products."
    """
    user = User.query.get_or_404(usr_id, "user_id")
    print(user)
    if order_adress is None:
        order_adress = user.adress
    order_email = user.email
    now = datetime.datetime.now()
    print(cart, "will be transformed into -> Order// Proceed? -> okay___ Order generating")

    if not isinstance(cart, dict):
        raise ValueError("Cart must be a dictionary containing product details.")

    if isinstance(order_adress, dict):
        order_adress = json.dumps(order_adress)

    if isinstance(cart, str):
        cart = json.loads(cart)
    

    order = Order(
        user_id = usr_id,
        #date=now,
        products=cart,
        total_price = price,
        status="pending",
        address= order_adress,
        email = order_email
    )
    db.session.add(order)
    db.session.commit()



def send_email(to, subject, body):
    sender_email = "around.cities@gmx.de"
    smtp_server = "mail.gmx.net"
    smtp_port = 587
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    print(smtp_password, smtp_user)

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, to, message.as_string())
        print(f"email to {to}.")
    except Exception as e:
        print(f"error sending email to {to}: {e}")