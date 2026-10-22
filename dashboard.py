import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi Tampilan Halaman
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# 1. Load Data dengan Caching agar Cepat
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    
    # Preprocessing singkat
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_mapping = {
        1: 'Clear/Partly Cloudy',
        2: 'Misty/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Heavy Rain/Ice Pallets'
    }
    
    day_df['season_label'] = day_df['season'].map(season_mapping)
    day_df['weather_label'] = day_df['weathersit'].map(weather_mapping)
    hour_df['season_label'] = hour_df['season'].map(season_mapping)
    hour_df['weather_label'] = hour_df['weathersit'].map(weather_mapping)
    
    return day_df, hour_df

day_df, hour_df = load_data()

# 2. Sidebar Filter
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2972/2972185.png", width=120)
st.sidebar.title("Filter Data")

# Filter Rentang Tanggal
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

try:
    start_date, end_date = st.sidebar.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
except ValueError:
    st.error("Pilih rentang tanggal yang valid.")
    start_date = min_date
    end_date = max_date

# Filter Musim
selected_season = st.sidebar.multiselect(
    "Pilih Musim:",
    options=day_df['season_label'].unique(),
    default=day_df['season_label'].unique()
)

# Filter Dataframe berdasarkan Sidebar
filtered_day_df = day_df[
    (day_df['dteday'] >= pd.to_datetime(start_date)) & 
    (day_df['dteday'] <= pd.to_datetime(end_date)) &
    (day_df['season_label'].isin(selected_season))
]

filtered_hour_df = hour_df[
    (hour_df['dteday'] >= pd.to_datetime(start_date)) & 
    (hour_df['dteday'] <= pd.to_datetime(end_date)) &
    (hour_df['season_label'].isin(selected_season))
]

# 3. Header & Key Performance Indicators (KPIs)
st.title("🚲 Bike Sharing Performance Dashboard")
st.markdown("Analisis interaktif penyewaan sepeda harian dan per jam berdasarkan musim dan cuaca.")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{filtered_day_df['cnt'].sum():,}")
with col2:
    st.metric("Pengguna Registered", value=f"{filtered_day_df['registered'].sum():,}")
with col3:
    st.metric("Pengguna Casual", value=f"{filtered_day_df['casual'].sum():,}")

st.divider()

# 4. Visualisasi Pertanyaan 1: Pola Peminjaman per Jam pada Hari Kerja
st.subheader("1. Pola Rata-Rata Penyewaan per Jam (Hari Kerja)")
hour_workingday = filtered_hour_df[filtered_hour_df['workingday'] == 1]
hourly_trend = hour_workingday.groupby('hr')[['casual', 'registered']].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(hourly_trend['hr'], hourly_trend['registered'], label='Registered Users', marker='o', color='#1f77b4', linewidth=2)
ax1.plot(hourly_trend['hr'], hourly_trend['casual'], label='Casual Users', marker='s', color='#ff7f0e', linewidth=2)
ax1.set_xlabel("Jam (00.00 - 23.00)")
ax1.set_ylabel("Rata-Rata Penyewaan")
ax1.set_xticks(range(0, 24))
ax1.legend()
ax1.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig1)

st.divider()

# 5. Visualisasi Pertanyaan 2: Pengaruh Musim & Cuaca
st.subheader("2. Rata-Rata Penyewaan Harian Berdasarkan Musim dan Cuaca")
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.barplot(
    data=filtered_day_df,
    x='season_label',
    y='cnt',
    hue='weather_label',
    palette='Blues_d',
    ax=ax2,
    errorbar=None
)
ax2.set_xlabel("Musim")
ax2.set_ylabel("Rata-Rata Penyewaan Harian")
ax2.legend(title="Kondisi Cuaca")
st.pyplot(fig2)

st.caption("Copyright © 2026 - Proyek Analisis Data Bike Sharing")
