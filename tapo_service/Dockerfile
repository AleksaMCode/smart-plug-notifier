FROM python:3.10-slim

WORKDIR /spn
COPY requirements.txt $WORKDIR
RUN pip3 install -r requirements.txt

COPY . $WORKDIR

CMD python3 service.py