import os
from src.models import (Product, Smartphone, LawnGrass, Category,
                        Order, BaseProduct, load_categories_from_json)


def get_data_path():
    """Возвращает правильный путь к файлу данных."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "data", "products.json")


def main():
    """Основная функция для демонстрации работы классов."""

    print("=== Демонстрация абстрактного класса и миксина ===")

    # Создание товаров с логированием (миксин)
    print("\nСоздание товаров (должны появиться сообщения о создании):")

    product1 = Product(
        name="Обычный товар",
        description="Простой товар для демонстрации",
        price=1000.0,
        quantity=10
    )

    smartphone1 = Smartphone(
        name="iPhone 15 Pro",
        description="Флагманский смартфон Apple",
        price=120000.0,
        quantity=8,
        efficiency=4.5,
        model="15 Pro",
        memory=256,
        color="Титановый синий"
    )

    lawn_grass1 = LawnGrass(
        name="Газонная трава Премиум",
        description="Элитная газонная трава для ландшафтного дизайна",
        price=2500.0,
        quantity=50,
        country="Германия",
        germination_period=14,
        color="Ярко-зеленый"
    )

    print("\n=== Проверка наследования от BaseProduct ===")
    print(f"Product является наследником BaseProduct: {isinstance(product1, BaseProduct)}")
    print(f"Smartphone является наследником BaseProduct: {isinstance(smartphone1, BaseProduct)}")
    print(f"LawnGrass является наследником BaseProduct: {isinstance(lawn_grass1, BaseProduct)}")

    print("\n=== Демонстрация работы Order класса (доп. задание) ===")

    try:
        # Создание заказа
        order1 = Order(product=smartphone1, quantity=2)
        print(f"Создан заказ: {order1}")

        # Попытка создать заказ с недостаточным количеством
        try:
            order_invalid = Order(product=smartphone1, quantity=20)
        except ValueError as e:
            print(f"Ошибка создания заказа (ожидаемо): {e}")

        # Попытка создать заказ с неправильным объектом
        try:
            order_invalid = Order(product="не товар", quantity=2)
        except TypeError as e:
            print(f"Ошибка создания заказа (ожидаемо): {e}")

    except Exception as e:
        print(f"Ошибка при работе с заказами: {e}")

    print("\n=== Демонстрация общего абстрактного класса BaseContainer ===")

    # Создание категории
    category = Category("Электроника", "Технические товары", [product1, smartphone1])
    print(f"Категория: {category}")
    print(f"Общее количество в категории: {category.get_total_quantity()}")

    # Создание заказа
    order = Order(product=smartphone1, quantity=1)
    print(f"Заказ: {order}")
    print(f"Общее количество в заказе: {order.get_total_quantity()}")

    print("\n=== Итерация по контейнерам ===")
    print("Товары в категории:")
    for product in category:
        print(f"  - {product}")

    print("Товары в заказе:")
    for product in order:
        print(f"  - {product}")

    print("\n=== Загрузка из JSON ===")
    data_file_path = get_data_path()
    categories = load_categories_from_json(data_file_path)

    if categories:
        print(f"Загружено категорий: {len(categories)}")
        for category in categories:
            print(f"\nКатегория: {category}")

    print("\n=== Итоговая статистика ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")


if __name__ == "__main__":
    main()