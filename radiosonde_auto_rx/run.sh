#!/usr/bin/env bash
set -e

python3 /gen_cfg.py /data/options.json

cp -f /data/station.cfg /opt/auto_rx/station.cfg

# Keep logs on the add-on's persistent /data volume instead of the
# throwaway container filesystem.
mkdir -p /data/log
rm -rf /opt/auto_rx/log
ln -s /data/log /opt/auto_rx/log

python3 /notify_nearby.py &

cd /opt/auto_rx
exec python3 auto_rx.py
