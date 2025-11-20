import os
import pytest
from src.models import (Product, Smartphone, LawnGrass, Category,
                        Order, BaseProduct, BaseContainer,
                        load_categories_from_json, CategoryIterator)


class TestBaseProduct:
    """Тесты для абстрактного базового класса BaseProduct."""

    def test_base_product_is_abstract(self):
        """Тест что BaseProduct является абстрактным классом."""
        # Нельзя создать экземпляр абстрактного класса
        with pytest.raises(TypeError):
            BaseProduct("Товар", "Описание", 1000.0, 5)

    def test_product_inherits_from_base_product(self):
        """Тест что Product наследуется от BaseProduct."""
        product = Product("Товар", "Описание", 1000.0, 5)
        assert isinstance(product, BaseProduct)

    def test_smartphone_inherits_from_base_product(self):
        """Тест что Smartphone наследуется от BaseProduct."""
        smartphone = Smartphone("Смартфон", "Описание", 50000.0, 3, 4.5, "Model", 128, "Black")
        assert isinstance(smartphone, BaseProduct)

    def test_lawn_grass_inherits_from_base_product(self):
        """Тест что LawnGrass наследуется от BaseProduct."""
        lawn_grass = LawnGrass("Трава", "Описание", 1500.0, 10, "Россия", 14, "Зеленый")
        assert isinstance(lawn_grass, BaseProduct)


class TestLoggingMixin:
    """Тесты для миксина логирования."""

    def test_logging_mixin_in_product(self, capsys):
        """Тест что миксин логирования работает в Product."""
        product = Product("Тестовый товар", "Описание", 1000.0, 5)

        # Проверяем что сообщение было напечатано
        captured = capsys.readouterr()
        assert "Создан объект Product с параметрами:" in captured.out
        assert "Тестовый товар" in captured.out

    def test_logging_mixin_in_smartphone(self, capsys):
        """Тест что миксин логирования работает в Smartphone."""
        smartphone = Smartphone("Смартфон", "Описание", 50000.0, 3, 4.5, "Model", 128, "Black")

        captured = capsys.readouterr()
        assert "Создан объект Smartphone с параметрами:" in captured.out

    def test_logging_mixin_in_lawn_grass(self, capsys):
        """Тест что миксин логирования работает в LawnGrass."""
        lawn_grass = LawnGrass("Трава", "Описание", 1500.0, 10, "Россия", 14, "Зеленый")

        captured = capsys.readouterr()
        assert "Создан объект LawnGrass с параметрами:" in captured.out


class TestBaseContainer:
    """Тесты для абстрактного базового класса BaseContainer."""

    def test_base_container_is_abstract(self):
        """Тест что BaseContainer является абстрактным классом."""
        with pytest.raises(TypeError):
            BaseContainer()

    def test_category_inherits_from_base_container(self):
        """Тест что Category наследуется от BaseContainer."""
        category = Category("Категория", "Описание")
        assert isinstance(category, BaseContainer)

    def test_order_inherits_from_base_container(self):
        """Тест что Order наследуется от BaseContainer."""
        product = Product("Товар", "Описание", 1000.0, 5)
        order = Order(product, 2)
        assert isinstance(order, BaseContainer)

    def test_get_total_quantity(self):
        """Тест метода get_total_quantity в BaseContainer."""
        product1 = Product("Товар 1", "Описание", 1000.0, 5)
        product2 = Product("Товар 2", "Описание", 2000.0, 3)
        category = Category("Категория", "Описание", [product1, product2])

        total_quantity = category.get_total_quantity()
        assert total_quantity == 8  # 5 + 3


class TestOrder:
    """Тесты для класса Order."""

    def test_order_initialization(self):
        """Тест корректной инициализации заказа."""
        product = Product("Товар", "Описание", 1000.0, 5)
        order = Order(product, 2)

        assert order.product == product
        assert order.quantity == 2
        assert order.total_price == 2000.0  # 1000 * 2

    def test_order_invalid_product_type(self):
        """Тест ошибки при создании заказа с неправильным типом товара."""
        with pytest.raises(TypeError, match="Заказ может содержать только объекты класса Product"):
            Order("не товар", 2)

    def test_order_invalid_quantity_zero(self):
        """Тест ошибки при создании заказа с нулевым количеством."""
        product = Product("Товар", "Описание", 1000.0, 5)
        with pytest.raises(ValueError, match="Количество товара должно быть положительным"):
            Order(product, 0)

    def test_order_invalid_quantity_negative(self):
        """Тест ошибки при создании заказа с отрицательным количеством."""
        product = Product("Товар", "Описание", 1000.0, 5)
        with pytest.raises(ValueError, match="Количество товара должно быть положительным"):
            Order(product, -1)

    def test_order_insufficient_quantity(self):
        """Тест ошибки при создании заказа с недостаточным количеством."""
        product = Product("Товар", "Описание", 1000.0, 5)
        with pytest.raises(ValueError, match="Недостаточно товара на складе"):
            Order(product, 10)

    def test_order_string_representation(self):
        """Тест строкового представления заказа."""
        product = Product("Тестовый товар", "Описание", 1000.0, 5)
        order = Order(product, 2)

        expected = "Заказ: Тестовый товар, Количество: 2, Итоговая стоимость: 2000.0 руб."
        assert str(order) == expected

    def test_order_iteration(self):
        """Тест итерации по заказу."""
        product = Product("Товар", "Описание", 1000.0, 5)
        order = Order(product, 2)

        products = list(order)
        assert len(products) == 1
        assert products[0] == product


class TestProduct:
    """Тесты для класса Product."""

    def test_product_initialization(self):
        """Тест корректной инициализации товара."""
        product = Product("Тестовый товар", "Описание", 1000.0, 5)
        assert product.name == "Тестовый товар"
        assert product.description == "Описание"
        assert product.price == 1000.0
        assert product.quantity == 5

    # ... остальные существующие тесты Product ...


class TestIntegration:
    """Интеграционные тесты."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_full_workflow_with_new_classes(self):
        """Тест полного рабочего процесса с новыми классами."""
        # Создаем товары
        smartphone = Smartphone("Смартфон", "Описание", 50000.0, 3, 4.5, "Model", 128, "Black")

        # Создаем категорию
        category = Category("Электроника", "Техника", [smartphone])

        # Создаем заказ
        order = Order(smartphone, 1)

        # Проверяем наследование
        assert isinstance(smartphone, BaseProduct)
        assert isinstance(category, BaseContainer)
        assert isinstance(order, BaseContainer)

        # Проверяем общие методы
        assert category.get_total_quantity() == 3
        assert order.get_total_quantity() == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])