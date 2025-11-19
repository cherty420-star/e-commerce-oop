import os
import pytest
from src.models import Product, Smartphone, LawnGrass, Category, load_categories_from_json, CategoryIterator


class TestProduct:
    """Тесты для базового класса Product."""

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

    def test_product_addition_same_type(self):
        """Тест сложения товаров одного типа."""
        product1 = Product("Товар 1", "Описание", 1000.0, 5)
        product2 = Product("Товар 2", "Описание", 2000.0, 3)

        total = product1 + product2

        assert total == 11000.0  # 1000*5 + 2000*3
        assert isinstance(total, float)

    def test_product_addition_different_type_error(self):
        """Тест ошибки при сложении товаров разных типов."""
        product = Product("Товар", "Описание", 1000.0, 5)
        smartphone = Smartphone("Смартфон", "Описание", 2000.0, 2, 4.5, "Model", 128, "Black")

        with pytest.raises(TypeError, match="Можно складывать только товары одного типа"):
            product + smartphone


class TestSmartphone:
    """Тесты для класса Smartphone."""

    def test_smartphone_initialization(self):
        """Тест корректной инициализации смартфона."""
        smartphone = Smartphone(
            name="Тестовый смартфон",
            description="Описание смартфона",
            price=50000.0,
            quantity=10,
            efficiency=4.5,
            model="Test Model",
            memory=256,
            color="Black"
        )

        assert smartphone.name == "Тестовый смартфон"
        assert smartphone.description == "Описание смартфона"
        assert smartphone.price == 50000.0
        assert smartphone.quantity == 10
        assert smartphone.efficiency == 4.5
        assert smartphone.model == "Test Model"
        assert smartphone.memory == 256
        assert smartphone.color == "Black"

    def test_smartphone_inheritance(self):
        """Тест что Smartphone наследуется от Product."""
        smartphone = Smartphone("Смартфон", "Описание", 50000.0, 10, 4.5, "Model", 128, "Black")

        assert isinstance(smartphone, Product)
        assert issubclass(Smartphone, Product)

    def test_smartphone_addition_same_type(self):
        """Тест сложения смартфонов одного типа."""
        smartphone1 = Smartphone("Смартфон 1", "Описание", 50000.0, 3, 4.5, "Model1", 128, "Black")
        smartphone2 = Smartphone("Смартфон 2", "Описание", 70000.0, 2, 4.8, "Model2", 256, "White")

        total = smartphone1 + smartphone2

        assert total == (50000.0 * 3) + (70000.0 * 2)
        assert isinstance(total, float)

    def test_smartphone_addition_different_type_error(self):
        """Тест ошибки при сложении смартфона с другим типом товара."""
        smartphone = Smartphone("Смартфон", "Описание", 50000.0, 3, 4.5, "Model", 128, "Black")
        lawn_grass = LawnGrass("Трава", "Описание", 2000.0, 10, "Россия", 14, "Зеленый")

        with pytest.raises(TypeError, match="Можно складывать только товары одного типа"):
            smartphone + lawn_grass

    def test_smartphone_string_representation(self):
        """Тест строкового представления смартфона."""
        smartphone = Smartphone("iPhone", "Смартфон", 80000.0, 5, 4.7, "15 Pro", 256, "Blue")

        expected = "iPhone, 80000.0 руб. Остаток: 5 шт."
        assert str(smartphone) == expected


class TestLawnGrass:
    """Тесты для класса LawnGrass."""

    def test_lawn_grass_initialization(self):
        """Тест корректной инициализации газонной травы."""
        lawn_grass = LawnGrass(
            name="Тестовая трава",
            description="Описание травы",
            price=1500.0,
            quantity=20,
            country="Россия",
            germination_period=14,
            color="Зеленый"
        )

        assert lawn_grass.name == "Тестовая трава"
        assert lawn_grass.description == "Описание травы"
        assert lawn_grass.price == 1500.0
        assert lawn_grass.quantity == 20
        assert lawn_grass.country == "Россия"
        assert lawn_grass.germination_period == 14
        assert lawn_grass.color == "Зеленый"

    def test_lawn_grass_inheritance(self):
        """Тест что LawnGrass наследуется от Product."""
        lawn_grass = LawnGrass("Трава", "Описание", 1500.0, 20, "Россия", 14, "Зеленый")

        assert isinstance(lawn_grass, Product)
        assert issubclass(LawnGrass, Product)

    def test_lawn_grass_addition_same_type(self):
        """Тест сложения газонной травы одного типа."""
        lawn_grass1 = LawnGrass("Трава 1", "Описание", 1500.0, 10, "Россия", 14, "Зеленый")
        lawn_grass2 = LawnGrass("Трава 2", "Описание", 2000.0, 5, "Германия", 21, "Темно-зеленый")

        total = lawn_grass1 + lawn_grass2

        assert total == (1500.0 * 10) + (2000.0 * 5)
        assert isinstance(total, float)

    def test_lawn_grass_addition_different_type_error(self):
        """Тест ошибки при сложении газонной травы с другим типом товара."""
        lawn_grass = LawnGrass("Трава", "Описание", 1500.0, 10, "Россия", 14, "Зеленый")
        smartphone = Smartphone("Смартфон", "Описание", 50000.0, 3, 4.5, "Model", 128, "Black")

        with pytest.raises(TypeError, match="Можно складывать только товары одного типа"):
            lawn_grass + smartphone

    def test_lawn_grass_string_representation(self):
        """Тест строкового представления газонной травы."""
        lawn_grass = LawnGrass("Газонная трава", "Качественная", 2500.0, 15, "Германия", 14, "Зеленый")

        expected = "Газонная трава, 2500.0 руб. Остаток: 15 шт."
        assert str(lawn_grass) == expected


class TestCategory:
    """Тесты для класса Category."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_add_product_valid(self):
        """Тест добавления валидного продукта в категорию."""
        category = Category("Категория", "Описание")
        product = Product("Товар", "Описание", 1000.0, 5)

        category.add_product(product)

        assert len(category.get_products_list()) == 1
        assert category.get_products_list()[0].name == "Товар"

    def test_add_smartphone_valid(self):
        """Тест добавления смартфона в категорию."""
        category = Category("Смартфоны", "Описание")
        smartphone = Smartphone("Смартфон", "Описание", 50000.0, 3, 4.5, "Model", 128, "Black")

        category.add_product(smartphone)

        assert len(category.get_products_list()) == 1
        assert isinstance(category.get_products_list()[0], Smartphone)

    def test_add_lawn_grass_valid(self):
        """Тест добавления газонной травы в категорию."""
        category = Category("Газонная трава", "Описание")
        lawn_grass = LawnGrass("Трава", "Описание", 1500.0, 10, "Россия", 14, "Зеленый")

        category.add_product(lawn_grass)

        assert len(category.get_products_list()) == 1
        assert isinstance(category.get_products_list()[0], LawnGrass)

    def test_add_product_invalid_type_error(self):
        """Тест ошибки при добавлении невалидного объекта в категорию."""
        category = Category("Категория", "Описание")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
            category.add_product("не товар")

    def test_add_product_invalid_object_error(self):
        """Тест ошибки при добавлении другого невалидного объекта."""
        category = Category("Категория", "Описание")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
            category.add_product(123)  # число вместо продукта

    def test_category_with_mixed_products(self):
        """Тест категории со смешанными типами продуктов."""
        category = Category("Разные товары", "Описание")

        product = Product("Обычный товар", "Описание", 1000.0, 5)
        smartphone = Smartphone("Смартфон", "Описание", 50000.0, 3, 4.5, "Model", 128, "Black")
        lawn_grass = LawnGrass("Трава", "Описание", 1500.0, 10, "Россия", 14, "Зеленый")

        category.add_product(product)
        category.add_product(smartphone)
        category.add_product(lawn_grass)

        assert len(category.get_products_list()) == 3
        assert Category.product_count == 3


class TestIntegration:
    """Интеграционные тесты."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_full_workflow_with_inheritance(self):
        """Тест полного рабочего процесса с наследованием."""
        # Создаем разные типы товаров
        smartphone = Smartphone("Смартфон", "Описание", 50000.0, 3, 4.5, "Model", 128, "Black")
        lawn_grass = LawnGrass("Трава", "Описание", 1500.0, 10, "Россия", 14, "Зеленый")

        # Создаем категории
        electronics = Category("Электроника", "Техника")
        garden = Category("Сад", "Растения")

        # Добавляем товары в категории
        electronics.add_product(smartphone)
        garden.add_product(lawn_grass)

        # Проверяем добавление
        assert len(electronics.get_products_list()) == 1
        assert len(garden.get_products_list()) == 1

        # Проверяем сложение одинаковых типов
        smartphone2 = Smartphone("Смартфон 2", "Описание", 60000.0, 2, 4.8, "Model2", 256, "White")
        total_smartphones = smartphone + smartphone2
        assert total_smartphones == (50000.0 * 3) + (60000.0 * 2)

        # Проверяем ошибку при сложении разных типов
        with pytest.raises(TypeError):
            smartphone + lawn_grass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])