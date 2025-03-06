import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi dasar Streamlit
st.set_page_config(page_title='Dashboard Interaktif Penyewaan Sepeda', layout='wide')

# Memuat data
all_data = pd.read_csv('all_data.csv')

# Membersihkan dataset
all_data = all_data[['dteday_x', 'season_x', 'mnth_x', 'hr', 'holiday_x', 'weekday_x',
                     'workingday_x', 'weathersit_x', 'temp_x', 'hum_x', 'windspeed_x',
                     'casual_x', 'registered_x', 'cnt_x']]

# Mengganti nama kolom
season_mapping = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
weather_mapping = {1: 'Cerah', 2: 'Berawan', 3: 'Hujan', 4: 'Kabut'}

all_data.columns = ['date', 'season', 'month', 'hour', 'holiday', 'weekday',
                    'workingday', 'weather', 'temp', 'humidity', 'windspeed',
                    'casual', 'registered', 'total_rentals']

all_data['season'] = all_data['season'].map(season_mapping)
all_data['weather'] = all_data['weather'].map(weather_mapping)

# Judul
st.title('Dashboard Analisis Penyewaan Sepeda')

# Sidebar untuk filter
st.sidebar.header('Filter Data')
selected_season = st.sidebar.selectbox('Pilih Musim', all_data['season'].unique())
selected_hour = st.sidebar.slider('Pilih Jam', min_value=all_data['hour'].min(), max_value=all_data['hour'].max())
selected_weather = st.sidebar.selectbox('Pilih Kondisi Cuaca', all_data['weather'].unique()) 

# Menampilkan data berdasarkan filter
filtered_data = all_data[(all_data['season'] == selected_season) & 
                         (all_data['hour'] == selected_hour) & 
                         (all_data['weather'] == selected_weather)]
st.write(f'Data untuk {selected_season}, jam {selected_hour}, dan kondisi cuaca {selected_weather}', 
         filtered_data.head())

# Visualisasi hasil filter data
fig, ax = plt.subplots()
sns.lineplot(data=filtered_data, y='total_rentals', x=filtered_data.index, marker='o', ax=ax, color='skyblue')

plt.xlabel('Indeks Data')
plt.ylabel('Total Penyewaan')
plt.title(f'Tren Penyewaan Sepeda pada {selected_season}, jam {selected_hour}, cuaca {selected_weather}')

st.pyplot(fig)


# Visualisasi jumlah penyewaan sepeda berdasarkan musim
st.subheader('Distribusi Jumlah Sewa Sepeda Berdasarkan Musim')
colors = ["#A3D1C6", "#A3D1C6", "#0D4715", "#A3D1C6"]
fig1, ax1 = plt.subplots()
sns.barplot(x='season', y='total_rentals', data=all_data, hue='season', palette=colors, ax=ax1, errorbar=None)
st.pyplot(fig1)

# Visualisasi jumlah penyewaan sepeda berdasarkan cuaca
st.subheader('Distribusi Jumlah Sewa Sepeda Berdasarkan Cuaca')
colors_weather = ["#0D4715", "#A3D1C6", "#A3D1C6", "#A3D1C6"]
fig2, ax2 = plt.subplots()
sns.barplot(x='weather', y='total_rentals', data=all_data, hue='weather', palette=colors_weather, ax=ax2, errorbar=None)
st.pyplot(fig2)

# Visualisasi distribusi penyewaan sepeda pada hari libur
st.subheader('Distribusi Jumlah Sewa Sepeda pada Hari Libur dan Bukan Libur')
fig3, ax3 = plt.subplots()
sns.histplot(data=all_data, x='total_rentals', hue='holiday', multiple='stack', kde=True, ax=ax3)
plt.legend(title=None, labels=['Bukan Libur', 'Libur'])
st.pyplot(fig3)

# Visualisasi rata-rata penyewaan sepeda per jam
st.subheader('Rata-rata Penyewaan Sepeda per Jam')
hourly_avg = all_data.groupby(by='hour')[['total_rentals', 'registered', 'casual']].mean().reset_index()
fig4, ax4 = plt.subplots()
sns.lineplot(data=hourly_avg, x='hour', y='total_rentals', label='Total Sewa Sepeda keseluruhan', marker='o', ax=ax4)
sns.lineplot(data=hourly_avg, x='hour', y='registered', label='Sewa oleh Pengguna Terdaftar', marker='o', ax=ax4)
sns.lineplot(data=hourly_avg, x='hour', y='casual', label='Sewa oleh Pengguna Casual', marker='o', ax=ax4)
st.pyplot(fig4)

# Analisis RFM
st.subheader('Analisis RFM (Recency, Frequency, Monetary)')
rfm_df = all_data.groupby('date', as_index=False).agg({
    'total_rentals': 'sum',  # Monetary
    'registered': 'sum',
    'casual': 'sum'
})
rfm_df['recency'] = (pd.to_datetime(all_data['date']).max() - pd.to_datetime(rfm_df['date'])).dt.days
rfm_df['frequency'] = rfm_df['registered'] + rfm_df['casual']
rfm_df['monetary'] = rfm_df['total_rentals']

# Visualisasi distribusi Recency, Frequency, Monetary
fig5, ax5 = plt.subplots()
sns.histplot(rfm_df['recency'], kde=True, color='blue', ax=ax5)
st.pyplot(fig5)

fig6, ax6 = plt.subplots()
sns.histplot(rfm_df['frequency'], kde=True, color='green', ax=ax6)
st.pyplot(fig6)

fig7, ax7 = plt.subplots()
sns.histplot(rfm_df['monetary'], kde=True, color='orange', ax=ax7)
st.pyplot(fig7)



# Checkbox untuk menampilkan raw data
if st.sidebar.checkbox('Tampilkan Data Mentah'):
    st.subheader('Data Mentah')
    st.write(all_data.head(50))

print(all_data['weathersit_x'].unique())  