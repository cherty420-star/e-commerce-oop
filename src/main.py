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
        description="Мобильные устройства",
        products=[product1, product2]
    )

    print("=== Ручное создание объектов ===")
    print(f"Категория: {smartphones.name}")
    print(f"Описание: {smartphones.description}")
    print(f"Количество товаров: {len(smartphones.products)}")
    first_product = smartphones.products[0]
    print(f"Первый товар: {first_product.name} - {first_product.price} руб.")

    print("\n=== Статистика ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    # Загрузка из JSON
    print("\n=== Загрузка из JSON ===")
    data_file_path = get_data_path()
    print(f"Ищем файл по пути: {data_file_path}")
    categories = load_categories_from_json(data_file_path)

    if categories:
        print(f"Загружено категорий: {len(categories)}")
        for category in categories:
            print(f"\nКатегория: {category.name}")
            print(f"Товаров: {len(category.products)}")
            for product in category.products:
                template = "  - {}: {} руб. (в наличии: {})"
                print(template.format(
                    product.name, product.price, product.quantity
                ))

    print("\n=== Итоговая статистика ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")


if __name__ == "__main__":
    main()
