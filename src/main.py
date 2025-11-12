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

    print("=== Строковое представление объектов ===")
    print("Товар 1:", product1)
    print("Товар 2:", product2)
    print("Категория:", smartphones)

    print("\n=== Магический метод сложения ===")
    total_value = product1 + product2
    print(f"Общая стоимость {product1.name} и {product2.name}: {total_value} руб.")

    # Демонстрация работы итератора (дополнительное задание)
    print("\n=== Итерация по товарам категории ===")
    print("Товары в категории (через цикл for):")
    for product in smartphones:
        print(f"  - {product}")

    # Демонстрация оптимизированного геттера products
    print("\n=== Оптимизированный геттер products ===")
    print(smartphones.products)

    # Демонстрация с другими товарами
    print("\n=== Дополнительная демонстрация сложения ===")
    product3 = Product("Ноутбук", "Игровой ноутбук", 150000.0, 2)
    product4 = Product("Планшет", "Графический планшет", 50000.0, 3)

    total_laptop_tablet = product3 + product4
    print(f"Общая стоимость {product3.name} и {product4.name}: {total_laptop_tablet} руб.")

    # Проверка расчета: 150000 * 2 + 50000 * 3 = 300000 + 150000 = 450000
    expected = (150000.0 * 2) + (50000.0 * 3)
    print(f"Проверка расчета: {expected} руб. (совпадает: {total_laptop_tablet == expected})")

    # Загрузка из JSON
    print("\n=== Загрузка из JSON ===")
    data_file_path = get_data_path()
    print(f"Ищем файл по пути: {data_file_path}")
    categories = load_categories_from_json(data_file_path)

    if categories:
        print(f"Загружено категорий: {len(categories)}")
        for category in categories:
            print(f"\nКатегория: {category}")  # Используем __str__
            print("Список товаров:")
            for product in category:  # Используем итератор
                print(f"  - {product}")

    print("\n=== Итоговая статистика ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")


if __name__ == "__main__":
    main()