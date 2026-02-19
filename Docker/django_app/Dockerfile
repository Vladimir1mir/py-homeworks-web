FROM python:3.10-alpine

WORKDIR /apps

COPY ./apps /apps

RUN pip install -r /apps/requirements.txt

ENV SECRET_KEY = 'django-insecure-nw^y+m^wmxza1asgk+)!ua2qx9)g+#v=6%76-9i8i(6eqiw94j'
ENV DEBUG = True

RUN python manage.py migrate
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]
