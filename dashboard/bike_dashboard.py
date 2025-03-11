import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi tampilan Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.markdown("""
    <style>
        .big-font {font-size:24px !important; font-weight: bold; color: #ff4b4b;}
        .sub-font {font-size:18px; color: #333333;}
        .sidebar .sidebar-content {background-color: #f0f2f6;}
    </style>
""", unsafe_allow_html=True)

# Sidebar untuk filter dan navigasi
st.sidebar.title("📊 Bike Sharing Analysis")
st.sidebar.markdown("Gunakan opsi ini untuk menyesuaikan tampilan data dan analisis.")

# Membaca file CSV
df = pd.read_csv('dashboard/main_data.csv')
df['dteday'] = pd.to_datetime(df['dteday'])
if df['workingday'].dtype != 'int64' and df['workingday'].dtype != 'float64':
    df['workingday'] = pd.to_numeric(df['workingday'], errors='coerce')

# Menampilkan Data Sample
st.sidebar.subheader("🔍 Sample Data")
st.sidebar.write(df.head(5))

# Korelasi Antar Variabel
st.markdown('<p class="big-font">🔗 Korelasi Antar Variabel Numerik</p>', unsafe_allow_html=True)
kolom_numerik = df.select_dtypes(include=['float64', 'int64'])
matrix_korelasi = kolom_numerik.corr()
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(matrix_korelasi, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Visualisasi 1: Pengaruh Suhu terhadap Jumlah Peminjaman
st.markdown('<p class="big-font">🌡️ Pengaruh Suhu terhadap Peminjaman Sepeda</p>', unsafe_allow_html=True)
bins = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
labels = ['0.0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1.0']
df['temp_interval'] = pd.cut(df['temp'], bins=bins, labels=labels, right=False)
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(x='temp_interval', data=df, palette='coolwarm', ax=ax)
ax.set_xlabel('Interval Suhu')
ax.set_ylabel('Total Rentals (cnt)')
st.pyplot(fig)

# Line Plot Hubungan Suhu dan Peminjaman Sepeda
fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(x='temp', y='cnt', data=df, color='purple', ax=ax)
ax.set_xlabel('Temperature')
ax.set_ylabel('Total Rentals (cnt)')
st.pyplot(fig)

# Visualisasi 2: Perbedaan Peminjaman berdasarkan Hari Kerja vs Hari Libur
st.markdown('<p class="big-font">📅 Peminjaman Sepeda: Hari Kerja vs Hari Libur</p>', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(x='workingday', data=df, palette='Set1', hue='workingday', ax=ax, legend=False)
ax.set_xlabel('Working Day (0 = Hari Libur, 1 = Hari Kerja)')
ax.set_ylabel('Total Rentals (cnt)')
st.pyplot(fig)

# Kesimpulan
st.markdown('<p class="big-font">📌 Kesimpulan</p>', unsafe_allow_html=True)
st.markdown("""
1. **Pengaruh Suhu terhadap Peminjaman Sepeda:**
   - Semakin tinggi suhu, jumlah peminjaman meningkat.
   - Kategori suhu tertentu memiliki lebih banyak peminjaman.
2. **Perbedaan Peminjaman di Hari Kerja dan Hari Libur:**
   - Peminjaman lebih tinggi pada hari kerja dibanding hari libur.
   - Indikasi bahwa sepeda digunakan lebih banyak sebagai alat transportasi harian.
""")
