# E-Commerce OOP Project

Учебный проект интернет-магазина на Python с использованием ООП.

## Реализованная функциональность

### Базовые возможности
- Классы Product и Category для товаров и категорий
- Приватные атрибуты с геттерами/сеттерами
- Загрузка данных из JSON файлов
- Комплексное тестирование с покрытием >85%

### Магические методы
- `__str__` для красивого строкового представления
- `__add__` для сложения товаров (только одинаковых типов)
- `__iter__` для итерации по товарам категории

### Наследование
- **Smartphone** - класс для смартфонов с дополнительными атрибутами
- **LawnGrass** - класс для газонной травы с дополнительными атрибутами

### Ограничения операций
- Ограничение сложения только товаров одинаковых классов
- Ограничение добавления только продуктов и наследников

### Абстрактные классы и миксины (НОВЫЙ ФУНКЦИОНАЛ)
- **BaseProduct** - абстрактный базовый класс для всех товаров
- **LoggingMixin** - миксин для логирования создания объектов
- **BaseContainer** - абстрактный класс для контейнеров с товарами

### Класс Order (НОВЫЙ ФУНКЦИОНАЛ)
- **Order** - класс для представления заказов
- Содержит товар, количество и итоговую стоимость
- Наследуется от BaseContainer

## 🛠 Установка и запуск

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск приложения
python src/main.py

# Запуск тестов
pytest tests/test_models.py -v

# Проверка покрытия
pytest --cov=src --cov-report=term-missing

Структура проекта

e-commerce-oop/
├── src/
│   ├── __init__.py
│   ├── models.py          # Все классы проекта: Product, Smartphone, LawnGrass, Category
│   └── main.py           # Демонстрация работы
├── tests/
│   ├── __init__.py
│   └── test_models.py    # Тесты для всех классов
├── data/
│   └── products.json     # Данные для загрузки
├── requirements.txt
└── README.md
Тестирование
Проект включает комплексные тесты для:

Базовых классов Product и Category

Классов-наследников Smartphone и LawnGrass

Магических методов

Ограничений сложения и добавления

Загрузки данных из JSON

Покрытие кода тестами: более 85%

💡 Примеры использования
Создание классов-наследников

# Создание смартфона
smartphone = Smartphone(
    name="iPhone 15 Pro",
    description="Флагманский смартфон",
    price=120000.0,
    quantity=8,
    efficiency=4.5,
    model="15 Pro",
    memory=256,
    color="Титановый синий"
)

# Создание газонной травы
lawn_grass = LawnGrass(
    name="Газонная трава Премиум",
    description="Элитная газонная трава",
    price=2500.0,
    quantity=50,
    country="Германия",
    germination_period=14,
    color="Зеленый"
)
Ограничения операций

# Корректное сложение (одинаковые типы)
total_smartphones = smartphone1 + smartphone2
total_grass = lawn_grass1 + lawn_grass2

# Ошибка сложения (разные типы)
try:
    invalid = smartphone + lawn_grass  # TypeError
except TypeError as e:
    print(e)

# Корректное добавление в категорию
category.add_product(smartphone)  # ✅
category.add_product(lawn_grass)  # ✅

# Ошибка добавления
try:
    category.add_product("не товар")  # TypeError
except TypeError as e:
    print(e)
История изменений
Версия 1.0
Базовые классы Product и Category

Приватные атрибуты и доступы

Магические методы

Версия 1.1 (ТЕКУЩАЯ)
Классы-наследники: Smartphone и LawnGrass

Ограничения операций: сложение и добавление

Улучшенная валидация типов

Расширенное тестирование

Разработка
Проект разработан в учебных целях для изучения ООП в Python.
Соответствует стандартам PEP 8 и включает полное тестовое покрытие.

Примеры использования нового функционала:
Абстрактный класс BaseProduct
# Все товары наследуются от BaseProduct
product = Product("Товар", "Описание", 1000.0, 5)
smartphone = Smartphone("Смартфон", "Описание", 50000.0, 3, 4.5, "Model", 128, "Black")

print(isinstance(product, BaseProduct))  # True
print(isinstance(smartphone, BaseProduct))  # True

Миксин логирования
# При создании объектов выводится информация в консоль
product = Product("Товар", "Описание", 1000.0, 5)
# В консоли: "Создан объект Product с параметрами: ..."

Класс Order
# Создание заказа
product = Product("Товар", "Описание", 1000.0, 5)
order = Order(product=product, quantity=2)
print(order)  # "Заказ: Товар, Количество: 2, Итоговая стоимость: 2000.0 руб."

# Ошибки при создании заказа
try:
    Order(product="не товар", quantity=2)  # TypeError
except TypeError as e:
    print(e)

try:
    Order(product=product, quantity=10)  # ValueError (недостаточно товара)
except ValueError as e:
    print(e)

Абстрактный класс BaseContainer
# Category и Order наследуются от BaseContainer
category = Category("Электроника", "Техника")
order = Order(product, 2)

print(isinstance(category, BaseContainer))  # True
print(isinstance(order, BaseContainer))  # True

# Общие методы
print(category.get_total_quantity())
print(order.get_total_quantity())