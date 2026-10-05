#!/usr/bin/env python3
"""Encode/decode string sensitif untuk source im3 (deterrence, bukan enkripsi).

 pakai:
   python3 tools/obfuscate.py enc "<string>"
   python3 tools/obfuscate.py dec "<blob>"
"""
import base64
import sys

KEY = b"im3-obf"


def _xor(data: bytes) -> bytes:
    return bytes(b ^ KEY[i % len(KEY)] for i, b in enumerate(data))


def enc(text: str) -> str:
    return base64.b64encode(_xor(text.encode())).decode()


def dec(blob: str) -> str:
    return _xor(base64.b64decode(blob)).decode()


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("enc", "dec"):
        raise SystemExit("pakai: python3 tools/obfuscate.py enc|dec <teks>")
    print((enc if sys.argv[1] == "enc" else dec)(sys.argv[2]))
