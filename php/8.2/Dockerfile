FROM php:8.2.0RC4

WORKDIR /tmp

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
COPY ./php/scripts/*.sh /tmp/
RUN chmod +x /tmp/*.sh

RUN apt-get update -yqq

RUN apt-get install \
    git \
    chromium \
    imagemagick \
    libgmp-dev \
    libpq-dev \
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
    libxslt1-dev \
    libssl-dev \
    libnss3 \
    locales \
    locales-all \
    unzip \
    zip \
    -yqq

RUN docker-php-ext-install \
    bcmath \
    bz2 \
    calendar \
    curl \
    exif \
    gmp \
    intl \
    mbstring \
    mysqli \
    opcache \
    pcntl \
    pdo_mysql \
    pdo_pgsql \
    pgsql \
    soap \
    xml \
    xsl \
    zip

RUN docker-php-ext-configure gd --with-freetype --with-jpeg --with-webp \
    && docker-php-ext-install gd

RUN pecl install imagick mongodb redis xdebug && docker-php-ext-enable imagick mongodb redis xdebug

RUN echo 'xdebug.mode=coverage' > /usr/local/etc/php/conf.d/20-xdebug.ini && \
  echo 'memory_limit=1024M' > /usr/local/etc/php/conf.d/zz-conf.ini && \
  rm -rf ~/.composer/cache/* && \
  bash ./cleanup.sh

WORKDIR /var/www