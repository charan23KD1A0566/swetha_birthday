import streamlit as st
import time
import random
import math
import os
import io
from datetime import date, datetime, timedelta
from PIL import Image, ImageFilter, ImageEnhance
import requests
import numpy as np

# FIXED Page config - 0 errors
st.set_page_config(
    page_title="💖 Happy Birthday Swetha! 💖",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# COMPLETE CUSTOM CSS - ALL ERRORS FIXED
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;600;700&family=Satisfy&family=Poppins:wght@200;300;400;500;600;700&display=swap');
    
    :root {
        --primary-pink: #ffb3d9;
        --light-pink: #ffeef0;
        --soft-pink: #ffcccb;
        --rose-pink: #ffc1e3;
        --bubblegum: #ff69b4;
        --heart-gold: #ffd700;
        --white-glow: rgba(255,255,255,0.9);
        --shadow-pink: rgba(255,182,217,0.3);
    }
    
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
        pointer-events: none; z-index: 1; overflow: hidden;
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
    
    .gift-box {
        font-size: 8rem !important; cursor: pointer; transition: all 0.3s ease;
        display: block; margin: 50px auto; animation: giftBounce 2s infinite;
    }
    
    .gift-box:hover { transform: scale(1.1) rotate(5deg); filter: drop-shadow(0 0 30px var(--heart-gold)); }
    
    @keyframes giftBounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-20px); }
        60% { transform: translateY(-10px); }
    }
    
    .gift-open { animation: giftOpen 2s ease-out forwards; }
    @keyframes giftOpen { 0% { transform: scale(1) rotate(0deg); } 50% { transform: scale(1.3) rotate(10deg); } 100% { transform: scale(0) rotate(360deg); } }
    
    .puppy-surprise {
        font-size: 4rem !important; animation: puppyDance 3s ease-in-out infinite;
        text-align: center; margin: 50px 0;
    }
    
    @keyframes puppyDance { 0%, 100% { transform: rotate(-5deg); } 50% { transform: rotate(5deg); } }
    
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
        .mega-btn { padding: 15px 30px !important; font-size: 1.3rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# Session State
def init_session_state():
    defaults = {
        'page': 'home', 'hearts_count': 0, 'confetti_active': False, 'game_score': 0,
        'photo_likes': {}, 'visitors_count': 0, 'admin_logged': False, 'gift_opened': False,
        'wishes': [], 'music_playing': False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Core Functions (ALL FIXED)
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
    setInterval(spawnHeart, 800);
    </script>
    """, unsafe_allow_html=True)

def launch_confetti_hearts():
    confetti_html = ""
    for i in range(100):
        left_pos = random.randint(0, 95)
        heart_type = random.choice(['💖','💕','💗','💝','🌸','✨'])
        confetti_html += f'<div style="position: fixed; left: {left_pos}%; top: -10%; font-size: 25px; pointer-events: none; z-index: 9999; animation: confettiFall 5s linear forwards {i*0.05}s;">{heart_type}</div>'
    st.markdown(f"""
    <style>
    @keyframes confettiFall {{ 0% {{ transform: translateY(-100vh) rotate(0deg); opacity: 1; }} 100% {{ transform: translateY(100vh) rotate(720deg); opacity: 0; }} }}
    </style>
    {confetti_html}
    """, unsafe_allow_html=True)

def birthday_countdown(target_date=None):
    if target_date is None: target_date = date(2026, 3, 1)
    now = date.today()
    if target_date < now: target_date = date(now.year + 1, target_date.month, target_date.day)
    delta = target_date - now
    seconds = int((datetime.combine(target_date, datetime.min.time()) - datetime.combine(now, datetime.min.time())).total_seconds())
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("💖 Days", delta.days, delta.days - 1)
    with col2: st.metric("⏰ Hours", seconds//3600, -1)
    with col3: st.metric("⭐ Minutes", (seconds%3600)//60, 1)
    with col4: st.metric("💕 Seconds", seconds%60, -2)

def load_photos(folder="photos"):
    photos = []
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                photos.append(os.path.join(folder, file))
    if not photos:
        photos = ["https://picsum.photos/400/400?random=1", "https://picsum.photos/400/400?random=2", "https://picsum.photos/400/400?random=3", "https://picsum.photos/400/400?random=4"]
    return photos

# 12-PAGE NAVIGATION
st.sidebar.markdown("""
<div style='padding: 20px; background: linear-gradient(45deg, var(--bubblegum), var(--primary-pink)); border-radius: 20px; margin: 10px 0; text-align: center;'>
    <h2 style='color: white; font-family: "Dancing Script", cursive; font-size: 1.8rem;'>💖 Swetha's Birthday Palace 💖</h2>
</div>
""", unsafe_allow_html=True)

pages = {
    "🏠 Home Sweet Home": "home", "💕 Love Messages": "messages", "📸 Memory Gallery": "gallery",
    "🎂 Birthday Games": "games", "🎁 Surprise Gifts": "gifts",
    "🎵 Music Corner": "music", "📊 Stats & Facts": "stats", "💖 Our Timeline": "timeline",
    "🎈 Virtual Party": "party", "🌟 Admin Control": "admin", "💌 Secret Notes": "secrets"
}

selected_page = st.sidebar.radio("Select a page", list(pages.keys()), index=list(pages.values()).index(st.session_state.page))
st.session_state.page = pages[selected_page]

st.session_state.hearts_count += 1
st.sidebar.metric("💖 Hearts Bloomed", st.session_state.hearts_count)

st.markdown('<div style="padding: 20px;">', unsafe_allow_html=True)

# ALL 12 PAGES - FULLY WORKING
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
                if photo_path.startswith('http'):
                    st.image(photo_path, width=280, caption=f"💖 Memory #{i+j+1}")
                else:
                    st.image(photo_path, width=280, caption=f"💖 Memory #{i+j+1}")

elif st.session_state.page == "games":
    st.markdown('<h1 class="main-title">🎮 Birthday Fun Zone! 🎉</h1>', unsafe_allow_html=True)
    if st.button("🎲 Spin Birthday Wheel!", key="wheel"):
        gifts = ["💝A journey Together  ","A day with me"]
        st.balloons()
        st.success(f"You won: **{random.choice(gifts)}** 🎊")

elif st.session_state.page == "gifts":
    st.markdown('<h1 class="main-title">🎁 Surprise Gifts for Swetha! 🎀</h1>', unsafe_allow_html=True)
    if not st.session_state.get('gift_opened', False):
        st.markdown("""
        <div style='text-align: center;'>
            <div class="gift-box" onclick="this.classList.add('gift-open'); setTimeout(() => { this.innerHTML = '🐶<br><div style=\\"font-size: 2rem; color: var(--bubblegum); margin-top: 20px;\\">Happy Birthday Swetha!</div>'; this.className = 'puppy-surprise'; }, 2000);">🎁</div>
            <p style='font-size: 2rem; color: var(--bubblegum); margin-top: 20px;'>Click the gift box! 💖</p>
        </div>
        <script>window.giftOpened = true;</script>
        """, unsafe_allow_html=True)
        st.session_state.gift_opened = True
    else:
        st.markdown("""
        <div class="puppy-surprise">
            🐶<br><div style='font-family: "Dancing Script", cursive; font-size: 3rem; color: var(--bubblegum); margin-top: 20px;'>Happy Birthday Swetha! 🎂💖</div>
        </div>
        """, unsafe_allow_html=True)
        st.success("🐕 Puppy delivered your birthday message! 💕")
        


elif st.session_state.page == "music":
    st.markdown('<h1 class="main-title">🎵 Birthday Music Corner 🎶</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎉 Happy Birthday Song!", key="birthday_song"):
            st.balloons()
            st.markdown('<div style="font-size: 2rem; color: var(--bubblegum); text-align: center;">🎵 Happy Birthday to you! 🎵<br>🎵 Happy Birthday dear Swetha! 🎵<br>🎵 Happy Birthday to you! 🎵</div>', unsafe_allow_html=True)
    with col2:
        if st.button("💃 Party Dance Mix!", key="dance_mix"):
            st.snow()
            st.success("🎧 Party beats ON! 💃🕺")
    with col3:
        if st.button("🌟 Celebration Playlist!", key="playlist"):
            st.info("🎼 Full party playlist loaded! 🎊")

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
        <p style='color: var(--primary-pink); font-size: 1.2rem;'>Egoistic! 🌟 |Rakshasiiii! 😍 |  Short girl | But very caring !😍</p>
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
            st.success("🎂 Cake sliced! receive it on 3 march  🍰")
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
        st.warning("🚫 Password: swethaforever123")

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
