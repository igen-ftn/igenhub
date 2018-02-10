FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD requirements.txt /code
RUN pip install -r /code/requirements.txt
ADD . /code
VOLUME /code/igenapp/media
EXPOSE 8021
WORKDIR /code
CMD python manage.py runserver 0.0.0.0:8021
