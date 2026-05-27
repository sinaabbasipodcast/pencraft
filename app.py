import streamlit as st
import re
from difflib import SequenceMatcher
from collections import Counter

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Pencraft",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 20% 20%, rgba(0, 196, 255, 0.10), transparent 25%),
        radial-gradient(circle at 80% 30%, rgba(255, 215, 0, 0.08), transparent 20%),
        radial-gradient(circle at 50% 80%, rgba(119, 0, 255, 0.08), transparent 25%),
        linear-gradient(180deg, #071018 0%, #05080d 100%);
    color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

::selection {
    background: rgba(0, 220, 255, 0.35);
    color: white;
}

.pencraft-title {
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: clamp(2.2rem, 5vw, 4.5rem);
    letter-spacing: 0.35em;
    color: #33d8ff;
    text-shadow: 0 0 10px rgba(51, 216, 255, 0.35), 0 0 30px rgba(51, 216, 255, 0.18);
    margin-top: 0.4rem;
    margin-bottom: 0.1rem;
}

.pencraft-subtitle {
    text-align: center;
    font-size: 0.95rem;
    color: rgba(230, 240, 255, 0.55);
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-bottom: 1.8rem;
}

.neon-card {
    background: linear-gradient(180deg, rgba(14, 19, 29, 0.92), rgba(8, 12, 18, 0.96));
    border: 1px solid rgba(72, 225, 255, 0.22);
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.03) inset,
        0 18px 50px rgba(0,0,0,0.45),
        0 0 35px rgba(0, 200, 255, 0.08);
    border-radius: 22px;
    padding: 1.15rem 1.2rem;
    backdrop-filter: blur(8px);
}

.hero-card {
    background:
        radial-gradient(circle at top left, rgba(58, 220, 255, 0.12), transparent 35%),
        radial-gradient(circle at bottom right, rgba(255, 215, 0, 0.08), transparent 30%),
        linear-gradient(180deg, rgba(12,18,29,0.96), rgba(7,10,16,0.98));
    border: 1px solid rgba(255, 215, 0, 0.20);
    box-shadow:
        0 25px 70px rgba(0,0,0,0.55),
        inset 0 1px 0 rgba(255,255,255,0.06);
    border-radius: 28px;
    padding: 1.4rem;
}

.mission-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    background: linear-gradient(180deg, rgba(14, 20, 31, 0.92), rgba(10, 14, 22, 0.92));
    border: 1px solid rgba(51, 216, 255, 0.22);
    border-radius: 18px;
    padding: 0.95rem 1.1rem;
    box-shadow: 0 14px 40px rgba(0,0,0,0.35);
    margin-bottom: 1.1rem;
}

.mission-label {
    font-family: 'Orbitron', sans-serif;
    color: #33d8ff;
    font-size: 1.0rem;
    letter-spacing: 0.12em;
}

.score-label {
    font-family: 'Orbitron', sans-serif;
    color: #ffd54a;
    font-size: 1.0rem;
    letter-spacing: 0.12em;
}

.prompt-title {
    text-align: center;
    color: rgba(255,255,255,0.55);
    font-style: italic;
    margin-bottom: 0.7rem;
    font-size: 0.95rem;
}

.prompt-text {
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-weight: 600;
    line-height: 1.55;
    font-size: clamp(1.25rem, 2.5vw, 2rem);
    color: #f4f7fb;
    word-break: break-word;
}

.small-help {
    color: rgba(230,240,255,0.62);
    font-size: 0.95rem;
    line-height: 1.7;
}

.good { color: #69f0ae; font-weight: 700; }
.bad { color: #ff7a86; font-weight: 700; }
.warn { color: #ffd54a; font-weight: 700; }

.teach-box {
    border-left: 4px solid #33d8ff;
    background: rgba(51, 216, 255, 0.08);
    padding: 0.95rem 1rem;
    border-radius: 14px;
    margin-top: 0.8rem;
    line-height: 1.75;
}

.keyword-chip {
    display: inline-block;
    padding: 0.18rem 0.5rem;
    margin: 0 0.1rem;
    border-radius: 999px;
    background: rgba(255, 215, 74, 0.18);
    border: 1px solid rgba(255, 215, 74, 0.35);
    color: #ffe98a;
    font-weight: 700;
}

.stButton > button {
    width: 100% !important;
    min-height: 68px !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255, 215, 74, 0.25) !important;
    color: #111 !important;
    background: linear-gradient(180deg, #ffd84d 0%, #c99700 100%) !important;
    box-shadow:
        0 7px 0 #7d6500,
        0 16px 24px rgba(0,0,0,0.30) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    transition: transform 0.06s ease, filter 0.08s ease !important;
    white-space: normal !important;
    line-height: 1.25 !important;
    text-align: center !important;
    padding: 0.9rem 0.9rem !important;
}

.stButton > button:hover { filter: brightness(1.06); }
.stButton > button:active {
    transform: translateY(3px);
    box-shadow:
        0 3px 0 #7d6500,
        0 10px 16px rgba(0,0,0,0.24) !important;
}

.secondary-btn > button {
    background: linear-gradient(180deg, rgba(57, 72, 100, 0.95), rgba(28, 36, 54, 0.98)) !important;
    color: #eff6ff !important;
    border: 1px solid rgba(51, 216, 255, 0.22) !important;
    box-shadow:
        0 7px 0 rgba(0, 130, 170, 0.45),
        0 16px 24px rgba(0,0,0,0.30) !important;
}

.primary-btn > button {
    background: linear-gradient(180deg, #6cf6ff 0%, #1bb9ff 100%) !important;
    color: #031018 !important;
    box-shadow:
        0 7px 0 #0a6b8f,
        0 16px 24px rgba(0,0,0,0.30) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# SESSION STATE
# =========================================================
defaults = {
    "page": "lobby",
    "score": 0,
    "pp_index": 0,
    "pp_stage": "answer",
    "pp_feedback": None,
    "pp_user_answer": "",
    "pp_teach_cursor": 0,
    "kw_index": 0,
    "kw_feedback": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================================
# DATA
# =========================================================
PARAPHRASE_BANK = [
    {
        "prompt": "I decided to leave early because I wasn’t feeling well.",
        "target_keywords": ["decided", "leave early", "wasn’t feeling well"],
        "teach": {
            "decided": "decide → choose / opt for. In paraphrase, you can change the verb form or use a synonym.",
            "leave early": "leave early → depart early / head home early / leave ahead of schedule.",
            "wasn’t feeling well": "wasn’t feeling well → felt unwell / was sick / was under the weather.",
        },
        "suggestions": [
            "Due to feeling unwell, I chose to leave ahead of schedule.",
            "Since I wasn’t in good health, I left earlier than planned.",
            "Because I felt unwell, I decided to depart early.",
        ],
    },
    {
        "prompt": "We need to finish this project before the end of the week.",
        "target_keywords": ["need to finish", "project", "before the end of the week"],
        "teach": {
            "need to finish": "need to finish → must complete / have to wrap up / are required to complete.",
            "project": "project → task / assignment / work.",
            "before the end of the week": "before the end of the week → by the weekend / by week’s end / before Friday finishes.",
        },
        "suggestions": [
            "The project must be completed by the weekend.",
            "We are required to wrap up this task before the week ends.",
            "This assignment needs to be finished by the end of the week.",
        ],
    },
    {
        "prompt": "The company introduced a new policy to reduce waste.",
        "target_keywords": ["company", "introduced", "new policy", "reduce waste"],
        "teach": {
            "introduced": "introduced → implemented / launched / rolled out.",
            "new policy": "new policy → fresh rule / updated regulation / revised guideline.",
            "reduce waste": "reduce waste → cut down on waste / minimize waste / lower waste production.",
        },
        "suggestions": [
            "The company implemented a new policy to minimize waste.",
            "A fresh policy was launched by the company to cut down on waste.",
            "To reduce waste, the company rolled out a revised guideline.",
        ],
    },
]

KEYWORDS_BANK = [
    {
        "ctx": "Someone is talking too much about minor details.",
        "sentence": "I understand the background, but could you please just __________?",
        "opts": ["get to the point", "arrive to the point", "hit the point", "reach on the point"],
        "ans": "get to the point",
        "exp": "The natural collocation is get to the point.",
    },
    {
        "ctx": "Your friend looks distracted and worried.",
        "sentence": "You’ve been quiet all night. Is something __________?",
        "opts": ["in your mind", "at your mind", "on your mind", "over your mind"],
        "ans": "on your mind",
        "exp": "The correct phrase is on your mind.",
    },
    {
        "ctx": "The team finally needs to choose one plan.",
        "sentence": "We can’t keep debating forever. We need to __________ by noon.",
        "opts": ["do a decision", "make a decision", "build a decision", "create a decision"],
        "ans": "make a decision",
        "exp": "The standard collocation is make a decision.",
    },
]

GAMES = [
    ("paraphrase", "Paraphrase Pro"),
    ("keywords", "Key Words for Fluency"),
    ("formal", "Formal Upgrade"),
    ("error", "Error Hunt"),
    ("micro", "Micro Expand"),
]

# =========================================================
# HELPERS
# =========================================================
def normalize(text):
    return re.sub(r"\s+", " ", text.lower().strip())

def tokenize(text):
    return re.findall(r"[A-Za-z']+", text.lower())

def go(page):
    st.session_state.page = page

def reset_game_state():
    st.session_state.pp_stage = "answer"
    st.session_state.pp_feedback = None
    st.session_state.pp_user_answer = ""
    st.session_state.pp_teach_cursor = 0
    st.session_state.kw_feedback = None

def highlight_text(text, keywords):
    out = text
    for kw in sorted(set(keywords), key=len, reverse=True):
        pattern = re.compile(rf"\b({re.escape(kw)})\b", re.IGNORECASE)
        out = pattern.sub(r"<span class='keyword-chip'>\\1</span>", out)
    return out

def rule_based_score(prompt, user_answer):
    p = tokenize(prompt)
    u = tokenize(user_answer)
    if not u:
        return 0, ["No answer provided."]
    p_set, u_set = set(p), set(u)
    overlap = len(p_set & u_set) / max(1, len(p_set))
    copy_penalty = SequenceMatcher(None, normalize(prompt), normalize(user_answer)).ratio()
    length_ratio = len(u) / max(1, len(p))
    notes = []
    if overlap > 0.45:
        notes.append("Too much word copying from the prompt.")
    if copy_penalty > 0.72:
        notes.append("Very close to the original wording; paraphrase strength is weak.")
    if length_ratio < 0.45:
        notes.append("Answer is probably too short.")
    if length_ratio > 2.8:
        notes.append("Answer is probably too long.")
    if not notes:
        notes.append("Good paraphrase attempt with some lexical change.")
    score = 0
    score += int(max(0, 40 - overlap * 50))
    score += int(max(0, 30 - copy_penalty * 30))
    score += int(max(0, 30 - abs(1.0 - length_ratio) * 25))
    return max(0, min(100, score)), notes

# =========================================================
# UI
# =========================================================
st.markdown("<div class='pencraft-title'>PENCRAFT</div>", unsafe_allow_html=True)
st.markdown("<div class='pencraft-subtitle'>IELTS Writing Mastery System</div>", unsafe_allow_html=True)

# =========================================================
# LOBBY
# =========================================================
if st.session_state.page == "lobby":
    st.markdown(
        """
        <div class="hero-card">
            <div style="text-align:center; color: rgba(255,255,255,0.75); line-height:1.8;">
                <div style="font-family:Orbitron; letter-spacing:0.14em; color:#33d8ff; margin-bottom:0.4rem;">
                    DARK NEON PREMIUM
                </div>
                <div>
                    Choose a mission below. Each game is isolated, polished, and fast.
                    The lobby is separate from gameplay by design.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.markdown("### ✨ Paraphrase Pro")
        st.markdown("Prompt → your answer → rule-based feedback → 3 suggestions → teaching mode.")
        if st.button("Launch Paraphrase Pro", key="launch_paraphrase"):
            st.session_state.page = "paraphrase"
            reset_game_state()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.markdown("### 💎 Key Words for Fluency")
        st.markdown("Grammar, collocations, and lexical precision with a 2×2 option layout.")
        if st.button("Launch Key Words", key="launch_keywords"):
            st.session_state.page = "keywords"
            reset_game_state()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("### Other Games")
    g1, g2, g3 = st.columns(3)
    for col, (slug, label) in zip([g1, g2, g3], GAMES[2:]):
        with col:
            st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
            st.markdown(f"#### {label}")
            st.markdown("Skeleton ready. Can be filled with your bank immediately.")
            if st.button(f"Open {label}", key=f"open_{slug}"):
                st.session_state.page = slug
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# PARAPHRASE PRO
# =========================================================
elif st.session_state.page == "paraphrase":
    if st.session_state.pp_index >= len(PARAPHRASE_BANK):
        st.markdown("## ✅ Paraphrase mission complete")
        st.success("All paraphrase prompts completed.")
        if st.button("Back to Lobby"):
            st.session_state.page = "lobby"
            st.rerun()
    else:
        data = PARAPHRASE_BANK[st.session_state.pp_index]

        st.markdown(
            f"""
            <div class="mission-bar">
                <div class="mission-label">MISSION: PARAPHRASE PRO</div>
                <div class="score-label">🏆 SCORE: {st.session_state.score}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='prompt-title'>Prompt {st.session_state.pp_index + 1}/{len(PARAPHRASE_BANK)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='prompt-text'>{data['prompt']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.markdown("<div class='textarea-label'>Your paraphrase</div>", unsafe_allow_html=True)
        st.session_state.pp_user_answer = st.text_area(
            label="",
            value=st.session_state.pp_user_answer,
            height=160,
            placeholder="Type your paraphrase here...",
            key=f"pp_input_{st.session_state.pp_index}",
        )
        col_a, col_b, col_c = st.columns([1, 1, 1])

        with col_a:
            if st.button("Evaluate", key=f"pp_eval_{st.session_state.pp_index}"):
                score, notes = rule_based_score(data["prompt"], st.session_state.pp_user_answer)
                st.session_state.pp_feedback = {
                    "score": score,
                    "notes": notes,
                    "keywords": data["target_keywords"],
                    "suggestions": data["suggestions"],
                    "teach": data["teach"],
                }
                st.session_state.score += score
                st.session_state.pp_stage = "feedback"
                st.rerun()

        with col_b:
            if st.button("Reset Answer", key=f"pp_reset_{st.session_state.pp_index}"):
                st.session_state.pp_user_answer = ""
                st.session_state.pp_feedback = None
                st.session_state.pp_stage = "answer"
                st.rerun()

        with col_c:
            if st.button("Back to Lobby", key=f"pp_back_{st.session_state.pp_index}"):
                st.session_state.page = "lobby"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.pp_feedback:
            fb = st.session_state.pp_feedback
            score = fb["score"]
            st.write("")
            st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
            if score >= 75:
                mood = "good"
            elif score >= 45:
                mood = "warn"
            else:
                mood = "bad"

            st.markdown(f"<div class='{mood}'>Score: {score}/100</div>", unsafe_allow_html=True)
            for n in fb["notes"]:
                st.markdown(f"- {n}")

            st.markdown("#### 3 Suggestions")
            for s in fb["suggestions"]:
                st.markdown(f"- {s}")

            st.markdown("#### Teaching Mode")
            kw_html = highlight_text(data["prompt"], fb["keywords"])
            st.markdown(f"<div class='teach-box'>{kw_html}</div>", unsafe_allow_html=True)
            for k, v in fb["teach"].items():
                st.markdown(f"<div class='teach-box'><b>{k}</b><br>{v}</div>", unsafe_allow_html=True)

            if st.button("Next Prompt", key=f"pp_next_{st.session_state.pp_index}"):
                st.session_state.pp_index += 1
                st.session_state.pp_feedback = None
                st.session_state.pp_user_answer = ""
                st.session_state.pp_stage = "answer"
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# KEY WORDS FOR FLUENCY
# =========================================================
elif st.session_state.page == "keywords":
    if st.session_state.kw_index >= len(KEYWORDS_BANK):
        st.markdown("## ✅ Key Words mission complete")
        st.success("All keyword questions completed.")
        if st.button("Back to Lobby", key="kw_back_done"):
            st.session_state.page = "lobby"
            st.rerun()
    else:
        q = KEYWORDS_BANK[st.session_state.kw_index]

        st.markdown(
            f"""
            <div class="mission-bar">
                <div class="mission-label">MISSION: KEY WORDS FOR FLUENCY</div>
                <div class="score-label">🏆 SCORE: {st.session_state.score}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-help'>{q['ctx']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='prompt-text' style='font-size:1.35rem;'>{q['sentence']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        o1, o2 = st.columns(2)
        o3, o4 = st.columns(2)

        options = q["opts"]
        buttons = [
            (o1, options[0], "kw_opt_0"),
            (o2, options[1], "kw_opt_1"),
            (o3, options[2], "kw_opt_2"),
            (o4, options[3], "kw_opt_3"),
        ]

        if st.session_state.kw_feedback is None:
            for col, opt, key in buttons:
                with col:
                    if st.button(opt, key=f"{key}_{st.session_state.kw_index}"):
                        correct = opt == q["ans"]
                        st.session_state.kw_feedback = {
                            "correct": correct,
                            "selected": opt,
                        }
                        if correct:
                            st.session_state.score += 10
                        st.rerun()

        if st.session_state.kw_feedback:
            fb = st.session_state.kw_feedback
            st.write("")
            st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
            if fb["correct"]:
                st.markdown("<div class='good'>Correct ✅</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bad'>Wrong ❌ — correct answer: {q['ans']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='teach-box'><b>Explanation:</b> {q['exp']}</div>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Next Question", key=f"kw_next_{st.session_state.kw_index}"):
                    st.session_state.kw_index += 1
                    st.session_state.kw_feedback = None
                    st.rerun()
            with c2:
                if st.button("Back to Lobby", key=f"kw_back_{st.session_state.kw_index}"):
                    st.session_state.page = "lobby"
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# PLACEHOLDERS
# =========================================================
elif st.session_state.page in ["formal", "error", "micro"]:
    st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
    st.markdown(f"## {dict(GAMES)[st.session_state.page]}")
    st.markdown("Skeleton is ready. Add your content bank here.")
    if st.button("Back to Lobby", key=f"back_{st.session_state.page}"):
        st.session_state.page = "lobby"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
