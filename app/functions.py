from .models import Order, User, db
import datetime, json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os, easypost
from dotenv import load_dotenv



load_dotenv()
easypost.api_key = "YOUR_TEST_API_KEY"



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


def create_order(cart, price, usr_id, order_address: None) -> Order:
    """
    Creates a new order with an ID, current date, and a list of products."
    """
    user = User.query.get_or_404(usr_id, "user_id")
    if order_address is None:
        order_address = user.address
    order_email = user.email
    now = datetime.datetime.now()

    if not isinstance(cart, dict):
        raise ValueError("Cart must be a dictionary containing product details.")

    if isinstance(order_address, dict):
        order_address = json.dumps(order_address)

    if isinstance(cart, str):
        cart = json.loads(cart)
    

    order = Order(
        user_id = usr_id,
        #date=now,
        products=cart,
        total_price = price,
        status="pending",
        address= order_address,
        email = order_email
    )
    db.session.add(order)
    db.session.commit()



def send_email(to, subject, body):
    print("SENDING EMAIL")
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

def get_my_address():
    """
    Returns the address of the sender.
    This is used for shipping calculations.
    """
    street = os.getenv("MY_street")
    city = os.getenv("MY_city")
    zip_code = os.getenv("MY_zip")
    country = os.getenv("MY_country")

    return {
        "street1": street,
        "city": city,
        "zip": zip_code,
        "country": country
    }

def get_shipping_cost_easypost(address, weight_grams):
    # Convert to ounces (EasyPost uses oz)
    weight_oz = weight_grams / 28.3495

    # Setup from/to address
    to_address = {
        "street1": address["street"],
        "city": address["city"],
        "zip": address["zip"],
        "country": address["country"]
    }

    from_address = get_my_address()

    # Create shipment
    parcel = easypost.Parcel.create(
        length=20,
        width=15,
        height=5,
        weight=weight_oz
    )

    shipment = easypost.Shipment.create(
        to_address=to_address,
        from_address=from_address,
        parcel=parcel
    )

    # Get the cheapest rate
    lowest = shipment.lowest_rate()
    return float(lowest.rate)



