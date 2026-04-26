# 🚲 Bike Sharing Analytics Dashboard

Dashboard interaktif untuk menganalisis pola peminjaman sepeda di Washington D.C. (2011–2012) berdasarkan faktor waktu, cuaca, musim, dan tipe hari.

## Author

**Shellomitha Sulvana Dewi - CDCC284D6X2761**

Proyek Akhir · Belajar Fundamental Analisis Data
Coding Camp 2026 powered by DBS Foundation × Dicoding

## Pertanyaan Bisnis

Analisis ini menggunakan framework **SMART** dalam merumuskan pertanyaan bisnis:

1. Bagaimana pola rata-rata jumlah peminjaman sepeda per jam (registered vs casual) berdasarkan kategori waktu selama 2011–2012, dan jam berapa yang memiliki permintaan tertinggi untuk optimasi ketersediaan armada?

2. Bagaimana pengaruh kondisi cuaca terhadap rata-rata peminjaman sepeda harian selama 2011–2012, dan kondisi cuaca apa yang paling signifikan menyebabkan penurunan permintaan lebih dari 30%?

3. Berapa pertumbuhan total peminjaman secara bulanan (Month-over-Month) selama 2011–2012, dan bulan apa yang mengalami pertumbuhan atau penurunan terbesar?

4. Apakah terdapat perbedaan signifikan rata-rata peminjaman antara hari kerja dan hari libur/weekend pada setiap musim selama 2011–2012?

## Dataset
Dataset yang digunakan:
- `hour.csv` → data peminjaman per jam (17.379 records)
- `day.csv` → data peminjaman per hari (731 records)

##  Fitur Dashboard
- Ringkasan metrik utama (total peminjaman, rata-rata harian, puncak harian)
- Analisis pola peminjaman per jam (registered vs casual)
- Analisis pengaruh kondisi cuaca terhadap peminjaman
- Tren bulanan & Month-over-Month growth
- Perbandingan peminjaman per musim dan tipe hari
- Analisis korelasi antar variabel & 5 hari tersibuk
- Filter interaktif berdasarkan tahun

## Hasil & Insight Utama

### Pola Peminjaman Per Jam

Pengguna **registered** memiliki pola bimodal dengan puncak pada jam **08.00 (335 unit)** saat berangkat kerja dan jam **17.00–18.00 (385–461 unit)** saat pulang kerja — mencerminkan aktivitas komuter. Pengguna **casual** lebih aktif merata di siang hingga sore (10.00–19.00) dengan rata-rata 60–75 unit per jam untuk rekreasi. **Sore hari (15.00–19.00)** menjadi kategori waktu dengan permintaan tertinggi secara keseluruhan (352 unit), menjadikannya prioritas utama untuk optimasi ketersediaan armada.

### Pengaruh Kondisi Cuaca

Cuaca terbukti berpengaruh signifikan. Cuaca **Clear** menghasilkan peminjaman tertinggi sebesar 4.877 unit/hari. **Cloudy/Mist** menyebabkan penurunan 17.2% (4.036 unit) — belum melampaui threshold 30%. **Light Rain/Snow** menjadi kondisi paling kritis dengan penurunan drastis **63%** (1.803 unit/hari) — jauh melampaui threshold yang ditetapkan.
➡️ Hal ini membuka peluang penerapan **harga dinamis** dan strategi promosi saat cuaca buruk.

### Tren Bulanan (MoM Growth)

Total peminjaman tumbuh konsisten dari 2011 ke 2012, dengan puncak tertinggi pada **September 2012 (219K unit)**. Pertumbuhan MoM tertinggi terjadi pada **Maret 2012 (+60%)**, didorong transisi musim dingin ke semi. Penurunan terbesar terjadi pada **November 2012 (−23%)**, konsisten dengan datangnya musim dingin.
➡️ Pola musiman ini berulang di kedua tahun sehingga dapat diprediksi untuk perencanaan armada jangka panjang.

### Musim & Hari Kerja

Terdapat perbedaan nyata antara hari kerja dan non-kerja di setiap musim. Musim **Fall** mencatat permintaan tertinggi — Workday 5.718 dan Non-Workday 5.475. Musim **Spring** terendah — Workday 2.781 dan Non-Workday 2.257. Hari kerja secara konsisten lebih tinggi di semua musim kecuali **Summer**, di mana Non-Workday (5.142) justru melampaui Workday (4.927).
➡️ Hal ini menunjukkan dominasi penggunaan rekreasi pada musim panas.

## Rekomendasi Action Item

*  **Optimasi armada jam puncak**
  Tambahkan ketersediaan sepeda pada jam 07.00–09.00 dan 16.00–19.00, terutama di hari kerja untuk mendukung kebutuhan komuter.

*  **Strategi cuaca buruk**
  Terapkan harga dinamis atau promo saat hujan karena permintaan bisa turun hingga 63%.

*  **Perencanaan musiman**
  Lakukan maintenance saat Winter dan siapkan armada penuh menjelang Spring–Summer.

*  **Retensi pengguna casual**
  Buat paket berlangganan khusus weekend di Summer & Fall untuk meningkatkan konversi ke registered user.

*  **Antisipasi musim Fall**
  Pastikan kapasitas armada maksimal karena ini periode tersibuk sepanjang tahun.

##  Kesimpulan

Permintaan peminjaman sepeda dipengaruhi oleh pola waktu harian, musim, dan kondisi cuaca. Penggunaan didominasi oleh aktivitas komuter dengan pola yang konsisten, sementara faktor lingkungan seperti suhu dan cuaca memiliki dampak signifikan terhadap fluktuasi permintaan. Dengan memahami pola ini, strategi operasional, distribusi armada, dan kebijakan harga dapat dioptimalkan secara lebih efektif dan berbasis data.

## Struktur File

```
├── dashboard.py                          
├── Notebook_Proyek_Analisis_Data.ipynb   
├── hour.csv                              
├── day.csv                               
├── requirements.txt                      
└── README.md
```

## Setup Environment
```bash
pip install -r requirements.txt
```

## Run Streamlit App
```bash
streamlit run dashboard.py
```

Buka di browser: `http://localhost:8501`

##  Sumber Data

Bike Sharing Dataset (2011–2012) — Capital Bikeshare, Washington D.C.  
Fanaee-T & Gama (2013)
