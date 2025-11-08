import os
import pytest
from src.models import Product, Category, load_categories_from_json


class TestProduct:
    """Тесты для класса Product."""

    def test_product_initialization(self):
        """Тест корректной инициализации товара."""
        product = Product("Тестовый товар", "Описание", 1000.0, 5)

        assert product.name == "Тестовый товар"
        assert product.description == "Описание"
        assert product.price == 1000.0  # Используем геттер
        assert product.quantity == 5

    def test_product_with_different_data(self):
        """Тест инициализации товара с разными данными."""
        product = Product("Другой товар", "Другое описание", 500.50, 10)

        assert product.name == "Другой товар"
        assert product.description == "Другое описание"
        assert product.price == 500.50
        assert product.quantity == 10

    def test_price_setter_positive(self):
        """Тест сеттера цены с положительным значением."""
        product = Product("Товар", "Описание", 1000.0, 5)
        product.price = 1500.0

        assert product.price == 1500.0

    def test_price_setter_negative(self):
        """Тест сеттера цены с отрицательным значением."""
        product = Product("Товар", "Описание", 1000.0, 5)
        original_price = product.price

        # Попытка установить отрицательную цену
        product.price = -500.0

        # Цена не должна измениться
        assert product.price == original_price

    def test_price_setter_zero(self):
        """Тест сеттера цены с нулевым значением."""
        product = Product("Товар", "Описание", 1000.0, 5)
        original_price = product.price

        # Попытка установить нулевую цену
        product.price = 0

        # Цена не должна измениться
        assert product.price == original_price

    def test_class_method_new_product(self):
        """Тест класс-метода new_product."""
        product_data = {
            'name': 'Новый товар',
            'description': 'Описание нового товара',
            'price': 2000.0,
            'quantity': 3
        }

        product = Product.new_product(product_data)

        assert product.name == 'Новый товар'
        assert product.description == 'Описание нового товара'
        assert product.price == 2000.0
        assert product.quantity == 3

    def test_class_method_new_product_duplicate(self):
        """Тест класс-метода new_product с дубликатом."""
        existing_product = Product("Существующий товар", "Описание", 1000.0, 5)
        products_list = [existing_product]

        duplicate_data = {
            'name': 'Существующий товар',
            'description': 'Новое описание',
            'price': 1500.0,  # Более высокая цена
            'quantity': 3
        }

        # Должен вернуть существующий товар с обновленными данными
        result = Product.new_product(duplicate_data, products_list)

        assert result is existing_product
        assert result.quantity == 8  # 5 + 3
        assert result.price == 1500.0  # Выбрана более высокая цена

    def test_string_representation(self):
        """Тест строкового представления товара."""
        product = Product("Тестовый товар", "Описание", 1000.0, 5)

        expected = "Тестовый товар, 1000.0 руб. Остаток: 5 шт."
        assert str(product) == expected


class TestCategory:
    """Тесты для класса Category."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_initialization(self):
        """Тест корректной инициализации категории."""
        product = Product("Товар", "Описание", 1000.0, 5)
        category = Category("Категория", "Описание категории", [product])

        assert category.name == "Категория"
        assert category.description == "Описание категории"
        assert len(category.get_products_list()) == 1
        assert category.get_products_list()[0].name == "Товар"

    def test_category_count(self):
        """Тест подсчета количества категорий."""
        # До создания категорий
        assert Category.category_count == 0

        # После создания одной категории
        product = Product("Товар", "Описание", 1000.0, 5)
        Category("Категория 1", "Описание", [product])
        assert Category.category_count == 1

        # После создания второй категории
        Category("Категория 2", "Описание", [product])
        assert Category.category_count == 2

    def test_product_count(self):
        """Тест подсчета количества товаров."""
        # До создания категорий
        assert Category.product_count == 0

        # Создаем категорию с одним товаром
        product1 = Product("Товар 1", "Описание", 1000.0, 5)
        Category("Категория 1", "Описание", [product1])
        assert Category.product_count == 1

        # Создаем категорию с двумя товарами
        product2 = Product("Товар 2", "Описание", 2000.0, 3)
        product3 = Product("Товар 3", "Описание", 3000.0, 7)
        Category("Категория 2", "Описание", [product2, product3])
        assert Category.product_count == 3  # 1 + 2 = 3

    def test_empty_category(self):
        """Тест создания категории без товаров."""
        category = Category("Пустая категория", "Описание", [])

        assert category.name == "Пустая категория"
        assert len(category.get_products_list()) == 0
        assert Category.category_count == 1
        assert Category.product_count == 0

    def test_add_product_method(self):
        """Тест метода add_product."""
        category = Category("Категория", "Описание")
        product = Product("Товар", "Описание", 1000.0, 5)

        # Изначально нет товаров
        assert len(category.get_products_list()) == 0
        initial_product_count = Category.product_count

        # Добавляем товар
        category.add_product(product)

        assert len(category.get_products_list()) == 1
        assert category.get_products_list()[0].name == "Товар"
        assert Category.product_count == initial_product_count + 1

    def test_products_getter(self):
        """Тест геттера products."""
        product1 = Product("Товар 1", "Описание 1", 1000.0, 5)
        product2 = Product("Товар 2", "Описание 2", 2000.0, 3)

        category = Category("Категория", "Описание", [product1, product2])

        products_string = category.products
        expected_lines = [
            "Товар 1, 1000.0 руб. Остаток: 5 шт.",
            "Товар 2, 2000.0 руб. Остаток: 3 шт."
        ]

        # Проверяем, что каждая строка присутствует
        for expected_line in expected_lines:
            assert expected_line in products_string

    def test_private_products_access(self):
        """Тест, что атрибут _products приватный."""
        category = Category("Категория", "Описание")

        # Проверяем, что доступ к _products возможен только через методы
        assert hasattr(category, '_products')

        # Прямой доступ должен работать (в Python приватность условна)
        # Но мы проверяем, что используем методы доступа
        assert isinstance(category._products, list)


class TestJSONLoading:
    """Тесты для загрузки данных из JSON."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_load_categories_from_json(self):
        """Тест загрузки категорий из JSON файла."""
        # Получаем правильный путь к файлу
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        json_path = os.path.join(project_root, "data", "products.json")

        print(f"Ищем файл по пути: {json_path}")
        print(f"Файл существует: {os.path.exists(json_path)}")

        categories = load_categories_from_json(json_path)

        assert len(categories) == 2
        assert categories[0].name == "Смартфоны"
        assert categories[1].name == "Телевизоры"

        # Проверяем товары в первой категории
        smartphones = categories[0]
        assert len(smartphones.get_products_list()) == 3
        assert smartphones.get_products_list()[0].name == "Samsung Galaxy C23 Ultra"
        assert smartphones.get_products_list()[0].price == 180000.0

        # Проверяем счетчики
        assert Category.category_count == 2
        assert Category.product_count == 4  # 3 смартфона + 1 телевизор

    def test_load_nonexistent_file(self):
        """Тест загрузки из несуществующего файла."""
        categories = load_categories_from_json("nonexistent.json")
        assert categories == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])