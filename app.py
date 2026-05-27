import streamlit as st

# --- CONFIGURATION ---
st.set_page_config(page_title="Pencraft Master", layout="wide", page_icon="🚀")

# --- CUSTOM COSMIC CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@400;600&display=swap');

    .stApp {
        background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    .status-bar {
        display: flex;
        justify-content: space-between;
        padding: 12px 25px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(0, 212, 255, 0.3);
        margin-bottom: 25px;
        backdrop-filter: blur(5px);
    }
    .stat-text { font-family: 'Orbitron', sans-serif; color: #00d4ff; font-weight: bold; }

    .q-card {
        background: linear-gradient(145deg, #1e2a38, #000000);
        border: 3px solid #d4af37;
        border-radius: 20px;
        padding: 35px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.8);
        margin-bottom: 30px;
    }
    .q-mission { color: #00d4ff; font-family: 'Orbitron', sans-serif; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 10px;}
    .q-context { color: #aaa; font-style: italic; font-size: 0.9rem; margin-bottom: 15px; }
    .q-main-text { font-family: 'Orbitron', sans-serif; font-size: 2rem; color: #fff; line-height: 1.4; }

    /* Button Grid Consistency */
    .stButton>button {
        width: 100% !important;
        background: linear-gradient(180deg, #ffd700 0%, #b8860b 100%) !important;
        color: #000 !important;
        font-weight: 800 !important;
        font-family: 'Inter', sans-serif !important;
        border-radius: 12px !important;
        border: 2px solid #555 !important;
        height: 75px !important;
        box-shadow: 0 6px 0 #555, 0 10px 15px rgba(0,0,0,0.4) !important;
        transition: all 0.1s !important;
        font-size: 0.95rem !important;
        white-space: normal !important;
    }
    .stButton>button:active { transform: translateY(4px) !important; box-shadow: 0 2px 0 #555 !important; }
    .stButton>button:hover { filter: brightness(1.15); border-color: #fff !important; }

    .analysis-panel {
        background: rgba(0, 212, 255, 0.1);
        border-right: 5px solid #00d4ff;
        padding: 20px;
        margin-top: 20px;
        direction: rtl;
        border-radius: 10px;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- REAL DATABASE ---
KEYWORDS_BANK = [
    {"q": "I understand the background, but could you please just __________?", "ctx": "Someone is talking too much about minor details.", "opts": ["get to the point", "arrive to the point", "hit the point", "reach on the point"], "ans": "get to the point", "exp": "عبارت get to the point یک اصطلاح رایج برای 'رفتن سر اصل مطلب' است."},
    {"q": "You’ve been quiet all night. Is something __________?", "ctx": "Your friend looks distracted and worried.", "opts": ["in your mind", "at your mind", "on your mind", "over your mind"], "ans": "on your mind", "exp": "وقتی چیزی فکر کسی را مشغول کرده باشد از حرف اضافه on استفاده می‌کنیم: on your mind."},
    {"q": "We can’t keep debating forever. We need to __________ by noon.", "ctx": "The team finally needs to choose one plan.", "opts": ["do a decision", "make a decision", "build a decision", "create a decision"], "ans": "make a decision", "exp": "کالوکیشن صحیح برای تصمیم گرفتن، فعل make است."},
    {"q": "You’ve worked hard and made impressive __________ in your writing.", "ctx": "Reviewing a student's improvement.", "opts": ["progress", "progresses", "a progress", "the progresses"], "ans": "progress", "exp": "کلمه Progress غیرقابل شمارش (Uncountable) است و نباید 's' یا 'a' بگیرد."},
    {"q": "Don’t worry—everyone __________ from time to time.", "ctx": "Speaking to an employee who made an error.", "opts": ["does mistakes", "creates mistakes", "makes mistakes", "takes mistakes"], "ans": "makes mistakes", "exp": "برای اشتباه کردن همیشه از فعل make استفاده می‌شود."},
    {"q": "Please __________ and listen carefully.", "ctx": "Teacher trying to calm a noisy classroom.", "opts": ["give attention", "make attention", "pay attention", "put attention"], "ans": "pay attention", "exp": "اصطلاح استاندارد برای توجه کردن pay attention است."},
] # ... (بقیه ۳۰ سوال را به همین ترتیب در لیست قرار دهید)

PARAPHRASE_BANK = [
    {"q": "I decided to leave early because I wasn’t feeling well.", "opts": ["Due to my illness, I chose to depart ahead of schedule.", "I left soon because I am sick.", "Early leaving was my choice for bad feeling.", "I feel bad so I go early."], "ans": "Due to my illness, I chose to depart ahead of schedule.", "exp": "استفاده از Due to و depart ahead of schedule سطح پارافریز را به آکادمیک نزدیک می‌کند."},
    {"q": "We need to finish this project before the end of the week.", "opts": ["The project must be completed by the weekend.", "We should end this stuff soon.", "End this project before Friday is needed.", "Project finishing is required now."], "ans": "The project mus be completed by the weekend.", "exp": "تغییر ساختار به مجهول (Passive) یکی از تکنیک‌های اصلی پارافریز در آیلتس است."},
]

# --- STATE MANAGEMENT ---
if 'page' not in st.session_state: st.session_state.page = "lobby"
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'score' not in st.session_state: st.session_state.score = 0
if 'feedback' not in st.session_state: st.session_state.feedback = None

def navigate(to):
    st.session_state.page = to
    st.session_state.q_idx = 0
    st.session_state.feedback = None

# --- UI LOGIC ---
if st.session_state.page ==
