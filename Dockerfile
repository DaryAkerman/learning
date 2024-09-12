FROM python:3.8-slim

WORKDIR /app
RUN mkdir -p /app/templates

COPY app.py /app/
COPY /templates/ /app/templates

RUN pip install flask
EXPOSE 5000
CMD ["python3", "app.py"]