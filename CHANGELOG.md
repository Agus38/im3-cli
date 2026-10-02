# Changelog

Format mengikuti [Keep a Changelog](https://keepachangelog.com). **Setiap update
yang dirilis wajib bump versi di `VERSION` (dalam script `im3`) dan dicatat di sini.**

## 0.2 — 2026-10-02

### Ditambahkan
- `im3 watch` — pantau saldo, sisa kuota per bagian, masa aktif/tenggang, dan
  akhir paket aktif dalam satu layar.
- Peringatan berbasis ambang: `--saldo-min` (Rp), `--kuota-min` (%),
  `--hari` (hari sebelum habis); nilai 0 / -1 mematikan cek masing-masing.
- Notifikasi Telegram opsional: `--setup-telegram TOKEN CHAT_ID` dan `--test`.
- Anti-spam: `--cooldown` (default 6 jam) per masalah yang sama, `--force`
  untuk mengabaikan cooldown. State disimpan di `~/.im3-cli/watch-state.json`.
- Mode sekali jalan (default; exit code `2` bila ada peringatan, cocok untuk cron)
  dan `--loop --interval N` untuk pemantauan terus-menerus.
- Flag `-V` / `--version`.
- Konfigurasi tersimpan di `~/.im3-cli/config.json` (permission 600).

## 0.1 — 2026-09-30

### Ditambahkan
- Rilis awal: `login` (OTP), `logout`, `balance`, `packages`, `profile`,
  `transactions`, `packlist`, `search`, `userdata`, `buy` (default dry-run),
  `raw`, dan menu interaktif tanpa argumen.
