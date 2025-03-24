from .models import Order, User, db
import datetime, json

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

    # ✅ Ensure cart is a dictionary before storing
    if not isinstance(cart, dict):
        raise ValueError("Cart must be a dictionary containing product details.")

    # ✅ Convert address to JSON if it's a dictionary
    if isinstance(order_adress, dict):
        order_adress = json.dumps(order_adress)  # Convert dict to JSON string

    # ✅ Ensure products is stored as a dict (not a string)
    if isinstance(cart, str):  # If cart was accidentally converted to a string
        cart = json.loads(cart)  # Convert it back to a dict
    

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

