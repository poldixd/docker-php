#!/usr/bin/env bash

# Thx to edbizarro
#
# https://github.com/edbizarro/gitlab-ci-pipeline-php/blob/46f0ffa0631ccf161ee64c9f0929587f792255e6/php/scripts/cleanup.sh

set -euo pipefail

apt-get purge -yq --auto-remove -o APT::AutoRemove::RecommendsImportant=false -o APT::AutoRemove::SuggestsImportant=false \
    apt-utils \
    build-essential \
    dpkg-dev \
    file \
    libc-client-dev \
    libc-dev \
    libpcre3-dev \
    pkg-config \
    re2c \
    wget

apt-get autoremove -yq --purge
apt-get autoclean -yq
apt-get clean
rm -rf /var/cache/apt/ /var/lib/apt/lists/* /var/log/* /tmp/* /var/tmp/* /usr/share/doc /usr/share/doc-base /usr/share/groff/* /usr/share/info/* /usr/share/linda/* /usr/share/lintian/overrides/* /usr/share/locale/* /usr/share/man/* /usr/share/locale/* /usr/share/gnome/help/*/* /usr/share/doc/kde/HTML/*/* /usr/share/omf/*/*-*.emf