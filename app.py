from flask import Flask, render_template, request, json, redirect, url_for
from flask_mysqldb import MySQL
import dao

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "zzharrybin219"
app.config['MYSQL_DB'] = "demo"
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/showSignUp')
def showSignUp():
    return render_template("signup.html")

@app.route("/signup",methods=["POST"])
def signup():
    if request.method == "POST":
        _username = request.form['username']
        _password = request.form['password']
        _email = request.form['email']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO demo.customer (user_username,user_password,user_email) VALUES (%s,%s,%s)",(_username,_password,_email))
        mysql.connection.commit()
        cursor.close()
        return showLogin()
    return render_template("index.html")

@app.route("/showLogin")
def showLogin():
    return render_template("login.html")

@app.route("/login",methods=["POST"])
def login():
    if request.method == "POST":
        _username = request.form['username']
        _password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM demo.customer")
        data = cursor.fetchall()
        for row in data:
            if _username == row[1]:
                if _password == row[2]:
                    return "Đăng nhập thành công."
        else:
            cursor.close()
            return "Sai tài khoản hoặc mật khẩu, vui lòng thử lại!."
@app.route("/products")
def product_list():
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    return render_template("products.html",
                           products=dao.read_products(keyword=kw,from_price=from_price,to_price=to_price))

@app.route("/products/add",methods=["POST","GET"])
def add_products():
    error = ""
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        amount = request.form.get("amount")
        category_id = request.form.get("category_id")
        if dao.add_product(name=name,description=description,price=price,category_id=category_id,amount=amount):
            return redirect(url_for("product_list"))
        else:
            error = "Something went wrong! PLease back later!."
    return render_template("add_products.html",categories=dao.read_categories(),error=error)

if __name__ == "__main":
    app.run()