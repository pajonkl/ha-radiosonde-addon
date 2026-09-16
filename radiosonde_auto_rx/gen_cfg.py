import configparser
import json
import sys

with open(sys.argv[1]) as f:
    o = json.load(f)

config = configparser.ConfigParser()
config.read("/station.cfg.template")

if not config.has_section("location"):
    config.add_section("location")
config.set("location", "station_lat", str(o.get("station_lat", 48.2082)))
config.set("location", "station_lon", str(o.get("station_lon", 16.3738)))
config.set("location", "station_alt", str(o.get("station_alt", 180)))

if not config.has_section("sdr_1"):
    config.add_section("sdr_1")
config.set("sdr_1", "device_idx", str(o.get("device_idx", 0)))
config.set("sdr_1", "ppm", str(o.get("ppm", 0)))
config.set("sdr_1", "gain", str(o.get("gain", -1)))
config.set("sdr_1", "bias", str(bool(o.get("bias", False))))

if not config.has_section("sondehub"):
    config.add_section("sondehub")
config.set("sondehub", "sondehub_enabled", "True")
config.set(
    "sondehub",
    "sondehub_contact_email",
    str(o.get("sondehub_contact_email", "none@none.com")),
)

if not config.has_section("habitat"):
    config.add_section("habitat")
config.set("habitat", "uploader_callsign", str(o.get("uploader_callsign", "HA-User")))

with open("/data/station.cfg", "w") as f:
    config.write(f)
