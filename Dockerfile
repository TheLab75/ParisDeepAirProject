from python:3.10.6-buster
WORKDIR /code
COPY requirements.txt requirements.txt
COPY myapp myapp
RUN pip install -r requirements.txt
CMD unicorn workflow.api:app --host 0.0.0.0 --port $PORT
