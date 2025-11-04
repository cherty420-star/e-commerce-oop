import os
from src.models import Product, Category, load_categories_from_json


class TestProduct:
    """Тесты для класса Product."""

    def test_product_initialization(self):
        """Тест корректной инициализации товара."""
        product = Product("Тестовый товар", "Описание", 1000.0, 5)

        assert product.name == "Тестовый товар"
        assert product.description == "Описание"
        assert product.price == 1000.0
        assert product.quantity == 5

    def test_product_with_different_data(self):
        """Тест инициализации товара с разными данными."""
        product = Product("Другой товар", "Другое описание", 500.50, 10)

        assert product.name == "Другой товар"
        assert product.description == "Другое описание"
        assert product.price == 500.50
        assert product.quantity == 10


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
        assert len(category.products) == 1
        assert category.products[0].name == "Товар"

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
        assert len(category.products) == 0
        assert Category.category_count == 1
        assert Category.product_count == 0


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
        assert len(smartphones.products) == 3
        assert smartphones.products[0].name == "Samsung Galaxy C23 Ultra"
        assert smartphones.products[0].price == 180000.0

        # Проверяем счетчики
        assert Category.category_count == 2
        assert Category.product_count == 4  # 3 смартфона + 1 телевизор

    def test_load_nonexistent_file(self):
        """Тест загрузки из несуществующего файла."""
        categories = load_categories_from_json("nonexistent.json")
        assert categories == []
