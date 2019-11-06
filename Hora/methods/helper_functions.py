import hashlib
from uuid import uuid4
from datetime import datetime
from db_models.models import User, Category, Product, Cart, Orders


def perform_md5_hash(text):
    result = hashlib.md5(text.encode())
    return result.hexdigest()


def perform_signin_operation(payload):
    user_name = payload.get('username', "")
    password = payload.get('password', "")

    result_set = User.objects(UserName=user_name)
    if result_set:
        document = result_set[0]
        hash_in_db = document.Password
        password_hash = perform_md5_hash(password)
        if password_hash == hash_in_db:
            return {"Success": "User - {} logged-in successfully".format(user_name)}
        else:
            return {"Error": "Password does not match, retry", "ErrorCode": 102}

    else:
        return {"Error": "UserName does not exists in the system", "ErrorCode": 103}


def perform_signup_operation(payload):
    user_name = payload.get('username', "")
    password = payload.get('password', "")
    first_name = payload.get('firstName', "")
    last_name = payload.get('lastName', "")
    address = payload.get('address', "")

    result_set = User.objects(UserName=user_name)
    if result_set:
        return {"Error": "UserName - {0} already exists in the system".format(user_name), "ErrorCode": 101}

    data_dict = {'Password': perform_md5_hash(password), 'FirstName':first_name, 'LastName': last_name, 'Address': address}

    user_doc = User.objects(UserName=user_name). \
        modify(upsert=True, new=True, ModifiedDate=datetime.utcnow(), IsActive=True, **data_dict)

    return {"Success": "User - {0} created successfully".format(user_name)}


def get_product_categories():
    response = []
    category_docs = Category.objects()
    for document in category_docs:
        temp_dict = {'Name': document.Name, 'URL': document.URL}
        response.append(temp_dict)

    return {"Categories": response}


def get_products_from_category(url):
    response = []
    result_set = Category.objects(URL=url)
    if result_set:
        category_doc = result_set[0]
        product_docs = Product.objects(Category=category_doc)
        for document in product_docs:
            temp_dict = {'Name': document.Name, 'URL': document.URL}
            response.append(temp_dict)

        return {"CategoryName": category_doc.Name, "Products": response}

    else:
        return {"Error": "Invalid Product Category URL - {0} Entered".format(url), "ErrorCode": "106"}


def get_product(url):
    response = {}
    result_set = Product.objects(URL=url)
    if result_set:
        document = result_set[0]
        response.update({"Name": document.Name, "URL": document.URL,
                         "OriginalPrice":document.OriginalPrice, "OfferPrice": document.OfferPrice})
        return response
    else:
        return {"Error": "Invalid Product Name Entered", "ErrorCode": "404"}


def add_product_category(payload):
    name = payload.get('name', "")
    url = payload.get('url', "")

    result_set = Category.objects(Name=name)
    if result_set:
        return {"Error": "Category with name - {0} already exists".format(name), "ErrorCode": "105"}
    else:
        category_doc = Category.objects(Name=name).\
            modify(upsert=True, new=True, ModifiedDate=datetime.utcnow(), IsActive=True, URL=url)

    return {"Success": "Category - {0} added successfully".format(name)}

def add_product(payload):
    category_name = payload.get('categoryName', "")
    product_name = payload.get('name', "")
    product_url = payload.get('url', "")
    original_price = payload.get('origPrice', 0)
    offer_price = payload.get('offerPrice', 0)

    result_set = Category.objects(Name=category_name)
    if result_set:
        category_doc = result_set[0]
        data_dict = {"URL": product_url, "OriginalPrice": original_price, "OfferPrice": offer_price}
        product_doc = Product.objects(Category=category_doc, Name=product_name).\
            modify(upsert=True, new=True, ModifiedDate=datetime.utcnow(), IsActive=True, **data_dict)

        return {"Success": "Product - {0} added successfully".format(product_name)}
    else:
        return {"Error": "Invalid Product Category - {0} Entered".format(category_name), "ErrorCode": "104"}



if __name__ == '__main__':
    perform_md5_hash("password")