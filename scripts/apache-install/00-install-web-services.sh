#!/bin/bash

set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

function install_dependencies() {
echo '[+] Updating apt package lists (apt-get update)'
sudo --preserve-env=DEBIAN_FRONTEND \
  apt update 1>/dev/null

echo '[+] Installing additional dependencies via apt (apt install)'
sudo --preserve-env=DEBIAN_FRONTEND \
    apt install --yes 1>/dev/null \
        apache2 \
        php \
        libapache2-mod-php \
        php-cli \
        php-cgi \
        php-mysql \
        php-pgsql \
        certbot \
        python3-certbot-apache \
    ;
}

install_dependencies

echo "+++++ Host OS Configuration Complete!"
