FROM python:alpine3.8

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN  pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
