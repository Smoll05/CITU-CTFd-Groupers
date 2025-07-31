FROM php:7.0-apache

RUN mkdir /var/www/html/chal

RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf \
    # enable autoindex for directory listing
    && sed -i 's/Options -Indexes/Options Indexes/' /etc/apache2/conf-available/docker-php.conf \ 
    && a2enmod autoindex \
    && service apache2 restart

WORKDIR /var/www/html/chal

RUN useradd ctf-player
COPY . /var/www/html/chal

RUN chown -R root:ctf-player /var/www/html/chal \
    && find /var/www/html/chal -type d -exec chmod 755 {} + \
    && find /var/www/html/chal/images -type f -exec chmod 755 {} +

EXPOSE 10180

USER ctf-player

CMD ["apache2-foreground"]

