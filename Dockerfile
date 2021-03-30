FROM python:3.8.5

ADD $PWD /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD python vaccineFinder.py