python manage.py makemigrations common
python manage.py migrate
python manage.py crontab remove
python manage.py crontab add
python manage.py collectstatic
yes
python manage.py runserver 8000 --noreload
