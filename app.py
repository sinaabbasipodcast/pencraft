import streamlit as st
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Pencraft: Writing Mastery", layout="wide", page_icon="✍️")

# --- CUSTOM CSS FOR MODERN & BOLD UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #f8f9fa;
    }

    /* Card Style */
    .game-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid #eee;
        margin-bottom: 2rem;
    }

    /* Highlight Key Words */
    .highlight {
        color: #d4af37;
        font-weight: 900;
        text-decoration: underline;
    }
    
    .informal-highlight {
        background-color: #ffe5e5;
        color: #d90429;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }

    /* Buttons Customization */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #1e1e1e;
        color: white;
        font-weight: bold;
        transition: all 0.3s;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: #d4af37;
        color: black;
        transform: translateY(-2px);
    }

    /* Badges */
    .skill-badge {
        background-color: #e9ecef;
        color: #495057;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-bottom: 1rem;
        display: inline-block;
    }

    /* Feedback Boxes */
    .feedback-correct {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    
    .feedback-wrong {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    
    .analysis-box {
        background-color: #fff9db;
        border-left: 5px solid #fab005;
        padding: 1rem;
        margin-top: 1rem;
        font-size: 0.95rem;
        color: #444;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# --- DATABASES ---

# 1. Paraphrase Database
paraphrase_db = [
    {
        "original": "The government needs to spend more money on schools to help students learn better.",
        "options": [
            "Allocating more resources to education is essential for improving student outcomes.",
            "Increased investment in the educational sector is vital to enhance the learning process.",
            "Expanding the education budget is necessary to foster better academic achievement."
        ],
        "analysis": "در اینجا عبارت 'spend more money' به 'allocating resources' یا 'investment' تغییر یافته که رسمی‌تر است. همچنین 'help students learn better' به 'enhance the learning process' یا 'foster academic achievement' تبدیل شده که عمق تحلیل آکادمیک متن شما را بالا می‌برد."
    },
    {
        "original": "People are using cars too much, and this is bad for the air in our cities.",
        "options": [
            "The excessive reliance on private vehicles significantly contributes to urban air pollution.",
            "Over-dependence on automobiles is detrimental to the air quality in metropolitan areas.",
            "The heavy use of personal transport has a negative impact on the atmospheric conditions of cities."
        ],
        "analysis": "کلمه 'bad' یک کلمه ضعیف است که در اینجا با 'detrimental' یا 'negative impact' جایگزین شده. همچنین 'using cars too much' به عبارتی دقیق‌تر مثل 'excessive reliance' تبدیل شده است."
    }
]

# 2. Key Words (Collocation) Database (As provided by user)
keywords_db = [
    {"keyword": "Education", "context": "Academic Achievement", "sentence": "A high standard of education is _______ for a country's economic success.", "options": ["vital", "big", "fast", "heavy"], "answer": "vital", "explanation": "In academic writing, 'vital' or 'essential' are strong collocations for education's importance.", "tag": "Collocation"},
    {"keyword": "Policy", "context": "Government Actions", "sentence": "The government decided to _______ a new policy to tackle unemployment.", "options": ["make", "introduce", "do", "give"], "answer": "introduce", "explanation": "We 'introduce' or 'implement' a policy, we don't just 'make' it.", "tag": "Register"},
    {"keyword": "Research", "context": "Evidence", "sentence": "Recent research _______ that social media can affect mental health.", "options": ["tells", "suggests", "speaks", "shows up"], "answer": "suggests", "explanation": "'Research suggests' is a classic academic collocation.", "tag": "Precision"}
]

# 3. Formal Upgrade Database
formal_upgrade_db = [
    {"sentence": "Many young people are <span class='informal-highlight'>crazy about</span> social media.", "highlight": "crazy about", "options": ["mad for", "highly interested in", "obsessed on", "into very much"], "answer": "highly interested in", "explanation": "Highly interested in is more formal and suitable for academic writing.", "tag": "Register"},
    {"sentence": "The government needs to <span class='informal-highlight'>deal with</span> this issue quickly.", "highlight": "deal with", "options": ["handle", "do with", "work against", "react on"], "answer": "handle", "explanation": "Handle is more formal and concise than the phrasal verb 'deal with'.", "tag": "Academic Tone"},
    {"sentence": "Fast food is <span class='informal-highlight'>bad for</span> people's health.", "highlight": "bad for", "options": ["not nice to", "harmful to", "rough on", "weak for"], "answer": "harmful to", "explanation": "Harmful to is a precise academic term for negative effects.", "tag": "Precision"}
]

# 4. Error Hunt Database
error_hunt_db = [
    {"original": "The government should do stricter laws to reduce air pollution.", "options": ["The government should do stricter laws", "The government should make stricter laws", "The government should introduce stricter laws", "The government should create up stricter laws"], "answer": "The government should introduce stricter laws", "explanation": "In formal writing, 'introduce' or 'enact' laws is the correct collocation.", "tag": "Collocation"},
    {"original": "Education is a essential part of modern society.", "options": ["Education is a essential part", "Education is an essential part", "Education is essential part", "Education is the essential part"], "answer": "Education is an essential part", "explanation": "The word 'essential' starts with a vowel sound, so it requires the article 'an'.", "tag": "Grammar"}
]

# 5. Micro Expand Database
micro_expand_db = [
    {"base": "Public transport should be improved.", "task": "Add a clear reason.", "options": ["This is a topic many people talk about.", "This is necessary because it can reduce traffic congestion and air pollution.", "Public transport is a thing in cities.", "There are buses and trains in many countries."], "answer": "This is necessary because it can reduce traffic congestion and air pollution.", "explanation": "This option provides a logical and academically relevant reason.", "tag": "Logic & Cohesion"},
    {"base": "Online learning can be effective.", "task": "Add a specific example.", "options": ["For example, many university students can attend recorded lectures at flexible times.", "For example, learning is important for students.", "For example, education exists in many forms.", "For example, some people study and some do not."], "answer": "For example, many university students can attend recorded lectures at flexible times.", "explanation": "A good example must be specific and directly support the main idea.", "tag": "Development"}
]

# --- SESSION STATE MANAGEMENT ---
if 'game_index' not in st.session_state:
    st.session_state.game_index = 0
if 'feedback' not in st.session_state:
    st.session_state.feedback = None
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False

def next_question():
    st.session_state.game_index += 1
    st.session_state.feedback = None
    st.session_state.show_analysis = False

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🖋️ Pencraft Mastery")
    game_choice = st.radio("Select a Game:", 
                           ["Paraphrase Pro", "Key Words for Fluency", "Formal Upgrade", "Error Hunt", "Micro Expand"])
    st.info("Level: Upper-Intermediate / IELTS")
    if st.button("Reset Game"):
        st.session_state.game_index = 0
        st.rerun()

# --- MAIN GAME LOGIC ---

st.markdown(f"<h1>{game_choice}</h1>", unsafe_allow_html=True)

# 1. PARAPHRASE PRO
if game_choice == "Paraphrase Pro":
    db = paraphrase_db
    idx = st.session_state.game_index % len(db)
    item = db[idx]
    
    st.markdown(f"""<div class='game-card'>
        <div class='skill-badge'>Skill: Academic Reformulation</div>
        <h3>Original Sentence:</h3>
        <p style='font-size:1.2rem; color:#555;'>"{item['original']}"</p>
    </div>""", unsafe_allow_html=True)
    
    st.subheader("High-Level Paraphrase Options:")
    for opt in item['options']:
        # Highlight logic (simplified for display)
        highlighted_opt = opt.replace("Allocating", "<span class='highlight'>Allocating</span>")\
                             .replace("investment", "<span class='highlight'>investment</span>")\
                             .replace("enhance", "<span class='highlight'>enhance</span>")\
                             .replace("pollutant", "<span class='highlight'>pollutant</span>")
        st.markdown(f"- {highlighted_opt}", unsafe_allow_html=True)
    
    if st.button("Show Deep Analysis (Persian)"):
        st.session_state.show_analysis = True
    
    if st.session_state.show_analysis:
        st.markdown(f"<div class='analysis-box'><b>تحلیل تخصصی:</b><br>{item['analysis']}</div>", unsafe_allow_html=True)
        if st.button("Next Sentence"):
            next_question()
            st.rerun()

# 2. KEY WORDS FOR FLUENCY
elif game_choice == "Key Words for Fluency":
    db = keywords_db
    idx = st.session_state.game_index % len(db)
    item = db[idx]
    
    st.markdown(f"""<div class='game-card'>
        <div class='skill-badge'>Skill: {item['tag']}</div>
        <h3>Keyword: <span style='color:#d4af37;'>{item['keyword']}</span></h3>
        <p style='font-size:1.2rem;'>{item['sentence']}</p>
    </div>""", unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, opt in enumerate(item['options']):
        if cols[i%2].button(opt, key=f"opt_{i}"):
            if opt == item['answer']:
                st.session_state.feedback = ("correct", item['explanation'])
            else:
                st.session_state.feedback = ("wrong", item['explanation'])
    
    if st.session_state.feedback:
        status, msg = st.session_state.feedback
        if status == "correct":
            st.markdown(f"<div class='feedback-correct'>✅ <b>Correct!</b> {msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='feedback-wrong'>❌ <b>Try Again.</b> The correct answer was <b>{item['answer']}</b>. <br>{msg}</div>", unsafe_allow_html=True)
        
        if st.button("Next Challenge"):
            next_question()
            st.rerun()

# 3. FORMAL UPGRADE
elif game_choice == "Formal Upgrade":
    db = formal_upgrade_db
    idx = st.session_state.game_index % len(db)
    item = db[idx]
    
    st.markdown(f"""<div class='game-card'>
        <div class='skill-badge'>Skill: {item['tag']}</div>
        <h3>Upgrade the Highlighted Part:</h3>
        <p style='font-size:1.3rem;'>{item['sentence']}</p>
    </div>""", unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, opt in enumerate(item['options']):
        if cols[i%2].button(opt, key=f"formal_{i}"):
            if opt == item['answer']:
                st.session_state.feedback = ("correct", item['explanation'])
            else:
                st.session_state.feedback = ("wrong", item['explanation'])
                
    if st.session_state.feedback:
        status, msg = st.session_state.feedback
        if status == "correct":
            st.markdown(f"<div class='feedback-correct'>🔥 <b>Great Upgrade!</b> {msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='feedback-wrong'>💡 <b>Better Choice:</b> {item['answer']}. <br>{msg}</div>", unsafe_allow_html=True)
        
        if st.button("Next Upgrade"):
            next_question()
            st.rerun()

# 4. ERROR HUNT
elif game_choice == "Error Hunt":
    db = error_hunt_db
    idx = st.session_state.game_index % len(db)
    item = db[idx]
    
    st.markdown(f"""<div class='game-card'>
        <div class='skill-badge'>Skill: {item['tag']}</div>
        <h3>Find the Best Correction:</h3>
        <p style='font-size:1.2rem; color:#d90429;'>Original: "{item['original']}"</p>
    </div>""", unsafe_allow_html=True)
    
    for i, opt in enumerate(item['options']):
        if st.button(opt, key=f"error_{i}"):
            if opt == item['answer']:
                st.session_state.feedback = ("correct", item['explanation'])
            else:
                st.session_state.feedback = ("wrong", item['explanation'])
                
    if st.session_state.feedback:
        status, msg = st.session_state.feedback
        if status == "correct":
            st.markdown(f"<div class='feedback-correct'>🎯 <b>Target Spotted!</b> {msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='feedback-wrong'>❌ <b>Missed it.</b> The correct version is: <b>{item['answer']}</b>. <br>{msg}</div>", unsafe_allow_html=True)
        
        if st.button("Next Hunt"):
            next_question()
            st.rerun()

# 5. MICRO EXPAND
elif game_choice == "Micro Expand":
    db = micro_expand_db
    idx = st.session_state.game_index % len(db)
    item = db[idx]
    
    st.markdown(f"""<div class='game-card'>
        <div class='skill-badge'>Skill: {item['tag']}</div>
        <h3>Base Idea: <br><b>{item['base']}</b></h3>
        <p style='color:#666;'>Task: {item['task']}</p>
    </div>""", unsafe_allow_html=True)
    
    for i, opt in enumerate(item['options']):
        if st.button(opt, key=f"expand_{i}"):
            if opt == item['answer']:
                st.session_state.feedback = ("correct", item['explanation'])
            else:
                st.session_state.feedback = ("wrong", item['explanation'])
                
    if st.session_state.feedback:
        status, msg = st.session_state.feedback
        if status == "correct":
            st.markdown(f"<div class='feedback-correct'>🚀 <b>Excellent Expansion!</b> {msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='feedback-wrong'>🧐 <b>Not quite.</b> A better development would be: <i>{item['answer']}</i>. <br>{msg}</div>", unsafe_allow_html=True)
        
        if st.button("Next Expansion"):
            next_question()
            st.rerun()

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #999;'>Pencraft v1.5 | Powered by GPT-5.5 Logic</p>", unsafe_allow_html=True)
