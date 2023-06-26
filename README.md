# Toman Interview

Toman Interview Project

I chose Django and DjangoRestFramework for developing thie project.

## How to Run Manually

 - First create a virtualenv and activate it

```
python -m venv venv
source venv/bin/activate
```

- Install requirements
```
pip install -r requirements.txt
```

- Migrate migration files
```
python manage.py migrate
```

- Create super-user
```
python manage.py createsuperuser
```
enter your username and password

now you can run the project with the following command
```
python manage.py runserver 0.0.0.0:8000
```
`0.0.0.0` because project get visible through network 

## How to Run with Docker
Build docker image
```
docker build -t interview_project .
```

Run docker image with following command
```
docker run -p 8000:8000 -t interview_project
```

### TODO list
- add swagger for endpoints