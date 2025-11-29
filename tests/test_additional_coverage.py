import pytest
import json
from unittest.mock import patch
from src.models import (
    Product, Smartphone, LawnGrass, Category, Order,
    BaseProduct, ZeroQuantityError, load_categories_from_json
)


class TestAdditionalCoverage:
    """Дополнительные тесты для повышения покрытия кода."""

    def test_product_price_setter_with_confirmation_yes(self):
        """Тест сеттера цены с подтверждением понижения (ответ 'y')."""
        product = Product("Товар", "Описание", 1000.0, 5)

        with patch('builtins.input', return_value='y'):
            product.price = 800.0

        assert product.price == 800.0

    def test_product_price_setter_with_confirmation_no(self):
        """Тест сеттера цены с отменой понижения (ответ 'n')."""
        product = Product("Товар", "Описание", 1000.0, 5)

        with patch('builtins.input', return_value='n'):
            product.price = 800.0

        # Цена не должна измениться
        assert product.price == 1000.0

    def test_product_price_setter_same_price(self):
        """Тест сеттера цены с той же ценой."""
        product = Product("Товар", "Описание", 1000.0, 5)
        product.price = 1000.0  # Та же цена

        assert product.price == 1000.0

    def test_product_price_setter_higher_price(self):
        """Тест сеттера цены с более высокой ценой."""
        product = Product("Товар", "Описание", 1000.0, 5)
        product.price = 1500.0  # Более высокая цена

        assert product.price == 1500.0

    def test_load_categories_file_not_found(self):
        """Тест загрузки категорий с несуществующим файлом."""
        categories = load_categories_from_json("nonexistent.json")
        assert categories == []

    def test_load_categories_invalid_json(self, tmp_path):
        """Тест загрузки категорий с невалидным JSON."""
        # Создаем временный файл с невалидным JSON
        invalid_json_file = tmp_path / "invalid.json"
        invalid_json_file.write_text("{invalid json")

        categories = load_categories_from_json(str(invalid_json_file))
        assert categories == []

    def test_load_categories_missing_key(self, tmp_path):
        """Тест загрузки категорий с отсутствующим ключом."""
        # Создаем временный файл с отсутствующим ключом (используем латиницу)
        missing_key_json = tmp_path / "missing_key.json"
        missing_key_json.write_text('''
        [
            {
                "name": "Category",
                "description": "Description"
                # missing "products"
            }
        ]
        ''', encoding='utf-8')

        categories = load_categories_from_json(str(missing_key_json))
        assert categories == []

    def test_category_add_product_type_error(self):
        """Тест добавления невалидного объекта в категорию."""
        category = Category("Категория", "Описание")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
            category.add_product("не товар")

    def test_order_insufficient_quantity(self):
        """Тест создания заказа с недостаточным количеством."""
        product = Product("Товар", "Описание", 1000.0, 5)

        with pytest.raises(ValueError, match="Недостаточно товара на складе"):
            Order(product, 10)

    def test_product_addition_same_type_detailed(self):
        """Тест сложения товаров с детальной проверкой."""
        product1 = Product("Товар 1", "Описание", 100.0, 10)  # 1000
        product2 = Product("Товар 2", "Описание", 200.0, 5)  # 1000
        total = product1 + product2

        assert total == 2000.0  # 100*10 + 200*5

    def test_smartphone_addition_same_type_detailed(self):
        """Тест сложения смартфонов с детальной проверкой."""
        phone1 = Smartphone("Phone 1", "Desc", 50000.0, 2, 4.5, "M1", 128, "Black")  # 100000
        phone2 = Smartphone("Phone 2", "Desc", 75000.0, 1, 4.8, "M2", 256, "White")  # 75000
        total = phone1 + phone2

        assert total == 175000.0  # 50000*2 + 75000*1

    def test_lawn_grass_addition_same_type_detailed(self):
        """Тест сложения газонной травы с детальной проверкой."""
        grass1 = LawnGrass("Grass 1", "Desc", 2000.0, 10, "RU", 14, "Green")  # 20000
        grass2 = LawnGrass("Grass 2", "Desc", 3000.0, 5, "DE", 21, "Dark")  # 15000
        total = grass1 + grass2

        assert total == 35000.0  # 2000*10 + 3000*5

    def test_category_str_with_products(self):
        """Тест строкового представления категории с товарами."""
        product1 = Product("Товар 1", "Описание", 1000.0, 3)
        product2 = Product("Товар 2", "Описание", 2000.0, 2)
        category = Category("Категория", "Описание", [product1, product2])

        assert str(category) == "Категория, количество продуктов: 5 шт."

    def test_category_str_empty(self):
        """Тест строкового представления пустой категории."""
        category = Category("Пустая категория", "Описание")

        assert str(category) == "Пустая категория, количество продуктов: 0 шт."

    def test_order_str(self):
        """Тест строкового представления заказа."""
        product = Product("Товар", "Описание", 1500.0, 10)
        order = Order(product, 3)

        expected = "Заказ: Товар, Количество: 3, Итоговая стоимость: 4500.0 руб."
        assert str(order) == expected

    def test_product_str(self):
        """Тест строкового представления товара."""
        product = Product("Тестовый товар", "Описание товара", 1234.56, 7)

        expected = "Тестовый товар, 1234.56 руб. Остаток: 7 шт."
        assert str(product) == expected

    def test_smartphone_str(self):
        """Тест строкового представления смартфона."""
        smartphone = Smartphone("iPhone", "Смартфон", 80000.0, 3, 4.7, "15 Pro", 256, "Blue")

        expected = "iPhone, 80000.0 руб. Остаток: 3 шт."
        assert str(smartphone) == expected

    def test_lawn_grass_str(self):
        """Тест строкового представления газонной травы."""
        lawn_grass = LawnGrass("Газонная трава", "Качественная", 2500.0, 15, "Германия", 14, "Зеленый")

        expected = "Газонная трава, 2500.0 руб. Остаток: 15 шт."
        assert str(lawn_grass) == expected

    def test_category_iteration(self):
        """Тест итерации по категории."""
        product1 = Product("Товар 1", "Описание", 1000.0, 5)
        product2 = Product("Товар 2", "Описание", 2000.0, 3)
        category = Category("Категория", "Описание", [product1, product2])

        products = list(category)
        assert len(products) == 2
        assert products[0].name == "Товар 1"
        assert products[1].name == "Товар 2"

    def test_order_iteration(self):
        """Тест итерации по заказу."""
        product = Product("Товар", "Описание", 1000.0, 5)
        order = Order(product, 2)

        products = list(order)
        assert len(products) == 1
        assert products[0].name == "Товар"

    def test_category_get_products_list(self):
        """Тест метода get_products_list."""
        product1 = Product("Товар 1", "Описание", 1000.0, 5)
        product2 = Product("Товар 2", "Описание", 2000.0, 3)
        category = Category("Категория", "Описание", [product1, product2])

        products = category.get_products_list()
        assert len(products) == 2
        assert products[0].name == "Товар 1"
        assert products[1].name == "Товар 2"

    def test_category_products_property_format(self):
        """Тест формата вывода свойства products."""
        product1 = Product("Товар 1", "Описание", 1000.0, 5)
        product2 = Product("Товар 2", "Описание", 2000.0, 3)
        category = Category("Категория", "Описание", [product1, product2])

        products_str = category.products
        lines = products_str.split('\n')
        assert len(lines) == 2
        assert "Товар 1, 1000.0 руб. Остаток: 5 шт." in lines[0]
        assert "Товар 2, 2000.0 руб. Остаток: 3 шт." in lines[1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])