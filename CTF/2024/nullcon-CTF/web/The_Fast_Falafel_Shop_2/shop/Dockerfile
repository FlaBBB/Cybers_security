FROM php:8.3-apache

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update -y && \
    apt upgrade -y && \
    apt install chromium -y && \
    apt install python3 -y && \
    apt install python3-pip -y && \
    pip3 install pyppeteer --break-system-packages

WORKDIR /opt

COPY ./scripts ./
COPY ./apache2.conf /etc/apache2/apache2.conf

COPY ./pages /var/www/html/
COPY ./images /var/www/html/images/

RUN mkdir -p /var/www/html/uploads

RUN chown -R www-data:www-data /var/www/

ENTRYPOINT [ "bash", "./entrypoint.sh" ]
