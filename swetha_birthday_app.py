import streamlit as st
import time
import random
import math
import os
import io
import base64
from datetime import date, datetime, timedelta
from PIL import Image, ImageFilter, ImageEnhance
import requests
import numpy as np


# THEME SWITCHER
if "theme" not in st.session_state:
    st.session_state.theme = "pink"
theme_colors = {
    "pink": {
        "--primary-pink": "#ffb3d9",
        "--light-pink": "#ffeef0",
        "--soft-pink": "#ffcccb",
        "--rose-pink": "#ffc1e3",
        "--bubblegum": "#ff69b4",
        "--heart-gold": "#ffd700"
    },
    "lavender": {
        "--primary-pink": "#d1b3ff",
        "--light-pink": "#f3e8ff",
        "--soft-pink": "#e0c3fc",
        "--rose-pink": "#e9d6ff",
        "--bubblegum": "#b39ddb",
        "--heart-gold": "#ffd700"
    },
    "gold": {
        "--primary-pink": "#ffe066",
        "--light-pink": "#fff9e3",
        "--soft-pink": "#fff3bf",
        "--rose-pink": "#ffe066",
        "--bubblegum": "#ffd700",
        "--heart-gold": "#ffb300"
    }
}
st.sidebar.markdown("### 🎨 Theme")
theme_choice = st.sidebar.radio("Choose a theme", ["pink", "lavender", "gold"], index=["pink", "lavender", "gold"].index(st.session_state.theme), horizontal=True)
st.session_state.theme = theme_choice

theme_vars = theme_colors[st.session_state.theme]
theme_css = ":root {\n" + "\n".join([f"    {k}: {v};" for k, v in theme_vars.items()]) + "\n}"
st.markdown(f"<style>{theme_css}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="💖 Happy Birthday Swetha! 💖",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ENHANCED CUSTOM CSS - FIXED GIFT + MUSIC + RESPONSIVE
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;600;700&family=Satisfy&family=Poppins:wght@200;300;400;500;600;700&display=swap');
    /* ...existing code, but REMOVE the :root block above, so only the dynamic theme_css is used ... */
    section[data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, var(--light-pink) 0%, var(--primary-pink) 25%, var(--soft-pink) 50%, var(--rose-pink) 75%, var(--bubblegum) 100%);
        background-size: 400% 400%;
        animation: pinkGradientShift 20s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes pinkGradientShift {
        0%, 100% { background-position: 0% 50%; }
        25% { background-position: 100% 50%; }
        50% { background-position: 100% 100%; }
        75% { background-position: 0% 100%; }
    }
    
    .hearts-container {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none; z-index: 1000; overflow: hidden;
    }
    
    .blooming-heart {
        position: absolute; font-size: 20px; color: var(--bubblegum);
        animation: heartBloom 8s ease-in-out infinite; text-shadow: 0 0 10px var(--heart-gold);
    }
    
    @keyframes heartBloom {
        0% { transform: scale(0) rotate(0deg) translateY(100vh); opacity: 0; }
        10% { opacity: 1; }
        20% { transform: scale(1.2) rotate(180deg); }
        50% { transform: scale(1.5) rotate(360deg); }
        80% { transform: scale(1.2) rotate(720deg); }
        90% { opacity: 1; }
        100% { transform: scale(0) rotate(1080deg) translateY(-100px); opacity: 0; }
    }
    
    .main-title {
        font-family: 'Dancing Script', cursive !important; font-size: 6rem !important; font-weight: 700 !important;
        background: linear-gradient(45deg, #fff, var(--heart-gold), var(--bubblegum));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin: 30px 0;
        animation: titleGlowPulse 3s ease-in-out infinite; text-shadow: 0 0 40px var(--shadow-pink);
    }
    
    @keyframes titleGlowPulse {
        0%, 100% { filter: drop-shadow(0 0 20px var(--white-glow)) drop-shadow(0 0 40px var(--shadow-pink)); transform: scale(1); }
        50% { filter: drop-shadow(0 0 40px var(--heart-gold)) drop-shadow(0 0 80px var(--bubblegum)); transform: scale(1.05); }
    }
    
    .subtitle {
        font-family: 'Satisfy', cursive; font-size: 2.5rem !important; color: var(--bubblegum) !important;
        text-align: center; margin: 20px 0; animation: subtitleFloat 4s ease-in-out infinite;
    }
    
    @keyframes subtitleFloat { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-15px); } }
    
    .pink-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(255,238,240,0.9));
        backdrop-filter: blur(20px); border-radius: 25px; padding: 30px; margin: 15px 0;
        border: 2px solid var(--shadow-pink);
        box-shadow: 0 20px 60px rgba(255,107,180,0.3), inset 0 1px 0 rgba(255,255,255,0.8);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); position: relative; overflow: hidden;
    }
    
    .pink-card::before {
        content: '💖'; position: absolute; top: -50%; left: -50%; font-size: 100px; opacity: 0.05;
        animation: heartRotate 20s linear infinite;
    }
    
    @keyframes heartRotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    
    .pink-card:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0 30px 80px rgba(255,107,180,0.4), 0 0 40px rgba(255,182,217,0.6);
        border-color: var(--bubblegum);
    }
    
    /* FIXED GIFT BOX - WORKING VERSION */
    .gift-container {
        text-align: center;
        position: relative;
        display: inline-block;
        margin: 50px auto;
        z-index: 1001;
    }
    .gift-box {
        font-size: 8rem !important; 
        cursor: pointer; 
        display: block; 
        transition: all 0.3s ease;
        position: relative; 
        z-index: 10;
        animation: giftBounce 2s infinite;
    }
    .gift-box:hover {
        transform: scale(1.1);
        filter: drop-shadow(0 0 30px var(--heart-gold));
    }
    .gift-box.open {
        animation: shake 0.5s ease-in-out;
        transform: scale(0.8);
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0) rotate(0deg); }
        25% { transform: translateX(-15px) rotate(-5deg); }
        75% { transform: translateX(15px) rotate(5deg); }
    }
    @keyframes giftBounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-25px); }
        60% { transform: translateY(-12px); }
    }
    .puppy {
        position: absolute;
        top: -150px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 7rem;
        z-index: 20;
        opacity: 0;
        transition: all 0.6s ease;
    }
    .puppy.show {
        animation: jump-out 1.2s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
    }
    @keyframes jump-out {
        0% {
            opacity: 0;
            transform: translateX(-50%) translateY(0) scale(0) rotate(-180deg);
        }
        50% {
            opacity: 1;
            transform: translateX(-50%) translateY(-50px) scale(1.3) rotate(0deg);
        }
        100% {
            opacity: 1;
            transform: translateX(-50%) translateY(-180px) scale(1) rotate(10deg);
        }
    }
    .birthday-text {
        font-family: "Dancing Script", cursive;
        font-size: 3.5rem;
        color: var(--bubblegum);
        margin-top: 60px;
        opacity: 0;
        transform: translateY(30px);
    }
    .birthday-text.show {
        animation: fade-in-up 1s ease forwards 0.8s;
    }
    @keyframes fade-in-up {
        to { opacity: 1; transform: translateY(0); }
    }
    
    .puppy-surprise {
        font-size: 5rem !important; 
        animation: puppyDance 2s ease-in-out infinite;
        text-align: center; 
        margin: 50px 0;
    }
    @keyframes puppyDance { 
        0%, 100% { transform: rotate(-8deg) translateY(0); } 
        25% { transform: rotate(0deg) translateY(-10px); }
        75% { transform: rotate(8deg) translateY(-5px); }
    }
    
    .music-player {
        background: linear-gradient(145deg, rgba(255,255,255,0.9), var(--soft-pink));
        padding: 25px;
        border-radius: 25px;
        border: 3px solid var(--bubblegum);
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 15px 40px rgba(255,105,180,0.4);
    }
    
    .music-btn {
        background: linear-gradient(45deg, var(--bubblegum), var(--heart-gold));
        color: white !important;
        border: none !important;
        padding: 18px 40px !important;
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        border-radius: 40px !important;
        cursor: pointer !important;
        font-family: 'Poppins', sans-serif !important;
        margin: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(255,105,180,0.4);
    }
    .music-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(255,105,180,0.6);
    }
    .music-btn.playing {
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .wish-item {
        background: linear-gradient(45deg, var(--soft-pink), var(--rose-pink));
        padding: 20px; border-radius: 20px; margin: 15px 0; border-left: 5px solid var(--bubblegum);
        animation: wishSlide 0.8s ease-out;
    }
    
    @keyframes wishSlide { from { opacity: 0; transform: translateX(-50px); } to { opacity: 1; transform: translateX(0); } }
    
    .mega-btn {
        background: linear-gradient(45deg, var(--bubblegum), var(--heart-gold), var(--primary-pink));
        color: white !important; border: none !important; padding: 20px 50px !important;
        font-size: 1.6rem !important; font-weight: 600 !important; border-radius: 50px !important;
        cursor: pointer !important; font-family: 'Poppins', sans-serif !important; text-transform: uppercase;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255,238,240,0.95), rgba(255,179,217,0.9)) !important;
    }
    
    @media (max-width: 768px) {
        .main-title { font-size: 4rem !important; }
        .mega-btn, .music-btn { padding: 15px 30px !important; font-size: 1.3rem !important; }
        .gift-box { font-size: 6rem !important; }
        .puppy { font-size: 5rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# Session State
def init_session_state():
    defaults = {
        'page': 'home', 'hearts_count': 0, 'confetti_active': False, 'game_score': 0,
        'photo_likes': {}, 'visitors_count': 0, 'admin_logged': False, 'gift_opened': False,
        'wishes': [], 'music_playing': False, 'gift_clicked': False, 'music_clicked': {}
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# FIXED FUNCTIONS
def create_blooming_hearts():
    st.markdown("""
    <div class="hearts-container" id="hearts-container">
        <div class="blooming-heart" style="left: 10%; animation-delay: 0s;">💖</div>
        <div class="blooming-heart" style="left: 20%; animation-delay: 1s;">💕</div>
        <div class="blooming-heart" style="left: 30%; animation-delay: 2s;">💗</div>
        <div class="blooming-heart" style="left: 40%; animation-delay: 3s;">💝</div>
        <div class="blooming-heart" style="left: 50%; animation-delay: 4s;">💖</div>
    </div>
    <script>
    function spawnHeart() {
        const container = document.getElementById('hearts-container');
        const heart = document.createElement('div');
        heart.innerHTML = ['💖','💕','💗','💝','🌸','✨'][Math.floor(Math.random()*6)];
        heart.className = 'blooming-heart';
        heart.style.left = Math.random() * 95 + '%';
        heart.style.animationDuration = (Math.random() * 3 + 6) + 's';
        heart.style.animationDelay = Math.random() * 2 + 's';
        container.appendChild(heart);
        setTimeout(() => heart.remove(), 9000);
    }
    setInterval(spawnHeart, 1200);
    </script>
    """, unsafe_allow_html=True)

def launch_confetti_hearts():
    confetti_html = ""
    for i in range(120):
        left_pos = random.randint(0, 95)
        heart_type = random.choice(['💖','💕','💗','💝','🌸','✨'])
        confetti_html += f'<div style="position: fixed; left: {left_pos}%; top: -10%; font-size: 22px; pointer-events: none; z-index: 9999; animation: confettiFall 6s linear forwards {i*0.04}s;">{heart_type}</div>'
    st.markdown(f"""
    <style>
    @keyframes confettiFall {{ 0% {{ transform: translateY(-100vh) rotate(0deg); opacity: 1; }} 100% {{ transform: translateY(100vh) rotate(720deg); opacity: 0; }} }}
    </style>
    {confetti_html}
    """, unsafe_allow_html=True)

def birthday_countdown(target_date=None):
    if target_date is None: 
        target_date = date(2026, 3, 1)
    now = datetime.now()
    target_datetime = datetime.combine(target_date, datetime.min.time())
    if target_datetime < now: 
        target_datetime = datetime(now.year + 1, target_date.month, target_date.day)
    
    delta = target_datetime - now
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    seconds = delta.seconds % 60
    
    # Animated countdown timer using flip effect
    st.markdown("""
    <style>
    .flip-timer { display: flex; justify-content: center; gap: 18px; margin-bottom: 18px; }
    .flip-unit { background: var(--soft-pink); border-radius: 18px; padding: 18px 12px; box-shadow: 0 2px 12px var(--shadow-pink); text-align: center; min-width: 70px; }
    .flip-label { font-size: 1.1rem; color: var(--bubblegum); margin-bottom: 6px; }
    .flip-num { font-family: 'Poppins', sans-serif; font-size: 2.8rem; color: var(--heart-gold); font-weight: bold; display: inline-block; animation: flipIn 0.7s; }
    @keyframes flipIn { 0% { transform: rotateX(90deg); opacity: 0; } 100% { transform: rotateX(0deg); opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class='flip-timer'>
        <div class='flip-unit'><div class='flip-label'>💖 Days</div><div class='flip-num'>{days}</div></div>
        <div class='flip-unit'><div class='flip-label'>⏰ Hours</div><div class='flip-num'>{hours:02d}</div></div>
        <div class='flip-unit'><div class='flip-label'>⭐ Minutes</div><div class='flip-num'>{minutes:02d}</div></div>
        <div class='flip-unit'><div class='flip-label'>💕 Seconds</div><div class='flip-num'>{seconds:02d}</div></div>
    </div>
    """, unsafe_allow_html=True)

# FIXED PHOTOS - CLOUDFLARE/STREAMLIT DEPLOYMENT READY
def load_photos():
    # Always include these default local photos (if present)
    # Use public URLs for default photos so everyone can see them
    default_public_photos = [
        # swetha5.jpg from Dropbox
        "https://www.dropbox.com/scl/fi/lrafmg8j2s0edcwybrq73/swetha5.jpg?rlkey=16xl4ef45bmnm21xans8a924r&st=kq1ycxsx&raw=1",
        # swetha2.jpg from Dropbox (latest link)
        "https://www.dropbox.com/scl/fi/vt8i4q8cdcz3xexk9f9si/swetha2.jpg?rlkey=oru2f0do8wp1qqjnu7pvov2ry&st=7pk35ir3&raw=1",
        #
        "https://www.dropbox.com/scl/fi/lrafmg8j2s0edcwybrq73/swetha5.jpg?rlkey=16xl4ef45bmnm21xans8a924r&st=kq1ycxsx&raw=1",
        #  Add more links here as needed
        "https://www.dropbox.com/scl/fi/94avuwj1ddd5v2wn14b1n/me-and-divi.jpeg?rlkey=8bvptadhdy7vuvv12pawnwe3g&st=1x7igyxh&raw=1",
    ]
    photos = []
    # Add all images in the folder (if any)
    if os.path.exists("photos"):
        for file in os.listdir("photos"):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                path = f"photos/{file}"
                if path not in photos:
                    photos.append(path)
    # Always include public URLs for default photos
    for url in default_public_photos:
        if url not in photos:
            photos.append(url)
    # Fallback to online photos for deployment
    if not photos:
        photos = [
            "https://images.unsplash.com/photo-1516589178581-6cd7838eb79f?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop",
            
        ]
    return photos

# MUSIC FUNCTION WITH ARZ KIYA
def create_music_section():
    st.markdown('<h1 class="main-title">🎵 Birthday Music Corner 🎶</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎉 Happy Birthday Song!", key="birthday_song"):
            st.balloons()
            st.markdown('<div style="font-size: 2rem; color: var(--bubblegum); text-align: center;">🎵 Happy Birthday to you! 🎵<br>🎵 Happy Birthday dear Swetha! 🎵<br>🎵 Happy Birthday to you! 🎵</div>', unsafe_allow_html=True)
    
    with col2:
        music_key = "arz_kiya"
        # Ensure session state is initialized
        if "music_clicked" not in st.session_state:
            st.session_state.music_clicked = {}
        is_playing = st.session_state.music_clicked.get(music_key, False)

        # Button to toggle music
        if st.button("🎸 Blue Sky 💖", key="btn_arz_kiya", help="Click to play in background"):
            st.session_state.music_clicked[music_key] = not is_playing
            st.rerun()

        if is_playing:
            # Correct YouTube embed URL
            video_id = "IpFX2vq8HKw"
            embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&loop=1&playlist={video_id}"
            st.markdown(f"""
                <div class="music-player">
                    <div style='font-size: 1.2rem; color: #FFC0CB;'>🎵 Now Playing: Arz Kiya... 💖</div>
                    <iframe width="280" height="80" src="{embed_url}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                    <div style='font-size:0.9rem;color:#888;'>If audio doesn't start, click the play button in the player above.</div>
                </div>
            """, unsafe_allow_html=True)

    
    with col3:
        if st.button("💃 Party Dance Mix!", key="dance_mix"):
            st.snow()
            st.success("🎧 Party beats ON! 💃🕺")

# Sidebar
st.sidebar.markdown("""
<div style='padding: 20px; background: linear-gradient(45deg, var(--bubblegum), var(--primary-pink)); border-radius: 20px; margin: 10px 0; text-align: center;'>
    <h2 style='color: white; font-family: "Dancing Script", cursive; font-size: 1.8rem;'>💖 Swetha's Birthday Palace 💖</h2>
</div>
""", unsafe_allow_html=True)

pages = {
    "🏠 Home Sweet Home": "home", "💕 Love Messages": "messages", "📸 Memory Gallery": "gallery",
    "🎂 Birthday Games": "games",
    "🎵 Music Corner": "music", "📊 Stats & Facts": "stats", "💖 Our Timeline": "timeline",
    "🎈 Virtual Party": "party", "🌟 Admin Control": "admin", "💌 Secret Notes": "secrets"
}

selected_page = st.sidebar.radio("Select a page", list(pages.keys()), index=list(pages.values()).index(st.session_state.page))
st.session_state.page = pages[selected_page]

st.session_state.hearts_count += 1
st.sidebar.metric("💖 Hearts Bloomed", st.session_state.hearts_count)

st.markdown('<div style="padding: 20px;">', unsafe_allow_html=True)

# MAIN PAGES
if st.session_state.page == "home":
    create_blooming_hearts()
    st.markdown('<h1 class="main-title">Happy Birthday Swetha! 🎂💖✨</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle">To the most amazing friend ever! 🌟💕</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="pink-card">
            <h1 style='font-size: 4rem; color: var(--bubblegum); margin: 0;'>💕</h1>
            <h3 style='color: var(--primary-pink);'>Years of</h3>
            <h2 style='font-size: 2.5rem; color: var(--heart-gold);'>Pure Magic</h2>
        </div>
        """, unsafe_allow_html=True)
    
    birthday_countdown()
    
    col5, col6 = st.columns(2)
    with col5:
        if st.button("🚀 Launch Heart Storm!", key="heart_storm"):
            launch_confetti_hearts()
            st.success("💖 Heart storm activated!")
    with col6:
        if st.button("🎉 BIG CELEBRATION!", key="big_party"):
            st.balloons()
            st.snow()
            st.success("🎊 HAPPY BIRTHDAY SWETHA 🎊")

elif st.session_state.page == "messages":
    st.markdown('<h1 class="main-title">💌 Love Messages for Swetha 💕</h1>', unsafe_allow_html=True)
    messages = ["Swetha, you're my sunshine everyday! ☀️💖", "Best friend adventures forever! 🌟✨", "Your smile makes my whole day! 😍💕", "To endless laughter & happy moments! 🎈🎉", "You're the sparkle in my life! ✨🌟", "My heart smiles when I think of you! 💓💖", "My heart beats faster everytime i get closer to you🌸💕", "Here's to many more memories together! 📸❤️"]
    cols = st.columns(3)
    for i, msg in enumerate(messages):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="pink-card">
                <div style='font-size: 1.5rem; color: var(--bubblegum); padding: 20px;'>{msg}</div>
                <div style='text-align: right; color: var(--primary-pink);'>💕 From Your Bestie</div>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.page == "gallery":
    st.markdown('<h1 class="main-title">📸 Our Beautiful Memories 💕</h1>', unsafe_allow_html=True)
    photos = load_photos()
    cols_per_row = 4
    for i in range(0, len(photos), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, photo_path in enumerate(photos[i:i+cols_per_row]):
            with cols[j]:
                st.image(photo_path, width=280, caption=f"💖 Memory #{i+j+1}")

elif st.session_state.page == "games":
    st.markdown('<h1 class="main-title">🎮 Birthday Fun Zone! 🎉</h1>', unsafe_allow_html=True)
    if st.button("🎲 Spin Birthday Wheel!", key="wheel"):
        gifts = ["💝A journey Together ", "A day with me"]
        st.balloons()
        st.success(f"You won: **{random.choice(gifts)}** 🎊")



elif st.session_state.page == "music":
    create_music_section()

elif st.session_state.page == "stats":
    st.markdown('<h1 class="main-title">📊 Swetha Birthday Stats 📈</h1>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("💖 Total Hearts", st.session_state.hearts_count)
    with col2: st.metric("👥 Visitors", st.session_state.visitors_count)
    with col3: st.metric("🎮 Game Score", st.session_state.game_score)
    with col4: st.metric("💌 Wishes", len(st.session_state.wishes))
    
    st.markdown("""
    <div class="pink-card" style='text-align: center;'>
        <h3 style='color: var(--bubblegum);'>🎂 Swetha Fun Facts 🎂</h3>
        <p style='color: var(--primary-pink); font-size: 1.2rem;'>Egoistic! 🌟 |Rakshasiiii! 😍 | Short girl | But very caring !😍</p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "timeline":
    st.markdown('<h1 class="main-title">💖 Our Friendship Timeline ⏳</h1>', unsafe_allow_html=True)
    timeline = [
        {"year": "2023", "event": "First met & became besties! 💕"},
        {"year": "2024", "event": "Countless Talks! 🌟"},
        {"year": "2025", "event": "A year of fights! 📸"},
        {"year": "2026", "event": "Made Never Ending Memories 🎂✨"}
    ]
    for event in timeline:
        st.markdown(f"""
        <div class="pink-card">
            <h2 style='color: var(--heart-gold); text-align: center;'>{event['year']}</h2>
            <div style='font-size: 1.5rem; color: var(--bubblegum); text-align: center;'>{event['event']}</div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page == "party":
    st.markdown('<h1 class="main-title">🎈 Virtual Birthday Party! 🎉</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎊 Launch Party!", key="party_launch"):
            st.balloons()
            st.snow()
            launch_confetti_hearts()
            st.success("🎉 PARTY MODE FULL ON! 🎉")
    with col2:
        if st.button("🍰 Cut the Cake!", key="cake_cut"):
            st.success("🎂 Cake sliced! receive it on 3 march 🍰")
    with col3:
        if st.button("🎤 Sing Together!", key="sing_along"):
            st.markdown('<div style="font-size: 2rem; color: var(--bubblegum); text-align: center;">🎵 Happy Birthday dear Swetha... 🎵</div>', unsafe_allow_html=True)

elif st.session_state.page == "admin":
    st.markdown('<h1 class="main-title">🔐 Admin Control 🔧</h1>', unsafe_allow_html=True)
    admin_pass = st.text_input("🔑 Password", type="password")
    if admin_pass == "swethaforever123":
        st.session_state.admin_logged = True
        st.success("✅ Admin access granted! 🌟")
        st.subheader("📤 Upload Photos")
        uploaded_files = st.file_uploader("Choose photos", accept_multiple_files=True)
        if uploaded_files:
            os.makedirs("photos", exist_ok=True)
            for file in uploaded_files:
                with open(f"photos/{file.name}", "wb") as f:
                    f.write(file.getbuffer())
            st.success(f"✅ {len(uploaded_files)} photos added!")
            st.rerun()
        if st.button("🔄 Reset Stats", key="reset_stats"):
            st.session_state.hearts_count = 0
            st.session_state.visitors_count = 0
            st.session_state.game_score = 0
            st.session_state.wishes = []
            st.success("✅ Reset complete!")
            st.rerun()
    else:
        st.warning("🚫 Password: swethaforever12")

elif st.session_state.page == "secrets":
    st.markdown('<h1 class="main-title">💌 Secret Notes for Swetha 💕</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="pink-card">
        <h3 style='color: var(--bubblegum); text-align: center;'>🌟 Special Messages 🌟</h3>
        <div style='font-size: 1.5rem; color: var(--primary-pink); text-align: center;'>
            Having u in my life is the greatest gift i could ever ask for ✨<br>
            You mean everything to me! 💖<br>
            You're family, not just a friend! 💖<br>
            So lucky to have u by my side! 💖<br>
            World is better with you in it! ✨<br>
            Endless happiness wishes! 🎂💕
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
col_left, col_right = st.columns([3,1])
with col_left:
    st.markdown("""
    <div class="pink-card">
        <h3 style='color: var(--bubblegum); text-align: center;'>💖 Made with Love 💖</h3>
        <p style='text-align: center; color: var(--primary-pink);'>For Swetha on her special day! 🎂✨</p>
    </div>
    """, unsafe_allow_html=True)
with col_right:
    st.metric("🌟 Visits", st.session_state.visitors_count + 1)
    st.metric("💖 Score", st.session_state.game_score)

st.session_state.visitors_count += 1
st.markdown('</div>', unsafe_allow_html=True)
