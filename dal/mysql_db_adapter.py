from .base_db_adapter import BaseDatabaseAdapter
import pymysql


class MySqlDBAdapter(BaseDatabaseAdapter):
    def __init__(self):
        self._connection = pymysql.connect(host="localhost",
                                           user="root",
                                           password="root",
                                           db="my_store")

    def is_category_exist_by_name(self, category_name):
        return self.execute_query("SELECT * FROM category WHERE `name` = '{}';".format(category_name))

    def is_category_exist_by_id(self, category_id):
        return self.execute_query("SELECT * FROM category WHERE `id` = '{}';".format(category_id))

    def is_product_exist(self, product_id):
        return self.execute_query("SELECT * FROM product WHERE `id` = '{}';".format(product_id))

    def execute_query(self, query):
        print({'DEBUG DB': {'query': query}})
        with self._connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            self._connection.commit()
            return result

    def get_last_category_id(self):
        return self.execute_query("SELECT `id` FROM `category` WHERE `id`  = LAST_INSERT_ID()");

    # Create Category
    def create_category(self, category_name):
        query = "INSERT INTO `category` (`name`) VALUES('{}');".format(category_name)
        self.execute_query(query);

    # Delete Category
    def delete_category(self, category_id):
        query = "DELETE FROM `category` WHERE(`id` = '{}');".format(category_id)
        self.execute_query(query);

    # Get All Categories
    def get_categories(self):
        query = "SELECT `id`,`name` FROM category;"
        return self.execute_query(query);

    # Add a Product
    def add_product(self, prod_title, prod_desc, prod_price, prod_img_url, prod_category_id, prod_is_favorite):
        query = "INSERT INTO `product`(`title`, `desc`, `price`, `img_url`, `category_id`, `favorite`) VALUES('{}', '{}', '{}', '{}', '{}', {});".format(
            prod_title, prod_desc, prod_price, prod_img_url, prod_category_id, prod_is_favorite)
        self.execute_query(query)

    # Edit a Product
    def edit_product(self, prod_id, prod_title, prod_desc, prod_price, prod_img_url, prod_category_id,
                     prod_is_favorite):
        query = "UPDATE `product` SET `title` = '{}' , `desc` = '{}' , `price` = '{}' , `img_url` = '{}' , `category_id` = '{}' , `favorite` = '{}' WHERE(`id` = '{}');".format(
            prod_title, prod_desc, prod_price, prod_img_url, prod_category_id, prod_is_favorite, prod_id)
        self.execute_query(query)

    #  Get Product
    def get_product(self, product_id):
        query = "SELECT (`category_id`, `desc`, `price`, `title`, `favorite`, `img_url`, `id`) FROM product WHERE `id` = {};".format(
            product_id)
        return self.execute_query(query)

    # Delete Product
    def delete_product(self, product_id):
        query = "DELETE FROM `product` WHERE(`id` = '{}');".format(product_id)
        self.execute_query(query)

    # Get All Products
    def get_products(self):
        query = "SELECT * FROM product"
        return self.execute_query(query)

    # List Products by Category
    def get_products_by_category(self, category_id):
        query = "SELECT * FROM product where `category_id` = {}".format(category_id)
        return self.execute_query(query)
