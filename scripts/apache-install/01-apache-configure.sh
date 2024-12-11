#!/bin/bash

set -euo pipefail

export apacheConf=/etc/apache2/sites-available/choco.conf

createUser() {
    username="${1}"

  echo "Creating ${username} system user"
  if ! getent passwd "${username}" >/dev/null ; then
    sudo /usr/sbin/adduser "${username}"
    sudo /usr/sbin/usermod -aG sudo "${username}"
    echo "${username} ALL=(ALL) NOPASSWD:ALL" | sudo tee -a /etc/sudoers.d/90-cloud-ini-users
    rsync --archive --chown="${username}:${username}" ~/.ssh "${home_dir}"
  fi
}


createUser choco

sudo ufw allow 'Apache'
sudo ufw allow 'OpenSSH'
sudo ufw allow 'Apache Full'
sudo ufw allow 'Apache Secure'
sudo mkdir -p -m=0755 /var/www/natemollica-dev/net/
sudo chown -R choco:choco /var/www/natemollica-dev/net

cat <<-EOF > "${apacheConf}"
<VirtualHost *:80>
    ServerAdmin nathanmollica@gmail.com
    ServerName natemollica-dev.net
    ServerAlias www.natemollica-dev.net
    DocumentRoot /var/www/natemollica-dev/net
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOF

cat <<-EOF > /var/www/natemollica-dev/net/index.html
<html>
    <head>
        <title>Welcome to natemollica-dev.net!</title>
    </head>
    <body>
        <h1>Success!  The natemollica-dev.net virtual host is working!</h1>
    </body>
</html>
EOF

sudo a2ensite choco.conf
sudo a2dissite 000-default.conf
sudo apache2ctl configtest
sudo service apache2 restart

sudo certbot --apache --non-interactive --agree-tos --redirect --email nathanmollica@gmail.com --domains choco.natemollica-dev.net --domains natemollica-dev.net