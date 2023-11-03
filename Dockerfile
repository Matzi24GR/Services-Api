FROM python:3.11.6-alpine

WORKDIR /services-api

COPY requirements.txt requirements.txt
#RUN apk --update add bash curl
RUN pip3 install -r requirements.txt

COPY app/ app/

ENV FLASK_APP=app/app.py
ENV PYTHONPATH=app/

EXPOSE 80
#ENTRYPOINT python src/app.py
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:80", "app:app"]