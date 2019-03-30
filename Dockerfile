FROM python:3

WORKDIR /app
COPY . .
RUN pip install -r webapp/requirements.txt

WORKDIR /app
CMD [ "python", "./server.py" ]
