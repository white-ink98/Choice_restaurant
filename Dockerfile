FROM python:3.11

WORKDIR /Choice_restaurant

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /Choice_restaurant/