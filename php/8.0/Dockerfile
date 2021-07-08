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
    libzip-dev \
    libonig-dev \
    libcurl4-openssl-dev \
    libicu-dev \
    libpng-dev \
    libxml2-dev \
    libbz2-dev \
    -yqq

RUN docker-php-ext-install \
    mbstring  \
    pdo_mysql  \
    curl \
    intl \
    gd \
    xml \
    zip \
    bz2 \
    pcntl

RUN pecl install redis && docker-php-ext-enable redis

RUN adduser --disabled-password --gecos "" $IMAGE_USER && \
  echo "$IMAGE_USER  ALL = ( ALL ) NOPASSWD: ALL" >> /etc/sudoers && \
  mkdir -p /var/www/html \
  && rm -rf ~/.composer/cache/* \
  && chown -R $IMAGE_USER:$IMAGE_USER /var/www $HOME \
  && bash ./cleanup.sh

USER $IMAGE_USER

WORKDIR /var/www/html