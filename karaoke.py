import streamlit as st
import yt_dlp
import random

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Ruang Karaoke Online",
    page_icon="🎤",
    layout="wide"
)

# Judul Aplikasi
st.title("🎤 Ruang Karaoke Online & Smart Scoring System")
st.markdown("Cari lagu karaoke favoritmu langsung dari YouTube, nyanyi sepuasnya, dan uji skor vokalmu di sini!")

# Fungsi untuk mencari lagu di YouTube menggunakan yt-dlp
@st.cache_data(ttl=600)
def search_youtube(query, max_results=5):
    ydl_opts = {
        'format': 'best',
        'default_search': f'ytsearch{max_results}',
        'noplaylist': True,
        'quiet': True,
    }
    results = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    results.append({
                        'title': entry.get('title'),
                        'id': entry.get('id'),
                        'url': f"https://www.youtube.com/watch?v={entry.get('id')}",
                    })
    except Exception as e:
        st.error(f"Gagal mencari lagu: {e}")
    return results

# --- SIDEBAR: PENCARIAN & PILIHAN LAGU ---
st.sidebar.header("🔍 Cari Lagu di YouTube")
search_query = st.sidebar.text_input("Ketik judul lagu & artist:", "Judika Cinta Karena Cinta karaoke")

# Inisialisasi session state untuk video default
if 'selected_video_url' not in st.session_state:
    st.session_state['selected_video_url'] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    st.session_state['selected_title'] = "Silakan cari dan pilih lagu di sebelah kiri"

if st.sidebar.button("Cari Lagu 🔎", use_container_width=True):
    if search_query:
        with st.spinner("Sedang mencari lagu dari YouTube..."):
            st.session_state['search_results'] = search_youtube(search_query)
    else:
        st.sidebar.warning("Masukkan judul lagu terlebih dahulu!")

# Tampilkan hasil pencarian di sidebar jika ada
if 'search_results' in st.session_state and st.session_state['search_results']:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Pilih Hasil Pencarian:")
    for idx, song in enumerate(st.session_state['search_results']):
        if st.sidebar.button(f"▶ {song['title'][:40]}...", key=f"song_{idx}", use_container_width=True):
            st.session_state['selected_video_url'] = song['url']
            st.session_state['selected_title'] = song['title']
            st.session_state['score'] = None
            st.rerun()

# --- LAYOUT UTAMA ---
col1, col2 = st.columns([1.3, 0.7])

with col1:
    st.subheader(f"🎶 {st.session_state['selected_title']}")
    # Pemutar video YouTube
    st.video(st.session_state['selected_video_url'])
    
    # Tombol efek penonton
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("👏 Beri Tepuk Tangan", use_container_width=True):
            st.balloons()
            st.success("Prok prok prok! Penonton bersorak meriah! 🎉")
    with col_btn2:
        if st.button("🔥 Kasih Suasana Meriah", use_container_width=True):
            st.toast("Woohoo! Suasananya makin panas!", icon="🔥")

with col2:
    st.subheader("🏆 Mesin Juri Pintar")
    st.markdown("Selesai nyanyi? Pilih dulu bagaimana performa kamu hari ini:")

    # Pilihan penyesuaian skor agar lebih adil dan relevan
    vibe_penampilan = st.selectbox(
        "Bagaimana performa vokalmu tadi?",
        [
            "🔥 Totalitas, nada tinggi tembus, ekspresi dapet!",
            "🎸 Lumayan stabil, tapi ada fals dikit di bagian reff",
            "😅 Banyak lupa lirik & suara habis di tengah jalan",
            "🎤 Nyanyi sambil berteriak penuh emosi jiwa"
        ]
    )
    
    # Tombol Hitung Skor
    if st.button("Kalkulasi Nilai Juri 🎯", type="primary", use_container_width=True):
        if "Totalitas" in vibe_penampilan:
            generated_score = random.randint(90, 99)
            grade = "🌟 LUAR BIASA! Juri standing ovation melihat performamu!"
        elif "Lumayan" in vibe_penampilan:
            generated_score = random.randint(80, 89)
            grade = "🔥 KEREN! Tinggal poles sedikit lagi di nada tinggi, Bang."
        elif "Banyak lupa" in vibe_penampilan:
            generated_score = random.randint(60, 74)
            grade = "📉 HAMPIR KANDAS! Kurang banyak latihan, tapi semangatnya juara!"
        else:
            generated_score = random.randint(75, 88)
            grade = "💥 ENERGI LEVEL TINGGI! Tetangga sebelah sampe kebangun nih!"

        st.session_state['score'] = generated_score
        st.session_state['grade'] = grade

    # Tampilkan Hasil Skor Juri
    if 'score' in st.session_state and st.session_state['score'] is not None:
        st.metric(label="Skor Akhir Penampilan", value=f"{st.session_state['score']} / 100")
        st.info(st.session_state['grade'])
        
        if st.session_state['score'] >= 90:
            st.balloons()

    st.markdown("---")
    st.markdown("### 💡 Tips Karaoke:")
    st.markdown("""
    - Tambahkan kata **'karaoke'** atau **'instrumental'** di belakang pencarian agar langsung mendapatkan versi tanpa vokal asli.
    - Sistem nilai disesuaikan dengan tingkat kesulitan dan tingkat percaya diri performa kamu!
    """)

# Footer
st.markdown("---")
st.caption("Streamlit Online Karaoke App • Powered by Python & yt-dlp 🚀")