# Hardening Services & Standarts

## Hardening Standarts
1. Delete all sudoers except root
2. Delete all users except root `userdel -r <username>` and create new user `adduser <username>`
3. Change root password
4. Check all open ports `netstat -tulpn` or `ss -tulpn`
5. Check with linpeas.sh
6. Check if any interesting groups (like docker, lxd, etc)
7. Check if any interesting cronjobs `crontab -l`
8. Check if any interesting services `systemctl list-units --type=service` (likely not used in this LKS Prov case)
9. Check if any vulnerable applications `dpkg -l` (likely not used in this LKS Prov case, used only if application appears in linpeas.sh)

## Hardening Services
### SSH : (Dir location: `/etc/ssh/sshd_config`)
1. Disable root login `PermitRootLogin no`
2. Disable password authentication `PasswordAuthentication no`
3. Enable public key authentication `PubkeyAuthentication yes`
4. Disable empty passwords `PermitEmptyPasswords no`
5. Generate SSH keys `ssh-keygen`

### FTP : (Dir location: `/etc/vsftpd.conf`)
1. Disable anonymous login `anonymous_enable=NO`
2. Disable write access `write_enable=NO`
3. Enable chroot jail `chroot_local_user=YES`


### Samba : (Dir location: `/etc/samba/smb.conf`)
1. Disable anonymous login `map to guest = never`
2. Disable write access `writable = no`

### Apache :
1. Run auto-script to hardening ssh 
```
Thats already contain:
1. Instal Modsecurity and use OWASP rules + settings them all
2. Disable directory listing with `a2dismod --force autoindex`
```

2. Disable server signature with `ServerSignature Off` and `ServerTokens Prod` in `/etc/apache2/apache2.conf` (not used in this LKS Prov case)

### Nginx :
1. Disable server signature with `server_tokens off;` in `/etc/nginx/nginx.conf` (not used in this LKS Prov case)
2. Install Modsecurity (this hardening might be takes quite long time)
```
Steps: (Ref: https://www.tecmint.com/install-modsecurity-nginx-debian-ubuntu/)
1. Install dependencies `apt install libmodsecurity3`
2. Clone Nginx modsecurity `git clone --depth 1 -b v3/master --single-branch https://github.com/SpiderLabs/ModSecurity /usr/local/src/ModSecurity/`
3. Move dir `cd /usr/local/src/ModSecurity/`
4. Install Sub Modules `sudo git submodule init` & `sudo git submodule update`
5. Build environment `sudo ./build.sh` & `sudo ./configure`
6. Install library `sudo make -j4` (this process can takes 25 min) & `sudo make install`
7. Install Nginx connector `git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git /usr/local/src/ModSecurity-nginx/`
8. Move dir `cd /usr/local/src/ModSecurity-nginx/`
9. Install build dependencies `sudo apt build-dep nginx` & `sudo apt install uuid-dev`
10. Compile Nginx connector `sudo ./configure --with-compat --add-dynamic-module=/usr/local/src/ModSecurity-nginx
11. Build Nginx connector `sudo make modules`
12. Copy builded modules `sudo cp objs/ngx_http_modsecurity_module.so /usr/share/nginx/modules/`
13. Load module in `/etc/nginx/nginx.conf` and Enable Modsecurity in all virtual hosted 
load_module modules/ngx_http_modsecurity_module.so; 
modsecurity on; 
modsecurity_rules_file /etc/nginx/modsec/main.conf;
```
![Enable-Mod_Security-for-Nginx-vHosts](https://github.com/FlaBBB/Cybers_security/assets/91487840/f62f8035-002c-4f03-a9b8-7f28f815cd4e)
```
14. Create main.conf directory `sudo mkdir /etc/nginx/modsec/` and copy Modsecurity conf `sudo cp /usr/local/src/ModSecurity/modsecurity.conf-recommended /etc/nginx/modsec/modsecurity.conf`
15. Edit main.conf `sudo nano /etc/nginx/modsec/main.conf` and change `SecRuleEngine DetectionOnly` to `SecRuleEngine On`
16. Create `/etc/nginx/modsec/main.conf` and append `Include /etc/nginx/modsec/modsecurity.conf` inside the file
17. (Additionally) Copy unicode mapping file `sudo cp /usr/local/src/ModSecurity/unicode.mapping /etc/nginx/modsec/`
18. Test the config `sudo nginx -t` and restart nginx `sudo systemctl restart nginx`
19. Download OWASP rule `wget https://github.com/coreruleset/coreruleset/archive/v3.3.0.tar.gz`
20. Extract the file `tar -xvzf v3.3.0.tar.gz`
21. Move the file `sudo mv coreruleset-3.3.0/ /etc/nginx/modsec/`
22. Rename the conf file `sudo mv /etc/nginx/modsec/coreruleset-3.3.0/crs-setup.conf.example /etc/nginx/modsec/coreruleset-3.3.0/crs-setup.conf`
23. Edit ModSecurity conf file and append below text to the file
Include /etc/nginx/modsec/coreruleset-3.3.0/crs-setup.conf 
Include /etc/nginx/modsec/coreruleset-3.3.0/rules/*.conf 
![Configure-ModSecurity-Rules](https://github.com/FlaBBB/Cybers_security/assets/91487840/6854b5fe-4ba8-4d8c-8115-52ba8b2ba25d)
24. Finally restart nginx `sudo systemctl restart nginx`
```
3. Disable directory listing with `autoindex off;` in `/etc/nginx/sites-available/default` (not used in this LKS Prov case)

### MySQL :
1. Disable remote login `bind-address = 127.0.0.1` in `/etc/mysql/mysql.conf.d/mysqld.cnf`
2. Remove anonymous users `DROP USER ''@'localhost';`
3. Change root password `ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';`

### PHP :
1. Disable remote code execution `allow_url_fopen = Off` and `allow_url_include = Off` in `/etc/php/7.4/apache2/php.ini`
2. Check if there is any backdoor module installed `php -m`
