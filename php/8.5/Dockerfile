FROM php:8.5.0-cli

ARG INSTALL_CHROMIUM=false

ADD https://github.com/mlocati/docker-php-extension-installer/releases/latest/download/install-php-extensions /usr/local/bin/

RUN apt-get update -yqq && apt-get install -yqq --no-install-recommends \
    bash \
    curl \
    ghostscript \
    libfreetype6-dev \
    g++ \
    gcc \
    libicu-dev \
    imagemagick \
    libc-dev \
    libzip-dev \
    make \
    mariadb-client \
    openssh-client \
    rsync \
    git \
 && if [ "$INSTALL_CHROMIUM" = "true" ]; then \
      apt-get install -yqq --no-install-recommends chromium; \
    fi \
 && rm -rf /var/lib/apt/lists/*

RUN chmod +x /usr/local/bin/install-php-extensions && \
    install-php-extensions \
    @composer \
    bcmath \
    bz2 \
    calendar \
    exif \
    gd \
    gmp \
    imagick \
    intl \
    mongodb-stable \
    mysqli \
    opcache \
    pcntl \
    pdo_mysql \
    pdo_pgsql \
    pgsql \
    redis-stable \
    soap \
    sockets \
    xdebug \
    xsl \
    zip

COPY php/8.5/imagemagick-policy.xml .

RUN mv imagemagick-policy.xml /etc/ImageMagick-7/policy.xml

RUN echo 'memory_limit=-1' > /usr/local/etc/php/conf.d/zz-conf.ini

RUN echo 'xdebug.mode=coverage' > /usr/local/etc/php/conf.d/20-xdebug.ini

ENV PATH=./vendor/bin:/composer/vendor/bin:/root/.composer/vendor/bin:/usr/local/bin:$PATH

RUN composer global require "squizlabs/php_codesniffer=*"

# Node.js
RUN curl -sL https://deb.nodesource.com/setup_24.x | bash -
RUN apt-get install -y nodejs
RUN npm install npm@latest -g
RUN corepack enable && corepack prepare yarn@stable --activate
RUN command -v yarn
RUN command -v node
RUN command -v npm


RUN apt-get purge -y gcc g++ make && \
    apt-get -y autoremove && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf ~/.composer/cache/*

WORKDIR /var/www
