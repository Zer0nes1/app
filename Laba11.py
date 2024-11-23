import json
from xml.etree import ElementTree as ET

# 1. Продукт
class Product:
    def __init__(self, id, name, description, price, category):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category = category

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category.to_json()
        }

    def from_json(js):
        id = js['id']
        name = js['name']
        description = js['description']
        price = js['price']
        category = Category.from_json(js['category'])
        return Product(id, name, description, price, category)

    def to_xml(self):
        product_elem = ET.Element("Product")
        ET.SubElement(product_elem, "Id").text = str(self.id)
        ET.SubElement(product_elem, "Name").text = self.name
        ET.SubElement(product_elem, "Description").text = self.description
        ET.SubElement(product_elem, "Price").text = str(self.price)
        product_elem.append(self.category.to_xml())
        return product_elem

    def from_xml(elem):
        id = int(elem.find("Id").text)
        name = elem.find("Name").text
        description = elem.find("Description").text
        price = float(elem.find("Price").text)
        category_elem = elem.find("Category")
        category = Category.from_xml(category_elem)
        return Product(id, name, description, price, category)

# 2. Категория
class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def from_json(js):
        return Category(js['id'], js['name'])

    def to_xml(self):
        category_elem = ET.Element("Category")
        ET.SubElement(category_elem, "Id").text = str(self.id)
        ET.SubElement(category_elem, "Name").text = self.name
        return category_elem

    def from_xml(elem):
        id = int(elem.find("Id").text)
        name = elem.find("Name").text
        return Category(id, name)

# 3. Администратор
class Admin:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

    def from_json(js):
        return Admin(js['id'], js['username'], js['email'])

    def to_xml(self):
        admin_elem = ET.Element("Admin")
        ET.SubElement(admin_elem, "Id").text = str(self.id)
        ET.SubElement(admin_elem, "Username").text = self.username
        ET.SubElement(admin_elem, "Email").text = self.email
        return admin_elem

    def from_xml(elem):
        id = int(elem.find("Id").text)
        username = elem.find("Username").text
        email = elem.find("Email").text
        return Admin(id, username, email)

# 4. Клиент
class Customer:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    def from_json(js):
        return Customer(js['id'], js['name'], js['email'])

    def to_xml(self):
        customer_elem = ET.Element("Customer")
        ET.SubElement(customer_elem, "Id").text = str(self.id)
        ET.SubElement(customer_elem, "Name").text = self.name
        ET.SubElement(customer_elem, "Email").text = self.email
        return customer_elem

    def from_xml(elem):
        id = int(elem.find("Id").text)
        name = elem.find("Name").text
        email = elem.find("Email").text
        return Customer(id, name, email)

# 5. Позиция заказа
class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def to_json(self):
        return {
            'product': self.product.to_json(),
            'quantity': self.quantity
        }

    def from_json(js):
        product = Product.from_json(js['product'])
        quantity = js['quantity']
        return OrderItem(product, quantity)

    def to_xml(self):
        order_item_elem = ET.Element("OrderItem")
        order_item_elem.append(self.product.to_xml())
        ET.SubElement(order_item_elem, "Quantity").text = str(self.quantity)
        return order_item_elem

    def from_xml(elem):
        product_elem = elem.find("Product")
        product = Product.from_xml(product_elem)
        quantity = int(elem.find("Quantity").text)
        return OrderItem(product, quantity)

# 6. Заказ
class Order:
    def __init__(self, id, customer, items, total_price, status):
        self.id = id
        self.customer = customer
        self.items = items
        self.total_price = total_price
        self.status = status

    def to_json(self):
        return {
            'id': self.id,
            'customer': self.customer.to_json(),
            'items': [item.to_json() for item in self.items],
            'total_price': self.total_price,
            'status': self.status
        }

    def from_json(js):
        id = js['id']
        customer = Customer.from_json(js['customer'])
        items = [OrderItem.from_json(item) for item in js['items']]
        total_price = js['total_price']
        status = js['status']
        return Order(id, customer, items, total_price, status)

    def to_xml(self):
        order_elem = ET.Element("Order")
        ET.SubElement(order_elem, "Id").text = str(self.id)
        order_elem.append(self.customer.to_xml())
        items_elem = ET.SubElement(order_elem, "Items")
        for item in self.items:
            items_elem.append(item.to_xml())
        ET.SubElement(order_elem, "TotalPrice").text = str(self.total_price)
        ET.SubElement(order_elem, "Status").text = self.status
        return order_elem

    def from_xml(elem):
        id = int(elem.find("Id").text)
        customer_elem = elem.find("Customer")
        customer = Customer.from_xml(customer_elem)
        items_elem = elem.find("Items")
        items = [OrderItem.from_xml(item_elem) for item_elem in items_elem]
        total_price = float(elem.find("TotalPrice").text)
        status = elem.find("Status").text
        return Order(id, customer, items, total_price, status)

# 7. Отзывы
class Feedback:
    def __init__(self, customer, product, rating, comment):
        self.customer = customer
        self.product = product
        self.rating = rating
        self.comment = comment

    def to_json(self):
        return {
            'customer': self.customer.to_json(),
            'product': self.product.to_json(),
            'rating': self.rating,
            'comment': self.comment
        }

    def from_json(js):
        customer = Customer.from_json(js['customer'])
        product = Product.from_json(js['product'])
        rating = js['rating']
        comment = js['comment']
        return Feedback(customer, product, rating, comment)

    def to_xml(self):
        feedback_elem = ET.Element("Feedback")
        feedback_elem.append(self.customer.to_xml())
        feedback_elem.append(self.product.to_xml())
        ET.SubElement(feedback_elem, "Rating").text = str(self.rating)
        ET.SubElement(feedback_elem, "Comment").text = self.comment
        return feedback_elem

    def from_xml(elem):
        customer_elem = elem.find("Customer")
        customer = Customer.from_xml(customer_elem)
        product_elem = elem.find("Product")
        product = Product.from_xml(product_elem)
        rating = int(elem.find("Rating").text)
        comment = elem.find("Comment").text
        return Feedback(customer, product, rating, comment)

# 8. Купоны
class Coupon:
    def __init__(self, code, discount):
        self.code = code
        self.discount = discount

    def to_json(self):
        return {
            'code': self.code,
            'discount': self.discount
        }

    def from_json(js):
        return Coupon(js['code'], js['discount'])

    def to_xml(self):
        coupon_elem = ET.Element("Coupon")
        ET.SubElement(coupon_elem, "Code").text = self.code
        ET.SubElement(coupon_elem, "Discount").text = str(self.discount)
        return coupon_elem

    def from_xml(elem):
        code = elem.find("Code").text
        discount = float(elem.find("Discount").text)
        return Coupon(code, discount)

# 9. Список желаемого
class Wishlist:
    def __init__(self, id, customer, products):
        self.id = id
        self.customer = customer
        self.products = products

    def to_json(self):
        return {
            'id': self.id,
            'customer': self.customer.to_json(),
            'products': [product.to_json() for product in self.products]
        }

    def from_json(js):
        id = js['id']
        customer = Customer.from_json(js['customer'])
        products = [Product.from_json(product) for product in js['products']]
        return Wishlist(id, customer, products)

    def to_xml(self):
        wishlist_elem = ET.Element("Wishlist")
        ET.SubElement(wishlist_elem, "Id").text = str(self.id)
        wishlist_elem.append(self.customer.to_xml())
        products_elem = ET.SubElement(wishlist_elem, "Products")
        for product in self.products:
            products_elem.append(product.to_xml())
        return wishlist_elem

    def from_xml(elem):
        id = int(elem.find("Id").text)
        customer_elem = elem.find("Customer")
        customer = Customer.from_xml(customer_elem)
        products_elem = elem.find("Products")
        products = [Product.from_xml(product_elem) for product_elem in products_elem]
        return Wishlist(id, customer, products)

# 10. Инвентарь
class Inventory:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def to_json(self):
        return {
            'product': self.product.to_json(),
            'quantity': self.quantity
        }

    def from_json(js):
        product = Product.from_json(js['product'])
        quantity = js['quantity']
        return Inventory(product, quantity)

    def to_xml(self):
        inventory_elem = ET.Element("Inventory")
        inventory_elem.append(self.product.to_xml())
        ET.SubElement(inventory_elem, "Quantity").text = str(self.quantity)
        return inventory_elem

    def from_xml(elem):
        product_elem = elem.find("Product")
        product = Product.from_xml(product_elem)
        quantity = int(elem.find("Quantity").text)
        return Inventory(product, quantity)

        # CRUD-функции для JSON
def create_object_json(filename, obj):
    """Добавить объект в JSON файл"""
    try:
        data = load_from_json(filename)
    except FileNotFoundError:
        data = []
    data.append(obj)
    save_to_json(filename, data)

def read_objects_json(filename):
    """Прочитать все объекты из JSON файла"""
    try:
        return load_from_json(filename)
    except FileNotFoundError:
        return []

def update_object_json(filename, obj_id, updated_obj):
    """Обновить объект по ID в JSON файле"""
    data = read_objects_json(filename)
    for i, obj in enumerate(data):
        if obj.id == obj_id:
            data[i] = updated_obj
            save_to_json(filename, data)
            return True
    return False

def delete_object_json(filename, obj_id):
    """Удалить объект по ID из JSON файла"""
    data = read_objects_json(filename)
    data = [obj for obj in data if obj.id != obj_id]
    save_to_json(filename, data)

# CRUD-функции для XML
def create_object_xml(filename, obj):
    """Добавить объект в XML файл"""
    try:
        root = load_from_xml(filename)
    except FileNotFoundError:
        root = []
    root.append(obj)
    save_to_xml(filename, root)

def read_objects_xml(filename):
    """Прочитать все объекты из XML файла"""
    try:
        return load_from_xml(filename)
    except FileNotFoundError:
        return []

def update_object_xml(filename, obj_id, updated_obj):
    """Обновить объект по ID в XML файле"""
    objects = read_objects_xml(filename)
    for i, obj in enumerate(objects):
        if obj.id == obj_id:
            objects[i] = updated_obj
            save_to_xml(filename, objects)
            return True
    return False

def delete_object_xml(filename, obj_id):
    """Удалить объект по ID из XML файла"""
    objects = read_objects_xml(filename)
    objects = [obj for obj in objects if obj.id != obj_id]
    save_to_xml(filename, objects)
    
    # CRUD-функции 
def create_object_json(filename, obj):
    """Добавить объект в JSON файл"""
    try:
        data = load_from_json(filename)
    except FileNotFoundError:
        data = []
    data.append(obj)
    save_to_json(filename, data)

def read_objects_json(filename):
    """Прочитать все объекты из JSON файла"""
    try:
        return load_from_json(filename)
    except FileNotFoundError:
        return []

def update_object_json(filename, obj_id, updated_obj):
    """Обновить объект по ID в JSON файле"""
    data = read_objects_json(filename)
    for i, obj in enumerate(data):
        if obj.id == obj_id:
            data[i] = updated_obj
            save_to_json(filename, data)
            return True
    return False

def delete_object_json(filename, obj_id):
    """Удалить объект по ID из JSON файла"""
    data = read_objects_json(filename)
    data = [obj for obj in data if obj.id != obj_id]
    save_to_json(filename, data)


    # Пример объектов
category = Category(1, "Electronics")
product = Product(1, "Laptop", "A powerful laptop", 1000.0, category)
customer = Customer(1, "John Doe", "john@example.com")
order_item = OrderItem(product, 2)
order = Order(1, customer, [order_item], 2000.0, "Pending")

# Функции для работы с JSON файлами

def load_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return [Order.from_json(item) if 'status' in item else Feedback.from_json(item) for item in data]


def load_from_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return [Order.from_xml(elem) for elem in root]

# Функции для сохранения объектов
def save_to_json(filename, objects):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump([obj.to_json() for obj in objects], file, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении в {filename}: {e}")

def save_to_xml(filename, objects):
    root_elem = ET.Element("Root")
    for obj in objects:
        root_elem.append(obj.to_xml())
    tree = ET.ElementTree(root_elem)
    tree.write(filename, encoding="utf-8", xml_declaration=True)

# Сохранение данных
save_to_json("orders.json", [order])
save_to_xml("orders.xml", [order])

# Пример загрузки из JSON
loaded_orders = load_from_json("orders.json")
for order in loaded_orders:
    print(order.id, order.customer.name)

# Пример загрузки из XML
loaded_orders = load_from_xml("orders.xml")
for order in loaded_orders:
    print(order.id, order.customer.name)

