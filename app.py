from flask import Flask, render_template, request, json, redirect, url_for, jsonify, session
from MySQL.mysql_config import *
import dao
import os
import random
import flask
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(16)
mysql.init_app(app)


def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return check


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    msg = ""
    if request.method == "POST":
        _username = request.form['username']
        _email = request.form['email']
        _password = request.form['password']
        _password2 = request.form['password2']
        if dao.check_username(_username):
            msg = "Tên đăng nhập đã tồn tại!"
        elif not dao.validate_password(_password):
            msg = "Vui lòng nhập mật khẩu dài 6-32 ký tự, có ký tự chữ số, chữ hoa, chữ thường và kí tự đặc biệt."
        elif dao.check_email(_email):
            msg = "Email đã tồn tại! Vui lòng sử dụng email khác!"
        else:
            if dao.signup(_username, _password, _password2, _email):
                return redirect(url_for("login"))
            else:
                msg = "Mật khẩu không khớp! Vui lòng nhập lại!"
    return render_template("signup.html", msg=msg)


@app.route("/login/", methods=["POST", "GET"])
def login():
    msg = ""
    if request.method == "POST":
        _username = request.form['username']
        _password = request.form['password']
        if dao.login(_username, _password):
            if request.args.get('next'):
                return redirect(request.args["next"])
            return redirect(url_for('home'))
        else:
            msg = "Sài tài khoản hoặc mật khẩu! Vui lòng thử lại."
    return render_template('login.html', msg=msg)


@app.route("/logout")
def logout():
    session['user'] = None
    return redirect(url_for('login'))


@app.route("/products/")
@login_required
def product_list():
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    category_id = request.args.get("category_id")
    branch_id = request.args.get("branch_id")
    return render_template("products.html",
                           products=dao.read_products(
                               category_id=category_id,
                               keyword=kw,
                               from_price=from_price,
                               to_price=to_price,branch_id=branch_id),
                           categories=dao.read_categories(), branches=dao.read_branches())


@app.route("/products/update/", methods=["POST", "GET"])
def update_product():
    print("test")
    error = None
    product = None
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        category_id = request.form.get('category_id')
        amount = request.form.get('amount')
        branch_id = request.form.get('branch_id')
        product_id = request.args.get("product_id")
        if dao.update_product(
                name=name, description=description, price=price,
                amount=amount, product_id=product_id, category_id=category_id, branch_id=branch_id):
            return redirect(url_for("product_list"))
        else:
            error = "Something went wrong! PLease back later!."
    if request.args.get('product_id'):  # Chạy được
        product = dao.read_product_id(request.args['product_id'])

    return render_template('update_products.html', categories=dao.read_categories(),
                           error=error, product=product, branches=dao.read_branches())


@app.route("/products/add", methods=["POST", "GET"])
def add_product():
    error = None
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price', 0)
        category_id = request.form.get('category_id')
        amount = request.form.get('amount', 0)
        branch_id = request.form.get('branch_id')
        barcode = 'SP' + str(random.randint(1000,9999))
        if dao.add_product(
                name=name,description=description,price=price,
                category_id=category_id,amount=amount,branch_id=branch_id,barcode=barcode):
            return redirect(url_for('product_list'))
        else:
            error = "Something went wrong! PLease back later!."

    return render_template("add_products.html", categories=dao.read_categories(),
                           error=error, branches=dao.read_branches())


@app.route('/api/products/<int:product_id>',methods=["DELETE"])
def delete_product(product_id):
    if dao.delete_product(product_id):
        return jsonify({
            "status": 200,
            "message": "Delete successfully",
            "data": {"product_id": product_id}
        })
    return jsonify({
        "status": 500,
        "message": "Delete not successfully"
    })


@app.route('/employee/')
@login_required
def emp_list():
    emp_id = request.args.get('emp_id')
    return render_template("list_emp.html", employees=dao.read_employees(emp_id=emp_id))


@app.route('/employee/add', methods=['POST', 'GET'])
def add_emp():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        sex = request.form.get('sex')
        birth = request.form.get('birth')
        role = request.form.get('role')
        pos = request.form.get('pos')
        phone = request.form.get('phone')
        email = request.form.get('email')
        emp_id = request.form.get("emp_id")
        if dao.read_employee_by_id(emp_id) is not None:
            error = "Mã nhân viên đã tồn tại."
        else:
            if dao.add_employee(
                    name=name, phone=phone, email=email,
                    emp_id=emp_id, sex=sex, birth=birth, role=role, pos=pos):
                return redirect(url_for("emp_list"))
            else:
                error = "Something went wrong! PLease back later!."

    return render_template('add_emp.html', error=error)

@app.route('/employee/update/', methods=['POST', 'GET'])
def update_emp():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        sex = request.form.get('sex')
        birth = request.form.get('birth')
        role = request.form.get('role')
        pos = request.form.get('pos')
        phone = request.form.get('phone')
        email = request.form.get('email')
        emp_id = request.args.get('emp_id')
        if dao.update_employee(
                name=name, phone=phone, email=email,
                emp_id=emp_id, sex=sex, birth=birth, role=role, pos=pos):
            return redirect(url_for("emp_list"))
        else:
            error = "Something went wrong! PLease back later!."
    if request.args.get("emp_id"):
        emp = dao.read_employee_by_id(request.args["emp_id"])

    return render_template('update_emp.html', error=error, emp=emp)

@app.route('/api/employee/<emp_id>', methods=["DELETE"])
def delete_emp(emp_id):
    if dao.delete_emp(emp_id):
        return jsonify({
            "status": 200,
            "message": "Delete successfully",
            "data": {"emp_id": emp_id}
        })
    return jsonify({
        "status": 500,
        "message": "Delete not successfully"
    })

@app.route("/api/carts", methods=["POST"])
def add_to_cart(category_id):
    products = dao.read_product_by_category_id(category_id)
    return render_template("products.html", products=products)


if __name__ == "__main":
    app.run()
