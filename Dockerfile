FROM python:3.11.9

WORKDIR /crud

COPY app.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
