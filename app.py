from flask import Flask, render_template, request, json, redirect, url_for, jsonify, session
from flask_mysqldb import MySQL
import dao, os

app = Flask(__name__)
app.secret_key = os.urandom(16)
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

@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method == "POST":
        _username = request.form['username']
        _password = request.form['password']
        _email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO demo.customer (user_username,user_password,user_email) VALUES (%s,%s,%s)",(_username,_password,_email))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login",methods=["POST","GET"])
def login():
    error = ""
    if request.method == "POST":
        _username = request.form['username']
        _password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM demo.customer")
        data = cursor.fetchall()
        for row in data:
            if _username == row[1]:
                if _password == row[2]:
                    session['user'] = row
                    return redirect(url_for('home'))
        else:
            cursor.close()
            error = "Sài tài khoản hoặc mật khẩu! Vui lòng thử lại."
    return render_template('login.html',error=error)

@app.route("/logout")
def logout():
    session['user'] = None
    return redirect(url_for('home'))

@app.route("/products/")
def product_list():
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    category_id = request.args.get("category_id")
    return render_template("products.html",
                           products=dao.read_products(category_id=category_id,keyword=kw,from_price=from_price,to_price=to_price),categories = dao.read_categories())
@app.route("/products/<int:category_id>")
def category_list(category_id):
    products = dao.read_product_by_category_id(category_id)
    return render_template("products.html",
                           products=products)
'''
@app.route("/api/products",methods=["GET","POST"])
def api_product_list():
    if request.method == "POST":
        error = ""
        product_id = request.args.get('product_id')
        product = None
        if product_id:
            product = dao.read_product_id(product_id=int(product_id))
'''

@app.route('/products/update',methods=["POST","GET"])
def update_product():
    error = None
    product = None
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        category_id = request.form.get('category_id')
        amount = request.form.get('amount')
        product_id = request.form.get('product_id')
        if dao.update_product(
                name=name,
                description=description,
                price=price,
                amount=amount,
                product_id=product_id,
                category_id=category_id):
            return redirect(url_for("product_list"))
        else:
            error = "Something went wrong! PLease back later!."


    if request.args.get('product_id'):# Chạy được
        product = dao.read_product_id(int(request.args['product_id']))

    return render_template('update_products.html', categories=dao.read_categories(), error=error, product=product)

@app.route("/products/add",methods=["POST","GET"])
def add_product():
    error = None
    product = None
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        category_id = request.form.get('category_id')
        amount = request.form.get('amount')
        if dao.add_product(name,description,price,category_id,amount):
            return redirect(url_for("product_list"))
        else:
            error = "Something went wrong! PLease back later!."

    return render_template("add_products.html",categories=dao.read_categories(),error=error,product=product)

@app.route('/api/products/<int:product_id>',methods=["DELETE"])
def delete_product(product_id):
    if dao.delete_product(product_id=product_id):
        return jsonify({
            "status": 200,
            "message": "Delete successfully",
            "data": {"product_id": product_id}
        })
    return jsonify({
        "status": 500,
        "message": "Delete not successfully"
    })

if __name__ == "__main":
    app.run()