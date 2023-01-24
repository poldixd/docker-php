FROM php:8.2-alpine

ADD https://github.com/mlocati/docker-php-extension-installer/releases/latest/download/install-php-extensions /usr/local/bin/

RUN apk add --no-cache \
    bash \
    chromium \
    curl \
    freetype-dev \
    g++ \
    gcc \
    git \
    icu-dev \
    icu-libs \
    imagemagick \
    libc-dev \
    libzip-dev \
    make \
    mysql-client \
    nodejs \
    npm \
    oniguruma-dev \
    openssh-client \
    postgresql-libs \
    rsync \
    yarn \
    zlib-dev

RUN chmod +x /usr/local/bin/install-php-extensions && \
    install-php-extensions \
    @composer \
    bcmath \
    bz2 \
    calendar \
    exif \
    gd \
    gmp \
    imagick-stable \
    intl \
    mongodb-stable \
    mysqli \
    opcache \
    pcntl \
    pcov \
    pdo_mysql \
    pdo_pgsql \
    pgsql \
    redis-stable \
    soap \
    xdebug-beta \
    xsl \
    zip

RUN echo 'xdebug.mode=coverage' > /usr/local/etc/php/conf.d/20-xdebug.ini && \
  echo 'memory_limit=-1' > /usr/local/etc/php/conf.d/zz-conf.ini && \
  rm -rf ~/.composer/cache/*

ENV PATH ./vendor/bin:/composer/vendor/bin:/root/.composer/vendor/bin:/usr/local/bin:$PATH

RUN composer global require "squizlabs/php_codesniffer=*"

WORKDIR /var/www