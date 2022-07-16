# logs-backend
LOGS - A real time tracking of student's learning outcomes and their academic progress across schools

## Setup:

Create a virtual environment
```
python -m venv name
```
Connect to virtual environment (Windows):
```
name\Scripts\activate.bat
```

Clone the repo:
```
git clone https://github.com/fausan123/locus-backend.git
```
Goto the created repo folder and install the requirements file:
```
pip install -r requirements.txt
```
Initialise database:
``` 
python manage.py makemigrations
python manage.py migrate
```
To create a superuser for viewing the admin interface:
```
python manage.py createsuperuser
```
Finally, to run the server:
```
python manage.py runserver
```

## View APIs
To view the developed apis, run the server and goto http://localhost:8000/. You will be directed to an API documentation
