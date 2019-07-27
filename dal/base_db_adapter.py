from abc import ABC, abstractmethod


class BaseDatabaseAdapter(ABC):
    # Create Category
    @abstractmethod
    def create_category(self, category_name):
        pass

    # Delete Category
    @abstractmethod
    def delete_category(self, category_id):
        pass

    # Get All Categories
    @abstractmethod
    def get_categories(self):
        pass

    # Add a Product
    @abstractmethod
    def add_product(self, prod_id, prod_title, prod_desc, prod_price, prod_img_url, prod_category_id, prod_is_favorite):
        pass

    # Edit a Product
    @abstractmethod
    def edit_product(self, prod_id, prod_title, prod_desc, prod_price, prod_img_url, prod_category_id,
                     prod_is_favorite):
        pass

    # Get Product
    @abstractmethod
    def get_product(self, prod_id):
        pass

    # Delete Product
    @abstractmethod
    def delete_product(self, prod_id):
        pass

    # Get All Products
    @abstractmethod
    def get_products(self):
        pass

    # List Products by Category
    @abstractmethod
    def get_product_by_category(self):
        pass
