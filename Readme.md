# Hiker

Website for hikers to share their experiences and find new trails to explore.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software:

- Python 3.x
- Requirements from requirements.txt


### Installing

A step-by-step series of examples that tell you how to get a development environment running:

1. Clone the repository:
```bash
git clone https://github.com/elaiviaien/hiker_api.git
```

2. Navigate to the project directory:
```bash
cd hiker_api
```

3. Install the requirements:
```bash
pip install -r requirements.txt
```

4. Create and apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run the development server:
```bash
python manage.py runserver
```
or just run the following command to start the server with docker:
```
docker compose up -d
```

Navigate to http://localhost:8000 in your web browser to view the application.

## Built With

- Django Rest Framework
- Django
- Docker
- PostgreSQL
- Nginx
- Gunicorn