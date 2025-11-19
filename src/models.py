import json
from typing import List, Dict


class Product:
    """
    Базовый класс для представления товара.

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
        if type(self) != type(other):
            raise TypeError("Можно складывать только товары одного типа")

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
                    existing_product.quantity += quantity
                    if price > existing_product.price:
                        existing_product.price = price
                    return existing_product

        return cls(name, description, price, quantity)


class Smartphone(Product):
    """
    Класс для представления смартфона.

    Attributes:
        efficiency (float): Производительность
        model (str): Модель смартфона
        memory (int): Объем встроенной памяти (ГБ)
        color (str): Цвет
    """

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str):
        """
        Инициализация смартфона.

        Args:
            name: Название товара
            description: Описание товара
            price: Цена товара
            quantity: Количество в наличии
            efficiency: Производительность
            model: Модель смартфона
            memory: Объем встроенной памяти (ГБ)
            color: Цвет
        """
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __repr__(self):
        """Представление объекта для отладки."""
        return (f"Smartphone('{self.name}', '{self.description}', {self.price}, "
                f"{self.quantity}, {self.efficiency}, '{self.model}', {self.memory}, '{self.color}')")


class LawnGrass(Product):
    """
    Класс для представления газонной травы.

    Attributes:
        country (str): Страна-производитель
        germination_period (int): Срок прорастания (дни)
        color (str): Цвет
    """

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: int, color: str):
        """
        Инициализация газонной травы.

        Args:
            name: Название товара
            description: Описание товара
            price: Цена товара
            quantity: Количество в наличии
            country: Страна-производитель
            germination_period: Срок прорастания (дни)
            color: Цвет
        """
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __repr__(self):
        """Представление объекта для отладки."""
        return (f"LawnGrass('{self.name}', '{self.description}', {self.price}, "
                f"{self.quantity}, '{self.country}', {self.germination_period}, '{self.color}')")


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

        Raises:
            TypeError: Если переданный объект не является продуктом или его наследником
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """Геттер для списка товаров в формате строк."""
        products_str = ""
        for product in self.__products:
            products_str += f"{product}\n"
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
        all_products = []

        for category_data in data:
            for product_data in category_data['products']:
                product = Product.new_product(product_data, all_products)
                if product not in all_products:
                    all_products.append(product)

        for category_data in data:
            category_products = []
            for product_data in category_data['products']:
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