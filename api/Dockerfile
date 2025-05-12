FROM python:3.12

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]