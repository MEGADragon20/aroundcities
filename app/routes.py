from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request, send_from_directory, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User, Product, Order
from .forms import SignupForm, LoginForm
from werkzeug.utils import secure_filename
from .functions import transform_in_euro, transform_out_euro, create_order
from sqlalchemy.sql import text
import flask, os, stripe, logging
main = Blueprint("main", __name__)

API_KEY = "1234"
logging.basicConfig(filename='web_log.txt', level=logging.INFO, format='%(asctime)s %(message)s')
@main.before_request
def log_request_info():
    user_ip = request.remote_addr
    url = request.url 
    logging.info(f'request from {user_ip} to {url}')
    print(f'request from {user_ip} to {url}')



@main.route('/get_icon/<filename>')
def get_icon(filename):
    return send_from_directory("static/icons", filename)

@main.route('/get_image/<filename>', defaults={'foldername': None})
@main.route('/get_image/<filename>/<foldername>')
def get_image(filename, foldername):
    if foldername is None:
        return send_from_directory("static/uploads", filename)
    else:
        return send_from_directory(f"static/uploads/{foldername}", filename)

@main.route('/get_style/<filename>')
def get_style(filename):
    return send_from_directory("static/styles", filename)

@main.route('/get_script/<filename>')
def get_scripts(filename):
    return send_from_directory("static/scripts", filename)

@main.route('/get_stripe_public_key')
def get_stripe_public_key():
    user_api_key = request.headers.get("X-API-KEY")
    
    if user_api_key != API_KEY:
        return render_template("error.html", error_num = 403, error_message = "No access")
    
    return jsonify({"publicKey": os.getenv("STRIPE_PUBLIC_KEY")})
@main.route("/")
def home():
    return render_template("index.html")

@main.route("/pay")
def pay():
    return render_template("pay.html")
@main.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered!", "danger")
            return redirect(url_for("main.signup"))
        adress = {
            "street": form.street.data,
            "number": form.number.data,
            "city": form.city.data,
            "country": form.country.data,
            "postal_code": form.postal_code.data,
        }
        new_user = User(username=form.username.data, email=form.email.data, adress=adress)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("main.dashboard"))

    return render_template("signup.html", form=form)

@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            next = flask.request.args.get('next')
            print(next)
            # next_is_valid should check if the user has valid
            # permission to access the `next` url
            return redirect(url_for("main.dashboard"))
        flash("Invalid email or password!", "danger")
    print(current_user)
    return render_template("login.html", form=form)

@main.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        request.args.get("filters")
        products = Product.query.all()
        return render_template("products.html", products=products)

@main.route("/about_us")
def about_us():
    return render_template("about_us.html")


@main.route("/product", methods=["GET", "POST"])
def product():
    if request.method == "GET":
        product_id = request.args.get("id")
        product = Product.query.get(product_id)
        return render_template("product.html", product=product)

@main.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    product_id = request.form.get('product_id')
    modification = request.form.get('modification')
    size = request.form.get('size')
    product = Product.query.get(product_id)
    product_name = product.name

    print(product_id)
    m = product.modifications.index(modification)
    s = list(product.stock.keys()).index(size) #list bc of py datatypes. Keys is just a view? check python 3.0
    ucic = f"{product_id}_{m}_{s}"


    print("productprice", product.price)
    if ucic in cart:
        cart[ucic]["count"] += 1
    else:
        cart[ucic] = {}
        cart[ucic]["count"] = 1
        cart[ucic]["product_id"] = product_id
        cart[ucic]["price"] = product.price
        cart[ucic]["name"] = product_name
        cart[ucic]["modification"] = modification
        cart[ucic]["size"] = size
    session.modified = True  # Tells Flask that the session has changed

    flash("Product added to cart!", "success")
    return redirect(url_for("main.products"))
@main.route("/cart", methods=["GET"])
def cart():
# TODO: implement sharing carts ig
    cart = session.get('cart', {})
    print("cart", cart)
    return render_template("cart.html", cart=cart)

@main.route("/remove_from_cart/<ucic>", methods=["GET"])
def remove_from_cart(ucic): #? Needs to be checked pls
    cart = session.get('cart', {})
    if ucic in cart:
        del cart[ucic]
        session.modified = True  # Tells Flask that the session has changed
    flash("Product removed from cart!", "success")
    return redirect(url_for("main.cart"))

@main.route("/submit_cart", methods=["GET"])
def submit_cart():
    cart = session.get('cart', {})
    total_price = 0
    for ucic, stuff in cart.items():
        product = Product.query.get(stuff["product_id"])
        price = product.price 
        price = transform_out_euro(price)* stuff['count']
        total_price += price
    print("total", total_price)
    total_price_str = transform_in_euro(total_price)
    flash("Cart submitted!", "success")
    return render_template("pay.html", total_price=total_price, total_price_str= total_price_str)

#! Profile

@main.route("/pay_cart", methods=["POST"])
def pay_cart():
    try:
        #cart = session.get('cart', {})
        #current_user_id = current_user.id
        #current_user_adress = current_user.adress
        price_to_pay = request.get_json().get('amount', 1000)
        currency = request.form.get('currency', 'eur')
        payment_intent = stripe.PaymentIntent.create(amount=price_to_pay,currency=currency)
        return jsonify({"clientSecret": payment_intent.client_secret})
        
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    
    #create_order(cart=cart, price=price_to_pay, usr_id=current_user_id, order_adress=current_user_adress)
    





@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    session.clear()
    return redirect(url_for("main.login"))





#! Admin

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@main.route("/admin")
@admin_required
def admin():
    order_statuss = db.session.execute(statement=text('SELECT status FROM public."order"'))
    print(order_statuss)
    pending = 0
    packing = 0
    packed = 0
    shipping = 0
    shipped = 0
    for i in order_statuss:
        if i.status == "pending":
            pending += 1
        elif i.status == "packing":
            packing += 1
        elif i.status == "packed":
            packed += 1
        elif i.status == "shipping":
            shipping += 1
        elif i.status == "shipped":
            shipped += 1
    print(pending, packing, packed, shipping, shipped)
        
    return render_template("admin.html", pending=pending, packing=packing, packed = packed, shipping=shipping, shipped = shipped)

@main.route("/admin/static/styles/admin_products.css", methods=["GET", "POST"])
@admin_required
def redirection():
    return flask.send_from_directory("static", "styles/admin_products.css")


@main.route("/admin/products", methods=["GET", "POST"])
@admin_required
def admin_products():
    products = Product.query.all()
    return render_template("admin_products.html", products=products)

@main.route("/admin/products/add", methods=["GET", "POST"])
@admin_required
def admin_products_add():
    if request.method == "POST":
        print("req", request.form)
        name = request.form.get("name")
        description = request.form.get("description")
        raw_content = request.form.get("content")
        price = transform_in_euro(int(request.form.get("price")))
        stock_XS = int(request.form.get("stockXS"))
        stock_S = int(request.form.get("stockS"))
        stock_M = int(request.form.get("stockM"))
        stock_L = int(request.form.get("stockL"))
        stock_XL = int(request.form.get("stockXL"))
        stock_XXL = int(request.form.get("stockXXL"))
        stock= {"XS": stock_XS, "S": stock_S, "M": stock_M, "L": stock_L, "XL": stock_XL, "XXL": stock_XXL}
        raw_collections = request.form.get("collections")
        raw_modifications = request.form.get("modifications")
        images = request.files.getlist("images")
        print("images", images, len(images))
        print(name, description, raw_content, price, stock, raw_collections, raw_modifications)
        if not name or not description or not raw_content or not price or not stock or not raw_collections or not raw_modifications:
            print("HELP!")
            return render_template("admin_products_add.html")
        content = raw_content.split(",")
        collections = raw_collections.split(",")
        modifications = raw_modifications.split(",")
        max_id = db.session.query(db.func.max(Product.id)).scalar() or 0
        new_id = max_id + 1
        if not os.path.exists("app/static/uploads/"+ str(new_id)):
                os.makedirs("app/static/uploads/"+ str(new_id))
        counter = 0
        final_images = []
        for image in images:
            print("image: ", image)
            ext = image.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(str(counter)+ "." + ext)
            image_path = os.path.join("app/static/uploads/" + str(new_id), filename)
            image.save(image_path)
            final_images.append(filename)
            counter +=1


        new_product = Product(name=name, description=description, content=content, price=price, stock=stock, image=final_images, collections=collections, modifications=modifications)
        print("new product: ", new_product)
        db.session.add(new_product)
        db.session.commit()



    return render_template("admin_products_add.html")


@main.route('/admin/orders')
@admin_required
def admin_orders():
    orders = Order.query.all()
    return render_template('admin_orders.html', orders=orders)

@main.route('/admin/order/<int:id>', methods=['GET'])
@admin_required
def admin_order(id):
    order = Order.query.get_or_404(id)
    return render_template('admin_order.html', order=order)