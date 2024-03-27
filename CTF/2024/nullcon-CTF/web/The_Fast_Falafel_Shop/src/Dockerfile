FROM php:7.2-apache
RUN apt-get update
COPY apache2.conf /etc/apache2/apache2.conf
COPY . /var/www/html/
RUN chmod -R 755 .
RUN chown -R root:www-data /var/www/html/
RUN chown -R www-data:www-data /var/www/html/uploads/
ENTRYPOINT bash entrypoint.sh
