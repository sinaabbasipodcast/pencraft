import streamlit as st
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Pencraft Universe", layout="wide", page_icon="🚀")

# --- ADVANCED COSMIC UI (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@400;700&display=swap');

    /* Global Cosmic Background */
    .stApp {
        background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* Status Bar (Header) */
    .status-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.05);
        padding: 10px 30px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 30px;
        backdrop-filter: blur(10px);
    }
    .status-item { font-family: 'Orbitron', sans-serif; color: #00d4ff; font-weight: bold; }

    /* Lobby Hero Section */
    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to right, #00d4ff, #0055ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 5px;
    }

    /* Game Selection Cards (Lobby) */
    .lobby-card {
        background: rgba(255, 255, 255, 0.03);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        transition: all 0.4s ease;
        cursor: pointer;
        height: 100%;
    }
    .lobby-card:hover {
        transform: translateY(-10px);
        background: rgba(0, 212, 255, 0.1);
        border-color: #00d4ff;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
    }

    /* Metallic Game Question Card (Reflecting User Image) */
    .q-card {
        background: linear-gradient(135deg, #2c3e50, #000000);
        border: 4px solid #d4af37;
        border-radius: 25px;
        padding: 50px;
        text-align: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8), inset 0 0 20px rgba(212, 175, 55, 0.2);
        margin: 20px auto;
        max-width: 800px;
    }
    .q-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        color: #ffffff;
        margin-bottom: 20px;
        text-shadow: 0 0 15px rgba(255,255,255,0.5);
    }

    /* Metallic Choice Buttons */
    .stButton>button {
        background: linear-gradient(180deg, #ffd700 0%, #b8860b 100%);
        color: #000 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 1.1rem;
        border-radius: 15px;
        border: 2px solid #555;
        height: 100px;
        box-shadow: 0 8px 0 #666, 0 15px 20px rgba(0,0,0,0.5);
        transition: all 0.1s;
        white-space: normal;
    }
    .stButton>button:active {
        box-shadow: 0 2px 0 #666;
        transform: translateY(6px);
    }
    .stButton>button:hover {
        filter: brightness(1.2);
        border-color: #fff;
    }

    /* Analysis Box */
    .analysis-panel {
        background: rgba(0, 0, 0, 0.6);
        border-right: 5px solid #00d4ff;
        padding: 20px;
        border-radius: 10px;
        direction: rtl;
        font-size: 1.1rem;
        line-height: 1.8;
    }

</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "lobby"
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'score' not in st.session_state: st.session_state.score = 0
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'feedback' not in st.session_state: st.session_state.feedback = None

def go_to_game(game_name):
    st.session_state.page = game_name
    st.session_state.q_idx = 0
    st.session_state.feedback = None

def back_to_lobby():
    st.session_state.page = "lobby"

# --- MOCK DATA ---
keywords_data = [
    {"q": "mobile home", "opts": ["a large caravan which stays in one place", "a river boat you live in", "a set of rooms in a building"], "ans": "a large caravan which stays in one place", "exp": "معمولاً به کاروان‌های بزرگی گفته می‌شود که در یک جا ثابت می‌مانند و به عنوان خانه استفاده می‌شوند."},
    {"q": "academic success", "opts": ["doing well in school/uni", "buying a new car", "winning a marathon"], "ans": "doing well in school/uni", "exp": "موفقیت تحصیلی مستقیماً به عملکرد در محیط‌های آموزشی اشاره دارد."}
]

# --- UI COMPONENTS ---

def render_status_bar():
    st.markdown(f"""
    <div class="status-bar">
        <div class="status-item">⏱️ TIME: 09:57</div>
        <div class="status-item" style="font-size:1.5rem; color:#fff;">PENCRAFT UNIVERSE</div>
        <div class="status-item">🏆 SCORE: {st.session_state.score} | ✨ XP: {st.session_state.xp}</div>
    </div>
    """, unsafe_allow_html=True)

# --- PAGE: LOBBY ---
if st.session_state.page == "lobby":
    st.markdown("<div class='hero-title'>PENCRAFT</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.2rem; color:#aaa; margin-bottom:50px;'>SELECT YOUR MISSION TO MASTER WRITING</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='lobby-card'><h3>🔍 Paraphrase Pro</h3><p>Master the art of rewording</p></div>", unsafe_allow_html=True)
        if st.button("START MISSION", key="g1"): go_to_game("paraphrase")
        
    with col2:
        st.markdown("<div class='lobby-card'><h3>💎 Key Words</h3><p>Perfect your collocations</p></div>", unsafe_allow_html=True)
        if st.button("START MISSION", key="g2"): go_to_game("keywords")
        
    with col3:
        st.markdown("<div class='lobby-card'><h3>🎩 Formal Upgrade</h3><p>Level up your register</p></div>", unsafe_allow_html=True)
        if st.button("START MISSION", key="g3"): go_to_game("formal")

# --- PAGE: KEY WORDS GAME (The one you highlighted) ---
elif st.session_state.page == "keywords":
    render_status_bar()
    
    data = keywords_data[st.session_state.q_idx % len(keywords_data)]
    
    st.markdown(f"""
    <div class="q-card">
        <div style="color:#00d4ff; font-weight:bold; margin-bottom:10px;">MISSION: VOCABULARY PRECISION</div>
        <div class="q-text">{data['q']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, opt in enumerate(data['opts']):
        if cols[i].button(opt, key=f"btn_{i}"):
            if opt == data['ans']:
                st.session_state.feedback = "correct"
                st.session_state.score += 10
                st.session_state.xp += 5
            else:
                st.session_state.feedback = "wrong"
    
    if st.session_state.feedback:
        if st.session_state.feedback == "correct":
            st.success("🎯 EXCELLENT! +10 Score")
        else:
            st.error(f"❌ INCORRECT. The answer was: {data['ans']}")
            
        st.markdown(f"<div class='analysis-panel'><b>تحلیل تخصصی:</b><br>{data['exp']}</div>", unsafe_allow_html=True)
        
        if st.button("NEXT QUESTION ➡️"):
            st.session_state.q_idx += 1
            st.session_state.feedback = None
            st.rerun()

    if st.button("⬅️ ABORT MISSION (Back to Lobby)"):
        back_to_lobby()
        st.rerun()

# --- OTHER PAGES (Placeholders with same Style) ---
else:
    render_status_bar()
    st.warning(f"The {st.session_state.page} mission is being calibrated...")
    if st.button("Back to Lobby"):
        back_to_lobby()
        st.rerun()
