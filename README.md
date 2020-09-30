# curriculum-dev
A Django based web application to aid with curriculum development by analysing learning outcomes / learning objectives (LOs).

# Installation
Clone the repo:
```
git clone https://github.com/Aviemusca/curriculum-dev.git 
```
Change into the directory and create a new virtual environment.
Then, run
```
pip install -r requirements.txt
```
Create a postgres database and store the name, user and password of the database in, respectively, the DB_NAME, DB_USER and DB_PASS exported variables in the .env file.
Generate a secret key for django, e.g.
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
and store it in the SECRET_KEY exported variable in .env.
Source the environment file:
```
source .env
```
Then run 
```
python manage.py migrate
```
Next you will need to start a celery worker for asynchronous task management:
```
celery -A LO_analysis_project worker -l info
```
Finally, start the server:
```
python manage.py runserver
```
