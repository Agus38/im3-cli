import base64
import hashlib
import json
import time
import uuid

import requests

BASE = "https://myim3api1.ioh.co.id/api/v2"
HE = "https://myim3-he.indosatooredoo.com/api/v2/token/web/v2"

HDR_AUTH = "642d1cc69d90666962726e"
SERVICE_KEY = "i4WxFMMLvWqnrvuAyg58"
APP_VERSION = "82.2.0"
CHANNEL = "PORTAL"
PROJECT = "myim3"
RC4_KEY = b"Ind0s@t001!"


def rc4(data: str) -> str:
    s = list(range(256))
    k = [RC4_KEY[i % len(RC4_KEY)] for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + s[i] + k[i]) % 256
        s[i], s[j] = s[j], s[i]
    out = bytearray()
    i = j = 0
    for ch in data.encode("latin-1"):
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        out.append(ch ^ s[(s[i] + s[j]) % 256])
    return out.hex()


def odd_chars(s: str) -> str:
    return "".join(s[i] for i in range(0, len(s), 2))


def guest_token(device: str = None) -> dict:
    """Guest token flow via myim3-he. Returns dict with tid, jwt, network, userclass."""
    device = device or uuid.uuid4().hex
    tid = str(int(time.time() * 1000))
    params = {
        "X-IMI-TOKENID": "",
        "X-IMI-CHANNEL": rc4(CHANNEL),
        "X-IMI-LANGUAGE": rc4("ID"),
        "tid": rc4(tid),
        "X-IMI-App-OS": rc4("WEB"),
        "pf": PROJECT,
        "X-DEVICEID": rc4(device),
    }
    r = requests.get(
        HE,
        params=params,
        headers={
            "Origin": "https://myim3app.indosatooredoo.com",
            "Referer": "https://myim3app.indosatooredoo.com/",
            "User-Agent": UA,
        },
        timeout=30,
        allow_redirects=False,
    )
    loc = r.headers.get("location", "")
    frag = loc.split("#/he/")[-1]
    raw = base64.b64decode(frag + "=" * (-len(frag) % 4)).decode("utf-8", "replace")
    session_id, jwt, ntwk, _, _ = raw.split("|")[:5]
    payload = json.loads(base64.urlsafe_b64decode(jwt.split(".")[1] + "=="))
    return {"tid": session_id, "jwt": jwt, "ntwk": ntwk, "device": device,
            "claims": payload, "token": jwt}


UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


class Im3:
    def __init__(self, msisdn=None, token=None, device=None):
        self.guest = guest_token(device)
        self.token = token or self.guest["jwt"]
        self.msisdn = msisdn
        self.device = self.guest["device"]

    def _headers(self, body=None):
        salt = odd_chars(self.token)
        h = {
            "Authorization": HDR_AUTH,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-IMI-App-OS": "WEB",
            "X-IMI-APPVERSION": APP_VERSION,
            "X-IMI-CHANNEL": CHANNEL,
            "X-IMI-LANGUAGE": "ID",
            "X-IMI-VERSION": APP_VERSION,
            "X-IMI-SERVICEKEY": SERVICE_KEY,
            "X-DEVICEID": self.device,
            "X-DEVICENAME": "WEB",
            "Origin": "https://myim3app.indosatooredoo.com",
            "Referer": "https://myim3app.indosatooredoo.com/",
            "User-Agent": UA,
        }
        if body is not None:
            raw = json.dumps(body, separators=(",", ":"))
            h["x-imi-oauth"] = hashlib.sha512(
                f"REQBODY={raw}&SALT={salt}".encode()).hexdigest()
        base = f"{self.msisdn or 'parent'}$WEB${APP_VERSION}${self.token}"
        h["X-IMI-HASH"] = hashlib.sha512(f"{base}&SALT={salt}".encode()).hexdigest()
        h["X-IMI-TOKENID"] = self.token
        if self.msisdn:
            h["X-IMI-UID"] = self.msisdn
        return h

    def post(self, path, body=None, timeout=30):
        url = BASE + path
        r = requests.post(url, data=json.dumps(body or {}, separators=(",", ":")),
                          headers=self._headers(body or {}), timeout=timeout)
        try:
            return r.json()
        except ValueError:
            return {"_raw": r.text, "_status": r.status_code}

    def get(self, path, timeout=30):
        r = requests.get(BASE + path, headers=self._headers(None), timeout=timeout)
        try:
            return r.json()
        except ValueError:
            return {"_raw": r.text, "_status": r.status_code}


if __name__ == "__main__":
    c = Im3()
    print("guest claims:", json.dumps(c.guest["claims"], indent=2)[:400])
    print("\n-- /profile/get --")
    print(json.dumps(c.post("/profile/get"), indent=2)[:600])
    print("\n-- /otp/send/v1 (invalid msisdn, header smoke test) --")
    print(json.dumps(c.post("/otp/send/v1", {"msisdn": "62000", "action": ""}),
                     indent=2)[:600])