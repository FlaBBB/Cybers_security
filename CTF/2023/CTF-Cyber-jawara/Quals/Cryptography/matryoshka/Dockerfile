FROM python:3.9

EXPOSE 8000

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app.py /app/main.py
COPY ./challenge.py /app/challenge.py
COPY ./flag.txt /app/flag.txt
COPY ./static /app/static

CMD ["uvicorn", "main:app","--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]