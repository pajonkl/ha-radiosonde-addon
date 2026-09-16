#!/usr/bin/env bash
set -e

python3 /gen_cfg.py /data/options.json

cp -f /data/station.cfg /opt/auto_rx/station.cfg

mkdir -p /data/log
rm -rf /opt/auto_rx/log
ln -s /data/log /opt/auto_rx/log

cd /opt/auto_rx
exec python3 auto_rx.py
