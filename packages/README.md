# vwa-accounts

Reusable Django accounts microservice and package

### Quick Start

- Add "accounts" to your INSTALLED_APPS setting like this:

```py
INSTALLED_APPS = [
    ...
    'accounts',
]
```

- Include de viewset into your urls.py like this:

```py
from accounts import views as account_views

router = routers.DefaultRouter()
router.register('users', account_views.UserViewSet, basename="user")

urlpatterns += router.urls
```

- In settings.py insert:

```py
AUTH_USER_MODEL = 'accounts.User'
```

- Run "python3 manage.py makemigrations" and "python3 manage.py migrate" to create the accounts models.

- Start the development server and visit http://127.0.0.1:8000/users/
to list all users and create one, you need to be authenticated to edit
and delete onde user in http://127.0.0.1:8000/users/<pk>/.

### Requirements

```
pip3 install django
pip3 install djangorestframework
pip3 install pillow
pip3 install pytest-django
```
