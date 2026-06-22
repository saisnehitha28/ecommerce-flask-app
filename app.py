from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "ecommerce123"

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 50000,
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853"
    },
    {
        "id": 2,
        "name": "Mobile",
        "price": 20000,
        "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9"
    },
    {
        "id": 3,
        "name": "Headphones",
        "price": 3000,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e"
    },
    {
        "id": 4,
        "name": "Smart Watch",
        "price": 5000,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30"
    }
]
users = []
orders = []

@app.route("/")
def home():
    return render_template("index.html", products=products)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users.append({
            "username": username,
            "password": password
        })

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        for user in users:
            if user["username"] == username and user["password"] == password:
                session["user"] = username
                return redirect("/")

    return render_template("login.html")

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):

    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]
    cart.append(id)
    session["cart"] = cart

    return redirect("/")

@app.route("/cart")
def cart():

    cart_items = []

    if "cart" in session:
        for pid in session["cart"]:
            for p in products:
                if p["id"] == pid:
                    cart_items.append(p)

    total = sum(item["price"] for item in cart_items)

    return render_template(
        "cart.html",
        items=cart_items,
        total=total
    )

@app.route("/checkout")
def checkout():

    if "user" in session:

        orders.append({
            "user": session["user"],
            "status": "Order Placed"
        })

    session["cart"] = []

    return redirect("/orders")

@app.route("/orders")
def order_page():
    return render_template("orders.html", orders=orders)

if __name__ == "__main__":
    app.run(debug=True)