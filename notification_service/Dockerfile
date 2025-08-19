FROM python:3.10-slim

WORKDIR /spn
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

ENV PYTHONPATH=/spn

CMD python3 service.py