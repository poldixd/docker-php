FROM php:8.3.4

ADD https://github.com/mlocati/docker-php-extension-installer/releases/latest/download/install-php-extensions /usr/local/bin/

RUN apt-get update -yqq

RUN apt-get install \
    git \
    bash \
    chromium \
    curl \
    libfreetype6-dev \
    g++ \
    gcc \
    git \
    libicu-dev \
    imagemagick \
    libc-dev \
    libzip-dev \
    make \
    mariadb-client \
    nodejs \
    npm \
    openssh-client \
    rsync \
    yarn \
    -yqq

RUN chmod +x /usr/local/bin/install-php-extensions && \
    install-php-extensions \
    @composer \
    bcmath \
    bz2 \
    calendar \
    exif \
    gd \
    gmp \
    imagick/imagick@master \
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
    xsl \
    zip

COPY php/8.3/imagemagick-policy.xml .

RUN mv imagemagick-policy.xml /etc/ImageMagick-6/policy.xml

RUN echo 'memory_limit=-1' > /usr/local/etc/php/conf.d/zz-conf.ini

ENV PATH ./vendor/bin:/composer/vendor/bin:/root/.composer/vendor/bin:/usr/local/bin:$PATH

RUN composer global require "squizlabs/php_codesniffer=*"

# Node.js
RUN curl -sL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs
RUN npm install npm@10 -g
RUN command -v node
RUN command -v npm

RUN apt-get purge -y gcc make && \
    apt-get -y autoremove && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf ~/.composer/cache/*

WORKDIR /var/www
