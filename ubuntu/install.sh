#!/usr/bin/env bash

apt update && apt upgrade

apt install build-essential apache2 postgresql libpq-dev python3-dev virtualenv \
libapache2-mod-wsgi-py3 npm -y

npm install -g bower

psql -u postgres -c "alter user postgres with password 'ABC123#$'"

psql -c "create database comprafacil"


cd /var/www

git clone https://bitbucket.org/xangcastle/comprafacil.git

cd comprafacil

mkdir venv

virtualenv venv/ -p python3

source venv/bin/activate

pip install -r requirements.txt

