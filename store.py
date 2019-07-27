from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
from dal.mysql_db_adapter import MySqlDBAdapter

_db_adapter = MySqlDBAdapter()


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@post("/category")
def create_category():
    forms = request.forms

    try:
        category_name = forms["name"]
    except Exception as error:
        missing_parameters(error)

    try:
        if _db_adapter.is_category_exist_by_name(category_name):
            result = {'STATUS': "ERROR", 'MSG': 'Category already exists', 'CODE': 200}
            return json.dumps(result)

        _db_adapter.create_category(category_name)
        last_category_id = _db_adapter.get_last_category_id()[0][0]
        result = {'STATUS': "SUCCESS", 'MSG': 'The category was created successfully', 'CAT_ID': last_category_id,
                  'CODE': 201}
        return json.dumps(result)

    except Exception as error:
        internal_error(error)


@delete("/category/<category_id>")
def delete_category_by_id(category_id):
    try:
        if not _db_adapter.is_category_exist_by_id(category_id):
            result = {'STATUS': "ERROR", 'MSG': 'category not found', 'CODE': 404}
            return json.dumps(result)

        _db_adapter.delete_category(category_id)

        result = {'STATUS': "SUCCESS", 'CODE': 201}
        return json.dumps(result)

    except Exception as error:
        internal_error(error)


@get("/categories")
def get_categories():
    try:
        db_result = _db_adapter.get_categories()
        result = {'STATUS': "SUCCESS", 'MSG': 'The category was created successfully', 'CATEGORIES': db_result,
                  'CODE': 200}
        return json.dumps(result)

    except Exception as error:
        internal_error(error)


@post("/product")
def get_categories():
    forms = request.forms

    try:
        prod_id = forms["id"]
        prod_title = forms["title"]
        prod_desc = forms["description"]
        prod_price = forms["price"]
        prod_img_url = forms["img_url"]
        prod_category_id = forms["category_id"]
        prod_is_favorite = forms["is_favorite"]
    except Exception as error:
        return missing_parameters(error)

    try:
        if not _db_adapter.is_category_exist_by_id(prod_category_id):
            result = {'STATUS': "ERROR", 'MSG': 'category not found', 'CODE': 404}
            return json.dumps(result)

        if not _db_adapter.is_product_exist(prod_id):
            _db_adapter.add_product(prod_id, prod_title, prod_desc, prod_price, prod_img_url,
                                    prod_category_id, prod_is_favorite)
        else:
            _db_adapter.edit_product(prod_id, prod_title, prod_desc, prod_price, prod_img_url,
                                     prod_category_id, prod_is_favorite)

        result = {'STATUS': "SUCCESS", 'PRODUCT_ID': prod_id, 'CODE': 201}
        return json.dumps(result)

    except Exception as error:
        internal_error(error)


def missing_parameters(error):
    print({"Missing Parameters": error})
    result = {'STATUS': "ERROR", 'MSG': 'missing parameters', 'CODE': 400}
    return json.dumps(result)


def internal_error(error):
    print({"Error": error})
    result = {'STATUS': "ERROR", 'MSG': 'Internal error', 'CODE': 500}
    return json.dumps(result)


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


run(host='localhost', port=argv[1])
