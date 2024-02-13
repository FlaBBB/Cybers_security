FROM ubuntu:jammy
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -yq xinetd git gcc make python3
RUN groupadd -r ctf && useradd -r -g ctf ctf

WORKDIR /home/ctf

# clone and build minivm pure from github
RUN git clone https://github.com/FastVM/minivm.git --recursive && \
    cd minivm && \
    git submodule update --init && \
    # make it fast
    make -Bj OPT='-O3 -flto'

RUN echo '#!/bin/bash\nservice xinetd restart && /bin/sleep infinity' > /etc/init.sh
RUN echo 'service ctf\n\
{\n\
    disable = no\n\
    socket_type = stream\n\
    protocol = tcp\n\
    wait = no\n\
    user = ctf\n\
    type = UNLISTED\n\
    port = 31337\n\
    bind = 0.0.0.0\n\
    server = /home/ctf/run.py\n\
}' > /etc/xinetd.d/ctf

COPY run.py /home/ctf/run.py
RUN echo 'TCF2024{kali_ini_bener}' > /home/ctf/flag.txt

RUN chmod 400 /etc/xinetd.d/ctf
RUN chmod 550 /home/ctf/run.py /etc/init.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chown -R ctf:ctf /home/ctf

RUN service xinetd restart
