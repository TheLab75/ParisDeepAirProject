FROM python:3.10.6-buster
WORKDIR /code
COPY . ParisDeepAirProject
RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install ./ParisDeepAirProject
CMD uvicorn ParisDeepAirProject.workflow.api:app --host 0.0.0.0 --port $PORT
