# Red Hot ОГУ Peppers
___
## Пошаговая установка и запуск проекта

**1. Клонировать репозиторий**
```
git clone https://github.com/xaxaton/server.git
```
**2. Создать и активировать виртуальное окружение**
```
python -m venv venv
.\venv\Scripts\activate
```
**3. Установить зависимости**
```
pip install requirements/dev.txt
pip install requirements/prod.txt
pip install requirements/test.txt
```
**4. Создать .env файл, содержащий секреты**
Этот файл должен быть в корневой папке. Его содержимое должно выглядеть следующим образом:
```
SECRET_KEY = writesecretkeyhere
DEBUG = True/False
ALLOWED_HOSTS = host1 host2 host3
EMAIL_SENDER = writehere
EMAIL_PASSWORD = writehere
```
**5. Запустить сервер**
```
python manage.py runserver
```
___

# API
##### Внимание: swagger используется исключительно для демонстрации доступных эндпоинтов. Не во всех эндпоинты можно передать необходимые параметры, для тестирования используйте разработанное нами веб-приложение или ПО для отправки запросов.
###### * SWAGGER: <a href="http://127.0.0.1:8000/swagger/">http://127.0.0.1:8000/swagger/</a>
###### * REDOC: <a href="http://127.0.0.1:8000/redoc/">http://127.0.0.1:8000/redoc/</a>
###### * АДМИНКА: <a href="http://127.0.0.1:8000/docs/">http://127.0.0.1:8000/admin/</a>
