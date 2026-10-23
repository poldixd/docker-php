# syntax=docker/dockerfile:1
FROM node:24.22.1-trixie-slim AS node
FROM composer:2.10.3 AS composer
FROM mlocati/php-extension-installer:2.12.3 AS extensions

FROM php:8.4.27-cli-trixie AS runtime

ARG INSTALL_CHROMIUM=false

COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules/npm /usr/local/lib/node_modules/npm
COPY --from=composer /usr/bin/composer /usr/local/bin/composer
COPY --from=extensions /usr/bin/install-php-extensions /usr/local/bin/install-php-extensions

RUN --mount=type=bind,source=php/common,target=/tmp/php-image \
    sh /tmp/php-image/install.sh

ENV PATH="./vendor/bin:/usr/local/bin:$PATH" \
    XDEBUG_MODE=off

WORKDIR /var/www

FROM runtime AS test
RUN --mount=type=bind,source=tests,target=/tmp/image-tests \
    sh /tmp/image-tests/smoke.sh "$INSTALL_CHROMIUM"
