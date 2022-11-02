FROM python:3.10-slim
WORKDIR /usr/app
COPY . .
RUN pip install -r requirements.txt
CMD [ "gunicorn", "main:app", "-b", "0.0.0.0" ]
