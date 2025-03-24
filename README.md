# Тестирование функционала расписания Skyeng

Проект автоматизирует тестирование UI и API для работы с персональными событиями в личном кабинете преподавателей Skyeng.

## 📂 Структура проекта
* .
* ├── pages/
* │ ├── ui_class.py # Page Object Model для UI тестов
* │ └── api_class.py # Клиент для API запросов
* ├── tests/
* │ ├── test_ui.py # Тесты через Selenium
* │ └── test_api.py # Тесты через Requests
* ├── requirements.txt # Список зависимостей
* └── README.md # Документация
## 🚀 Запуск тестов

1. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   pytest tests/test_ui.py --alluredir=allure-results
   pytest tests/test_api.py --alluredir=allure-results
   allure serve allure-results
   
🔍 UI-тесты (Selenium)
* Авторизация в системе
* Создание события
* Изменение цвета и описания события
* Удаление события
* Выхода из аккаунта

API-тесты (Requests)
* Авторизация в системе
* Создание события
* Изменение цвета и описания события
* Удаление события
* Выхода из аккаунта

⚙️ Настройки
* Данные авторизации: ui_class.py (логин/пароль)
* API-токен: api_class.py
* Тестовые данные: заголовки, описания и даты заданы в классах

---

### Как использовать:
1. Для UI-тестов убедитесь, что версия Chrome совместима с ChromeDriver
2. Для API-тестов проверьте актуальность токена в `api_class.py`