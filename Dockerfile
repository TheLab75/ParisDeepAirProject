FROM python:3.10.6-buster
WORKDIR /code
COPY requirements_prod.txt requirements.txt
COPY myapp myapp
RUN pip install .
CMD unicorn workflow.api:app --host 0.0.0.0 --port $PORT
