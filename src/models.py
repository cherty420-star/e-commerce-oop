import json
from typing import List


class Product:
    """
    Класс для представления товара.

    Attributes:
        name (str): Название товара
        description (str): Описание товара
        price (float): Цена товара
        quantity (int): Количество в наличии
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Инициализация товара.

        Args:
            name: Название товара
            description: Описание товара
            price: Цена товара
            quantity: Количество в наличии
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """
    Класс для представления категории товаров.

    Attributes:
        name (str): Название категории
        description (str): Описание категории
        products (List[Product]): Список товаров в категории

    Class Attributes:
        category_count (int): Общее количество категорий
        product_count (int): Общее количество товаров
    """

    # Атрибуты класса
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        """
        Инициализация категории.

        Args:
            name: Название категории
            description: Описание категории
            products: Список товаров в категории
        """
        self.name = name
        self.description = description
        self.products = products

        # Увеличиваем счетчик категорий
        Category.category_count += 1

        # Увеличиваем счетчик товаров на количество товаров в этой категории
        Category.product_count += len(products)


def load_categories_from_json(file_path: str) -> List[Category]:
    """
    Загружает категории и товары из JSON файла.

    Args:
        file_path: Путь к JSON файлу

    Returns:
        List[Category]: Список объектов Category
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        categories = []
        for category_data in data:
            products = []
            for product_data in category_data['products']:
                product = Product(
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    quantity=product_data['quantity']
                )
                products.append(product)

            category = Category(
                name=category_data['name'],
                description=category_data['description'],
                products=products
            )
            categories.append(category)

        return categories

    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON файла {file_path}")
        return []
    except KeyError as e:
        print(f"Отсутствует обязательное поле в JSON: {e}")
        return []
