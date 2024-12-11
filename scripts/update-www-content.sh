#!/bin/bash

set -euo pipefail

[[ ! ( "${HOSTNAME}" =~ choco ) ]] && exit 1

export chocoSiteRoot=/var/www/natemollica-dev
export chocoSite="${chocoSiteRoot}"/net

git clone https://github.com/natemollica-nm/web-server #  --rebase

rm -rf "${chocoSiteRoot}"/docs/* "${chocoSite}"/*

cp --recursive Files/docs/* "${chocoSiteRoot}"/docs/ 
cp --recursive Files/www/* "${chocoSite}"/

sudo service apache2 restart