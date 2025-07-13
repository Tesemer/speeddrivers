FROM python:3.9

WORKDIR /app

ADD . /app
ADD config.cfg /app/config.cfg

RUN pip install -r requirements.txt

CMD ["python", "./driver_connection_handler.py"]