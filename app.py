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

    # Tampilkan data Invoice dan Rekening Koran
    st.subheader("Data Invoice")
    st.write(invoice_data)

    st.subheader("Data Rekening Koran")
    st.write(bank_statement_data)

    # Fitur Filter Tanggal
    st.subheader("Filter Berdasarkan Tanggal")
    start_date_invoice = st.date_input("Tanggal Mulai Invoice", pd.to_datetime(invoice_data['TANGGAL INVOICE'].min()))
    end_date_invoice = st.date_input("Tanggal Akhir Invoice", pd.to_datetime(invoice_data['TANGGAL INVOICE'].max()))

    start_date_bank = st.date_input("Tanggal Mulai Rekening Koran", pd.to_datetime(bank_statement_data['Posting Date'].min()))
    end_date_bank = st.date_input("Tanggal Akhir Rekening Koran", pd.to_datetime(bank_statement_data['Posting Date'].max()))

    # Filter data berdasarkan tanggal
    filtered_invoice_data = invoice_data[
        (invoice_data['TANGGAL INVOICE'] >= start_date_invoice) & 
        (invoice_data['TANGGAL INVOICE'] <= end_date_invoice)
    ]

    filtered_bank_statement_data = bank_statement_data[
        (bank_statement_data['Posting Date'] >= start_date_bank) & 
        (bank_statement_data['Posting Date'] <= end_date_bank)
    ]

    # Tampilkan data yang telah difilter
    st.subheader("Data Invoice yang Difilter")
    st.write(filtered_invoice_data)

    st.subheader("Data Rekening Koran yang Difilter")
    st.write(filtered_bank_statement_data)

else:
    st.warning("Harap upload kedua file: Invoice dan Rekening Koran.")
