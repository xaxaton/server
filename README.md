# Red Hot ОГУ Peppers
### * ПРОЕКТ: <a href="https://osu-team.site/">https://osu-team.site/</a>
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
SECRET_KEY = secretkeyhere
DEBUG = True/False
ALLOWED_HOSTS = host1 host2 host3
EMAIL_SENDER = e@gmail.ru
EMAIL_PASSWORD = password
DB_NAME = dbname
DB_USER = dbname
DB_PASSWORD = dbpass
DB_HOST = dbhost
```
**5. При запуске на новой базе данных**
```
python manage.py migrate
```
**6. Запустить сервер**
```
python manage.py runserver
```
___

# API
##### Внимание: swagger используется исключительно для демонстрации доступных эндпоинтов. Не во всех эндпоинты можно передать необходимые параметры, для тестирования используйте разработанное нами веб-приложение или ПО для отправки запросов.
###### * SWAGGER: <a href="https://osu-team.site/swagger/">https://osu-team.site/swagger/</a>
###### * АДМИНКА: <a href="https://osu-team.site/admin/">https://osu-team.site/admin/</a>
