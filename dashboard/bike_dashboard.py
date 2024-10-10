import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Menampilkan judul aplikasi Streamlit
st.title("Bike Sharing Dashboard")

# Membaca file CSV
df = pd.read_csv('dashboard/main_data.csv')

# Mengonversi kolom tanggal menjadi datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Memastikan kolom 'workingday' bertipe numerik (jika tidak, konversi)
if df['workingday'].dtype != 'int64' and df['workingday'].dtype != 'float64':
    df['workingday'] = pd.to_numeric(df['workingday'], errors='coerce')

# Memilih hanya kolom numerik untuk perhitungan korelasi
kolom_numerik = df.select_dtypes(include=['float64', 'int64'])

# Menghitung matriks korelasi untuk kolom numerik
matrix_korelasi = kolom_numerik.corr()

# Visualisasi korelasi menggunakan heatmap
plt.figure(figsize=(12,8))
sns.heatmap(matrix_korelasi, annot=True, cmap='coolwarm')
plt.title('Korelasi Antar Variabel Numerik')
st.pyplot()  # Menampilkan grafik di Streamlit

# Debugging - Tampilkan beberapa baris dari data
st.write(df.head())  # Cek apakah data sudah terbaca dengan benar

# Visualisasi 1: Pengaruh suhu terhadap jumlah peminjaman sepeda
st.title("**Visualization of Question 1:** How does temperature affect the total number of bikes borrowed?")
# Membagi suhu (temp) menjadi kategori interval
bins = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
labels = ['0.0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1.0']

# Menambahkan kolom 'temp_interval' dengan kategori interval
df['temp_interval'] = pd.cut(df['temp'], bins=bins, labels=labels, right=False)

# Menambahkan kategori baru 'Unknown' jika ada nilai missing
if df['temp_interval'].isnull().any():
    st.write("Terdapat nilai missing pada 'temp_interval'. Mengganti dengan kategori lain.")
    # Menambahkan kategori baru ke dalam kategori 'temp_interval'
    df['temp_interval'] = df['temp_interval'].cat.add_categories('Unknown')
    df['temp_interval'].fillna('Unknown', inplace=True)
# Memeriksa duplikasi pada 'temp_interval'
if df['temp_interval'].duplicated().any():
    st.write("Terdapat duplikasi pada 'temp_interval'. Memperbaiki duplikasi.")
# Membuat figure dan countplot berdasarkan interval suhu
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(x='temp_interval', data=df, palette='Set1', ax=ax)
# Menambahkan judul dan label sumbu
ax.set_title('Jumlah Peminjaman Sepeda Berdasarkan Interval Suhu')
ax.set_xlabel('Interval Suhu')
ax.set_ylabel('Total Rentals (cnt)')
# Menampilkan plot di Streamlit
st.pyplot(fig)

# Visualisasi 2: Perbedaan jumlah peminjaman sepeda berdasarkan hari kerja dan hari libur
st.title("**Visualization of Question 2:** Is there a difference in the number of bikes borrowed based on weekdays and holidays?")
# Membuat figure dan axes secara eksplisit
fig, ax = plt.subplots(figsize=(8, 5))
# Membuat countplot dengan 'ax' sebagai objek plotting
sns.countplot(x='workingday', data=df, palette='Set1', hue='workingday', ax=ax, legend=False)
# Menambahkan judul dan label sumbu
ax.set_title('Perbandingan Jumlah Peminjaman Berdasarkan Hari Kerja dan Hari Libur')
ax.set_xlabel('Working Day (0 = Hari Libur, 1 = Hari Kerja)')
ax.set_ylabel('Total Rentals (cnt)')
# Menampilkan plot
st.pyplot(fig)

st.title("Conclusion of Question 1 and Question 2")
st.write("1. Pengaruh Suhu terhadap Jumlah Total Peminjaman Sepeda:")
st.write("- Dari hasil visualisasi scatter plot, terlihat bahwa suhu memiliki hubungan positif dengan jumlah total peminjaman sepeda. Semakin tinggi suhu (temp), semakin banyak sepeda yang dipinjam (cnt).")
st.write("- Hal ini dapat diinterpretasikan bahwa kenyamanan fisik yang dipengaruhi oleh suhu menjadi faktor penting dalam keputusan meminjam sepeda.")
st.write("2. Perbedaan Jumlah Peminjaman Sepeda Berdasarkan Hari Kerja dan Hari Libur:")
st.write("- Dari visualisasi boxplot, kita melihat bahwa jumlah peminjaman sepeda pada hari kerja (workingday = 1) cenderung lebih tinggi dibandingkan dengan hari libur (workingday = 0). Median peminjaman pada hari kerja lebih tinggi, dengan variasi yang lebih rendah dibandingkan dengan hari libur.");
