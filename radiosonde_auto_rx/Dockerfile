FROM ghcr.io/projecthorus/radiosonde_auto_rx:latest

ADD https://raw.githubusercontent.com/projecthorus/radiosonde_auto_rx/master/auto_rx/station.cfg.example /station.cfg.template
COPY run.sh /run.sh
COPY gen_cfg.py /gen_cfg.py
COPY notify_nearby.py /notify_nearby.py
RUN chmod a+x /run.sh
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && update-ca-certificates && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["/usr/bin/tini", "--", "/run.sh"]
