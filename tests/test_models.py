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

    def test_product_private_price(self):
        """Тест, что атрибут цены действительно приватный."""
        product = Product("Тестовый товар", "Описание", 1000.0, 5)

        # Проверяем, что атрибут приватный (с именем _Product__price)
        assert hasattr(product, '_Product__price')
        assert product._Product__price == 1000.0

        # Проверяем, что прямой доступ к __price не работает
        with pytest.raises(AttributeError):
            _ = product.__price

    def test_price_getter(self):
        """Тест геттера для цены."""
        product = Product("Товар", "Описание", 1000.0, 5)

        # Проверяем, что геттер возвращает правильное значение
        assert product.price == 1000.0

        # Проверяем, что геттер работает через свойство
        assert isinstance(type(product).price, property)

    def test_price_setter_positive(self):
        """Тест сеттера цены с положительным значением."""
        product = Product("Товар", "Описание", 1000.0, 5)
        product.price = 1500.0

        assert product.price == 1500.0
        assert product._Product__price == 1500.0  # Проверяем приватный атрибут

    def test_price_setter_negative(self):
        """Тест сеттера цены с отрицательным значением."""
        product = Product("Товар", "Описание", 1000.0, 5)
        original_price = product.price

        # Попытка установить отрицательную цену
        product.price = -500.0

        # Цена не должна измениться
        assert product.price == original_price
        assert product._Product__price == original_price

    def test_price_setter_zero(self):
        """Тест сеттера цены с нулевым значением."""
        product = Product("Товар", "Описание", 1000.0, 5)
        original_price = product.price

        # Попытка установить нулевую цену
        product.price = 0

        # Цена не должна измениться
        assert product.price == original_price
        assert product._Product__price == original_price

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

    def test_category_private_products(self):
        """Тест, что атрибут products действительно приватный."""
        product = Product("Товар", "Описание", 1000.0, 5)
        category = Category("Категория", "Описание", [product])

        # Проверяем, что атрибут приватный (с именем _Category__products)
        assert hasattr(category, '_Category__products')
        assert len(category._Category__products) == 1

        # Проверяем, что прямой доступ к __products не работает
        with pytest.raises(AttributeError):
            _ = category.__products

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

        # Проверяем форматирование вывода
        expected_line1 = "Товар 1, 1000.0 руб. Остаток: 5 шт."
        expected_line2 = "Товар 2, 2000.0 руб. Остаток: 3 шт."

        assert expected_line1 in products_string
        assert expected_line2 in products_string

        # Проверяем, что геттер возвращает строку
        assert isinstance(products_string, str)

    def test_products_getter_format(self):
        """Тест формата вывода геттера products."""
        product = Product("Тестовый товар", "Описание", 1234.56, 7)
        category = Category("Категория", "Описание", [product])

        products_string = category.products
        expected = "Тестовый товар, 1234.56 руб. Остаток: 7 шт."

        assert products_string == expected

    def test_products_getter_empty(self):
        """Тест геттера products для пустой категории."""
        category = Category("Пустая категория", "Описание", [])

        products_string = category.products
        assert products_string == ""

    def test_get_products_list_method(self):
        """Тест метода get_products_list."""
        product1 = Product("Товар 1", "Описание 1", 1000.0, 5)
        product2 = Product("Товар 2", "Описание 2", 2000.0, 3)

        category = Category("Категория", "Описание", [product1, product2])

        products_list = category.get_products_list()

        # Проверяем, что возвращается список объектов Product
        assert isinstance(products_list, list)
        assert len(products_list) == 2
        assert all(isinstance(product, Product) for product in products_list)
        assert products_list[0].name == "Товар 1"
        assert products_list[1].name == "Товар 2"


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

    def test_json_loading_private_attributes(self):
        """Тест, что после загрузки из JSON атрибуты остаются приватными."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        json_path = os.path.join(project_root, "data", "products.json")

        categories = load_categories_from_json(json_path)

        # Проверяем, что у всех категорий атрибут products приватный
        for category in categories:
            assert hasattr(category, '_Category__products')
            with pytest.raises(AttributeError):
                _ = category.__products

        # Проверяем, что у всех товаров атрибут price приватный
        for category in categories:
            for product in category.get_products_list():
                assert hasattr(product, '_Product__price')
                with pytest.raises(AttributeError):
                    _ = product.__price


class TestIntegration:
    """Интеграционные тесты."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_full_workflow(self):
        """Тест полного рабочего процесса."""
        # Создаем товары
        product1 = Product("Товар 1", "Описание 1", 1000.0, 5)
        product2 = Product("Товар 2", "Описание 2", 2000.0, 3)

        # Создаем категорию
        category = Category("Категория", "Описание")

        # Добавляем товары через метод
        category.add_product(product1)
        category.add_product(product2)

        # Проверяем состояние
        assert len(category.get_products_list()) == 2
        assert Category.category_count == 1
        assert Category.product_count == 2

        # Проверяем геттер
        products_str = category.products
        assert "Товар 1, 1000.0 руб. Остаток: 5 шт." in products_str
        assert "Товар 2, 2000.0 руб. Остаток: 3 шт." in products_str

        # Проверяем приватность атрибутов
        assert hasattr(category, '_Category__products')
        assert hasattr(product1, '_Product__price')
        assert hasattr(product2, '_Product__price')

    def test_price_validation_workflow(self):
        """Тест workflow с валидацией цены."""
        product = Product("Товар", "Описание", 1000.0, 5)

        # Успешное изменение цены
        product.price = 1500.0
        assert product.price == 1500.0

        # Неуспешное изменение (отрицательная цена)
        product.price = -500.0
        assert product.price == 1500.0  # Цена не изменилась

        # Неуспешное изменение (нулевая цена)
        product.price = 0
        assert product.price == 1500.0  # Цена не изменилась


if __name__ == "__main__":
    pytest.main([__file__, "-v"])