FROM python:3.11-slim

WORKDIR /app

COPY guestbook.py /app/
RUN pip install flask

VOLUME /data

CMD ["python", "guestbook.py"]
