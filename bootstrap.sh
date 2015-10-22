#!/usr/bin/env bash

# install required packages
apt-get update
apt-get install -y python3 python3-pip redis-server
apt-get build-dep -y python3-lxml

# bot root directory
BOT_DIR='/vagrant'

# install required python packages
pip3 install -r $BOT_DIR/requirements.txt

# run bot
python3 $BOT_DIR/mr_roboto.py $BOT_DIR/settings.ini
