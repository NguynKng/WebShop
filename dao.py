import json, os, hashlib
def read_products(category_id=0, keyword=None, from_price=None, to_price=None):
    f = open("data/products.json","r",encoding="utf-8")
    products = json.load(f)
    if category_id:
        products = [p for p in products if p["category_id"] == int(category_id)]
    if keyword:
        products = [p for p in products if keyword.lower() in p["name"].lower() or keyword.lower() in p["description"].lower()]
    if from_price and to_price:
        products = [p for p in products if p["price"] >= float(from_price) and p["price"] <= float(to_price)]
    return products

def read_categories():
    f = open("data/categories.json","r",encoding="utf-8")
    categories = json.load(f)
    return categories

def read_product_by_category_id(category_id):
    products = read_products()
    for p in products:
        if p["category_id"] == category_id:
            return p
    return None

def read_product_id(product_id):
    products = read_products()
    for p in products:
        if p["id"] == product_id:
            return p
    return None
def AI_id():
    lst_id = []
    products = read_products()
    for p in products:
        lst_id.append(p["id"])
    return int(max(lst_id))+1

def write_json(products,filename):
    try:
        f = open(filename,"w",encoding="utf-8")
        json.dump(products, f, ensure_ascii=False, indent=4)
        return True
    except Exception as ex:
        print(ex)
        return False

def add_product(name, description, price, category_id, amount):
    filename = "data/products.json"
    products = read_products()
    new_product = {
        "id": AI_id(),
        "category_id": int(category_id),
        "name": name,
        "description": description,
        "price": int(price),
        "amount": int(amount)
    }
    products.append(new_product)
    return write_json(products,filename)

def update_product(name, description, price, amount, product_id, category_id):
    filename = "data/products.json"
    products = read_products()
    for idx, p in enumerate(products):
        if p["id"] == int(product_id):
            products[idx]["name"] = name
            products[idx]["description"] = description
            products[idx]["price"] = int(price)
            products[idx]["amount"] = int(amount)
            products[idx]["category_id"] = int(category_id)
            break
    return write_json(products,filename)

def delete_product(product_id):
    filename = "data/products.json"
    products = read_products()
    for idx, p in enumerate(products):
        if p['id'] == int(product_id):
            del products[idx]
            break
    return write_json(products,filename)

if __name__ == "__main__":
    print(read_products())