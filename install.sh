#!/bin/sh
# Installer IM3 CLI — jalankan langsung:
#   curl -fsSL https://raw.githubusercontent.com/Agus38/im3-cli/main/install.sh | sh
# Hapus lagi:
#   curl -fsSL https://raw.githubusercontent.com/Agus38/im3-cli/main/install.sh | sh -s -- --uninstall
set -eu

RAW="https://raw.githubusercontent.com/Agus38/im3-cli/main"
NAME="im3"
BIN_DIR="${IM3_PREFIX:-/usr/local/bin}"

die() { echo "error: $*" >&2; exit 1; }

if [ "${1:-}" = "--uninstall" ]; then
    target="$BIN_DIR/$NAME"
    if [ -e "$target" ]; then
        rm -f "$target"
        echo "dihapus: $target"
    else
        echo "tidak ditemukan: $target"
    fi
    exit 0
fi

command -v python3 >/dev/null 2>&1 \
    || die "python3 tidak ditemukan — pasang Python 3.8+ terlebih dahulu"

# ambil file im3: pakai salinan lokal bila script dijalankan dari clone repo
here=$(CDPATH= cd -- "$(dirname -- "$0")" 2>/dev/null && pwd || echo ".")
tmp=""
if [ -f "$here/$NAME" ]; then
    src="$here/$NAME"
else
    tmp="$(mktemp)"
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL "$RAW/$NAME" -o "$tmp"
    elif command -v wget >/dev/null 2>&1; then
        wget -qO "$tmp" "$RAW/$NAME"
    else
        rm -f "$tmp"
        die "butuh curl atau wget untuk mengunduh"
    fi
    src="$tmp"
fi

if ! python3 -c "import requests" >/dev/null 2>&1; then
    echo "memasang dependensi: requests"
    python3 -m pip install --user requests >/dev/null 2>&1 \
        || die "gagal memasang requests — coba manual: python3 -m pip install requests"
fi

if [ ! -d "$BIN_DIR" ]; then
    mkdir -p "$BIN_DIR" 2>/dev/null || true
fi
if [ ! -w "$BIN_DIR" ]; then
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
fi

if command -v install >/dev/null 2>&1; then
    install -m 755 "$src" "$BIN_DIR/$NAME"
else
    cp "$src" "$BIN_DIR/$NAME"
    chmod 755 "$BIN_DIR/$NAME"
fi
if [ -n "$tmp" ]; then
    rm -f "$tmp"
fi

echo "terpasang: $BIN_DIR/$NAME"
if ! command -v "$NAME" >/dev/null 2>&1; then
    echo "catatan: tambahkan $BIN_DIR ke PATH, contoh:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi
"$BIN_DIR/$NAME" --version
