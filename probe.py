import base64, hashlib, json, uuid, requests

def _dec(blob):
    """Dekode string terobfuscasi (XOR+base64). Lihat tools/obfuscate.py."""
    raw = base64.b64decode(blob)
    key = b"im3-obf"
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(raw)).decode()

BASE = _dec("ARlHXRxYSUYASkQCUQcZBAIDBg0ORw5cAwYGSQgdWgIZUA==")
AUTH = _dec("X1kBSV4BBV9UVxRfVFBfVAUfWFBQDA==")
SVC  = _dec("AFlkVSkvKyUbZFwBEBAcLEpKWlo=")
ORIGIN_APP = _dec("ARlHXRxYSUYASkQCUQcZHR1EAQYJGgxHQgAQAw0CXAMMDQs=")
VER  = "82.2.0"

def odd(s): return "".join(s[i] for i in range(0, len(s), 2))

def hdr(token, msisdn=None, os_="WEB", body=None, appversion=VER):
    salt = odd(token or "")
    h = {
        "Authorization": AUTH,
        "Content-Type": "application/json",
        "X-IMI-App-OS": os_,
        "X-IMI-APPVERSION": appversion,
        "X-IMI-CHANNEL": "PORTAL",
        "X-IMI-LANGUAGE": "ID",
        "X-IMI-VERSION": appversion,
        "X-IMI-SERVICEKEY": SVC,
        "X-DEVICEID": "web-" + uuid.uuid4().hex[:16],
        "X-DEVICENAME": "Chrome",
        "Origin": ORIGIN_APP,
        "Referer": ORIGIN_APP + "/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0 Safari/537.36",
    }
    if body is not None:
        h["x-imi-oauth"] = hashlib.sha512(f"REQBODY={json.dumps(body,separators=(',',':'))}&SALT={salt}".encode()).hexdigest()
    if token:
        h["X-IMI-TOKENID"] = token
        base = (msisdn or "parent") + "$" + os_ + "$" + appversion + "$" + token
        h["X-IMI-HASH"] = hashlib.sha512(f"{base}&SALT={salt}".encode()).hexdigest()
        h["X-IMI-UID"] = msisdn or ""
    return h

r = requests.get(BASE + "/token/guest", headers=hdr(None), timeout=30)
print("guest token:", r.status_code)
print(r.text[:600])
