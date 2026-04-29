import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")
sns.set_theme(style="white")

# --- 2. LOAD DATA ---
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    
    if not os.path.exists(file_path):
        st.error(f"File {file_path} tidak ditemukan!")
        return pd.DataFrame()

    df = pd.read_csv(file_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Pre-processing Kategorikal Bulan
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    if 'mnth' in df.columns:
        df['mnth'] = pd.Categorical(df['mnth'], categories=month_order, ordered=True)
    
    # Manual Grouping untuk Performa Harian
    bins = [0, 3100, 6000, df['cnt'].max()]
    labels = ['Low Performance', 'Medium Performance', 'High Performance']
    df['rental_category'] = pd.cut(df['cnt'], bins=bins, labels=labels)
    
    return df

main_df = load_data()

# Inisialisasi variabel
df_filtered = pd.DataFrame()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("Bike Sharing Analytics")
    
    # Logo Handling
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, "..", "img", "bike-sharing-logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path)
    
    st.markdown("### 📊 Filter Analisis")
    if not main_df.empty:
        year_options = sorted(main_df['yr'].unique())
        selected_year = st.selectbox("Pilih Tahun:", options=year_options)
        df_filtered = main_df[main_df['yr'] == selected_year]
    
    st.markdown("---")
    st.info("Dashboard ini menyajikan analisis mendalam mengenai pola penggunaan sepeda berdasarkan cuaca, waktu, dan suhu.")

# --- 4. MAIN PAGE ---
if df_filtered.empty:
    st.warning("Silakan periksa ketersediaan data pada file main_data.csv.")
else:
    st.title(f"Bike Sharing Interactive Dashboard 🚲")
    st.markdown(f"Eksplorasi Data Terintegrasi Tahun **{selected_year}**")

    # --- 5. KEY METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Rental", f"{df_filtered['cnt'].sum():,}")
    with col2:
        st.metric("Rata-rata Suhu", f"{round(df_filtered['temp'].mean() * 41, 1)}°C")
    with col3:
        registered_rate = (df_filtered['registered'].sum() / df_filtered['cnt'].sum()) * 100
        st.metric("Rasio Member", f"{registered_rate:.1f}%")
    with col4:
        high_perf_days = df_filtered[df_filtered['rental_category'] == 'High Performance'].shape[0]
        st.metric("Hari Performa Tinggi", f"{high_perf_days} Hari")

    st.divider()

    # --- BARIS 1: CUACA & MUSIM GUGUR ---
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("I. Rata-rata Sewa per Kondisi Cuaca")
        weather_data = df_filtered.groupby('weathersit', observed=False)['cnt'].mean().reset_index()
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        sns.barplot(x='weathersit', y='cnt', data=weather_data, palette='viridis', ax=ax1)
        for p in ax1.patches:
            ax1.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                         ha='center', va='bottom', fontsize=10, fontweight='bold')
        sns.despine(); st.pyplot(fig1)

    with col_b:
        st.subheader("II. Sewa Musim Gugur (Work vs Holiday)")
        fall_data = df_filtered[df_filtered['season'].isin(['Fall', 3])].copy()
        if not fall_data.empty:
            fall_data['mnth'] = fall_data['mnth'].astype(str)
            # Normalisasi label bulan 
            month_map = {'6': 'Jun', '7': 'Jul', '8': 'Aug', '9': 'Sep', 'Jun': 'Jun', 'Jul': 'Jul', 'Aug': 'Aug', 'Sep': 'Sep'}
            fall_data['mnth_display'] = fall_data['mnth'].map(month_map)
            fall_data['day_type'] = fall_data['workingday'].map({1: 'Working Day', 0: 'Holiday/Weekend'})
            fall_grouped = fall_data.groupby(['mnth_display', 'day_type'], observed=True)['cnt'].mean().reset_index()
            
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            sns.barplot(x='mnth_display', y='cnt', hue='day_type', data=fall_grouped, 
                        palette='Set2', order=['Jun', 'Jul', 'Aug', 'Sep'], ax=ax2)
            
            # Anotasi Angka Musim Gugur
            for p in ax2.patches:
                if p.get_height() > 0:
                    ax2.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                                 ha='center', va='bottom', fontsize=9, fontweight='bold', xytext=(0, 5), textcoords='offset points')
            
            ax2.legend(title=None, frameon=False, loc='upper right', fontsize='small')
            ax2.set_ylim(0, fall_grouped['cnt'].max() * 1.15)
            sns.despine(); st.pyplot(fig2)
        else:
            st.info("Data Musim Gugur tidak tersedia.")

    st.divider()

    # --- BARIS 2: YOY & KORELASI SUHU ---
    col_c, col_d = st.columns(2)
    
    with col_c:
        st.subheader("III. Pertumbuhan Penyewaan (YoY)")
        yearly_total = main_df.groupby('yr')['cnt'].sum().reset_index()
        yearly_total['yr'] = yearly_total['yr'].map({0: 2011, 1: 2012}) if yearly_total['yr'].max() <=1 else yearly_total['yr']
        fig3, ax3 = plt.subplots(figsize=(8, 6))
        sns.barplot(x='yr', y='cnt', data=yearly_total, palette='Blues', ax=ax3)
        for p in ax3.patches:
            ax3.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                         ha='center', va='bottom', fontsize=11, fontweight='bold')
        sns.despine(); st.pyplot(fig3)

    with col_d:
        st.subheader("IV. Korelasi Suhu terhadap Sewa")
        fig4, ax4 = plt.subplots(figsize=(8, 6))
        correlation = df_filtered['temp'].corr(df_filtered['cnt'])
        sns.regplot(x='temp', y='cnt', data=df_filtered, scatter_kws={'alpha':0.3, 'color':'#2E86C1'}, 
                    line_kws={'color':'red', 'linewidth':2}, ci=None, ax=ax4)
        # Menampilkan teks Korelasi Pearson
        ax4.text(0.05, 0.95, f'Pearson Correlation: {correlation:.2f}', 
                 transform=ax4.transAxes, fontsize=12, fontweight='bold', bbox=dict(facecolor='white', alpha=0.5))
        sns.despine(); st.pyplot(fig4)

    st.divider()

    # --- BARIS 3: RFM & PERFORMA HARIAN ---
    col_e, col_f = st.columns(2)

    with col_e:
        st.subheader("V. Analisis Lanjutan: RFM (Monthly)")
        recent_date = df_filtered['dteday'].max() + pd.Timedelta(days=1)
        rfm_df = df_filtered.groupby(by="mnth", observed=False).agg({
            "dteday": lambda x: (recent_date - x.max()).days,
            "cnt": ["count", "sum"]
        })
        rfm_df.columns = ["Recency", "Frequency", "Monetary"]
        st.write("") 
        st.dataframe(rfm_df.style.background_gradient(cmap='YlGnBu'), use_container_width=True, height=350)

    with col_f:
        st.subheader("VI. Analisis Performa Harian")
        fig6, ax6 = plt.subplots(figsize=(8, 6))
        sns.countplot(x='rental_category', data=df_filtered, palette='viridis', 
                      order=['Low Performance', 'Medium Performance', 'High Performance'], ax=ax6)
        for p in ax6.patches:
            ax6.annotate(f'{int(p.get_height())} Hari', (p.get_x() + p.get_width() / 2., p.get_height()), 
                         ha='center', va='bottom', fontsize=10, fontweight='bold')
        sns.despine(); st.pyplot(fig6)

# --- 9. FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Copyright © Dian Ayu A 2026 | Proyek Analisis Data - Bike Sharing Dataset</p>", unsafe_allow_html=True)