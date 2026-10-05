# im3 — CLI myIM3

Client command-line untuk mengelola akun myIM3 (Indosat Ooredoo / IOH) langsung
dari terminal: cek saldo, paket, riwayat, cari & beli paket, sampai pemantauan
kuota dengan peringatan.

> Proyek tidak resmi, tidak berafiliasi dengan Indosat/IOH. Hanya untuk nomor
> milik sendiri, dan bisa berubah sewaktu-waktu mengikuti perubahan aplikasi
> myIM3.

## Instal

Butuh Python 3.8+. Satu baris:

```sh
curl -fsSL https://raw.githubusercontent.com/Agus38/im3-cli/main/install.sh | sh
```

Installer otomatis memasang dependensi (`requests`) dan menaruh `im3` di PATH.
Belum punya `curl`? Pakai alternatif manual:

```sh
git clone https://github.com/Agus38/im3-cli.git
cd im3-cli
python3 -m pip install requests
sudo cp im3 /usr/local/bin/
```

Cek hasilnya:

```sh
im3 --version
```

Menghapus kembali:

```sh
curl -fsSL https://raw.githubusercontent.com/Agus38/im3-cli/main/install.sh | sh -s -- --uninstall
```

## Mulai cepat

```sh
im3            # menu interaktif (paling mudah untuk pemula)
im3 login      # login sekali dengan OTP
im3 balance    # saldo, masa aktif, registrasi & lama bergabung
im3 packages   # paket aktif + sisa kuota
im3 watch      # pantau saldo, kuota, masa aktif
```

## Perintah

| Perintah             | Fungsi                                    |
|----------------------|-------------------------------------------|
| `im3`                | menu interaktif                           |
| `im3 login` / `logout` | masuk / keluar sesi                     |
| `im3 balance`        | saldo, masa aktif, registrasi & lama bergabung |
| `im3 packages`       | paket aktif + sisa kuota                   |
| `im3 profile`        | profil pelanggan                          |
| `im3 transactions`   | riwayat transaksi                         |
| `im3 userdata`       | pemakaian & langganan                     |
| `im3 packlist` / `im3 search` | katalog & pencarian paket          |
| `im3 buy <kode>`     | beli paket (default hanya simulasi)       |
| `im3 watch`          | pantau + peringatan                       |
| `im3 update`         | perbarui ke versi terbaru                 |
| `im3 raw`            | panggil endpoint API (tingkat lanjut)     |

## Pembaruan

`im3` memeriksa versi terbaru secara berkala (maksimal tiap 6 jam). Jika ada
versi baru, **semua perintah diblokir** sampai Anda memperbarui:

```sh
im3 update
```

Lewati pemeriksaan satu kali (mis. offline atau pengembang):

```sh
IM3_NO_UPDATE_CHECK=1 im3 balance
```

## watch — pemantauan & peringatan

```sh
im3 watch                          # cek sekali, keluar
im3 watch --loop --interval 300    # pantau terus tiap 5 menit

# atur ambang peringatan
im3 watch --saldo-min 10000 --kuota-min 15 --hari 5
```

Notifikasi Telegram (opsional):

```sh
im3 watch --setup-telegram TOKEN CHAT_ID
im3 watch --test
```

Peringatan yang sama tidak dikirim ulang sebelum cooldown (default 6 jam);
`--force` untuk mengabaikan. Untuk cron, `im3 watch` keluar dengan kode `0`
(aman) atau `2` (ada peringatan).

## Catatan

- Sesi login dan konfigurasi disimpan lokal di komputer Anda. Tidak ada
  telemetry; data hanya dikirim ke layanan myIM3 (dan Telegram bila Anda
  mengaktifkan notifikasi).
- Simpan file sesi Anda seperti kata sandi — jangan dibagikan.

## Pengembangan

- Sumber: satu file `im3` (script Python executable).
- **Setiap update wajib bump `VERSION`** di bagian atas script dan menambah
  entri baru di [CHANGELOG.md](CHANGELOG.md).
- String sensitif (URL API, header, kunci) disimpan terobfuscasi (XOR+base64),
  bukan teks polos. Encode/decode saat mengembangkan:
  `python3 tools/obfuscate.py enc|dec "<string>"`.
- Cek cepat: `python3 -m py_compile im3 && ./im3 --version`
