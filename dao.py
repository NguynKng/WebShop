from mysql_config import mysql
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import re


def read_products(category_id=0, keyword=None, from_price=None, to_price=None, branch_id=None):
    cursor = mysql.connection.cursor()
    cursor.execute("select * from products")
    products = cursor.fetchall()
    if branch_id:
        products = [p for p in products if p[6] == branch_id]
    if category_id:
        products = [p for p in products if p[1] == int(category_id)]
    if keyword:
        products = [p for p in products if keyword.lower() in p[2].lower() or keyword.lower() in p[3].lower()]
    if from_price and to_price:
        products = [p for p in products if p[4] >= int(from_price) and p[4] <= int(to_price)]
    cursor.close()
    return products


def read_branches():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM branches")
    branches = cursor.fetchall()
    cursor.close()
    return branches


def read_categories():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    cursor.close()
    return categories


def read_product_by_category_id(category_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products WHERE category_id = %s", (category_id,))
    product = cursor.fetchone()
    return product


def read_product_id(product_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    return product


def add_product(name, description, price, category_id, amount, branch_id, barcode):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO products (category_id,name,description,price,amount,branch_id,barcode) values (%s,%s,%s,%s,%s,%s,%s)",
                   (category_id, name, description, price, amount, branch_id, barcode))
    mysql.connection.commit()
    cursor.close()
    return True


def update_product(name, description, price, amount, product_id, category_id, branch_id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE products SET category_id = %s, name = %s, description = %s, price = %s, amount = %s, branch_id = %s WHERE id = %s",
        (category_id, name, description, price, amount, branch_id, product_id))
    mysql.connection.commit()
    cursor.close()
    return True


def delete_product(product_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM products WHERE (id = %s)", (product_id,))
    mysql.connection.commit()
    cursor.close()
    return True


def read_employees(emp_id=None):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM employee")
    employee = cursor.fetchall()
    if emp_id:
        employee = [e for e in employee if e[0] == int(emp_id)]
    cursor.close()
    return employee


def read_employee_by_id(emp_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM employee WHERE emp_id = %s", (emp_id,))
    employee = cursor.fetchone()
    cursor.close()
    return employee


def update_employee(emp_id, name, sex, birth, role, pos, email, phone):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE employee SET name = %s, sex = %s, birth = %s, role = %s, pos = %s, email = %s, phone = %s WHERE emp_id = %s",
        (name, sex, birth, role, pos, email, phone, emp_id))
    mysql.connection.commit()
    cursor.close()
    return True


def add_employee(emp_id, name, sex, birth, role, pos, email, phone):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO employee (emp_id,name,sex,birth,role,pos,email,phone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                   (emp_id, name, sex, birth, role, pos, email, phone))
    mysql.connection.commit()
    cursor.close()
    return True

def delete_emp(emp_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM employee WHERE (emp_id = %s)", (emp_id,))
    mysql.connection.commit()
    cursor.close()
    return True


def login(_username, _password):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM customer WHERE user_username = %s", (_username,))
    data = cursor.fetchone()
    if data:
        if check_password_hash(data[2], _password):
            session['user'] = data
            return True
        else:
            cursor.close()
            return False
    else:
        cursor.close()
        return False


def signup(_username, _password, _password2, _email):
    hash = generate_password_hash(_password, method='pbkdf2:md5', salt_length=8)
    if check_password_hash(hash, _password2):
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO customer (user_username,user_password,user_email) VALUES (%s,%s,%s)",
                       (_username, hash, _email))
        mysql.connection.commit()
        cursor.close()
    return True


def validate_password(password):
    pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&.*-]).{8,}$"
    match = re.match(pattern, password)
    return bool(match)


def check_email(_email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT user_email FROM customer where user_email = %s", (_email,))
    data = cursor.fetchone()
    if data:
        cursor.close()
        return True
    else:
        cursor.close()
        return False


def check_username(_username):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT user_username FROM customer where user_username = %s", (_username,))
    data = cursor.fetchone()
    if data:
        cursor.close()
        return True
    else:
        cursor.close()
        return False


if __name__ == "__main__":
    print(read_products())
