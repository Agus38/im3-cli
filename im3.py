import hashlib, json, requests

RC4KEY = b"Ind0s@t001!"

def rc4(data: str) -> str:
    S = list(range(256)); K = [RC4KEY[i % 11] for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + S[i] + K[i]) % 256
        S[i], S[j] = S[j], S[i]
    out = bytearray(); i = j = 0
    for ch in data.encode("latin-1"):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(ch ^ S[(S[i] + S[j]) % 256])
    return out.hex()

HE = "https://myim3-he.indosatooredoo.com/api/v2/token/web/v2"

def he_token(tid, os_="WEB", device="web-" + "0" * 16, lang="ID"):
    p = {
        "X-IMI-TOKENID": "",
        "X-IMI-CHANNEL": rc4("PORTAL"),
        "X-IMI-LANGUAGE": rc4(lang),
        "tid": rc4(tid),
        "X-IMI-App-OS": rc4(os_),
        "pf": "myim3",
        "X-DEVICEID": rc4(device),
    }
    r = requests.get(HE, params=p, headers={"Origin": "https://myim3app.indosatooredoo.com",
        "Referer": "https://myim3app.indosatooredoo.com/",
        "User-Agent": "Mozilla/5.0 Chrome/120.0"}, timeout=30, allow_redirects=False)
    return r

if __name__ == "__main__":
    import time, uuid
    r = he_token(str(int(time.time() * 1000)), device=uuid.uuid4().hex)
    print(r.status_code)
    print(r.headers.get("location", "")[:300])
    print(r.text[:400])
