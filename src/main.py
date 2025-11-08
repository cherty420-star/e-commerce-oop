import os
from src.models import Product, Category, load_categories_from_json


def get_data_path():
    """Возвращает правильный путь к файлу данных."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "data", "products.json")


def main():
    """Основная функция для демонстрации работы классов."""

    # Создание товаров вручную
    product1 = Product(
        name="Samsung Galaxy S23",
        description="Флагманский смартфон",
        price=80000.0,
        quantity=10
    )

    product2 = Product(
        name="iPhone 14",
        description="Премиум смартфон",
        price=90000.0,
        quantity=5
    )

    # Создание категории вручную
    smartphones = Category(
        name="Смартфоны",
        description="Мобильные устройства"
    )

    # Добавление товаров через метод add_product
    smartphones.add_product(product1)
    smartphones.add_product(product2)

    print("=== Ручное создание объектов ===")
    print(f"Категория: {smartphones.name}")
    print(f"Описание: {smartphones.description}")
    print(f"Количество товаров: {len(smartphones.get_products_list())}")

    print("\n=== Список товаров через геттер ===")
    print(smartphones.products)

    print("\n=== Статистика ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    # Демонстрация работы с ценой
    print("\n=== Демонстрация сеттера цены ===")
    print(f"Текущая цена {product1.name}: {product1.price} руб.")

    # Попытка установить отрицательную цену
    product1.price = -1000  # Должно вывести сообщение об ошибке

    # Установка корректной цены
    product1.price = 75000.0
    print(f"Новая цена {product1.name}: {product1.price} руб.")

    # Демонстрация класс-метода
    print("\n=== Демонстрация класс-метода ===")
    new_product_data = {
        'name': 'Xiaomi Redmi Note 12',
        'description': 'Бюджетный смартфон',
        'price': 25000.0,
        'quantity': 8
    }

    new_product = Product.new_product(new_product_data)
    print(f"Создан новый товар: {new_product}")

    # Добавляем новый товар в категорию
    smartphones.add_product(new_product)
    print(f"\nОбновленный список товаров в категории '{smartphones.name}':")
    print(smartphones.products)

    # Загрузка из JSON
    print("\n=== Загрузка из JSON ===")
    data_file_path = get_data_path()
    print(f"Ищем файл по пути: {data_file_path}")
    categories = load_categories_from_json(data_file_path)

    if categories:
        print(f"Загружено категорий: {len(categories)}")
        for category in categories:
            print(f"\nКатегория: {category.name}")
            print(f"Товаров: {len(category.get_products_list())}")
            print("Список товаров:")
            print(category.products)

    print("\n=== Итоговая статистика ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")


if __name__ == "__main__":
    main()