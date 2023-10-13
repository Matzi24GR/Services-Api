FROM python:3.11.6-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
#RUN apk --update add bash curl
RUN pip3 install -r requirements.txt

COPY app/ src/

ENV FLASK_APP=src/app.py
ENV PYTHONPATH=src/

EXPOSE 80
#ENTRYPOINT python src/app.py
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:80", "app:app"]