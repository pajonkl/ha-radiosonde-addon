import json
import math
import os
import time
import urllib.request

OPTIONS_PATH = "/data/options.json"
STATE_PATH = "/data/notified.json"
SONDEHUB_URL = "https://api.v2.sondehub.org/sondes"
HA_BASE = "http://supervisor/core/api"
TOGGLE_ENTITY = "input_boolean.powiadomienie_radiosondy_w_poblizu"


def load_options():
    with open(OPTIONS_PATH) as f:
        return json.load(f)


def load_state():
    try:
        with open(STATE_PATH) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(state):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f)


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def ha_get(path, token):
    req = urllib.request.Request(f"{HA_BASE}{path}", headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def ha_post(path, token, payload):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{HA_BASE}{path}",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read()


def notifications_enabled(token):
    try:
        state = ha_get(f"/states/{TOGGLE_ENTITY}", token)
        return state.get("state") == "on"
    except Exception:
        return True  # fail open if HA/helper not reachable yet


def main():
    token = os.environ.get("SUPERVISOR_TOKEN")
    while True:
        try:
            o = load_options()
            lat = float(o.get("station_lat", 48.2082))
            lon = float(o.get("station_lon", 16.3738))
            radius_km = float(o.get("proximity_km", 15))
            notify_service = o.get("notify_service", "")
            cooldown_minutes = float(o.get("notify_cooldown_minutes", 30))

            if notify_service and token and notifications_enabled(token):
                url = f"{SONDEHUB_URL}?lat={lat}&lon={lon}&distance={int(radius_km * 1000)}&last=3600"
                with urllib.request.urlopen(url, timeout=15) as resp:
                    sondes = json.loads(resp.read().decode())

                state = load_state()
                now = time.time()
                best = None
                for serial, positions in sondes.items():
                    if not isinstance(positions, dict) or not positions:
                        continue
                    latest_ts = sorted(positions.keys())[-1]
                    pos = positions[latest_ts]
                    plat, plon, palt = pos.get("lat"), pos.get("lon"), pos.get("alt")
                    if plat is None or plon is None:
                        continue
                    dist = haversine_km(lat, lon, plat, plon)
                    if dist <= radius_km and (best is None or dist < best[1]):
                        best = (serial, dist, palt)

                if best:
                    serial, dist, alt = best
                    if now - state.get(serial, 0) > cooldown_minutes * 60:
                        msg = f"Radiosonda {serial} przelatuje {dist:.1f} km od Ciebie, na wysokości {alt:.0f} m — sprawdź niebo!"
                        ha_post(
                            f"/services/notify/{notify_service}",
                            token,
                            {"message": msg, "title": "🎈 Balon nad Tobą"},
                        )
                        state[serial] = now
                        save_state(state)
        except Exception:
            pass
        time.sleep(120)


if __name__ == "__main__":
    main()
