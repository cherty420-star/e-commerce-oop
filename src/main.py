import os
from src.models import (Product, Smartphone, LawnGrass, Category,
                        Order, BaseProduct, ZeroQuantityError, load_categories_from_json)


def get_data_path():
    """Возвращает правильный путь к файлу данных."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "data", "products.json")


def main():
    """Основная функция для демонстрации работы классов."""

    print("=== Демонстрация обработки нулевого количества товаров ===")

    # Попытка создать товар с нулевым количеством
    print("\n1. Попытка создать товар с quantity=0:")
    try:
        invalid_product = Product(
            name="Невалидный товар",
            description="Товар с нулевым количеством",
            price=1000.0,
            quantity=0
        )
    except ValueError as e:
        print(f"   Ошибка (ожидаемо): {e}")

    # Создание валидных товаров
    print("\n2. Создание валидных товаров:")
    try:
        product1 = Product(
            name="Валидный товар 1",
            description="Товар с положительным количеством",
            price=1000.0,
            quantity=5
        )
        print(f"   Успешно создан: {product1}")

        product2 = Product(
            name="Валидный товар 2",
            description="Еще один валидный товар",
            price=2000.0,
            quantity=3
        )
        print(f"   Успешно создан: {product2}")

    except ValueError as e:
        print(f"   Неожиданная ошибка: {e}")

    print("\n=== Демонстрация метода calculate_average_price() ===")

    # Создание категории
    category = Category("Тестовая категория", "Для демонстрации")

    # Средняя цена пустой категории
    print(f"Средняя цена пустой категории: {category.calculate_average_price()} руб.")

    # Добавление товаров и расчет средней цены
    category.add_product(product1)
    category.add_product(product2)

    average_price = category.calculate_average_price()
    print(f"Средняя цена после добавления товаров: {average_price} руб.")
    print(f"Проверка: (1000 + 2000) / 2 = {1500.0} руб.")

    print("\n=== Демонстрация ZeroQuantityError (доп. задание) ===")

    # Создание товара с нулевым количеством для теста
    try:
        zero_product = Product(
            name="Товар с нулем",
            description="Этот товар не должен быть создан",
            price=500.0,
            quantity=0
        )
    except ValueError:
        # Создаем товар с нулевым количеством "вручную" для демонстрации
        class TempProduct:
            def __init__(self):
                self.name = "Временный товар с 0"
                self.quantity = 0

        temp_product = TempProduct()

        print("Попытка добавить товар с нулевым количеством в категорию:")
        try:
            category.add_product(temp_product)  # Должен вызвать TypeError
        except (TypeError, ZeroQuantityError) as e:
            print(f"   Ошибка: {e}")

    print("\n=== Демонстрация создания заказа с нулевым количеством ===")
    try:
        valid_product = Product(
            name="Товар для заказа",
            description="Подходящий товар",
            price=1500.0,
            quantity=10
        )

        # Попытка создать заказ с нулевым количеством
        try:
            zero_order = Order(product=valid_product, quantity=0)
        except ZeroQuantityError as e:
            print(f"   Ошибка при создании заказа: {e}")

        # Успешное создание заказа
        valid_order = Order(product=valid_product, quantity=2)
        print(f"   Успешно создан заказ: {valid_order}")

    except Exception as e:
        print(f"   Неожиданная ошибка: {e}")

    print("\n=== Демонстрация с классами-наследниками ===")
    try:
        smartphone = Smartphone(
            name="Тестовый смартфон",
            description="Смартфон для теста",
            price=50000.0,
            quantity=2,  # Положительное количество
            efficiency=4.5,
            model="Test Model",
            memory=128,
            color="Black"
        )
        print(f"   Успешно создан смартфон: {smartphone}")

        # Попытка создать с нулевым количеством
        try:
            invalid_smartphone = Smartphone(
                name="Невалидный смартфон",
                description="С нулевым количеством",
                price=50000.0,
                quantity=0,  # Нулевое количество
                efficiency=4.5,
                model="Invalid",
                memory=128,
                color="Black"
            )
        except ValueError as e:
            print(f"   Ошибка при создании смартфона: {e}")

    except Exception as e:
        print(f"   Неожиданная ошибка: {e}")

    print("\n=== Загрузка из JSON с обработкой ошибок ===")
    data_file_path = get_data_path()
    if os.path.exists(data_file_path):
        categories = load_categories_from_json(data_file_path)
        if categories:
            print(f"Успешно загружено категорий: {len(categories)}")
            for category in categories:
                avg_price = category.calculate_average_price()
                print(
                    f"  - {category.name}: {len(category.get_products_list())} товаров, средняя цена: {avg_price:.2f} руб.")
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