FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
VOLUME /app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r /app/requirements.txt
EXPOSE 80
COPY . /app
CMD [ "gunicorn"  , "-b", "0.0.0.0:80", "app:app" ]