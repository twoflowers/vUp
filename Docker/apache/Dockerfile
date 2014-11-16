FROM eboraas/apache
MAINTAINER vUp

# Update the default apache site with the config we created.
ADD vup.conf /etc/apache2/sites-enabled/000-default.conf

# Copy site into place.
ADD www /var/www


