#!/bin/bash
sudo apt update
sudo apt install libapache2-mod-evasive -y

cat <<EOT >> /etc/apache2/mods-enabled/evasive.conf
DOSHashTableSize 3097
DOSPageCount 2
DOSSiteCount 50
DOSPageInterval 1
DOSSiteInterval 1
DOSBlockingPeriod 10
DOSLogDir "/var/log/apache2/"
EOT

sudo systemctl restart apache2
