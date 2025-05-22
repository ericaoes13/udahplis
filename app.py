import streamlit as st
import pandas as pd
import os

# Folder untuk menyimpan file yang diupload
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Judul Aplikasi
st.title('Web Rekonsiliasi Invoice dan Rekening Koran')

# Fungsi untuk meng-upload file
def upload_file(file_type):
    st.subheader(f"Upload File {file_type}")
    uploaded_file = st.file_uploader(f"Choose a {file_type} file", type=["xlsx"])
    return uploaded_file

# Upload file Invoice
invoice_file = upload_file("Invoice")

# Upload file Rekening Koran
bank_statement_file = upload_file("Rekening Koran")

# Jika kedua file sudah di-upload
if invoice_file and bank_statement_file:
    # Simpan file ke folder uploads
    invoice_path = os.path.join(UPLOAD_FOLDER, invoice_file.name)
    bank_statement_path = os.path.join(UPLOAD_FOLDER, bank_statement_file.name)

    with open(invoice_path, "wb") as f:
        f.write(invoice_file.getbuffer())

    with open(bank_statement_path, "wb") as f:
        f.write(bank_statement_file.getbuffer())

    # Baca data dari file Excel
    invoice_data = pd.read_excel(invoice_path)
    bank_statement_data = pd.read_excel(bank_statement_path)

    # Pastikan kolom 'TANGGAL INVOICE' dan 'Posting Date' adalah datetime
    invoice_data['TANGGAL INVOICE'] = pd.to_datetime(invoice_data['TANGGAL INVOICE'], errors='coerce')
    bank_statement_data['Posting Date'] = pd.to_datetime(bank_statement_data['Posting Date'], errors='coerce')
import streamlit as st
import pandas as pd
import os

# Folder untuk menyimpan file yang diupload
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Judul Aplikasi
st.title('Web Rekonsiliasi Invoice dan Rekening Koran')

# Fungsi untuk meng-upload file
def upload_file(file_type):
    st.subheader(f"Upload File {file_type}")
    uploaded_file = st.file_uploader(f"Choose a {file_type} file", type=["xlsx"])
    return uploaded_file

# Upload file Invoice
invoice_file = upload_file("Invoice")

# Upload file Rekening Koran
bank_statement_file = upload_file("Rekening Koran")

# Jika kedua file sudah di-upload
if invoice_file and bank_statement_file:
    # Simpan file ke folder uploads
    invoice_path = os.path.join(UPLOAD_FOLDER, invoice_file.name)
    bank_statement_path = os.path.join(UPLOAD_FOLDER, bank_statement_file.name)

    with open(invoice_path, "wb") as f:
        f.write(invoice_file.getbuffer())

    with open(bank_statement_path, "wb") as f:
        f.write(bank_statement_file.getbuffer())

    # Baca data dari file Excel
    invoice_data = pd.read_excel(invoice_path)
    bank_statement_data = pd.read_excel(bank_statement_path)

    # Pastikan kolom 'TANGGAL INVOICE' dan 'Posting Date' adalah datetime
    invoice_data['TANGGAL INVOICE'] = pd.to_datetime(invoice_data['TANGGAL INVOICE'], errors='coerce')
    bank_statement_data['Posting Date'] = pd.to_datetime(bank_statement_data['Posting Date'], errors='coerce')

    # Cek jika ada nilai NaT di kolom tanggal
    if invoice_data['TANGGAL INVOICE'].isna().sum() > 0 or bank_statement_data['Posting Date'].isna().sum() > 0:
        st.warning("Beberapa data tidak valid pada kolom tanggal. Periksa format tanggal.")

    # Tampilkan data Invoice dan Rekening Koran
    st.subheader("Data Invoice")
    st.write(invoice_data)

    st.subheader("Data Rekening Koran")
    st.write(bank_statement_data)

    # Fitur Filter Tanggal untuk Invoice
    st.subheader("Filter Berdasarkan Tanggal")
    start_date_invoice = st.date_input("Tanggal Mulai Invoice", pd.to_datetime(invoice_data['TANGGAL INVOICE'].min()).date())
    end_date_invoice = st.date_input("Tanggal Akhir Invoice", pd.to_datetime(invoice_data['TANGGAL INVOICE'].max()).date())

    # Pastikan start_date_invoice dan end_date_invoice adalah datetime
    start_date_invoice = pd.to_datetime(start_date_invoice)
    end_date_invoice = pd.to_datetime(end_date_invoice)

    # Filter data berdasarkan tanggal untuk Invoice
    filtered_invoice_data = invoice_data[
        (invoice_data['TANGGAL INVOICE'] >= start_date_invoice) & 
        (invoice_data['TANGGAL INVOICE'] <= end_date_invoice)
    ]

    # Filter data berdasarkan tanggal untuk Rekening Koran
    filtered_bank_statement_data = bank_statement_data[
        (bank_statement_data['Posting Date'] >= start_date_invoice) & 
        (bank_statement_data['Posting Date'] <= end_date_invoice)
    ]

    # Gabungkan data Invoice dan Rekening Koran berdasarkan Tanggal
    reconciled_data = pd.merge(filtered_bank_statement_data, filtered_invoice_data, 
                               left_on='Posting Date', right_on='TANGGAL INVOICE', how='inner')

    # Menambahkan kolom tanggal invoice di paling kiri
    reconciled_data.insert(0, 'Tanggal Invoice', reconciled_data['TANGGAL INVOICE'].dt.strftime('%d/%m/%y'))

    # Menambahkan kolom hasil sum invoice di paling kanan
    reconciled_data['Hasil Sum Invoice'] = reconciled_data.groupby('Tanggal Invoice')['HARGA'].transform('sum')

    # Menampilkan hasil rekonsiliasi dengan hanya satu tanggal per baris
    reconciled_data = reconciled_data[['Tanggal Invoice', 'Posting Date', 'Remark', 'Credit', 'HARGA', 'Hasil Sum Invoice']]

    # Menghilangkan duplikasi berdasarkan Posting Date
    reconciled_data = reconciled_data.drop_duplicates(subset=['Posting Date'])

    reconciled_data.columns = ['Tanggal Invoice', 'Posting Date', 'Remark', 'Credit', 'Invoice', 'Hasil Sum Invoice']

    st.subheader("Contoh Hasil Rekonsiliasi:")
    st.write(reconciled_data)

else:
    st.warning("Harap upload kedua file: Invoice dan Rekening Koran.")
