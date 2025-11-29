import pytest
from src.models import Product, Category, Order, ZeroQuantityError



class TestEdgeCases:
    """Тесты для крайних случаев."""

    def test_product_new_product_with_duplicate(self):
        """Тест new_product с дубликатом товара."""
        product_data1 = {
            'name': 'Товар',
            'description': 'Описание',
            'price': 1000.0,
            'quantity': 5
        }

        product_data2 = {
            'name': 'Товар',  # То же имя
            'description': 'Другое описание',
            'price': 1500.0,  # Более высокая цена
            'quantity': 3
        }

        # Создаем первый товар
        product1 = Product.new_product(product_data1)

        # Создаем второй товар (должен объединиться с первым)
        product2 = Product.new_product(product_data2, [product1])

        # Должен вернуть тот же объект
        assert product2 is product1
        # Количество должно суммироваться
        assert product1.quantity == 8  # 5 + 3
        # Цена должна быть максимальной
        assert product1.price == 1500.0

    def test_category_counters(self):
        """Тест счетчиков категорий и товаров."""
        initial_categories = Category.category_count
        initial_products = Category.product_count

        product1 = Product("Товар 1", "Описание", 1000.0, 5)
        product2 = Product("Товар 2", "Описание", 2000.0, 3)

        category = Category("Категория", "Описание", [product1, product2])

        # Проверяем счетчики
        assert Category.category_count == initial_categories + 1
        assert Category.product_count == initial_products + 2

    def test_empty_category_average_price(self):
        """Тест средней цены для пустой категории."""
        category = Category("Пустая категория", "Описание")
        assert category.calculate_average_price() == 0

    def test_single_product_average_price(self):
        """Тест средней цены для категории с одним товаром."""
        product = Product("Товар", "Описание", 1234.56, 5)
        category = Category("Категория", "Описание", [product])
        assert category.calculate_average_price() == 1234.56

    def test_base_container_inheritance(self):
        """Тест наследования от BaseContainer."""
        category = Category("Категория", "Описание")
        product = Product("Товар", "Описание", 1000.0, 5)
        order = Order(product, 2)

        # Проверяем что оба класса наследуются от BaseContainer
        from src.models import BaseContainer
        assert isinstance(category, BaseContainer)
        assert isinstance(order, BaseContainer)

    def test_zero_quantity_error_message(self):
        """Тест сообщения ZeroQuantityError."""
        product = Product("Товар", "Описание", 1000.0, 1)
        product.quantity = 0

        category = Category("Категория", "Описание")

        try:
            category.add_product(product)
        except ZeroQuantityError as e:
            assert "Товар 'Товар' имеет нулевое количество и не может быть добавлен" in str(e)