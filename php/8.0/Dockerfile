FROM php:8.0

ENV IMAGE_USER=php
ENV HOME=/home/$IMAGE_USER

USER root

WORKDIR /tmp

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
COPY ./php/scripts/*.sh /tmp/
RUN chmod +x /tmp/*.sh

RUN apt-get update -yqq

RUN apt-get install \
    git \
    imagemagick \
    libzip-dev \
    libonig-dev \
    libcurl4-openssl-dev \
    libicu-dev \
    libpng-dev \
    libxml2-dev \
    libbz2-dev \
    libmagickwand-dev \
    libfreetype6-dev \
    libjpeg-dev \
    libwebp-dev \
    unzip \
    zip \
    -yqq

RUN docker-php-ext-install \
    mbstring  \
    pdo_mysql  \
    curl \
    intl \
    xml \
    zip \
    bz2 \
    pcntl

RUN docker-php-ext-configure gd --with-freetype --with-jpeg --with-webp \
    && docker-php-ext-install gd

RUN pecl install imagick redis && docker-php-ext-enable imagick redis

RUN adduser --disabled-password --gecos "" $IMAGE_USER && \
  echo "$IMAGE_USER  ALL = ( ALL ) NOPASSWD: ALL" >> /etc/sudoers && \
  echo 'memory_limit=1024M' > /usr/local/etc/php/conf.d/zz-conf.ini && \
  mkdir -p /var/www/html \
  && rm -rf ~/.composer/cache/* \
  && chown -R $IMAGE_USER:$IMAGE_USER /var/www $HOME \
  && bash ./cleanup.sh

USER $IMAGE_USER

WORKDIR /var/www/html