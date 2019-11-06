from flask import Flask, request
from methods.helper_functions import perform_signin_operation, perform_signup_operation,\
    get_product_categories, get_product, get_products_from_category, add_product_category, add_product

app = Flask(__name__)

from db_models.models import connect_mongo

connect_mongo()


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/sign-up/", methods=['POST'])
def sign_up():
    request_payload = request.json
    response = perform_signup_operation(request_payload)
    return response


@app.route("/sign-in/", methods=['POST'])
def sign_in():
    request_payload = request.json
    response = perform_signin_operation(request_payload)
    return response


@app.route("/catalogue/", methods=['GET'])
def shopping_catalouge():
    response = get_product_categories()
    return response

@app.route("/category/", methods=['GET', 'POST'])
def product_categories():
    if request.method == "POST":
        response = add_product_category(request.json)
    elif request.method == "GET":
        url = request.args.get('url')
        response = get_products_from_category(url)
    return response

@app.route("/product/", methods=['GET', 'POST'])
def products():
    if request.method == "POST":
        response = add_product(request.json)
    elif request.method == "GET":
        url = request.args.get('url')
        response = get_product(url)
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')