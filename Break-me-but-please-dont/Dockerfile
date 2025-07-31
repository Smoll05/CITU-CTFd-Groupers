FROM php:7.0-apache

# Create the challenge directory
RUN mkdir -p /var/www/html/chal

# Configure Apache
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Set the DocumentRoot to the challenge directory
RUN sed -i 's|DocumentRoot /var/www/html|DocumentRoot /var/www/html/chal|' /etc/apache2/sites-available/000-default.conf
RUN sed -i 's|<Directory /var/www/>|<Directory /var/www/html/chal/>|' /etc/apache2/sites-available/000-default.conf
RUN sed -i 's|</Directory>|</Directory>|' /etc/apache2/sites-available/000-default.conf

WORKDIR /var/www/html/chal

# Create user for security
RUN useradd ctf-player

# Copy the HTML file
COPY ./index.html /var/www/html/chal/

# Set proper permissions
RUN chown -R www-data:www-data /var/www/html/chal \
    && chmod -R 755 /var/www/html/chal \
    && chmod 644 /var/www/html/chal/index.html

# Enable Apache modules if needed
RUN a2enmod rewrite

EXPOSE 80

# Start Apache in foreground
CMD ["apache2-foreground"]

