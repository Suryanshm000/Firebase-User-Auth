# Firebase-User-Auth

- This app is made using Django, DjangoRestFramework, Djongo and MongoDB

- To connect MongoDB with Django, I have used `Djongo`.

- Using a local mongodb database for storing the data.

# Screen Recording

https://github.com/Suryanshm000/Firebase-User-Auth/assets/65828169/d40f41e6-b15b-4c31-b7fa-2406ab4ed423


# Running at localhost

These are the steps to follow in order to run the project on local host: 
<br>

```
git clone https://github.com/Suryanshm000/Firebase-User-Auth.git`
```

```
cd Firebase-User-Auth
```

Virtual Environment setup
```
pip install virtualenv
python -m venv <name of environment>
cd <name of environment>/Scripts
activate
pip install -r requirements.txt
cd ..
cd ..
```

The *django server* is started via the following command.

```
python manage.py runserver
```

<br>

# URL references

```
http://127.0.0.1:8000/accounts/register/
http://127.0.0.1:8000/accounts/login/
http://127.0.0.1:8000/accounts/profile/view/
http://127.0.0.1:8000/accounts/profile/edit/
```

