import json
import sys

with open(sys.argv[1]) as f:
    o = json.load(f)

cfg = f"""[location]
station_lat = {o.get('station_lat', 48.2082)}
station_lon = {o.get('station_lon', 16.3738)}
station_alt = {o.get('station_alt', 180)}

gpsd_enabled = False

[sdr_1]
device_idx = {o.get('device_idx', 0)}
ppm = {o.get('ppm', 0)}
gain = {o.get('gain', -1)}
bias = {o.get('bias', False)}

[search_params]
min_freq = 400.05
max_freq = 406.0
rx_timeout = 180

[sondehub]
sondehub_enabled = True
sondehub_upload_rate = 15
sondehub_contact_email = {o.get('sondehub_contact_email', 'none@none.com')}

[habitat]
uploader_callsign = {o.get('uploader_callsign', 'HA-User')}
upload_listener_position = True
uploader_antenna = RTL-SDR, stock antenna
"""

with open('/data/station.cfg', 'w') as f:
    f.write(cfg)
