# syntax=docker/dockerfile:1
FROM node:26.13.1-trixie-slim AS node
FROM composer:2.11.2 AS composer
FROM mlocati/php-extension-installer:2.13.3 AS extensions

FROM php:8.6.0-cli-trixie AS runtime

ARG INSTALL_CHROMIUM=false
# PHP 8.6 support currently requires these extension prereleases.
ARG REDIS_VERSION=6.4.0RC1
# Install the upstream release tag; this prerelease is not on PECL.
ARG XDEBUG_SOURCE=xdebug/xdebug@3.6.0alpha1

COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules/npm /usr/local/lib/node_modules/npm
COPY --from=composer /usr/bin/composer /usr/local/bin/composer
COPY --from=extensions /usr/bin/install-php-extensions /usr/local/bin/install-php-extensions

# Pinned PECL releases still use XtOffsetOf, removed in PHP 8.6.
RUN --mount=type=bind,source=php/common,target=/tmp/php-image \
    CFLAGS="$CFLAGS -DXtOffsetOf=offsetof" sh /tmp/php-image/install.sh

ENV PATH="./vendor/bin:/usr/local/bin:$PATH"

WORKDIR /var/www

FROM runtime AS test
RUN --mount=type=bind,source=tests,target=/tmp/image-tests \
    sh /tmp/image-tests/smoke.sh "$INSTALL_CHROMIUM"
