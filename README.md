# Туристические маршруты
Веб проект по агрегации популярных походных маршрутов для самостоятельных путешественников (в текущей версии был выбран кавказкий заповедник). Интересные места, а также места палаточных остановок, обозначаются на карте ввиде маркеров. 


## Сборка репозитория и локальный запуск
#### Выполните в консоли:
~~~
git clone https://github.com/artur8833/Project_tourism.git
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
~~~
#### Работа с базой данных:
~~~
export FLASK_APP=webapp
flask db upgrade
~~~

## Настройка 
#### Настройка отображения погоды:
~~~
1. Регестрация на сайте: http://api.worldweatheronline.com/
2. Создаём файл config.py и вносим следующие строки:
3. WEATHER_DEFAULT_CITY = "Sochi,Russia"
   WEATHER_API_KEY = "Пропишите ваш ключ полученный на сайте 'worldweatheronline'"
   WEATHER_URL = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
~~~
#### Настройка в файле config.py:
~~~
Также в файле config.py пропишем следующие строки:
1. basedir = os.path.abspath(os.path.dirname(__file__))
2. SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'db.sqlite3')
3. SQLALCHEMY_TRACK_MODIFICATIONS = False
4. WEATHER_API_KEY = "Добавим в параметр SECRET_KEY"
5. REMEMBER_COOKIE_DURATION = timedelta(days=5)
~~~
## Запуск
~~~
Чтобы запустить, выполните в консоли:
Linux и Mac: (выполнить в консоли команду -
chmod +x run.sh - это сделает файл исполняемым).
После этого ввести в консоли ./run.sh
Windows: run.bat
~~~
