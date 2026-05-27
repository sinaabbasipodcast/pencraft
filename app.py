import streamlit as st
import random
import time

# --- CONFIG ---
st.set_page_config(page_title="PenCraft Pro: The Writing RPG", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS (The Neon-Cyber-Dark Look) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Vazirmatn:wght@300;700&display=swap');
    
    :root {
        --bg-color: #0E1117;
        --accent-gold: #FFD700;
        --accent-crimson: #DC143C;
        --neon-blue: #00F3FF;
    }

    .stApp {
        background-color: var(--bg-color);
        color: white;
        font-family: 'Vazirmatn', sans-serif;
    }

    /* XP Progress Bar */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #FFD700, #DC143C);
    }

    /* Neon Boxes */
    .game-card {
        background: rgba(255, 215, 0, 0.05);
        border: 2px solid var(--accent-gold);
        border-radius: 15px;
        padding: 20px;
        transition: 0.3s;
        text-align: center;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.2);
    }
    
    .game-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
        background: rgba(255, 215, 0, 0.1);
    }

    /* Blackboard Style for Paraphrase */
    .blackboard {
        background: #1a1a1a;
        border: 10px solid #5d4037;
        border-radius: 5px;
        padding: 20px;
        font-family: 'Vazirmatn', cursive;
        color: #eee;
        box-shadow: inset 0 0 20px black;
        margin-bottom: 20px;
    }

    h1, h2, h3, .level-text {
        font-family: 'Orbitron', sans-serif;
        color: var(--accent-gold);
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #DC143C, #FFD700);
        color: black !important;
        font-weight: bold !important;
        border: none;
        border-radius: 10px;
        height: 3em;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'streak' not in st.session_state:
    st.session_state.streak = 0

def add_xp(amount):
    st.session_state.xp += amount
    xp_needed = st.session_state.level * 100
    if st.session_state.xp >= xp_needed:
        st.session_state.xp -= xp_needed
        st.session_state.level += 1
        st.balloons()
        st.toast(f"LEVEL UP! حالا شدی لول {st.session_state.level} 🔥")

# --- LOGIN / GATEWAY ---
if not st.session_state.user_name:
    st.markdown("<h1 style='text-align: center;'>PENCRAFT PRO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>وارد دنیای رایتینگ شو، رفیق!</p>", unsafe_allow_html=True)
    name = st.text_input("اسم خفن خودت رو اینجا بنویس:", placeholder="مثلاً: Sina the Writer")
    if st.button("شروع ماجراجویی 🚀"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.stop()

# --- LOBBY (THE NEXUS) ---
st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <h2 style='margin: 0;'>PENCRAFT ACADEMY</h2>
        <div style='text-align: right;'>
            <span class='level-text'>LVL: {st.session_state.level}</span><br>
            <span style='color: #FFD700;'>🔥 Streak: {st.session_state.streak}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# XP Bar
xp_target = st.session_state.level * 100
st.progress(st.session_state.xp / xp_target)
st.caption(f"XP: {st.session_state.xp} / {xp_target} تا لول بعدی")

# NAVIGATION TABS
tabs = st.tabs(["🏠 لابی (Lobby)", "✍️ Paraphrase", "🎯 Key Words", "🧩 For/Against", "🌀 Maze", "🔫 Sniper"])

# --- GAME 1: PARAPHRASE (Blackboard Style) ---
with tabs[1]:
    st.markdown("<div class='blackboard'><h3>📝 مأموریت: بازنویسی خلاقانه</h3><p>این جمله رو طوری تغییر بده که معنیش عوض نشه ولی کلماتش خفن‌تر بشه.</p></div>", unsafe_allow_html=True)
    
    current_q = "The weather is very bad today, so we can't go to the park." # این می‌تواند از لیست تصادفی بیاید
    st.info(f"جمله ساده: {current_q}")
    
    user_p = st.text_area("توی دفترت بنویس:", placeholder="پاسخ تو...")
    
    if st.button("بررسی توسط استاد هوش مصنوعی"):
        if user_p:
            with st.spinner("در حال آنالیز جمله‌ات..."):
                time.sleep(1.5)
                # در اینجا منطق مقایسه هوشمند قرار می‌گیرد
                st.success("ایول! پارافریزت بد نبود، ولی بیا ببین چطور می‌تونستیم بهترش کنیم:")
                st.markdown("""
                ⚠️ **سه راه خفن‌تر:**
                1. *Due to the inclement weather, our park visit has been cancelled.* (آکادمیک)
                2. *The weather is absolutely dreadful today; hence, the park is out of the question.* (نیتیو)
                3. *Since it's pouring outside, we’d better ditch the park plan.* (کولوکیال)
                """)
                add_xp(25)
                st.session_state.streak += 1

# --- GAME 2: KEY WORDS (The Grid) ---
with tabs[2]:
    st.subheader("🎯 انتخاب بهترین ترکیب (Collocation)")
    st.markdown("**Context:** You are in a meeting. Someone is talking too much without getting to the main point.")
    st.markdown("---")
    st.markdown("### \"I wish you would just __________.\"")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("1. Get to the point"):
            st.success("✅ بوم! دقیقاً زدی تو هدف. نیتیوها همیشه از Get استفاده می‌کنن.")
            add_xp(15)
        if st.button("2. Reach the point"):
            st.error("❌ نه رفیق! این ترجمه تحت‌اللفظیه. دوباره تلاش کن.")
    with col2:
        if st.button("3. Hit the point"):
            st.error("❌ مگه بوکسه؟ نه اشتباهاست!")
        if st.button("4. Arrive at the point"):
            st.warning("⚠️ از نظر گرامری غلط نیست ولی کسی اینطوری نمیگه.")

# --- GAME 5: CONNECTOR MAZE ---
with tabs[4]:
    st.subheader("🌀 هزارتوی کانکتورها")
    st.write("جملات زیر رو با ربط‌دهنده مناسب به هم وصل کن تا از پیچ‌وتخم رایتینگ رد بشی!")
    sentence_a = "Studying abroad is expensive."
    sentence_b = "it provides a global perspective."
    
    option = st.selectbox("کدوم کلمه این دوتا رو درست وصل می‌کنه؟", ["Select...", "Moreover", "On the other hand", "Therefore"])
    if option == "On the other hand":
        st.success("آفرین! چون داری تضاد (Contrast) رو نشون میدی.")
        add_xp(20)

# --- GAME 6: WORD SNIPER ---
with tabs[5]:
    st.subheader("🔫 واژه‌کش (Word Sniper)")
    st.warning("این جمله پر از کلمات تکراری و ساده‌ست (Very). تک‌تیرانداز باش و با کلمات قوی اونا رو حذف کن!")
    st.code("The movie was VERY GOOD and the acting was VERY BAD.")
    
    target1 = st.text_input("جایگزین VERY GOOD (مثلاً: Magnificent):")
    target2 = st.text_input("جایگزین VERY BAD (مثلاً: Atrocious):")
    
    if st.button("شلیک! 🎯"):
        if target1.lower() in ["magnificent", "superb", "excellent"] and target2.lower() in ["atrocious", "awful", "horrendous"]:
            st.success("هدشات! رایتینگت از این رو به اون رو شد.")
            add_xp(30)
        else:
            st.info("تیرت به خطا رفت! کلمات قوی‌تری انتخاب کن.")

# بقیه بازی‌ها (For/Against) هم با ساختار مشابه اضافه می‌شوند...
