# Реализация работы с Контур Маркет API

## Общее описание

Набор скриптов для работы с API Контур Маркет.

## Установка

Скачать проект.

Установить виртуальное окружение командой:
```commandline
python3 -m venv env
```

Войти в виртуальное окружение командой:
```commandline
source env/bin/activate
```

Установить зависимости командой:
```commandline
pip install -r requirements.txt
```

Создать файл `.env` и заполнить его следующими занчениями:

`API_KEY=ваш API ключ` - Ключ необходимо получить на странице ['Как выпустить ключ API'](https://support.kontur.ru/pages/viewpage.action?pageId=93169068#id-%D0%98%D0%BD%D1%82%D0%B5%D0%B3%D1%80%D0%B0%D1%86%D0%B8%D1%8F%D1%81%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8EAPI-%D0%A2%D0%B5%D1%85%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F).

## Запуск

### test_connection.py

```python
python test_connection.py
```

Скрипт `test_connection.py` Выполняет проверку подключения к API и тест на правильный ключ API. Если в файл `.env` был 
внесен валидный ключ API, то в результате будет выведен список всех торговых точек организации.

Например:
```json
{
   "items": [
       {
           "id": "0c6e4b63-9876-1234-a886-e5152ef5537a",
           "organizationId": "f4b94eea-902d-44b3-87b0-b45b0dcc7064",
           "name": "Кафе \"У дома\"",
           "address": "г. Екатеринбург, Ленина, 2"
       },
       {
           "id": "1e5c6c32-9876-1234-8564-f86d2d6788bd",
           "organizationId": "f4b94eea-902d-44b3-87b0-b45b0dcc7064",
           "name": "Магазин",
           "address": "г. Екатеринбург, Ленина 1"
       }
   ]
}
```