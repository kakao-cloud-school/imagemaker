FROM python:3.8-slim

WORKDIR /app
RUN apt-get update && apt-get install -y gcc libffi-dev musl-dev
RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD ["streamlit", "run", "app.py"]
