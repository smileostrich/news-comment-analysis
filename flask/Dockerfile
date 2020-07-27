FROM python:3

# ENV PYTHONUNBUFFERED 0

# RUN apt-get update

# RUN apt-get install -y software-properties-common
# RUN apt-get update
# RUN apt-get install -y --no-install-recommends python3 python3-dev python3-pip python3-setuptools python3-wheel gcc

#RUN python3 -m pip install pip --upgrade

# CMD ["python3", "run.py"]

ENV PYTHONDONTWRITEBYTECODE=True

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

ADD . /usr/src/app