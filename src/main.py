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

    print("=== Демонстрация абстрактного класса BaseProduct ===")

    # Создание базового товара
    print("\n1. Создание объекта Product:")
    product = Product(
        name="Обычный товар",
        description="Простой товар для демонстрации",
        price=1000.0,
        quantity=10
    )
    print(f"   Создан: {product}")

    print("\n2. Создание объекта Smartphone:")
    smartphone = Smartphone(
        name="iPhone 15 Pro",
        description="Флагманский смартфон Apple",
        price=120000.0,
        quantity=8,
        efficiency=4.5,
        model="15 Pro",
        memory=256,
        color="Титановый синий"
    )
    print(f"   Создан: {smartphone}")

    print("\n3. Создание объекта LawnGrass:")
    lawn_grass = LawnGrass(
        name="Газонная трава Премиум",
        description="Элитная газонная трава",
        price=2500.0,
        quantity=50,
        country="Германия",
        germination_period=14,
        color="Ярко-зеленый"
    )
    print(f"   Создан: {lawn_grass}")

    print("\n=== Проверка наследования от BaseProduct ===")
    print(f"Product является наследником BaseProduct: {isinstance(product, BaseProduct)}")
    print(f"Smartphone является наследником BaseProduct: {isinstance(smartphone, BaseProduct)}")
    print(f"LawnGrass является наследником BaseProduct: {isinstance(lawn_grass, BaseProduct)}")

    print("\n=== Демонстрация работы Category ===")
    # Создание категории и добавление товаров
    electronics_category = Category("Электроника", "Технические товары")
    electronics_category.add_product(product)
    electronics_category.add_product(smartphone)

    garden_category = Category("Сад и огород", "Растения и инструменты")
    garden_category.add_product(lawn_grass)

    print(f"Категория: {electronics_category}")
    print(f"Категория: {garden_category}")

    print("\n=== Демонстрация сложения товаров ===")
    # Создаем еще один товар для сложения
    smartphone2 = Smartphone(
        name="Samsung Galaxy S24",
        description="Флагманский смартфон Samsung",
        price=100000.0,
        quantity=5,
        efficiency=4.8,
        model="S24 Ultra",
        memory=512,
        color="Черный"
    )

    try:
        total_smartphones = smartphone + smartphone2
        print(f"Суммарная стоимость смартфонов: {total_smartphones} руб.")
    except TypeError as e:
        print(f"Ошибка при сложении: {e}")

    print("\n=== Демонстрация класса Order (доп. задание) ===")
    try:
        # Успешное создание заказа
        order = Order(product=smartphone, quantity=2)
        print(f"Успешно создан заказ: {order}")

        # Заказ с недостаточным количеством
        try:
            Order(product=smartphone, quantity=20)
        except ValueError as e:
            print(f"Ошибка создания заказа (ожидаемо): {e}")

    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

    print("\n=== Демонстрация BaseContainer ===")
    print(f"Category наследуется от BaseContainer: {isinstance(electronics_category, type)}")
    print(f"Order наследуется от BaseContainer: {isinstance(order, type)}")

    print(f"Общее количество в категории электроники: {electronics_category.get_total_quantity()}")
    print(f"Количество в заказе: {order.get_total_quantity()}")

    print("\n=== Загрузка данных из JSON ===")
    data_file_path = get_data_path()
    if os.path.exists(data_file_path):
        categories = load_categories_from_json(data_file_path)
        if categories:
            print(f"Успешно загружено категорий: {len(categories)}")
            for category in categories:
                print(f"  - {category.name}: {len(category.get_products_list())} товаров")
        else:
            print("Не удалось загрузить категории из JSON")
    else:
        print(f"Файл данных не найден: {data_file_path}")

    print("\n=== Итоговая статистика ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")
    print("\nДемонстрация завершена успешно! ✅")


if __name__ == "__main__":
    main()