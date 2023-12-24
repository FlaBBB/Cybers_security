FROM ubuntu:latest

EXPOSE 5000

ARG binary
ENV binary=${binary}

RUN apt update && apt upgrade -y && apt update --fix-missing
RUN apt install curl python3 netcat-openbsd vim nano socat python3-pip -y

RUN mkdir /challs
COPY $binary /challs/$binary
COPY aes.py /challs/aes.py
COPY flag.txt /challs/flag.txt
WORKDIR /challs

RUN chown -R 755 /challs/

CMD socat TCP-LISTEN:5000,reuseaddr,fork EXEC:"python3 -u /challs/$binary"