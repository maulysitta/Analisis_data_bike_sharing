# Bike Sharing Dashboard 🚲

Dashboard interaktif untuk menganalisis data penyewaan sepeda tahun 2011–2012 menggunakan Streamlit.

## Setup Environment - Anaconda
bash
conda create --name bike-sharing python=3.9
conda activate bike-sharing
pip install -r requirements.txt

## Setup Environment - Shell/Terminal
Bash
mkdir bike-sharing
cd bike-sharing
pip install -r requirements.txt

## Run Streamlit App
streamlit run dashboard.py

## Fitur Dashboard
- Melihat total, rerata, dan distribusi pengguna penyewaan sepeda (Registered vs Casual).
- Memfilter data secara interaktif berdasarkan rentang tanggal dan musim (Spring, Summer, Fall, Winter).
- Menganalisis pola rerata penyewaan per jam pada hari kerja untuk mendeteksi jam sibuk (peak hours).
- Menganalisis dampak kondisi cuaca (Clear, Misty, Light Snow/Rain) dan musim terhadap volume penyewaan harian.

## Dataset
Dataset yang digunakan adalah Bike Sharing Dataset yang terdiri dari berkas day.csv dan hour.csv

## Tools
- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit
