sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql.service

sudo mysql

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '<password>';

sudo mysql_secure_installation

mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED WITH auth_socket;


CREATE USER 'phishing_user'@'localhost' IDENTIFIED WITH authentication_plugin BY '<password>';
FLUSH PRIVILEGES;
GRANT ALL PRIVILEGES ON * . * TO 'phishing_user'@'localhost';

mysql -u phishing_user -p

ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/tmp/mysql.sock' (2)

mysqld --verbose --help | grep "socket"

socket                                                       /tmp/mysql.sock

sudo find / -type s | grep sql

/run/mysqld/mysqld.sock

vim ~/.my.cnf

[client]
socket=/run/mysqld/mysqld.sock

mysql -u phishing_user -p

CREATE DATABASE phishing;
USE phishing;

source <pathtolocalgit>/Prototype/dataset/index.sql;

pip install mysql-connector-python

