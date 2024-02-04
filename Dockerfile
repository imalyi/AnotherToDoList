FROM python:3.10

ENV DockerHOME=/home/apps/todolist/

RUN mkdir -p $DockerHOME

RUN apt-get update -y -q
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential -y -q

WORKDIR $DockerHOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . $DockerHOME
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
