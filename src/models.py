import json
from typing import List, Dict
from abc import ABC, abstractmethod


class LoggingMixin:
    """
    Миксин для логирования создания объектов.
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализация с логированием параметров создания объекта.
        """
        super().__init__(*args, **kwargs)
        class_name = self.__class__.__name__
        print(f"Создан объект {class_name} с параметрами: {args}, {kwargs}")


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для товаров.

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
        self._price = price
        self.quantity = quantity

    @property
    @abstractmethod
    def price(self):
        """Абстрактный геттер для цены."""
        pass

    @price.setter
    @abstractmethod
    def price(self, value):
        """Абстрактный сеттер для цены."""
        pass

    @abstractmethod
    def __str__(self):
        """Абстрактный метод строкового представления."""
        pass

    @abstractmethod
    def __add__(self, other):
        """Абстрактный метод сложения товаров."""
        pass

    @classmethod
    @abstractmethod
    def new_product(cls, product_data: Dict, products_list: List['BaseProduct'] = None):
        """Абстрактный класс-метод для создания нового товара."""
        pass


class Product(LoggingMixin, BaseProduct):
    """
    Базовый класс для представления товара.

    Attributes:
        name (str): Название товара
        description (str): Описание товара
        _price (float): Цена товара (защищенный атрибут)
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
        super().__init__(name, description, price, quantity)

    @property
    def price(self):
        """Геттер для цены."""
        return self._price

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
            if hasattr(self, '_price') and new_price < self._price:
                confirmation = input(
                    f"Цена понижается с {self._price} до {new_price}. "
                    f"Подтвердите изменение (y/n): "
                )
                if confirmation.lower() != 'y':
                    print("Изменение цены отменено")
                    return

            self._price = new_price

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


class BaseContainer(ABC):
    """
    Абстрактный базовый класс для контейнеров с товарами.

    Attributes:
        items (List): Список элементов в контейнере
    """

    def __init__(self, items: List = None):
        """
        Инициализация контейнера.

        Args:
            items: Список элементов
        """
        self.items = items if items is not None else []

    @abstractmethod
    def __str__(self):
        """Абстрактный метод строкового представления."""
        pass

    @abstractmethod
    def __iter__(self):
        """Абстрактный метод для итерации по элементам."""
        pass

    def get_total_quantity(self) -> int:
        """
        Возвращает общее количество товаров в контейнере.

        Returns:
            int: Общее количество
        """
        return sum(item.quantity for item in self.items if hasattr(item, 'quantity'))


class Category(BaseContainer):
    """
    Класс для представления категории товаров.

    Attributes:
        name (str): Название категории
        description (str): Описание категории
        items (List[Product]): Список товаров в категории

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
        super().__init__(products)
        self.name = name
        self.description = description

        # Увеличиваем счетчик категорий
        Category.category_count += 1

        # Увеличиваем счетчик товаров на количество товаров в этой категории
        Category.product_count += len(self.items)

    def __str__(self):
        """Строковое представление категории."""
        total_quantity = self.get_total_quantity()
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        """
        Магический метод для итерации по товарам категории.

        Returns:
            CategoryIterator: Итератор для товаров категории
        """
        return CategoryIterator(self.items)

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

        self.items.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """Геттер для списка товаров в формате строк."""
        products_str = ""
        for product in self.items:
            products_str += f"{product}\n"
        return products_str.rstrip()

    def get_products_list(self):
        """Возвращает список объектов товаров (для внутреннего использования)."""
        return self.items

    def __repr__(self):
        """Представление объекта для отладки."""
        return f"Category('{self.name}', '{self.description}', {len(self.items)} products)"


class Order(BaseContainer):
    """
    Класс для представления заказа.

    Attributes:
        product (Product): Товар в заказе
        quantity (int): Количество товара
        total_price (float): Итоговая стоимость
    """

    def __init__(self, product: Product, quantity: int):
        """
        Инициализация заказа.

        Args:
            product: Товар в заказе
            quantity: Количество товара
        """
        if not isinstance(product, Product):
            raise TypeError("Заказ может содержать только объекты класса Product")

        if quantity <= 0:
            raise ValueError("Количество товара должно быть положительным")

        if quantity > product.quantity:
            raise ValueError("Недостаточно товара на складе")

        self.product = product
        self.quantity = quantity
        self.total_price = product.price * quantity
        self.items = [product]  # Для совместимости с BaseContainer

    def __str__(self):
        """Строковое представление заказа."""
        return (f"Заказ: {self.product.name}, "
                f"Количество: {self.quantity}, "
                f"Итоговая стоимость: {self.total_price} руб.")

    def __iter__(self):
        """
        Магический метод для итерации по товарам в заказе.

        Returns:
            CategoryIterator: Итератор для товаров в заказе
        """
        return CategoryIterator(self.items)

    def get_total_quantity(self) -> int:
        """
        Возвращает общее количество товаров в заказе.

        Returns:
            int: Общее количество товара в заказе
        """
        return self.quantity

    def __repr__(self):
        """Представление объекта для отладки."""
        return f"Order({self.product!r}, {self.quantity})"


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