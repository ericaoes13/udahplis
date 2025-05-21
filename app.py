import streamlit as st
import pandas as pd

# Fungsi untuk memuat data dari file yang diunggah
def load_data(uploaded_file):
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file, engine='openpyxl')  # Membaca file excel menggunakan openpyxl
        return data
    return None

# Fungsi untuk rekonsiliasi berdasarkan kriteria
def reconcile(bank_data, invoice_data, start_date_invoice, end_date_invoice, start_date_bank, end_date_bank):
    # Filter invoice data berdasarkan rentang tanggal invoice (start date dan end date)
    invoice_data_filtered = invoice_data[(invoice_data['TANGGAL INVOICE'] >= start_date_invoice) & 
                                         (invoice_data['TANGGAL INVOICE'] <= end_date_invoice)]
    
    # Filter bank data berdasarkan rentang tanggal rekening koran (start date dan end date)
    bank_data_filtered = bank_data[(bank_data['Posting Date'] >= start_date_bank) & 
                                    (bank_data['Posting Date'] <= end_date_bank)]
    
    # Hitung total nominal invoice per tanggal
    total_invoice_per_day = invoice_data_filtered['HARGA'].sum()

    # Siapkan hasil tabel
    result_table = bank_data_filtered[['Posting Date', 'Remark', 'Credit']].copy()
    result_table['Invoice Date'] = invoice_data_filtered['TANGGAL INVOICE'].values
    result_table['Invoice'] = invoice_data_filtered['HARGA'].values  # Menambahkan Harga

    # Return hasil
    return result_table, total_invoice_per_day, invoice_data_filtered[['TANGGAL INVOICE', 'HARGA']]

# Antarmuka Streamlit
st.title("Aplikasi Rekonsiliasi Data Rekening Koran dan Invoice")

# Unggah file invoice
st.sidebar.header("Unggah File Invoice")
uploaded_invoice_file = st.sidebar.file_uploader("Unggah File Invoice", type=["xlsx", "csv"])

# Unggah file rekening koran
st.sidebar.header("Unggah File Rekening Koran")
uploaded_bank_file = st.sidebar.file_uploader("Unggah File Rekening Koran", type=["xlsx", "csv"])

# Pilih rentang tanggal untuk Invoice
st.sidebar.subheader("Pilih Rentang Tanggal Invoice")
start_date_invoice = st.sidebar.date_input("Start Date Invoice", pd.to_datetime("2025-04-08"))
end_date_invoice = st.sidebar.date_input("End Date Invoice", pd.to_datetime("2025-04-13"))

# Pilih rentang tanggal untuk Rekening Koran
st.sidebar.subheader("Pilih Rentang Tanggal Rekening Koran")
start_date_bank = st.sidebar.date_input("Start Date Rekening Koran", pd.to_datetime("2025-04-08"))
end_date_bank = st.sidebar.date_input("End Date Rekening Koran", pd.to_datetime("2025-04-13"))

# Memuat data
if uploaded_invoice_file and uploaded_bank_file:
    # Memuat data dari file yang diunggah
    bank_data = load_data(uploaded_bank_file)
    invoice_data = load_data(uploaded_invoice_file)
    
    # Pastikan kolom TANGGAL INVOICE diformat sebagai datetime
    invoice_data['TANGGAL INVOICE'] = pd.to_datetime(invoice_data['TANGGAL INVOICE'], errors='coerce')

    # Tampilkan data mentah
    st.subheader("Data Rekening Koran")
    st.write(bank_data)
    
    st.subheader("Data Invoice")
    # Tampilkan seluruh data Invoice yang sudah difilter berdasarkan rentang tanggal
    st.write(invoice_data[['TANGGAL INVOICE', 'HARGA']])

    # Lakukan rekonsiliasi jika tombol ditekan
    if st.button("Rekonsiliasi"):
        result_table, total_invoice_per_day, invoice_data_filtered = reconcile(
            bank_data, invoice_data, start_date_invoice, end_date_invoice, start_date_bank, end_date_bank)

        # Tampilkan hasil rekonsiliasi
        st.subheader(f"Rekonsiliasi untuk Rentang Tanggal Invoice {start_date_invoice} - {end_date_invoice}")
        st.write(result_table)

        # Tampilkan total nominal invoice per hari
        st.subheader(f"Total Nominal Invoice pada Rentang Tanggal {start_date_invoice} - {end_date_invoice}")
        st.write(total_invoice_per_day)

        # Opsi untuk mengunduh hasil
        st.download_button("Unduh Hasil Rekonsiliasi", result_table.to_csv(index=False), "result.csv", "text/csv")
else:
    st.warning("Silakan unggah file invoice dan rekening koran untuk memulai rekonsiliasi.")
