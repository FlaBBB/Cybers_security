FROM rust:1.76.0

ENV DEBIAN_FRONTEND noninteractive

RUN apt update -y && \
    apt upgrade -y && \
    apt install socat -y

WORKDIR /usr/src/double-trouble
COPY ./Cargo.toml ./
COPY ./src ./src

RUN cargo build --release

ENTRYPOINT [ "socat", \
             "TCP-LISTEN:4322,fork,nodelay,reuseaddr,pktinfo,pf=ip4", \
             "EXEC:./target/release/double-trouble" ]
