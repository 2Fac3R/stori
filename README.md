# STORI

This repository is my implementation for the technical code challenge by Stori.

## Installation

Clone this repository

```sh
git clone https://github.com/2Fac3R/stori.git
```

Create and start your virtual environment [venv](https://docs.python.org/3/library/venv.html)

```sh
python3 -m venv .venv
source .env/bin/activate
```

Install requirements. Use the package manager [pip](https://pip.pypa.io/en/stable/)

```sh
pip install -r requirements.txt
```

Configure database settings.py to use PostgreSQL (or use SQLite by default)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<databasename>',
        'USER': '<username>',
        'PASSWORD': '<password>',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

Configure email settings with your credentials, rename *.env.example* to *.env*

```
EMAIL_HOST=<host>
EMAIL_HOST_USER=<your-username>
EMAIL_HOST_PASSWORD=<your-password>
```

Make migrations and migrate

```sh
python3 manage.py makemigrations
python3 manage.py migrate
```

Create a superuser

```sh
python3 manage.py createsuperuser
```

Run the server

```sh
python3 manage.py runserver
```


## Site

Two views are provided (*index, detail*) for each model. No root view (*'/'*) is provided yet.

Available urls:

    admin/
    accounts/
    accounts/<int:pk>
    transactions/
    transactions/<int:pk>

## Admin site
Log in with your superuser account.

    http://127.0.0.1:8000/admin

Now you have access to the administration site.

Manage models:

    http://127.0.0.1:8000/admin/transactions/account/
    http://127.0.0.1:8000/admin/transactions/transaction/
    ...

Create a new resource:

    http://127.0.0.1:8000/admin/transactions/<model>/add/

Edit a resource:

    http://127.0.0.1:8000/admin/transactions/<model>/<id>/change/

Delete a resource:

    http://127.0.0.1:8000/admin/transactions/<model>/<id>/delete/

Filter:

    http://127.0.0.1:8000/admin/transactions/<model>/?<field>=<value>
    http://127.0.0.1:8000/admin/transactions/transaction/?account__id__exact=<id>
    http://127.0.0.1:8000/admin/transactions/transaction/?month=<month>
    ...

Upload csv transactions file (*ex. transactions.csv*):

    http://127.0.0.1:8000/admin/transactions/transaction/upload-csv/

It handles the structure: **id,date,transaction** (see the following example). Date format **%m/d%**.

    1,7/2,-12.22
    2,7/3,+22.22
    3,7/4,+32.22
    4,12/5,-42.23
    5,7/6,-12.21
    6,1/6,-124.21
    7,2/4,+12.21
    ...

## Tests

You can run all tests

```sh
python3 manage.py test
```

Or individually

```sh
python3 manage.py test transactions.tests.<folder>.test_<model_in_plural>
python3 manage.py test transactions.tests.models.test_account
python3 manage.py test transactions.tests.views.test_account
...
```

## TODO:
* Improve reused code in email feature
* Add tests for uploader and email features

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Any feedback is appreciated.