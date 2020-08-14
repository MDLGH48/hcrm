FROM python:3.7.1

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["sh", "start.sh"]
