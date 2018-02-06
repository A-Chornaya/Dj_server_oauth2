# Dj_server_oauth2
Django Server
==============
Example client "Dj_client_oauth2":
https://github.com/A-Chornaya/Dj_client_oauth2.git


Installation
=============

Clone the repository:

```
https://github.com/A-Chornaya/Dj_server_oauth2.git
```

Create a virtual environment and install requirements:

```
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

Create the database:

```
$ python manage.py makemigrations server
$ python manage.py migrate
```

Configuration
=============

Set in the dj_server/settings.py:
EXPIRE_DELTA
EXPIRE_DELTA_PUBLIC
EXPIRE_CODE_DELTA
TOKEN_TYPE



Start the project
=============

```
$ python manage.py runserver 8080
```

The "Django OAuth2 Client" start at the port 8070



Open in browser
=============
Go to http://localhost:8080/server/ in your browser
You should see the index page, where you can register you client app
In the head of the page you can log in (sign up)/log out as a user.


