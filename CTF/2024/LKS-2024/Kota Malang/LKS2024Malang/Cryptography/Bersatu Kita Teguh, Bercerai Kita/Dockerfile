FROM ubuntu:22.04
RUN apt-get update && \
    apt-get -y install python3 socat python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/nobody
COPY src .

ENV FLAG=LKS2024Malang{D3Ar_G0d_CrYpt0G12ApHy_1S_T0o_3AzY_P3aZ1e_G1v3_M3_M0RE3}

USER nobody
EXPOSE 12000
CMD socat TCP-LISTEN:12000,reuseaddr,fork EXEC:"python3 -u chall.py"
