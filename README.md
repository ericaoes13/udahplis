# Aplikasi Rekonsiliasi Data Rekening Koran dan Invoice

Aplikasi ini membantu Anda melakukan rekonsiliasi antara data rekening koran dan data invoice berdasarkan **Tanggal Invoice** yang dipilih. Data rekening koran akan difilter berdasarkan deskripsi yang mengandung **"KLIK Indomaret"**.

## Fitur Utama:
1. Pilih **Tanggal Invoice** yang ingin dicocokkan.
2. Sistem secara otomatis menghitung **Total Nominal Invoice** per tanggal.
3. Cocokkan data **Credit** dari rekening koran dengan **Invoice**.
4. Tampilkan hasil rekonsiliasi dalam tabel dan memungkinkan pengunduhan hasil rekonsiliasi.

## Cara Menggunakan:
1. **Unggah file CSV** yang berisi data **Rekening Koran** (cleaned_rekening_koran.csv) dan **Invoice** (cleaned_invoice_data.csv).
2. Pilih **Tanggal Invoice** dari sidebar.
3. Klik tombol **Rekonsiliasi** untuk melihat hasilnya.
4. Unduh hasil rekonsiliasi dalam format CSV.

## Instalasi:
1. Clone repository ini ke komputer Anda.
2. Install dependensi:
   ```bash
   pip install -r requirements.txt
