# FSub Bot Docs

FSub Bot adalah bot Telegram berbasis Python/Hydrogram untuk menyimpan file atau postingan di channel database, membuat tautan akses khusus, dan memaksa pengguna bergabung ke channel/group tertentu sebelum konten dibuka.

## Daftar Isi

- [Fitur](#fitur)
- [Prasyarat](#prasyarat)
- [Instalasi Lokal](#instalasi-lokal)
- [Konfigurasi](#konfigurasi)
- [Menjalankan Bot](#menjalankan-bot)
- [Panduan Perintah](#panduan-perintah)
- [Alur Penggunaan](#alur-penggunaan)
- [Deployment Heroku](#deployment-heroku)
- [Troubleshooting](#troubleshooting)

## Fitur

- Force subscribe dinamis ke beberapa channel/group.
- Penyimpanan post/file ke `CHANNEL_DB` dan pembuatan link `/start` otomatis.
- Mode batch untuk membuat satu link berisi banyak post.
- Sistem role member, talent, admin, dan owner.
- Sistem koin, rating talent dengan 🍓, serta akses VIP talent.
- Pengaturan teks force subscribe dan judul tombol join dari database.
- Perintah `/idku` untuk melihat User ID Telegram secara cepat.

## Prasyarat

Pastikan sudah tersedia:

- Python 3.10 atau lebih baru.
- Bot Telegram dari [@BotFather](https://t.me/BotFather).
- MongoDB URI, misalnya dari MongoDB Atlas.
- Channel database Telegram yang sudah menambahkan bot sebagai admin.
- Channel/group force subscribe jika fitur force subscribe ingin dipakai.

## Instalasi Lokal

> Gunakan `python3` agar venv dibuat dengan interpreter Python 3.

```bash
git clone <url-repo-anda>
cd fsub
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
cp config.env.example config.env  # jika file contoh tersedia
```

Jika tidak ada `config.env.example`, buat file `config.env` sendiri dengan mengikuti bagian konfigurasi di bawah.

## Konfigurasi

Buat atau edit `config.env` di root project.

```env
BOT_TOKEN=123456:ABCDEF
CHANNEL_DB=-1001234567890
DATABASE_URL=mongodb+srv://user:password@cluster.example.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=fsub
ADMINS=111111111 222222222
OWNER=111111111

# Force subscribe bawaan dari environment; dapat ditambah juga lewat perintah admin.
FORCE_SUB_1=-1001234567891
FORCE_SUB_2=-1001234567892

BUTTON_TITLE=Join
BUTTON_ROW=2
RESTRICT=True
DISABLE_BUTTON=False
CUSTOM_CAPTION=
START_MESSAGE=Halo {mention}!\n\nKirim /help untuk melihat panduan bot.
FORCE_MESSAGE=Halo {mention}!\n\nSilakan join channel/group di bawah ini terlebih dahulu.
```

### Keterangan Variabel

| Variabel | Wajib | Keterangan |
| --- | --- | --- |
| `BOT_TOKEN` | Ya | Token bot dari BotFather. |
| `CHANNEL_DB` | Ya | ID channel database untuk menyimpan konten. Bot wajib admin. |
| `DATABASE_URL` | Ya | URI koneksi MongoDB. |
| `DATABASE_NAME` | Ya | Nama database MongoDB. |
| `ADMINS` | Disarankan | Daftar User ID admin, pisahkan dengan spasi. |
| `OWNER`/`OWNERS` | Disarankan | Daftar User ID owner, pisahkan dengan spasi. |
| `FORCE_SUB_1`, dst. | Opsional | ID channel/group wajib join. |
| `BUTTON_TITLE` | Opsional | Teks tombol join. Default: `ᴊᴏɪɴ`. |
| `BUTTON_ROW` | Opsional | Jumlah tombol join per baris. |
| `RESTRICT` | Opsional | Proteksi konten saat dikirim ke user. |
| `DISABLE_BUTTON` | Opsional | Nonaktifkan tombol share pada post channel database. |
| `CUSTOM_CAPTION` | Opsional | Template caption khusus untuk dokumen. |
| `START_MESSAGE` | Opsional | Pesan awal `/start`. |
| `FORCE_MESSAGE` | Opsional | Pesan saat user belum join. |

## Menjalankan Bot

```bash
source venv/bin/activate
python3 main.py
```

Untuk menghentikan bot, tekan `Ctrl+C`.

## Panduan Perintah

### Member

| Perintah | Fungsi |
| --- | --- |
| `/start` | Mulai bot atau membuka link konten. |
| `/help` | Menampilkan bantuan sesuai role pengguna. |
| `/idku` | Menampilkan User ID Telegram Anda. |
| `/ping` | Mengecek latensi bot. |
| `/uptime` | Mengecek waktu aktif bot. |
| `/mycoins` | Mengecek saldo koin. |
| `/talent` | Melihat daftar talent. |
| `/toptalent` | Melihat papan peringkat talent. |
| `/rate <id_talent>` | Memberi 1 🍓 ke talent dengan biaya koin. |

### Talent

| Perintah | Fungsi |
| --- | --- |
| `/setbio <bio>` | Mengatur bio profil talent. |
| `/setvip <chat_id>` | Mengatur channel VIP talent. |
| `/delvip` | Menghapus channel VIP talent. |

### Admin

| Perintah | Fungsi |
| --- | --- |
| `/users` | Melihat jumlah pengguna bot. |
| `/broadcast` | Mengirim pesan siaran dengan membalas pesan target. |
| `/batch` | Membuat link untuk rentang beberapa post. |
| `/addtalent <id>` | Menambahkan user sebagai talent. |
| `/deltalent <id>` | Menghapus talent. |
| `/tfcoin <id> <jumlah>` | Transfer koin ke user. |
| `/revokevip <id_talent> <id_user>` | Mencabut akses VIP member. |
| `/addsub <chat_id>` | Menambahkan channel/group force subscribe. |
| `/delsub <chat_id>` | Menghapus channel/group force subscribe. |
| `/listsub` | Menampilkan daftar force subscribe. |
| `/setforce <teks>` | Mengubah pesan force subscribe. |
| `/setjoin <teks>` | Mengubah teks tombol join. |

### Owner

| Perintah | Fungsi |
| --- | --- |
| `/addadmin <id>` | Menambahkan admin database. |
| `/unadmin <id>` | Menghapus admin database. |
| `/listadmin` | Menampilkan daftar admin database. |

## Alur Penggunaan

1. Tambahkan bot sebagai admin di `CHANNEL_DB`.
2. Tambahkan bot sebagai admin di channel/group force subscribe dan beri izin membuat invite link.
3. Jalankan bot.
4. Admin mengirim file/post ke chat pribadi bot untuk mendapatkan link khusus.
5. Member membuka link tersebut melalui bot.
6. Jika member belum join semua channel/group wajib, bot menampilkan tombol join dan tombol coba lagi.
7. Setelah member join, konten dikirim tanpa tombol `Bagikan Link` agar tombol share khusus admin tidak ikut tampil ke member.

## Deployment Heroku

Klik tombol berikut untuk deploy ke Heroku, lalu isi Config Vars sesuai bagian konfigurasi.

<a href="https://heroku.com/deploy?template=https://github.com/karaminarani/suherfsub2">
  <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku">
</a>

## Troubleshooting

### Bot gagal membuat invite link

- Pastikan bot adalah admin di channel/group force subscribe.
- Pastikan bot punya izin `Invite Users` atau membuat invite link.
- Periksa nilai `FORCE_SUB_*` atau data force subscribe dinamis.

### Link konten tidak bisa dibuka

- Pastikan post masih ada di `CHANNEL_DB`.
- Pastikan `CHANNEL_DB` benar dan bot masih admin.
- Pastikan member sudah join semua force subscribe.

### Database error

- Periksa `DATABASE_URL` dan `DATABASE_NAME`.
- Pastikan IP server diizinkan pada MongoDB Atlas.
- Pastikan dependency sudah terpasang di venv.

### Perintah admin malah tersimpan sebagai post

Pastikan perintah sudah terdaftar pada daftar pengecualian command di plugin post. Perintah umum seperti `/idku`, `/help`, `/batch`, dan perintah admin/talent utama sudah dikecualikan.
