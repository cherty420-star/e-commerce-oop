import os
import pytest
from src.models import (Product, Smartphone, LawnGrass, Category,
                        Order, BaseProduct, ZeroQuantityError,
                        load_categories_from_json, CategoryIterator)


class TestZeroQuantity:
    """Тесты для обработки нулевого количества товаров."""

    def test_product_zero_quantity_initialization(self):
        """Тест создания товара с нулевым количеством."""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            Product("Товар", "Описание", 1000.0, 0)

    def test_smartphone_zero_quantity_initialization(self):
        """Тест создания смартфона с нулевым количеством."""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            Smartphone("Смартфон", "Описание", 50000.0, 0, 4.5, "Model", 128, "Black")

    def test_lawn_grass_zero_quantity_initialization(self):
        """Тест создания газонной травы с нулевым количеством."""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            LawnGrass("Трава", "Описание", 1500.0, 0, "Россия", 14, "Зеленый")

    def test_product_valid_quantity_initialization(self):
        """Тест создания товара с валидным количеством."""
        product = Product("Товар", "Описание", 1000.0, 5)
        assert product.quantity == 5

    def test_new_product_zero_quantity(self):
        """Тест создания товара через new_product с нулевым количеством."""
        product_data = {
            'name': 'Новый товар',
            'description': 'Описание',
            'price': 1000.0,
            'quantity': 0
        }

        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            Product.new_product(product_data)


class TestAveragePrice:
    """Тесты для метода calculate_average_price."""

    def test_average_price_empty_category(self):
        """Тест средней цены для пустой категории."""
        category = Category("Пустая категория", "Описание")
        assert category.calculate_average_price() == 0

    def test_average_price_single_product(self):
        """Тест средней цены для категории с одним товаром."""
        product = Product("Товар", "Описание", 1000.0, 5)
        category = Category("Категория", "Описание", [product])

        assert category.calculate_average_price() == 1000.0

    def test_average_price_multiple_products(self):
        """Тест средней цены для категории с несколькими товарами."""
        product1 = Product("Товар 1", "Описание", 1000.0, 5)
        product2 = Product("Товар 2", "Описание", 2000.0, 3)
        product3 = Product("Товар 3", "Описание", 3000.0, 7)

        category = Category("Категория", "Описание", [product1, product2, product3])

        expected_average = (1000.0 + 2000.0 + 3000.0) / 3
        assert category.calculate_average_price() == expected_average

    def test_average_price_with_different_prices(self):
        """Тест средней цены с разными ценами."""
        product1 = Product("Товар 1", "Описание", 500.0, 2)
        product2 = Product("Товар 2", "Описание", 1500.0, 4)

        category = Category("Категория", "Описание", [product1, product2])

        expected_average = (500.0 + 1500.0) / 2
        assert category.calculate_average_price() == expected_average


class TestZeroQuantityError:
    """Тесты для пользовательского исключения ZeroQuantityError."""

    def test_zero_quantity_error_in_category_add_product(self):
        """Тест ZeroQuantityError при добавлении товара в категорию."""
        category = Category("Категория", "Описание")

        # Создаем реальный продукт с нулевым количеством через обходной путь
        # Сначала создаем с положительным количеством, потом меняем на 0
        product = Product("Товар с нулем", "Описание", 1000.0, 1)
        product.quantity = 0  # Меняем количество на 0

        with pytest.raises(ZeroQuantityError,
                           match="Товар 'Товар с нулем' имеет нулевое количество и не может быть добавлен"):
            category.add_product(product)

    def test_zero_quantity_error_in_order(self):
        """Тест ZeroQuantityError при создании заказа с нулевым количеством."""
        product = Product("Товар", "Описание", 1000.0, 5)

        with pytest.raises(ZeroQuantityError, match="Нельзя создать заказ с нулевым количеством товара"):
            Order(product, 0)

    def test_category_add_product_finally_block(self, capsys):
        """Тест что finally блок выполняется всегда при добавлении товара."""
        category = Category("Категория", "Описание")
        product = Product("Товар", "Описание", 1000.0, 5)

        category.add_product(product)

        captured = capsys.readouterr()
        assert "Товар 'Товар' успешно добавлен в категорию 'Категория'" in captured.out
        assert "Обработка добавления товара 'Товар' завершена" in captured.out

    def test_category_add_product_zero_quantity_finally_block(self, capsys):
        """Тест что finally блок выполняется при ошибке нулевого количества."""
        category = Category("Категория", "Описание")
        product = Product("Товар с нулем", "Описание", 1000.0, 1)
        product.quantity = 0  # Меняем количество на 0

        try:
            category.add_product(product)
        except ZeroQuantityError:
            pass  # Ожидаемая ошибка

        captured = capsys.readouterr()
        assert "Обработка добавления товара 'Товар с нулем' завершена" in captured.out


class TestOrderZeroQuantity:
    """Тесты для заказов с нулевым количеством."""

    def test_order_zero_quantity(self):
        """Тест создания заказа с нулевым количеством."""
        product = Product("Товар", "Описание", 1000.0, 5)

        with pytest.raises(ZeroQuantityError):
            Order(product, 0)

    def test_order_negative_quantity(self):
        """Тест создания заказа с отрицательным количеством."""
        product = Product("Товар", "Описание", 1000.0, 5)

        with pytest.raises(ValueError, match="Количество товара должно быть положительным"):
            Order(product, -1)

    def test_order_valid_quantity(self):
        """Тест создания заказа с валидным количеством."""
        product = Product("Товар", "Описание", 1000.0, 5)

        order = Order(product, 2)
        assert order.quantity == 2
        assert order.total_price == 2000.0


class TestIntegration:
    """Интеграционные тесты."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_full_workflow_with_zero_quantity_handling(self):
        """Тест полного рабочего процесса с обработкой нулевого количества."""
        # Создаем валидные товары
        product1 = Product("Товар 1", "Описание", 1000.0, 5)
        product2 = Product("Товар 2", "Описание", 2000.0, 3)

        # Создаем категорию
        category = Category("Категория", "Описание")

        # Добавляем товары
        category.add_product(product1)
        category.add_product(product2)

        # Проверяем среднюю цену
        average_price = category.calculate_average_price()
        expected_average = (1000.0 + 2000.0) / 2
        assert average_price == expected_average

        # Создаем заказ
        order = Order(product1, 2)
        assert order.total_price == 2000.0

    def test_zero_quantity_workflow(self):
        """Тест workflow с нулевым количеством."""
        # Попытка создать товар с нулевым количеством
        with pytest.raises(ValueError):
            Product("Невалидный товар", "Описание", 1000.0, 0)

        # Создаем валидный товар
        valid_product = Product("Валидный товар", "Описание", 1000.0, 5)

        # Попытка создать заказ с нулевым количеством
        with pytest.raises(ZeroQuantityError):
            Order(valid_product, 0)

    def test_average_price_with_zero_quantity_products(self):
        """Тест средней цены когда пытаемся добавить товар с нулевым количеством."""
        # Создаем товары с положительным количеством
        product1 = Product("Товар 1", "Описание", 1000.0, 5)
        product2 = Product("Товар 2", "Описание", 2000.0, 3)

        # Создаем категорию и добавляем товары
        category = Category("Категория", "Описание")
        category.add_product(product1)
        category.add_product(product2)

        # Проверяем среднюю цену (только добавленных товаров)
        average_price = category.calculate_average_price()
        expected_average = (1000.0 + 2000.0) / 2
        assert average_price == expected_average

        # Тестируем случай, когда пытаемся добавить товар с нулевым количеством
        # Создаем товар с положительным количеством, потом меняем на 0
        product3 = Product("Товар 3", "Описание", 3000.0, 1)
        product3.quantity = 0  # Меняем количество на 0

        # Пытаемся добавить товар с нулевым количеством - должен вызвать исключение
        with pytest.raises(ZeroQuantityError):
            category.add_product(product3)

        # Убеждаемся, что товар с нулевым количеством не был добавлен
        assert len(category.get_products_list()) == 2
        # Средняя цена не должна измениться
        assert category.calculate_average_price() == expected_average


if __name__ == "__main__":
    pytest.main([__file__, "-v"])