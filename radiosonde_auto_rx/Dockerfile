FROM ghcr.io/projecthorus/radiosonde_auto_rx:latest

COPY run.sh /run.sh
COPY gen_cfg.py /gen_cfg.py
RUN chmod a+x /run.sh

ENTRYPOINT ["/usr/bin/tini", "--", "/run.sh"]
