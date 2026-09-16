FROM ghcr.io/projecthorus/radiosonde_auto_rx:latest

ADD https://raw.githubusercontent.com/projecthorus/radiosonde_auto_rx/master/auto_rx/station.cfg.example /station.cfg.template
COPY run.sh /run.sh
COPY gen_cfg.py /gen_cfg.py
RUN chmod a+x /run.sh

ENTRYPOINT ["/usr/bin/tini", "--", "/run.sh"]
