# im3 — CLI myIM3 (tak resmi)

Client command-line untuk akun myIM3 (Indosat Ooredoo / IOH). Dibuat dari
reverse-engineering PWA publik `myim3app.indosatooredoo.com`.

> **Tidak resmi** — tidak berafiliasi dengan Indosat/IOH. Bisa berhenti bekerja
> sewaktu-waktu saat PWA/app diperbarui. Hanya untuk nomor milik sendiri.

## Instal

Butuh Python 3.8+ dan `requests`:

```sh
pip install requests
chmod +x im3
sudo cp im3 /usr/local/bin/        # atau taruh di PATH mana pun
im3 --version
```

## Perintah

| Perintah      | Fungsi                                                        |
|---------------|---------------------------------------------------------------|
| `im3`         | menu interaktif                                               |
| `im3 login`   | login dengan OTP                                              |
| `im3 balance` | saldo & masa aktif                                             |
| `im3 packages`| paket aktif + sisa kuota                                       |
| `im3 profile` | profil pelanggan                                              |
| `im3 transactions` | riwayat transaksi                                         |
| `im3 userdata`| pemakaian, langganan VAS, info pelanggan                       |
| `im3 packlist` / `im3 search` | katalog paket yang bisa dibeli                    |
| `im3 buy <pvr_code>` | beli paket; default dry-run, `--pay` untuk bayar         |
| `im3 watch`   | pantau saldo/kuota/masa aktif + peringatan                     |
| `im3 raw <path> [body]` | panggil endpoint API bebas                           |

## watch — pemantauan & peringatan

```sh
im3 watch                          # cek sekali; exit 2 bila ada peringatan
im3 watch --loop --interval 300    # pantau terus tiap 5 menit

im3 watch --saldo-min 10000 --kuota-min 15 --hari 5   # atur ambang
im3 watch --saldo-min 0 --kuota-min -1 --hari -1       # matikan satu-satu

im3 watch --setup-telegram <bot_token> <chat_id>       # simpan kredensial
im3 watch --test                                       # kirim pesan uji
```

Peringatan yang sama tidak dikirim ulang sebelum `--cooldown` (default 6 jam);
pakai `--force` untuk mengabaikan. State: `~/.im3-cli/watch-state.json`.

Cron example (cek tiap jam, hanya laporkan kalau ada peringatan):

```sh
0 * * * * im3 watch >/dev/null 2>&1 || notify-send "im3" "ada peringatan kuota/saldo"
```

## State & konfigurasi

Semua disimpan di `~/.im3-cli/` dengan permission 600:

- `session.json` — sesi login (token)
- `config.json` — kredensial Telegram
- `watch-state.json` — anti-spam peringatan
- `purchases.jsonl` — catatan pembelian

## Pengembangan

- Sumber: satu file `im3` (script Python executable).
- **Setiap update wajib bump `VERSION`** di bagian atas script dan menambah
  entri baru di [CHANGELOG.md](CHANGELOG.md).
- Cek cepat: `python3 -m py_compile im3 && ./im3 --version`
