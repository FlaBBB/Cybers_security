FROM python:3

RUN useradd -U -m -s /bin/bash ctf

RUN apt-get update && apt-get upgrade -y
RUN apt install -y python3 socat
WORKDIR /home/ctf

COPY ./* ./

USER ctf

RUN pip install --no-cache-dir pycryptodome
CMD socat TCP-L:17425,fork EXEC:"python3 /home/ctf/soal.py",reuseaddr,stderr