#!/bin/sh
set -eu
export DEBIAN_FRONTEND=noninteractive

case "$INSTALL_CHROMIUM" in
    true|false) ;;
    *) echo 'INSTALL_CHROMIUM must be true or false' >&2; exit 1 ;;
esac

apt-get update
apt-get install -y --no-install-recommends \
    bash ca-certificates curl ghostscript imagemagick git \
    libatomic1 libstdc++6 mariadb-client openssh-client rsync

# The installer manages and removes its own temporary build dependencies.
install-php-extensions \
    bcmath bz2 calendar exif gd gmp imagick-3.8.1 intl \
    mongodb-2.5.5 mysqli opcache pcntl pdo_mysql pdo_pgsql pgsql \
    redis-6.3.0 soap sockets xdebug-3.5.3 xsl zip

cp /tmp/php-image/imagemagick-policy.xml /etc/ImageMagick-7/policy.xml
printf '%s\n' 'memory_limit=-1' > /usr/local/etc/php/conf.d/zz-ci.ini
printf '%s\n' 'xdebug.mode=coverage' > /usr/local/etc/php/conf.d/zz-xdebug.ini

# npm is supplied with the pinned official Node image; avoid curl | bash.
ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm
ln -s /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx
npm install --global corepack@0.36.0
corepack enable
corepack install --global yarn@4.18.1

if [ "$INSTALL_CHROMIUM" = true ]; then
    # The extension installer may have cleared APT's package lists.
    apt-get update
    apt-get install -y --no-install-recommends chromium
    npx --yes playwright@1.64.0 install-deps
fi

apt-get clean
rm -rf /var/lib/apt/lists/* /root/.npm /tmp/pear
