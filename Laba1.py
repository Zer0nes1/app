import json
import xml.etree.ElementTree as ET

# -------------------- Основные классы --------------------

class Product:
    """Класс, представляющий товар."""
    next_id = 1

    def __init__(self, name, description, price, stock):
        self.id = f"product_{Product.next_id}"
        Product.next_id += 1
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

    def update_stock(self, quantity):
        """Обновляет количество товара на складе."""
        if quantity < 0 and abs(quantity) > self.stock:
            raise ValueError("Недостаточно товара на складе.")
        self.stock += quantity

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price}, stock={self.stock})"


class Category:
    """Класс, представляющий категорию товаров."""
    next_id = 1

    def __init__(self, name):
        self.id = f"category_{Category.next_id}"
        Category.next_id += 1
        self.name = name
        self.products = []

    def add_product(self, product):
        """Добавляет товар в категорию."""
        self.products.append(product)

    def remove_product(self, product_id):
        """Удаляет товар из категории по ID."""
        self.products = [product for product in self.products if product.id != product_id]

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, products={len(self.products)})"


class Admin:
    """Класс, представляющий администратора."""
    next_id = 1

    def __init__(self, username):
        self.id = f"admin_{Admin.next_id}"
        Admin.next_id += 1
        self.username = username

    def add_category(self, name, categories):
        """Создает новую категорию и добавляет ее в список категорий."""
        category = Category(name)
        categories.append(category)
        return category

    def remove_category(self, category_id, categories):
        """Удаляет категорию по ID."""
        categories = [category for category in categories if category.id != category_id]
        return categories

    def add_product(self, category, name, description, price, stock):
        """Добавляет новый товар в категорию."""
        product = Product(name, description, price, stock)
        category.add_product(product)
        return product

    def remove_product(self, category, product_id):
        """Удаляет товар по ID из категории."""
        category.remove_product(product_id)

    def __repr__(self):
        return f"Admin(id={self.id}, username={self.username})"


class Customer:
    """Класс, представляющий покупателя."""
    next_id = 1

    def __init__(self, name, email):
        self.id = f"customer_{Customer.next_id}"
        Customer.next_id += 1
        self.name = name
        self.email = email
        self.orders = []

    def place_order(self, order):
        """Добавляет заказ в список заказов покупателя."""
        self.orders.append(order)

    def __repr__(self):
        return f"Customer(id={self.id}, name={self.name}, email={self.email})"


class OrderItem:
    """Класс, представляющий элемент заказа."""
    def __init__(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным числом.")
        self.product = product
        self.quantity = quantity
        self.total_price = product.price * quantity

    def __repr__(self):
        return f"OrderItem(product={self.product.name}, quantity={self.quantity}, total_price={self.total_price})"


class Order:
    """Класс, представляющий заказ."""
    next_id = 1

    def __init__(self, customer):
        self.id = f"order_{Order.next_id}"
        Order.next_id += 1
        self.customer = customer
        self.items = []
        self.status = "Pending"

    def add_item(self, product, quantity):
        """Добавляет товар в заказ."""
        if product.stock < quantity:
            raise ValueError(f"Недостаточно товара {product.name} на складе.")
        product.update_stock(-quantity)
        self.items.append(OrderItem(product, quantity))

    def calculate_total(self):
        """Вычисляет общую сумму заказа."""
        return sum(item.total_price for item in self.items)

    def __repr__(self):
        return f"Order(id={self.id}, customer={self.customer.name}, total={self.calculate_total()}, status={self.status})"


class Feedback:
    """Класс для отзывов покупателей."""
    next_id = 1

    def __init__(self, customer, product, comment):
        self.id = f"feedback_{Feedback.next_id}"
        Feedback.next_id += 1
        self.customer = customer
        self.product = product
        self.comment = comment

    def __repr__(self):
        return f"Feedback(id={self.id}, customer={self.customer.name}, product={self.product.name}, comment={self.comment})"


class Wishlist:
    """Класс для списка желаемых товаров."""
    def __init__(self, customer):
        self.customer = customer
        self.products = []

    def add_product(self, product):
        """Добавляет товар в список желаемых товаров."""
        self.products.append(product)

    def remove_product(self, product_id):
        """Удаляет товар из списка желаемых товаров по ID."""
        self.products = [product for product in self.products if product.id != product_id]

    def __repr__(self):
        return f"Wishlist(customer={self.customer.name}, products={len(self.products)})"


class Coupon:
    """Класс для купонов на скидку."""
    def __init__(self, code, discount_percentage, active=True):
        self.code = code
        self.discount_percentage = discount_percentage
        self.active = active

    def apply_coupon(self, order):
        """Применяет купон к заказу."""
        if not self.active:
            raise ValueError("Купон неактивен.")
        discount = order.calculate_total() * (self.discount_percentage / 100)
        print(f"Скидка применена: {discount} руб.")
        return order.calculate_total() - discount

    def __repr__(self):
        return f"Coupon(code={self.code}, discount={self.discount_percentage}%)"


class Inventory:
    """Класс для управления инвентарем товаров."""
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        """Добавляет товар в инвентарь."""
        self.products[product.id] = product

    def get_product(self, product_id):
        """Получает товар по ID."""
        return self.products.get(product_id)

    def update_product(self, product_id, stock):
        """Обновляет количество товара по ID."""
        if product_id in self.products:
            self.products[product_id].update_stock(stock)
        else:
            print("Товар не найден.")

    def __repr__(self):
        return f"Inventory(products={len(self.products)})"


# -------------------- Функции для работы с файлами --------------------

def save_to_json(categories, customers, filename="store_data.json"):
    """Сохраняет данные в JSON-файл."""
    data = {
        "categories": [
            {
                "id": category.id,
                "name": category.name,
                "products": [
                    {
                        "id": product.id,
                        "name": product.name,
                        "description": product.description,
                        "price": product.price,
                        "stock": product.stock
                    }
                    for product in category.products
                ]
            }
            for category in categories
        ],
        "customers": [
            {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "orders": [
                    {
                        "id": order.id,
                        "items": [
                            {"product_id": item.product.id, "quantity": item.quantity}
                            for item in order.items
                        ],
                        "status": order.status,
                        "total_price": order.calculate_total()
                    }
                    for order in customer.orders
                ]
            }
            for customer in customers
        ]
    }
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_from_json():
    try:
        with open("store_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

            categories = []
            for category_data in data["categories"]:
                print(f"Загружаем категорию: {category_data['name']}")
                category = Category(category_data["name"])
                for product_data in category_data["products"]:
                    print(f"Добавляем продукт: {product_data['name']}")
                    product = Product(
                        product_data["name"],
                        product_data["description"],
                        product_data["price"],
                        product_data["stock"]
                    )
                    category.add_product(product)
                categories.append(category)

            customers = []
            for customer_data in data["customers"]:
                print(f"Загружаем клиента: {customer_data['name']}")
                customer = Customer(customer_data["name"], customer_data["email"])
                for order_data in customer_data["orders"]:
                    print(f"Добавляем заказ для клиента {customer_data['name']}")
                    order = Order(customer)
                    for item_data in order_data["items"]:
                        print(f"Добавляем товар в заказ: product_id={item_data['product_id']}, quantity={item_data['quantity']}")
                        product = categories[item_data["product_id"] - 1].products[item_data["product_id"] - 1]
                        order.add_item(product, item_data["quantity"])
                    customer.place_order(order)
                customers.append(customer)

            return categories, customers

    except Exception as e:
        print(f"Ошибка при загрузке JSON: {e}")
        return [], []

def save_to_xml(categories, customers, filename="store_data.xml"):
    """Сохраняет данные в XML-файл."""
    root = ET.Element("store")

    categories_el = ET.SubElement(root, "categories")
    for category in categories:
        category_el = ET.SubElement(categories_el, "category", id=category.id, name=category.name)
        for product in category.products:
            ET.SubElement(category_el, "product", id=product.id, name=product.name,
                          description=product.description, price=str(product.price), stock=str(product.stock))

    customers_el = ET.SubElement(root, "customers")
    for customer in customers:
        customer_el = ET.SubElement(customers_el, "customer", id=customer.id, name=customer.name,
                                    email=customer.email)
        for order in customer.orders:
            order_el = ET.SubElement(customer_el, "order", id=order.id, status=order.status,
                                     total_price=str(order.calculate_total()))
            for item in order.items:
                ET.SubElement(order_el, "item", product_id=item.product.id, quantity=str(item.quantity))

    tree = ET.ElementTree(root)
    tree.write(filename)


def load_from_xml():
    try:
        tree = ET.parse("store_data.xml")
        root = tree.getroot()

        categories = []
        for category_elem in root.findall("categories/category"):
            category_name = category_elem.get("name")
            print(f"Загружаем категорию: {category_name}")
            category = Category(category_name)
            for product_elem in category_elem.findall("product"):
                product_name = product_elem.get("name")
                print(f"Добавляем продукт: {product_name}")
                product = Product(
                    product_elem.get("name"),
                    product_elem.get("description"),
                    float(product_elem.get("price")),
                    int(product_elem.get("stock"))
                )
                category.add_product(product)
            categories.append(category)

        customers = []
        for customer_elem in root.findall("customers/customer"):
            customer_name = customer_elem.get("name")
            print(f"Загружаем клиента: {customer_name}")
            customer = Customer(customer_name, customer_elem.get("email"))
            for order_elem in customer_elem.findall("order"):
                print(f"Добавляем заказ для клиента {customer_name}")
                order = Order(customer)
                for item_elem in order_elem.findall("item"):
                    product_id = int(item_elem.get("product_id")) - 1
                    quantity = int(item_elem.get("quantity"))
                    print(f"Добавляем товар в заказ: product_id={product_id}, quantity={quantity}")
                    product = categories[product_id].products[product_id]
                    order.add_item(product, quantity)
                customer.place_order(order)
            customers.append(customer)

        return categories, customers

    except Exception as e:
        print(f"Ошибка при загрузке XML: {e}")
        return [], []

def show_menu():
    print("\nМеню:")
    print("1. Добавить категорию")
    print("2. Добавить товар в категорию")
    print("3. Создать заказ")
    print("4. Добавить товар в заказ")
    print("5. Показать заказы клиента")
    print("6. Сохранить данные в файл")
    print("7. Загрузить данные из файла")
    print("0. Выход")


if __name__ == "__main__":
    categories = []
    customers = [Customer("John Doe", "john@example.com")]
    admin = Admin("admin1")

    while True:
        show_menu()
        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Введите название категории: ")
            category = admin.add_category(name, categories)
            print(f"Добавлена категория: {category}")

        elif choice == "2":
            if not categories:
                print("Нет доступных категорий. Сначала добавьте категорию.")
                continue
            print("Категории:")
            for idx, category in enumerate(categories):
                print(f"{idx + 1}. {category.name}")
            cat_idx = int(input("Выберите категорию: ")) - 1
            category = categories[cat_idx]

            name = input("Название товара: ")
            description = input("Описание товара: ")
            price = float(input("Цена товара: "))
            stock = int(input("Количество на складе: "))
            product = admin.add_product(category, name, description, price, stock)
            print(f"Добавлен товар: {product}")

        elif choice == "3":
            print("Доступные клиенты:")
            for idx, customer in enumerate(customers):
                print(f"{idx + 1}. {customer.name} ({customer.email})")
            cust_idx = int(input("Выберите клиента: ")) - 1
            customer = customers[cust_idx]
            order = Order(customer)
            customer.place_order(order)
            print(f"Создан заказ: {order}")

        elif choice == "4":
            if not categories:
                print("Нет доступных категорий. Сначала добавьте категории и товары.")
                continue
            print("Категории:")
            for idx, category in enumerate(categories):
                print(f"{idx + 1}. {category.name}")
            cat_idx = int(input("Выберите категорию: ")) - 1
            category = categories[cat_idx]

            if not category.products:
                print("Нет доступных товаров в этой категории.")
                continue

            print("Товары:")
            for idx, product in enumerate(category.products):
                print(f"{idx + 1}. {product.name} (Цена: {product.price}, Остаток: {product.stock})")
            prod_idx = int(input("Выберите товар: ")) - 1
            product = category.products[prod_idx]

            quantity = int(input("Количество: "))
            try:
                customer = customers[0]  # Для примера используем первого клиента
                order = customer.orders[-1]  # Последний заказ
                order.add_item(product, quantity)
                print(f"Товар добавлен в заказ: {product.name}, Количество: {quantity}")
            except (ValueError, IndexError) as e:
                print(f"Ошибка: {e}")

        elif choice == "5":
            print("Доступные клиенты:")
            for idx, customer in enumerate(customers):
                print(f"{idx + 1}. {customer.name} ({customer.email})")
            cust_idx = int(input("Выберите клиента: ")) - 1
            customer = customers[cust_idx]

            if not customer.orders:
                print("У клиента нет заказов.")
            else:
                for order in customer.orders:
                    print(order)

        elif choice == "6":
            format_choice = input("Выберите формат (json/xml): ").strip().lower()
            if format_choice == "json":
                save_to_json(categories, customers)
                print("Данные сохранены в JSON-файл.")
            elif format_choice == "xml":
                save_to_xml(categories, customers)
                print("Данные сохранены в XML-файл.")
            else:
                print("Неверный формат.")

        elif choice == "7":
            format_choice = input("Выберите формат (json/xml): ").strip().lower()
            if format_choice == "json":
                data = load_from_json()
                print("Данные загружены из JSON-файла.")
            elif format_choice == "xml":
                data = load_from_xml()
                print("Данные загружены из XML-файла.")
            else:
                print("Неверный формат.")

        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")
