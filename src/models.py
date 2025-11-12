import json
from typing import List, Dict


class Product:
    """
    Класс для представления товара.

    Attributes:
        name (str): Название товара
        description (str): Описание товара
        __price (float): Цена товара (приватный атрибут)
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
        self.__price = price
        self.quantity = quantity

    @property
    def price(self):
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float):
        """
        Сеттер для цены с проверкой на положительное значение.

        Args:
            new_price: Новая цена товара
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            # Дополнительная логика с подтверждением пользователем
            if hasattr(self, '_Product__price') and new_price < self.__price:
                confirmation = input(
                    f"Цена понижается с {self.__price} до {new_price}. "
                    f"Подтвердите изменение (y/n): "
                )
                if confirmation.lower() != 'y':
                    print("Изменение цены отменено")
                    return

            self.__price = new_price

    def __str__(self):
        """Строковое представление товара."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Магический метод сложения товаров.

        Returns:
            float: Сумма произведений цены на количество для двух товаров
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        return (self.price * self.quantity) + (other.price * other.quantity)

    def __repr__(self):
        """Представление объекта для отладки."""
        return f"Product('{self.name}', '{self.description}', {self.price}, {self.quantity})"

    @classmethod
    def new_product(cls, product_data: Dict, products_list: List['Product'] = None):
        """
        Класс-метод для создания нового товара.

        Args:
            product_data: Данные товара в виде словаря
            products_list: Список существующих товаров для проверки дубликатов

        Returns:
            Product: Созданный объект товара
        """
        name = product_data['name']
        description = product_data['description']
        price = product_data['price']
        quantity = product_data['quantity']

        # Проверка на дубликаты
        if products_list:
            for existing_product in products_list:
                if existing_product.name.lower() == name.lower():
                    # Объединяем количество и выбираем максимальную цену
                    existing_product.quantity += quantity
                    if price > existing_product.price:
                        existing_product.price = price
                    return existing_product

        return cls(name, description, price, quantity)


class Category:
    """
    Класс для представления категории товаров.

    Attributes:
        name (str): Название категории
        description (str): Описание категории
        __products (List[Product]): Список товаров в категории (приватный)

    Class Attributes:
        category_count (int): Общее количество категорий
        product_count (int): Общее количество товаров
    """

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product] = None):
        """
        Инициализация категории.

        Args:
            name: Название категории
            description: Описание категории
            products: Список товаров в категории
        """
        self.name = name
        self.description = description
        self.__products = products if products is not None else []

        # Увеличиваем счетчик категорий
        Category.category_count += 1

        # Увеличиваем счетчик товаров на количество товаров в этой категории
        Category.product_count += len(self.__products)

    def __str__(self):
        """Строковое представление категории."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        """
        Магический метод для итерации по товарам категории.

        Returns:
            CategoryIterator: Итератор для товаров категории
        """
        return CategoryIterator(self.__products)

    def add_product(self, product: Product):
        """
        Добавляет товар в категорию.

        Args:
            product: Объект товара для добавления
        """
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """Геттер для списка товаров в формате строк."""
        products_str = ""
        for product in self.__products:
            products_str += f"{product}\n"  # Используем __str__ продукта
        return products_str.rstrip()

    def get_products_list(self):
        """Возвращает список объектов товаров (для внутреннего использования)."""
        return self.__products

    def __repr__(self):
        """Представление объекта для отладки."""
        return f"Category('{self.name}', '{self.description}', {len(self.__products)} products)"


class CategoryIterator:
    """
    Вспомогательный класс для итерации по товарам категории.
    """

    def __init__(self, products: List[Product]):
        """
        Инициализация итератора.

        Args:
            products: Список товаров для итерации
        """
        self._products = products
        self._index = 0

    def __iter__(self):
        """Возвращает сам итератор."""
        return self

    def __next__(self):
        """
        Возвращает следующий товар в итерации.

        Returns:
            Product: Следующий товар

        Raises:
            StopIteration: Когда товары закончились
        """
        if self._index < len(self._products):
            product = self._products[self._index]
            self._index += 1
            return product
        else:
            raise StopIteration


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
        all_products = []  # Для отслеживания всех товаров при создании

        # Первый проход: собираем все товары для проверки дубликатов
        for category_data in data:
            for product_data in category_data['products']:
                product = Product.new_product(product_data, all_products)
                if product not in all_products:
                    all_products.append(product)

        # Второй проход: создаем категории с товарами
        for category_data in data:
            category_products = []
            for product_data in category_data['products']:
                # Находим соответствующий товар в списке всех товаров
                for product in all_products:
                    if product.name == product_data['name']:
                        category_products.append(product)
                        break

            category = Category(
                name=category_data['name'],
                description=category_data['description'],
                products=category_products
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