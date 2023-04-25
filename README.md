![example workflow](https://github.com/shershlina/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg?event=push)
# foodgram
Project that allow you making your own cooking book and share it with community.
You can register on the site, creating recipes, add any recipe to favorite, you can follow
any author on the website. Also, you can add ingredients from recipes to the shopping cart
and download the shopping list.

Right now available at shershon.hopto.org

### Technologies:
![Django](https://img.shields.io/badge/django-3.2-%23092E20.svg?style=plastic&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DjangoREST-ff1709?style=plastic&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Python](https://img.shields.io/badge/python-3.9-3670A0?style=plastic&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=plastic&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=plastic&logo=nginx&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=plastic&logo=postgresql&logoColor=white)
![Yandex-Cloud](https://img.shields.io/badge/Yandex%20Cloud-025E8C?style=plastic)

### How to launch the project:

Clone the repository and open it through terminal.
In some cases you need to use "python" instead of "python3".

Create and activate virtual environment:
* If you have Linux/macOS

    ```
    python3 -m venv env 
    source env/bin/activate
    ```
* If you have windows

    ```
    python3 -m venv venv
    source venv/scripts/activate
    ```
```
python3 -m pip install --upgrade pip
```
Install all requirements from requirements.txt file:
```
pip install -r requirements.txt
```
Change the directory:
```
cd .\backend\
```
Make migrations:
```
python3 manage.py migrate
```
Fill the database with test data:
* If you want to upload a lot of ingredients:
  ```
  python3 manage.py import_csv
  ```
Run the project:
```
python3 manage.py runserver
```
In the second terminal you can run the frontend part of the project:
Change the directory:
```
cd .\frontend\
```
Install requirements:
```
npm i --legacy-peer-deps
```
If you see some critical vulnerabilities:
```
npm audit fix --force
```
Then start:
```
npm start
```

### How to launch the project through Docker:

Clone the repository and open it through terminal.
Note: You need to add winpty before the command in some cases.

Change the directory:
```
cd infra/
```
Expand containers:
```
docker-compose up -d --build 
```
Successively run migrations, create superuser, and collect static:
```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input 
```
If you want to add some ingredients and tags data:
```
docker-compose exec web python manage.py import_csv
```

Now you can visit webpage of project with your superuser on the http://localhost/admin/
API documentation and examples you can find at http://localhost/api/docs/redoc.html

### .env content template (you can find it in infra folder) located at infra/.env path:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

### Author of the project:
Lina Ivanova
