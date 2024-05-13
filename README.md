BackEnd iSi Technology test task

## About Project
 Django, DRF project. Has been implemented by Pavlo Ryndin.

 ### Basics

1. Fork/Clone
1. Activate a virtualenv
1. Install the requirements

### Create DB

Do migration

```sh
$ python manage.py migrate
```

## Run the Application

```sh
$ python manage.py runserver
```

Access the application at the address [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Accessible urls

```sh
'/admin'
'/register'
'/login'
'api/threads/create'
'api/threads/<thread_uuid>/delete'
'api/threads/'
'api/threads/messages/create'
'api/threads/<thread_uuid>/messages'
'api/threads/unread-messages'
```