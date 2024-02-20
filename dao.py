import json, os, hashlib
def read_products(category_id=0, keyword=None, from_price=None, to_price=None):
    f = open("data/products.json","r",encoding="utf-8")
    products = json.load(f)
    if category_id > 0:
        products = [p for p in products if p["category_id"] == category_id]
    if keyword:
        products = [p for p in products if keyword.lower() in p["name"].lower() or keyword.lower() in p["description"].lower()]
    if from_price and to_price:
        products = [p for p in products if p["price"] >= float(from_price) and p["price"] <= float(to_price)]
    return products

def read_categories():
    f = open("data/categories.json","r",encoding="utf-8")
    categories = json.load(f)
    return categories

def AI_id():
    lst_id = []
    products = read_products()
    for p in products:
        lst_id.append(p["id"])
    return max(lst_id)+1

def add_product(name, description, price, category_id, amount):
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
    try:
        f = open("data/products.json","w",encoding="utf-8")
        json.dump(products, f, ensure_ascii=False, indent=4)
        return True
    except Exception as ex:
        print(ex)
        return False

if __name__ == "__main__":
    print(read_products)