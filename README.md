# submission-analisa-data
# Setup Environment - Shell/Terminal
mkdir submission
cd submission
pipenv install
pipenv shell
pip freeze > requirements.txt

# Run steamlit app
streamlit run dashboard/dashboard.py

# Dashboard Pola Penggunaan Sepeda

Aplikasi dashboard ini dibuat menggunakan Streamlit untuk menganalisis pola penggunaan sepeda berdasarkan data penyewaan sepeda dari berbagai sumber. Dengan aplikasi ini, pengguna dapat menjelajahi data dan membuat analisis interaktif mengenai penyewaan sepeda berdasarkan musim, jam, dan faktor-faktor lainnya.

## Fitur

1. **Pola Penggunaan Sepeda Berdasarkan Musim**:
   - Menampilkan distribusi sepeda Bedasarkan musim dan cuaca.
2. **Bagaimana perbandingan sewa sepeda pada hari libur dan bukan libur?**:
   - Menampilkan pola penyewaan sepeda berdasarkan hari libur dan bukan hari libur.
3. **Filter Data**:
   - Pengguna dapat memfilter data berdasarkan rentang musim cuaca dan tertentu dan memilih jam yang diinginkan untuk analisis.

## Struktur File

- **dashboard.py**: Aplikasi Streamlit yang menjalankan dashboard interaktif.
- **all_data.csv**: Berisi Data harian penyewaan sepeda dan penyeewan sepeda bedasarkan jam.
