import os
import pytest
from src.models import Product, Category, load_categories_from_json, CategoryIterator


class TestProduct:
    """Тесты для класса Product."""

    def test_product_initialization(self):
        """Тест корректной инициализации товара."""
        product = Product("Тестовый товар", "Описание", 1000.0, 5)

        assert product.name == "Тестовый товар"
        assert product.description == "Описание"
        assert product.price == 1000.0
        assert product.quantity == 5

    def test_product_string_representation(self):
        """Тест строкового представления товара."""
        product = Product("Тестовый товар", "Описание", 1000.0, 5)

        expected = "Тестовый товар, 1000.0 руб. Остаток: 5 шт."
        assert str(product) == expected

    def test_product_string_representation_different_data(self):
        """Тест строкового представления с разными данными."""
        product = Product("Другой товар", "Другое описание", 500.50, 10)

        expected = "Другой товар, 500.5 руб. Остаток: 10 шт."
        assert str(product) == expected

    def test_product_addition(self):
        """Тест магического метода сложения."""
        product1 = Product("Товар 1", "Описание", 1000.0, 5)  # 1000 * 5 = 5000
        product2 = Product("Товар 2", "Описание", 2000.0, 3)  # 2000 * 3 = 6000

        total = product1 + product2

        assert total == 11000.0  # 5000 + 6000
        assert isinstance(total, float)

    def test_product_addition_with_different_quantities(self):
        """Тест сложения товаров с разным количеством."""
        product1 = Product("Товар 1", "Описание", 500.0, 10)  # 500 * 10 = 5000
        product2 = Product("Товар 2", "Описание", 750.0, 4)  # 750 * 4 = 3000

        total = product1 + product2

        assert total == 8000.0  # 5000 + 3000

    def test_product_addition_type_error(self):
        """Тест ошибки типа при сложении."""
        product = Product("Товар", "Описание", 1000.0, 5)

        with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
            product + "не товар"

    def test_product_private_price(self):
        """Тест, что атрибут цены действительно приватный."""
        product = Product("Тестовый товар", "Описание", 1000.0, 5)

        assert hasattr(product, '_Product__price')
        assert product._Product__price == 1000.0

        with pytest.raises(AttributeError):
            _ = product.__price


class TestCategory:
    """Тесты для класса Category."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_string_representation(self):
        """Тест строкового представления категории."""
        product1 = Product("Товар 1", "Описание", 1000.0, 5)
        product2 = Product("Товар 2", "Описание", 2000.0, 3)
        category = Category("Категория", "Описание", [product1, product2])

        expected = "Категория, количество продуктов: 8 шт."  # 5 + 3
        assert str(category) == expected

    def test_category_string_representation_empty(self):
        """Тест строкового представления пустой категории."""
        category = Category("Пустая категория", "Описание", [])

        expected = "Пустая категория, количество продуктов: 0 шт."
        assert str(category) == expected

    def test_category_string_representation_single_product(self):
        """Тест строкового представления категории с одним товаром."""
        product = Product("Товар", "Описание", 1000.0, 7)
        category = Category("Категория", "Описание", [product])

        expected = "Категория, количество продуктов: 7 шт."
        assert str(category) == expected

    def test_category_iteration(self):
        """Тест итерации по категории."""
        product1 = Product("Товар 1", "Описание 1", 1000.0, 5)
        product2 = Product("Товар 2", "Описание 2", 2000.0, 3)
        category = Category("Категория", "Описание", [product1, product2])

        # Тестируем итерацию
        products_from_iteration = []
        for product in category:
            products_from_iteration.append(product)

        assert len(products_from_iteration) == 2
        assert products_from_iteration[0].name == "Товар 1"
        assert products_from_iteration[1].name == "Товар 2"

    def test_category_iteration_empty(self):
        """Тест итерации по пустой категории."""
        category = Category("Пустая категория", "Описание", [])

        products_from_iteration = list(category)
        assert len(products_from_iteration) == 0

    def test_optimized_products_getter(self):
        """Тест оптимизированного геттера products."""
        product1 = Product("Товар 1", "Описание 1", 1000.0, 5)
        product2 = Product("Товар 2", "Описание 2", 2000.0, 3)
        category = Category("Категория", "Описание", [product1, product2])

        products_string = category.products

        # Проверяем, что используется __str__ продукта
        expected_line1 = "Товар 1, 1000.0 руб. Остаток: 5 шт."
        expected_line2 = "Товар 2, 2000.0 руб. Остаток: 3 шт."

        assert expected_line1 in products_string
        assert expected_line2 in products_string


class TestCategoryIterator:
    """Тесты для класса CategoryIterator."""

    def test_iterator_initialization(self):
        """Тест инициализации итератора."""
        products = [
            Product("Товар 1", "Описание 1", 1000.0, 5),
            Product("Товар 2", "Описание 2", 2000.0, 3)
        ]
        iterator = CategoryIterator(products)

        assert iterator._products == products
        assert iterator._index == 0

    def test_iterator_iteration(self):
        """Тест полной итерации."""
        products = [
            Product("Товар 1", "Описание 1", 1000.0, 5),
            Product("Товар 2", "Описание 2", 2000.0, 3)
        ]
        iterator = CategoryIterator(products)

        # Первый вызов
        product1 = next(iterator)
        assert product1.name == "Товар 1"
        assert iterator._index == 1

        # Второй вызов
        product2 = next(iterator)
        assert product2.name == "Товар 2"
        assert iterator._index == 2

        # Конец итерации
        with pytest.raises(StopIteration):
            next(iterator)

    def test_iterator_for_loop(self):
        """Тест использования итератора в цикле for."""
        products = [
            Product("Товар 1", "Описание 1", 1000.0, 5),
            Product("Товар 2", "Описание 2", 2000.0, 3)
        ]
        iterator = CategoryIterator(products)

        product_names = []
        for product in iterator:
            product_names.append(product.name)

        assert product_names == ["Товар 1", "Товар 2"]

    def test_iterator_empty(self):
        """Тест итератора с пустым списком."""
        iterator = CategoryIterator([])

        with pytest.raises(StopIteration):
            next(iterator)


class TestIntegration:
    """Интеграционные тесты."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_full_workflow_with_magic_methods(self):
        """Тест полного рабочего процесса с магическими методами."""
        # Создаем товары
        product1 = Product("Товар 1", "Описание 1", 1000.0, 5)
        product2 = Product("Товар 2", "Описание 2", 2000.0, 3)

        # Создаем категорию
        category = Category("Категория", "Описание")

        # Добавляем товары
        category.add_product(product1)
        category.add_product(product2)

        # Проверяем строковое представление
        assert str(product1) == "Товар 1, 1000.0 руб. Остаток: 5 шт."
        assert str(category) == "Категория, количество продуктов: 8 шт."

        # Проверяем сложение
        total_value = product1 + product2
        assert total_value == (1000.0 * 5) + (2000.0 * 3)

        # Проверяем итерацию
        product_count = 0
        for product in category:
            product_count += 1
            assert isinstance(product, Product)
        assert product_count == 2


class TestJSONLoadingWithMagicMethods:
    """Тесты загрузки из JSON с магическими методами."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_json_loading_string_representation(self):
        """Тест строкового представления после загрузки из JSON."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        json_path = os.path.join(project_root, "data", "products.json")

        categories = load_categories_from_json(json_path)

        # Проверяем, что строковое представление работает
        for category in categories:
            category_str = str(category)
            assert category.name in category_str
            assert "количество продуктов:" in category_str

            # Проверяем товары
            for product in category:
                product_str = str(product)
                assert product.name in product_str
                assert "руб." in product_str
                assert "Остаток:" in product_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])