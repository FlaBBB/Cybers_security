#!/bin/bash
# install ModSecurity
sudo apt update
sudo apt install libapache2-mod-security2 -y

sudo a2enmod headers
sudo a2dismod --force autoindex
sudo systemctl restart apache2

# configure Modsecurity
sudo cp /etc/modsecurity/modsecurity.conf-recommended  /etc/modsecurity/modsecurity.conf
sudo sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/modsecurity/modsecurity.conf
sudo systemctl restart apache2

# setup crs owasp
sudo rm -rf /usr/share/modsecurity-crs
sudo wget https://github.com/coreruleset/coreruleset/archive/refs/tags/v3.3.0.tar.gz
sudo tar -xzf v3.3.0.tar.gz
sudo mv coreruleset-3.3.0 /usr/share/modsecurity-crs
sudo cp /usr/share/modsecurity-crs/crs-setup.conf.example /usr/share/modsecurity-crs/crs-setup.conf
sudo mv /usr/share/modsecurity-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example /usr/share/modsecurity-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf

# enabling in apache
sudo echo '<IfModule security2_module>' > /etc/apache2/mods-available/security2.conf
sudo echo '	SecDataDir /var/cache/modsecurity' >> /etc/apache2/mods-available/security2.conf
sudo echo '	Include /usr/share/modsecurity-crs/crs-setup.conf' >> /etc/apache2/mods-available/security2.conf
sudo echo '	Include /usr/share/modsecurity-crs/rules/*.conf' >> /etc/apache2/mods-available/security2.conf
sudo echo '</IfModule>' >> /etc/apache2/mods-available/security2.conf
sudo systemctl restart apache2
