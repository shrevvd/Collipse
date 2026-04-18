# Collipse

Музыкальная социальная сеть с подбором собеседников по музыкальным предпочтениям.

## Технологии
- Django 7
- PostgreSQL
- Bootstrap 5

## Установка
```bash
git clone https://github.com/shrevvd/Collipse.git
cd Collipse
python -m venv venv
source venv/Scripts/activate  # для Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
