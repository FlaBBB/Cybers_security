FROM python:3.11

EXPOSE 5000


RUN apt update && apt upgrade -y && apt update --fix-missing
RUN apt install curl python3 nano socat python3-pip -y
RUN pip install pycryptodome

RUN mkdir /app
COPY ./challenge.py /app/challenge.py
COPY ./flag.txt /app/flag.txt
WORKDIR /app

RUN chown -R 755 /app/

CMD socat TCP-LISTEN:5000,reuseaddr,fork EXEC:"python3 -u /app/challenge.py"