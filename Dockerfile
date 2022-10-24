FROM python:3.10-slim

WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY project /project
COPY fixtures.json .
COPY security.json .
COPY create_tables.py .
COPY create_security.py .
COPY load_fixtures.py .
COPY run.py .

ENV FLASK_APP=run
ENV FLASK_ENV=development

RUN python3 create_tables.py
RUN python3 load_fixtures.py

RUN python3 -m pylint project

CMD flask run --host=0.0.0.0 --port=80
