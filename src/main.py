import os
from src.models import Product, Smartphone, LawnGrass, Category, load_categories_from_json


def get_data_path():
    """Возвращает правильный путь к файлу данных."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "data", "products.json")


def main():
    """Основная функция для демонстрации работы классов."""

    print("=== Демонстрация классов-наследников ===")

    # Создание смартфонов
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

    smartphone2 = Smartphone(
        name="Samsung Galaxy S24",
        description="Флагманский смартфон Samsung",
        price=100000.0,
        quantity=12,
        efficiency=4.8,
        model="S24 Ultra",
        memory=512,
        color="Черный"
    )

    # Создание газонной травы
    lawn_grass1 = LawnGrass(
        name="Газонная трава Премиум",
        description="Элитная газонная трава для ландшафтного дизайна",
        price=2500.0,
        quantity=50,
        country="Германия",
        germination_period=14,
        color="Ярко-зеленый"
    )

    lawn_grass2 = LawnGrass(
        name="Спортивный газон",
        description="Устойчивая трава для спортивных площадок",
        price=1800.0,
        quantity=30,
        country="Нидерланды",
        germination_period=21,
        color="Темно-зеленый"
    )

    print("Смартфоны:")
    print(f"  - {smartphone1}")
    print(f"    Модель: {smartphone1.model}, Память: {smartphone1.memory}ГБ")
    print(f"  - {smartphone2}")
    print(f"    Модель: {smartphone2.model}, Память: {smartphone2.memory}ГБ")

    print("\nГазонная трава:")
    print(f"  - {lawn_grass1}")
    print(f"    Страна: {lawn_grass1.country}, Прорастание: {lawn_grass1.germination_period} дней")
    print(f"  - {lawn_grass2}")
    print(f"    Страна: {lawn_grass2.country}, Прорастание: {lawn_grass2.germination_period} дней")

    print("\n=== Демонстрация сложения товаров одного типа ===")

    # Сложение смартфонов (должно работать)
    try:
        smartphones_total = smartphone1 + smartphone2
        print(f"Общая стоимость смартфонов: {smartphones_total} руб.")
    except TypeError as e:
        print(f"Ошибка при сложении смартфонов: {e}")

    # Сложение газонной травы (должно работать)
    try:
        lawn_grass_total = lawn_grass1 + lawn_grass2
        print(f"Общая стоимость газонной травы: {lawn_grass_total} руб.")
    except TypeError as e:
        print(f"Ошибка при сложении газонной травы: {e}")

    # Попытка сложить разные типы товаров (должна вызвать ошибку)
    print("\n=== Попытка сложить разные типы товаров ===")
    try:
        invalid_total = smartphone1 + lawn_grass1
        print(f"Результат: {invalid_total} руб.")
    except TypeError as e:
        print(f"Ошибка (ожидаемо): {e}")

    print("\n=== Демонстрация добавления товаров в категории ===")

    # Создание категорий
    smartphones_category = Category("Смартфоны", "Мобильные устройства")
    lawn_grass_category = Category("Газонная трава", "Растительность для ландшафта")

    # Добавление товаров в категории (должно работать)
    try:
        smartphones_category.add_product(smartphone1)
        smartphones_category.add_product(smartphone2)
        print("Смартфоны успешно добавлены в категорию")
    except TypeError as e:
        print(f"Ошибка при добавлении смартфона: {e}")

    try:
        lawn_grass_category.add_product(lawn_grass1)
        lawn_grass_category.add_product(lawn_grass2)
        print("Газонная трава успешно добавлена в категорию")
    except TypeError as e:
        print(f"Ошибка при добавлении газонной травы: {e}")

    # Попытка добавить неправильный объект (должна вызвать ошибку)
    print("\n=== Попытка добавить неправильный объект в категорию ===")
    try:
        smartphones_category.add_product("не товар")
        print("Объект добавлен")
    except TypeError as e:
        print(f"Ошибка (ожидаемо): {e}")

    print("\n=== Итоговые категории ===")
    print(f"Категория: {smartphones_category}")
    print("Товары:")
    for product in smartphones_category:
        print(f"  - {product}")

    print(f"\nКатегория: {lawn_grass_category}")
    print("Товары:")
    for product in lawn_grass_category:
        print(f"  - {product}")

    print("\n=== Итоговая статистика ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")


if __name__ == "__main__":
    main()