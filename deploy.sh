#!/usr/bin/env bash
set -ex

apt-get -y install zsh curl ufw
ufw allow 22
ufw allow 80
ufw allow 443
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw -f enable

apt-get update

sysctl -w net.ipv6.conf.all.disable_ipv6=0

apt-get install -y git supervisor nginx mysql-server python3-pip redis-server
pip3 install jinja2 flask gunicorn pymysql flask_sqlalchemy flask_admin marrow.mailer gevent flask_mail Celery

mysql  -u root -pCwm6213812. -e "DELETE FROM mysql.user WHERE User='';"
mysql  -u root -pCwm6213812. -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
mysql  -u root -pCwm6213812. -e "DROP DATABASE IF EXISTS test;"
mysql  -u root -pCwm6213812. -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"

mysql  -u root -pCwm6213812. -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Cwm6213812.';"

rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

cp /var/www/cwm/cwm.nginx /etc/nginx/sites-enabled/cwm

cp /var/www/cwm/cwm.conf /etc/supervisor/conf.d/cwm.conf

cp /var/www/cwm/celery.conf /etc/supervisor/conf.d/celery.conf

cd /var/www/cwm

python3 reset.py

service supervisor restart
service nginx restart

echo 'deploy success'