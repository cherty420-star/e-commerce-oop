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
- **Smartphone** - класс для смартфонов с дополнительными атрибутами:
  - Производительность (efficiency)
  - Модель (model)
  - Объем памяти (memory)
  - Цвет (color)

- **LawnGrass** - класс для газонной травы с дополнительными атрибутами:
  - Страна-производитель (country)
  - Срок прорастания (germination_period)
  - Цвет (color)

### Защита целостности данных
- Ограничение сложения только товаров одного типа
- Валидация добавляемых объектов в категории
- Проверка типов при операциях

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