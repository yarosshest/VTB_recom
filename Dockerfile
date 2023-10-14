FROM python:3.10
WORKDIR /api
ENV PYTHONPATH "${PYTHONPATH}:/api"
RUN pip install --upgrade pip

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY config.ini .
COPY main.py .

COPY /database /api/database
COPY /api /api/api

CMD [ "python", "api/api.py"]