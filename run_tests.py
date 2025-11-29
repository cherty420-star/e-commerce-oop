#!/usr/bin/env python3
"""
Скрипт для запуска тестов с проверкой покрытия кода.
"""

import subprocess
import sys


def run_tests_with_coverage():
    """Запускает тесты с проверкой покрытия кода."""

    print("🚀 Запуск тестов с проверкой покрытия кода...")
    print("=" * 50)

    # Запускаем все тесты
    cmd = [
        "pytest",
        "tests/",
        "-v",
        "--cov=src.models",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-fail-under=75"
    ]

    try:
        result = subprocess.run(cmd, text=True)

        print("=" * 50)

        if result.returncode == 0:
            print("✅ Все тесты прошли успешно!")
            print("✅ Покрытие тестами выше 75%!")
            print("📊 Отчет о покрытии сгенерирован в 'htmlcov/'")
        else:
            print("❌ Покрытие тестами ниже 75%")
            sys.exit(result.returncode)

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_tests_with_coverage()