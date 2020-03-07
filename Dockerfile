FROM python:3.6

RUN mkdir -p /app
WORKDIR /app
COPY . /app
EXPOSE 5000
RUN pip install -r requirements.txt

ENTRYPOINT python3 app.py
