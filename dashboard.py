import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CSS — Minimal, Colorful Pink Theme
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
* { font-family: 'Plus Jakarta Sans', sans-serif !important; }
html, body, [class*="css"], [data-testid] { 
    font-family: 'Plus Jakarta Sans', sans-serif !important; 
}

.stApp { background: #fff0f6; }
.block-container { padding: 1.5rem 2rem 3rem !important; max-width: 100% !important; }
#MainMenu, footer, header { visibility: hidden; }

[data-testid="stSidebar"] { background: #ffe4f0 !important; border-right: 2px solid #ffb3d1 !important; }

/* insight box */
.insight-box {
    background: #fff;
    border-left: 4px solid #e91e8c;
    border-radius: 0 12px 12px 0;
    padding: 12px 16px;
    margin: 8px 0 16px 0;
    font-size: 13px;
    color: #555;
    line-height: 1.7;
}
.insight-box strong { color: #e91e8c; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# COLOR PALETTE — Colorful / Pink
# ─────────────────────────────────────────
C = {
    'pink':   '#e91e8c',
    'purple': '#9c27b0',
    'blue':   '#2196f3',
    'teal':   '#00bcd4',
    'green':  '#4caf50',
    'orange': '#ff9800',
    'red':    '#f44336',
    'yellow': '#ffeb3b',
}

BG   = '#fff8fb'   # chart background
GRID = '#ffe0ef'   # chart grid

plt.rcParams.update({
    'figure.facecolor':  BG,
    'axes.facecolor':    BG,
    'axes.edgecolor':    '#ffb3d1',
    'axes.labelcolor':   '#880e4f',
    'xtick.color':       '#ad1457',
    'ytick.color':       '#ad1457',
    'grid.color':        GRID,
    'text.color':        '#4a0030',
    'legend.facecolor':  BG,
    'legend.edgecolor':  '#ffb3d1',
    'font.family':       'sans-serif',
    'axes.spines.top':   False,
    'axes.spines.right': False,
    'axes.grid':         True,
    'grid.alpha':        1.0,
    'grid.linestyle':    '-',
    'grid.linewidth':    0.6,
})

# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    base = Path(__file__).parent
    df_hour = pd.read_csv(base / 'hour.csv')
    df_day  = pd.read_csv(base / 'day.csv')
    for df in [df_hour, df_day]:
        df['dteday']           = pd.to_datetime(df['dteday'])
        df['season_label']     = df['season'].map({1:'Spring',2:'Summer',3:'Fall',4:'Winter'})
        df['weather_label']    = df['weathersit'].map({1:'Clear',2:'Cloudy/Mist',3:'Light Rain/Snow',4:'Heavy Rain/Storm'})
        df['year_label']       = df['yr'].map({0:'2011',1:'2012'})
        df['workingday_label'] = df['workingday'].map({0:'Non-Workday',1:'Workday'})
    def cat_hour(h):
        if 5 <= h <= 9:              return 'Pagi (05-09)'
        elif 10 <= h <= 14:          return 'Siang (10-14)'
        elif 15 <= h <= 19:          return 'Sore (15-19)'
        else:                        return 'Malam (20-04)'
    df_hour['time_category'] = df_hour['hr'].apply(cat_hour)
    monthly                  = df_day.groupby(df_day['dteday'].dt.to_period('M'))['cnt'].sum().reset_index()
    monthly.columns          = ['year_month','total_cnt']
    monthly['mom_growth']    = monthly['total_cnt'].pct_change() * 100
    monthly['year_month_str']= monthly['year_month'].astype(str)
    return df_hour, df_day, monthly

try:
    df_hour, df_day, monthly = load_data()
    data_ok = True
except FileNotFoundError:
    data_ok = False

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='text-align:center; font-size:60px;'>🚲</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-weight:700; font-size:18px;'>Bike Sharing</div>", unsafe_allow_html=True)
    st.caption("<div style='text-align:center;'>Washington D.C. (2011–2012)</div>", unsafe_allow_html=True)
    st.divider()


    if data_ok:
        st.markdown("**Filter Tahun**")
        yr_filter = st.multiselect("", ["2011","2012"], default=["2011","2012"], label_visibility="collapsed")
        df_hour_f = df_hour[df_hour['year_label'].isin(yr_filter)] if yr_filter else df_hour
        df_day_f  = df_day[df_day['year_label'].isin(yr_filter)]   if yr_filter else df_day

    st.divider()
    st.markdown("**Author**")
    st.markdown("Shellomitha Sulvana Dewi")
    st.caption("Project Akhir - Belajar Fundamental Analisis Data ·  Coding Camp 2026 powered by DBS Foundation - Dicoding")

# ─────────────────────────────────────────
# ERROR
# ─────────────────────────────────────────
if not data_ok:
    st.error("❌ File `hour.csv` dan `day.csv` tidak ditemukan. Letakkan di folder yang sama dengan file ini.")
    st.stop()

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def page_header(emoji, title, sub):
    st.title(f"{emoji} {title}")
    st.caption(sub)
    st.divider()

def insight(txt):
    st.markdown(f'<div class="insight-box">💡 {txt}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
# RINGKASAN — Selalu tampil (bukan tab)
# ─────────────────────────────────────────
st.title("🚲 Bike Sharing Analytics")
st.markdown("Analisis Pola Peminjaman Sepeda Berdasarkan Faktor Musiman dan Tipe Hari di Washington D.C. (2011–2012)")
st.divider()

total    = df_day_f['cnt'].sum()
avg_d    = df_day_f['cnt'].mean()
peak_val = df_day_f['cnt'].max()
peak_day = df_day_f.loc[df_day_f['cnt'].idxmax(),'dteday'].strftime('%d %b %Y')
reg_pct  = df_day_f['registered'].sum() / df_day_f['cnt'].sum() * 100

c1, c2, c3, c4 = st.columns(4)
c1.metric("🚲 Total Peminjaman",      f"{total/1e6:.2f}M",    "Seluruh periode")
c2.metric("📅 Rata-rata / Hari",       f"{avg_d:,.0f}",        "Unit per hari")
c3.metric("🏆 Puncak Harian",          f"{peak_val:,}",        peak_day)
c4.metric("👤 Pengguna Registered",    f"{reg_pct:.0f}%",      f"Casual {100-reg_pct:.0f}%")

st.subheader("Tren Peminjaman Harian")
fig, ax = plt.subplots(figsize=(14, 4))
ax.fill_between(df_day_f['dteday'], df_day_f['cnt'], alpha=0.25, color=C['pink'])
ax.plot(df_day_f['dteday'], df_day_f['cnt'], color=C['pink'], lw=2)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{x/1000:.0f}K'))
ax.set_ylabel("Total Peminjaman")
fig.tight_layout(pad=1.5)
st.pyplot(fig); plt.close()

insight("<strong>Dataset mencakup 731 hari (2011–2012)</strong> dengan total lebih dari 3 juta peminjaman. "
        "Pengguna <strong>registered mendominasi ~81%</strong> total peminjaman — mayoritas komuter rutin. "
        "Tren keseluruhan menunjukkan pertumbuhan konsisten dari tahun ke tahun.")

st.divider()

# ─────────────────────────────────────────
# TABS NAVIGASI — Di bawah ringkasan
# ─────────────────────────────────────────
tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🕐 Pola Per Jam",
    "🌤️ Pengaruh Cuaca",
    "📈 Tren Bulanan",
    "🍂 Musim & Hari Kerja",
    "🔬 Analisis Lanjutan",
])

# ─────────────────────────────────────────
# TAB 2: POLA PER JAM
# ─────────────────────────────────────────
with tab2:
    page_header("🕐", "Pola Peminjaman Per Jam", "Bagaimana pola penggunaan sepeda berubah sepanjang hari?")

    hourly   = df_hour_f.groupby('hr')[['casual','registered','cnt']].mean().reset_index()
    time_avg = df_hour_f.groupby('time_category')[['casual','registered','cnt']].mean().reset_index()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))

    ax1.fill_between(hourly['hr'], hourly['registered'], alpha=0.2, color=C['pink'])
    ax1.fill_between(hourly['hr'], hourly['casual'],     alpha=0.2, color=C['purple'])
    ax1.plot(hourly['hr'], hourly['registered'], color=C['pink'],   lw=2.5, marker='o', ms=3, label='Registered')
    ax1.plot(hourly['hr'], hourly['casual'],     color=C['purple'], lw=2.5, marker='s', ms=3, label='Casual')
    ax1.axvspan(7,  9,  alpha=0.08, color=C['blue'])
    ax1.axvspan(16, 19, alpha=0.08, color=C['orange'])
    y_max = max(hourly['registered'].max(), hourly['casual'].max())
    ax1.text(8,  y_max * 0.85, 'Rush AM', fontsize=9, color=C['blue'],   alpha=0.9, ha='center', fontweight='bold')
    ax1.text(17, y_max * 0.85, 'Rush PM', fontsize=9, color=C['orange'], alpha=0.9, ha='center', fontweight='bold')
    ax1.set_title('Pola Per Jam: Registered vs Casual', fontweight='bold', pad=12)
    ax1.set_xlabel('Jam'); ax1.set_ylabel('Rata-rata Peminjaman')
    ax1.set_xticks(range(0, 24)); ax1.legend(fontsize=9)

    time_order = ['Pagi (05-09)', 'Siang (10-14)', 'Sore (15-19)', 'Malam (20-04)']
    tp = time_avg.set_index('time_category').reindex(time_order)
    x = np.arange(len(time_order)); w = 0.3
    b1 = ax2.bar(x - w/2, tp['registered'], w, color=C['pink'],   alpha=0.85, label='Registered')
    b2 = ax2.bar(x + w/2, tp['casual'],     w, color=C['purple'], alpha=0.85, label='Casual')
    for bar in b1:
        ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+3,
                 f'{bar.get_height():.0f}', ha='center', fontsize=8, fontweight='bold', color=C['pink'])
    for bar in b2:
        ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+3,
                 f'{bar.get_height():.0f}', ha='center', fontsize=8, fontweight='bold', color=C['purple'])
    ax2.set_xticks(x); ax2.set_xticklabels(time_order, rotation=15)
    ax2.set_title('Rata-rata per Kategori Waktu', fontweight='bold', pad=12)
    ax2.set_ylabel('Rata-rata Peminjaman'); ax2.legend(fontsize=9)

    fig.tight_layout(pad=2)
    st.pyplot(fig); plt.close()

    peak_pagi = hourly.loc[hourly['hr'].between(5, 9),   'registered'].max()
    peak_sore = hourly.loc[hourly['hr'].between(15, 19), 'registered'].max()
    peak_cat  = time_avg.loc[time_avg['cnt'].idxmax(), 'time_category']

    c1, c2, c3 = st.columns(3)
    c1.metric("🌅 Puncak Pagi",  f"{peak_pagi:.0f} unit", "Registered · jam 05–09")
    c2.metric("🌇 Puncak Sore",  f"{peak_sore:.0f} unit", "Registered · jam 15–19")
    c3.metric("⏰ Periode Ramai", peak_cat,                "Rata-rata tertinggi")

    insight("Pengguna <strong>registered</strong> memiliki pola bimodal — puncak jam <strong>08.00 (~335 unit)</strong> dan "
            "<strong>17.00–18.00 (~461 unit)</strong>, mencerminkan komuter. "
            "Pengguna <strong>casual</strong> aktif merata di siang–sore untuk rekreasi. "
            "<strong>Sore hari (15–19)</strong> adalah periode permintaan tertinggi secara keseluruhan.")

# ─────────────────────────────────────────
# TAB 3: PENGARUH CUACA
# ─────────────────────────────────────────
with tab3:
    page_header("🌤️", "Pengaruh Kondisi Cuaca", "Seberapa besar cuaca memengaruhi jumlah peminjaman harian?")

    wa = df_day_f.groupby('weather_label')['cnt'].mean().reset_index()
    wa.columns = ['Kondisi Cuaca', 'Rata-rata Peminjaman']
    wa = wa.sort_values('Rata-rata Peminjaman', ascending=False)
    baseline = wa[wa['Kondisi Cuaca'] == 'Clear']['Rata-rata Peminjaman'].values[0]
    wa['penurunan_pct'] = ((wa['Rata-rata Peminjaman'] - baseline) / baseline * 100).round(2)

    wc = {'Clear': C['green'], 'Cloudy/Mist': C['blue'], 'Light Rain/Snow': C['orange'], 'Heavy Rain/Storm': C['red']}
    colors = [wc.get(c, C['pink']) for c in wa['Kondisi Cuaca']]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(wa['Kondisi Cuaca'], wa['Rata-rata Peminjaman'],
                  color=colors, alpha=0.85, edgecolor=BG, linewidth=2, width=0.5)
    for bar, row in zip(bars, wa.itertuples()):
        h = bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2, h + 40,
                f'{h:.0f}\n({row.penurunan_pct:.1f}%)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.axhline(y=baseline, color='#888', linestyle='--', alpha=0.6, lw=1.5, label='Baseline (Clear)')
    ax.set_title('Rata-rata Peminjaman Harian Berdasarkan Kondisi Cuaca', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Kondisi Cuaca'); ax.set_ylabel('Rata-rata Peminjaman')
    ax.set_ylim(0, baseline * 1.3); ax.legend()
    fig.tight_layout(pad=1.5)
    st.pyplot(fig); plt.close()

    def get_weather_val(label):
        row = wa[wa['Kondisi Cuaca'] == label]
        if row.empty: return 0, 0
        return row['Rata-rata Peminjaman'].values[0], row['penurunan_pct'].values[0]

    v_clear, p_clear = get_weather_val('Clear')
    v_cloud, p_cloud = get_weather_val('Cloudy/Mist')
    v_rain,  p_rain  = get_weather_val('Light Rain/Snow')

    c1, c2, c3 = st.columns(3)
    c1.metric("☀️ Clear",           f"{v_clear:,.0f}", f"Baseline · {p_clear:.1f}%")
    c2.metric("🌥️ Cloudy / Mist",   f"{v_cloud:,.0f}", f"↓ Turun {abs(p_cloud):.1f}%")
    c3.metric("🌧️ Light Rain/Snow", f"{v_rain:,.0f}",  f"↓ Turun {abs(p_rain):.1f}%")

    insight("Hanya <strong>Light Rain/Snow</strong> yang melampaui threshold penurunan 30% — turun <strong>63%</strong> dari baseline Clear. "
            "Cloudy/Mist hanya turun 17.2%, masih dalam batas wajar. "
            "<strong>Heavy Rain/Storm tidak tercatat</strong> di dataset harian. "
            "→ Rekomendasikan <strong>harga dinamis atau promosi diskon</strong> saat prakiraan hujan.")

# ─────────────────────────────────────────
# TAB 4: TREN BULANAN
# ─────────────────────────────────────────
with tab4:
    page_header("📈", "Tren Bulanan & MoM Growth", "Bagaimana pertumbuhan peminjaman dari bulan ke bulan?")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    fig.suptitle('Tren Bulanan Peminjaman Sepeda & Pertumbuhan MoM (2011–2012)',
                 fontsize=13, fontweight='bold', y=1.01)

    ax1.fill_between(monthly['year_month_str'], monthly['total_cnt'], alpha=0.2, color=C['pink'])
    ax1.plot(monthly['year_month_str'], monthly['total_cnt'], color=C['pink'], lw=2.5, marker='o', ms=5)
    ax1.set_ylabel('Total Peminjaman'); ax1.set_title('Total Peminjaman Bulanan')
    ax1.tick_params(axis='x', rotation=45, labelsize=9)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}K'))

    max_i = monthly['total_cnt'].idxmax(); min_i = monthly['total_cnt'].idxmin()
    for idx, off in [(max_i, 12), (min_i, -18)]:
        ax1.annotate(f"{monthly.loc[idx,'total_cnt']/1000:.0f}K",
                     xy=(monthly.loc[idx,'year_month_str'], monthly.loc[idx,'total_cnt']),
                     xytext=(0, off), textcoords='offset points',
                     ha='center', fontsize=9, fontweight='bold', color=C['pink'])

    mom_vals   = monthly['mom_growth'].fillna(0)
    bar_colors = [C['green'] if v >= 0 else C['red'] for v in mom_vals]
    ax2.bar(monthly['year_month_str'], monthly['mom_growth'], color=bar_colors, alpha=0.85)
    ax2.axhline(0, color='#aaa', lw=0.8)
    ax2.set_ylabel('Pertumbuhan MoM (%)'); ax2.set_title('Month-over-Month Growth (%)')
    ax2.tick_params(axis='x', rotation=45, labelsize=9)
    for bar, val in zip(ax2.patches, mom_vals):
        if abs(val) > 15:
            ax2.text(bar.get_x()+bar.get_width()/2, val + (1 if val > 0 else -2),
                     f'{val:.0f}%', ha='center', fontsize=8, fontweight='bold',
                     color=C['green'] if val > 0 else C['red'])
    for ax in [ax1, ax2]:
        ax.axvline(x='2012-01', color=C['purple'], linestyle='--', alpha=0.5, lw=1.2)
    ax1.text('2012-01', ax1.get_ylim()[1] * 0.92, '  2012', fontsize=9, color=C['purple'], fontweight='bold')

    fig.tight_layout(pad=2)
    st.pyplot(fig); plt.close()

    peak_row = monthly.loc[monthly['total_cnt'].idxmax()]
    mom_pos  = monthly[monthly['mom_growth'] > 0].nlargest(1, 'mom_growth').iloc[0]
    mom_neg  = monthly[monthly['mom_growth'] < 0].nsmallest(1, 'mom_growth').iloc[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("📈 Puncak Tertinggi",    f"{peak_row['total_cnt']/1000:.0f}K", peak_row['year_month_str'])
    c2.metric("🚀 MoM Growth Terbesar", f"+{mom_pos['mom_growth']:.0f}%",     mom_pos['year_month_str'])
    c3.metric("📉 Penurunan Terbesar",  f"{mom_neg['mom_growth']:.0f}%",      mom_neg['year_month_str'])

    insight("Puncak tertinggi tercapai pada <strong>September 2012 (219K)</strong>. "
            "Pertumbuhan MoM terbesar di <strong>Maret 2012 (+60%)</strong> — transisi musim dingin ke semi. "
            "Penurunan terbesar di <strong>November 2012 (−23%)</strong>. "
            "Pola musiman <strong>berulang konsisten</strong> di kedua tahun → dapat diprediksi untuk perencanaan armada.")

# ─────────────────────────────────────────
# TAB 5: MUSIM & HARI KERJA
# ─────────────────────────────────────────
with tab5:
    page_header("🍂", "Musim & Hari Kerja", "Apakah musim dan jenis hari memengaruhi pola peminjaman?")

    sw = df_day_f.groupby(['season_label','workingday_label'])['cnt'].mean().reset_index()
    sw.columns = ['Musim','Tipe Hari','Rata-rata Peminjaman']
    pivot = sw.pivot(index='Musim', columns='Tipe Hari', values='Rata-rata Peminjaman')
    pivot = pivot.reindex(['Spring','Summer','Fall','Winter'])

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(4); w = 0.35
    wk  = pivot.get('Workday',     pd.Series([0]*4, index=pivot.index))
    nwk = pivot.get('Non-Workday', pd.Series([0]*4, index=pivot.index))
    b1 = ax.bar(x - w/2, wk,  w, color=C['pink'],   alpha=0.85, label='Hari Kerja',     edgecolor=BG, lw=1.5)
    b2 = ax.bar(x + w/2, nwk, w, color=C['purple'], alpha=0.85, label='Hari Non-Kerja', edgecolor=BG, lw=1.5)
    for bar in b1:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+50,
                f'{bar.get_height():.0f}', ha='center', fontsize=9, fontweight='bold', color=C['pink'])
    for bar in b2:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+50,
                f'{bar.get_height():.0f}', ha='center', fontsize=9, fontweight='bold', color=C['purple'])
    ax.set_xticks(x); ax.set_xticklabels(['Spring','Summer','Fall','Winter'])
    ax.set_xlabel('Musim'); ax.set_ylabel('Rata-rata Peminjaman')
    ax.set_title('Rata-rata Peminjaman: Hari Kerja vs Non-Kerja per Musim', fontsize=12, fontweight='bold', pad=12)
    ax.legend()
    fig.tight_layout(pad=1.5)
    st.pyplot(fig); plt.close()

    sw_idx   = df_day_f.groupby(['season_label','workingday_label'])['cnt'].mean()
    fall_wk  = sw_idx.get(('Fall',   'Workday'),     0)
    fall_nwk = sw_idx.get(('Fall',   'Non-Workday'), 0)
    sum_nwk  = sw_idx.get(('Summer', 'Non-Workday'), 0)
    spr_nwk  = sw_idx.get(('Spring', 'Non-Workday'), 0)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🍂 Fall · Hari Kerja",  f"{fall_wk:,.0f}",  "Tertinggi keseluruhan")
    c2.metric("🍂 Fall · Non-Kerja",   f"{fall_nwk:,.0f}", "Runner up")
    c3.metric("☀️ Summer · Non-Kerja", f"{sum_nwk:,.0f}",  "Rekreasi dominan")
    c4.metric("🌱 Spring · Non-Kerja", f"{spr_nwk:,.0f}",  "Terendah keseluruhan")

    insight("Musim <strong>Fall tertinggi</strong> di semua kategori — Workday 5.718, Non-Workday 5.475. "
            "Musim <strong>Spring terendah</strong> — Workday 2.781, Non-Workday 2.257. "
            "Di <strong>Summer</strong> Non-Workday (5.142) melampaui Workday (4.927) — dominasi rekreasi musim panas. "
            "→ Strategi redistribusi sepeda perlu disesuaikan per musim dan jenis hari.")

# ─────────────────────────────────────────
# TAB 6: ANALISIS LANJUTAN
# ─────────────────────────────────────────
with tab6:
    page_header("🔬", "Analisis Lanjutan", "Korelasi antar variabel & hari-hari tersibuk")

    col1, col2 = st.columns(2)
    cmap = sns.diverging_palette(330, 200, as_cmap=True)

    with col1:
        st.subheader("Korelasi Faktor Lingkungan")
        corr_env = df_hour_f[['temp','hum','windspeed','cnt']].corr()
        fig, ax  = plt.subplots(figsize=(6, 5))
        sns.heatmap(corr_env, annot=True, fmt='.2f', cmap=cmap,
                    center=0, vmin=-1, vmax=1, square=True,
                    linewidths=2, linecolor=BG,
                    ax=ax, annot_kws={'size':12,'weight':'bold'})
        ax.set_title('Faktor Lingkungan vs Peminjaman', fontweight='bold', pad=12)
        ax.tick_params(axis='x', rotation=30)
        fig.tight_layout(); st.pyplot(fig); plt.close()

    with col2:
        st.subheader("Korelasi Semua Variabel Numerik")
        corr_all = df_hour_f[['temp','atemp','hum','windspeed','casual','registered','cnt']].corr()
        fig, ax  = plt.subplots(figsize=(6, 5))
        sns.heatmap(corr_all, annot=True, fmt='.2f', cmap=cmap,
                    center=0, vmin=-1, vmax=1, square=True,
                    linewidths=2, linecolor=BG,
                    ax=ax, annot_kws={'size':8,'weight':'bold'})
        ax.set_title('Semua Variabel Numerik', fontweight='bold', pad=12)
        ax.tick_params(axis='x', rotation=30)
        fig.tight_layout(); st.pyplot(fig); plt.close()

    insight("<strong>temp</strong> berkorelasi positif dengan cnt (~0.40) — suhu hangat mendorong lebih banyak peminjaman. "
            "<strong>hum</strong> berkorelasi negatif (~−0.32) — cuaca lembap mengurangi minat bersepeda. "
            "<strong>temp & atemp</strong> hampir identik (~0.99) — cukup gunakan salah satu untuk modeling. "
            "<strong>registered</strong> jauh lebih dominan terhadap cnt (~0.97) dibanding casual (~0.67).")

    st.subheader("🏆 5 Hari Tersibuk")
    busy = df_day_f.nlargest(5,'cnt')[['dteday','season_label','weather_label','cnt']].reset_index(drop=True)
    busy.index += 1
    busy.columns = ['Tanggal','Musim','Cuaca','Total Peminjaman']
    busy['Tanggal'] = busy['Tanggal'].dt.strftime('%d %b %Y')
    st.dataframe(busy, use_container_width=True)

    insight("Seluruh 5 hari tersibuk terjadi di musim <strong>Summer/Fall 2012</strong> — konsisten dengan cuaca Clear. "
            "Tidak ada hari tersibuk yang jatuh di musim Spring atau Winter. "
            "→ Konsentrasikan ketersediaan armada penuh pada periode <strong>Juni–September</strong>.")

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.divider()

col_l, col_r = st.columns([3, 1])

col_l.caption(
    "🚲 **Bike Sharing Analysis Dashboard** · "
    "Analisis Pola Peminjaman Sepeda Berdasarkan Musim & Tipe Hari · "
    "Washington D.C. (2011–2012)"
)
