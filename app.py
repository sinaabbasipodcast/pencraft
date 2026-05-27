import streamlit as st
import random
import subprocess
import time
import re
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="PenCraft Academy", page_icon="🖋️", layout="wide")

# =========================
# CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;700;800&family=Orbitron:wght@500;700;800&family=Inter:wght@400;600;700&display=swap');

:root{
    --bg:#06080f;
    --panel:#0f1724;
    --panel2:#131d2d;
    --gold:#f4c95d;
    --cyan:#63d8ff;
    --blue:#5b8cff;
    --violet:#9b7bff;
    --green:#00d084;
    --text:#ecf3ff;
    --muted:#aab8d6;
    --danger:#ff6b6b;
}

html, body, [class*="css"] {
    font-family: 'Vazirmatn', 'Inter', sans-serif !important;
}

.stApp {
    background:
        radial-gradient(circle at top right, rgba(91,140,255,0.18), transparent 25%),
        radial-gradient(circle at top left, rgba(155,123,255,0.12), transparent 20%),
        linear-gradient(180deg, #05070d 0%, #0a1020 100%);
    color: var(--text);
    direction: rtl;
}

h1, h2, h3 {
    font-family: 'Orbitron', 'Vazirmatn', sans-serif !important;
    color: #f7fbff !important;
    text-shadow: 0 0 16px rgba(99,216,255,0.18);
}

.status-shell {
    background: rgba(15, 23, 36, 0.88);
    border: 1px solid rgba(244,201,93,0.35);
    border-radius: 18px;
    padding: 14px 18px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
    backdrop-filter: blur(10px);
    margin-bottom: 14px;
}

.status-grid {
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:12px;
    flex-wrap:wrap;
}

.stat-pill {
    background: linear-gradient(135deg, rgba(91,140,255,0.18), rgba(99,216,255,0.12));
    border: 1px solid rgba(99,216,255,0.22);
    border-radius: 14px;
    padding: 10px 16px;
    color: white;
    font-weight: 700;
}

.mascot-box {
    background: linear-gradient(135deg, rgba(99,216,255,0.12), rgba(155,123,255,0.12));
    border: 1px solid rgba(99,216,255,0.35);
    border-radius: 20px;
    padding: 18px;
    margin: 12px 0 18px 0;
    box-shadow: 0 0 24px rgba(99,216,255,0.12);
}

.mascot-name {
    font-family: 'Orbitron', sans-serif;
    color: var(--gold);
    font-size: 1.05rem;
    margin-bottom: 8px;
}

.dialogue-text {
    color: var(--text);
    font-size: 1.02rem;
    line-height: 2;
}

.game-box {
    background: linear-gradient(180deg, rgba(19,29,45,0.92), rgba(12,18,30,0.92));
    border: 1px solid rgba(244,201,93,0.35);
    border-radius: 22px;
    padding: 22px;
    margin: 16px 0;
    box-shadow: 0 10px 35px rgba(0,0,0,0.35);
}

.lesson-card {
    background: linear-gradient(135deg, rgba(244,201,93,0.10), rgba(99,216,255,0.08));
    border: 1px solid rgba(244,201,93,0.24);
    border-right: 5px solid var(--gold);
    padding: 16px;
    border-radius: 18px;
    margin: 12px 0;
    color: var(--text);
}

.paragraph-box {
    background: #101827;
    border: 2px solid rgba(244,201,93,0.75);
    color: #ffffff;
    border-radius: 18px;
    padding: 18px;
    font-size: 1.15rem;
    line-height: 2.2;
    margin-bottom: 18px;
    min-height: 85px;
}

.lobby-title {
    text-align:center;
    font-size: 3rem;
    margin-top: 10px;
    margin-bottom: 8px;
    color: #f4f8ff;
}

.lobby-sub {
    text-align:center;
    color: var(--muted);
    font-size: 1.05rem;
    margin-bottom: 22px;
}

.game-card {
    background: linear-gradient(145deg, rgba(19,29,45,0.95), rgba(10,15,25,0.95));
    border-radius: 22px;
    padding: 22px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 28px rgba(0,0,0,0.35);
    min-height: 220px;
    margin-bottom: 16px;
}

.card-title {
    font-family: 'Orbitron', 'Vazirmatn', sans-serif;
    font-size: 1.3rem;
    color: white;
    margin-bottom: 8px;
}

.card-desc {
    color: var(--muted);
    line-height: 1.9;
    min-height: 68px;
    margin-bottom: 12px;
}

.card-tag {
    display:inline-block;
    padding:6px 12px;
    border-radius:999px;
    font-size:0.85rem;
    font-weight:700;
    margin-bottom:10px;
}

.gold {background: rgba(244,201,93,0.16); color: var(--gold);}
.cyan {background: rgba(99,216,255,0.16); color: var(--cyan);}
.violet {background: rgba(155,123,255,0.16); color: #cdbdff;}
.green {background: rgba(0,208,132,0.16); color: var(--green);}
.red {background: rgba(255,107,107,0.16); color: #ffb3b3;}

.score-box {
    background: rgba(255,255,255,0.04);
    border-radius: 16px;
    padding: 12px;
    margin: 10px 0;
    border: 1px solid rgba(255,255,255,0.08);
}

.stButton>button {
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(99,216,255,0.25);
    background: linear-gradient(135deg, #17243b, #10192b);
    color: white;
    font-weight: 800;
    padding: 0.7rem 1rem;
    transition: 0.2s ease;
}

.stButton>button:hover {
    border-color: rgba(244,201,93,0.55);
    box-shadow: 0 0 16px rgba(244,201,93,0.14);
    transform: translateY(-1px);
}

div[data-testid="stExpander"] {
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# =========================
# STATE
# =========================
def init_state():
    defaults = {
        "xp": 0,
        "level": 1,
        "game_mode": "lobby",
        "badges": [],
        "dialogue_step": {},
        "dialogue_done": {},
        "game_skill": {
            "formal": 1,
            "linker": 1,
            "para": 1,
            "punc": 1,
            "fa": 1
        },
        "game_stats": {
            "formal": {"correct": 0, "wrong": 0, "streak": 0},
            "linker": {"correct": 0, "wrong": 0, "streak": 0},
            "para": {"correct": 0, "wrong": 0, "streak": 0},
            "punc": {"correct": 0, "wrong": 0, "streak": 0},
            "fa": {"correct": 0, "wrong": 0, "streak": 0},
        },
        "current_questions": {},
        "last_feedback": {},
        "awaiting_next": {}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# =========================
# HELPERS
# =========================
def add_xp(amount):
    st.session_state.xp = max(0, st.session_state.xp + amount)
    st.session_state.level = st.session_state.xp // 100 + 1

def award_badge(name):
    if name not in st.session_state.badges:
        st.session_state.badges.append(name)
        st.toast(f"🏅 نشان جدید: {name}")

def reset_progress():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

def mascot_dialogue(dialogue_key, messages, mascot_name="NovaPen"):
    if dialogue_key not in st.session_state.dialogue_step:
        st.session_state.dialogue_step[dialogue_key] = 0

    step = st.session_state.dialogue_step[dialogue_key]

    if st.session_state.dialogue_done.get(dialogue_key, False):
        return True

    st.markdown(f"""
    <div class="mascot-box">
        <div class="mascot-name">🤖 {mascot_name}</div>
        <div class="dialogue-text">{messages[step]}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if step < len(messages) - 1:
            if st.button("ادامه توضیحات", key=f"next_dialogue_{dialogue_key}_{step}"):
                st.session_state.dialogue_step[dialogue_key] += 1
                st.rerun()
        else:
            if st.button("شروع مرحله", key=f"finish_dialogue_{dialogue_key}"):
                st.session_state.dialogue_done[dialogue_key] = True
                st.rerun()
    with c2:
        if st.button("رد کردن", key=f"skip_dialogue_{dialogue_key}"):
            st.session_state.dialogue_done[dialogue_key] = True
            st.rerun()

    return False

def update_adaptive_level(game_key, correct):
    skill = st.session_state.game_skill[game_key]
    stats = st.session_state.game_stats[game_key]

    if correct:
        stats["correct"] += 1
        stats["streak"] += 1
        if stats["streak"] >= 2:
            skill += 1
    else:
        stats["wrong"] += 1
        stats["streak"] = 0
        skill -= 1

    skill = max(1, min(5, skill))
    st.session_state.game_skill[game_key] = skill

def get_skill_label(skill):
    labels = {
        1: "خیلی آسان",
        2: "آسان",
        3: "متوسط",
        4: "سخت",
        5: "خیلی سخت"
    }
    return labels.get(skill, "متوسط")

def ensure_question(game_key, generator):
    if game_key not in st.session_state.current_questions or st.session_state.current_questions[game_key] is None:
        st.session_state.current_questions[game_key] = generator(st.session_state.game_skill[game_key])
        st.session_state.awaiting_next[game_key] = False
        st.session_state.last_feedback[game_key] = ""

def next_question(game_key, generator):
    st.session_state.current_questions[game_key] = generator(st.session_state.game_skill[game_key])
    st.session_state.awaiting_next[game_key] = False
    st.session_state.last_feedback[game_key] = ""

# =========================
# QUESTION GENERATORS
# =========================
formal_templates = {
    1: [
        ("kids", "children", "children رسمی‌تر از kids است."),
        ("a lot", "many", "many در نوشتار رسمی مناسب‌تر است."),
        ("get", "obtain", "obtain رسمی‌تر از get است."),
        ("help", "assist", "assist واژه‌ای رسمی‌تر است."),
    ],
    2: [
        ("buy", "purchase", "purchase آکادمیک‌تر از buy است."),
        ("show", "demonstrate", "demonstrate رسمی‌تر است."),
        ("need", "require", "require در writing رسمی رایج‌تر است."),
        ("enough", "sufficient", "sufficient رسمی‌تر است."),
    ],
    3: [
        ("find out", "discover", "discover ساختار رسمی‌تری دارد."),
        ("deal with", "address", "address رسمی‌تر از deal with است."),
        ("leave out", "omit", "omit برای متن رسمی مناسب‌تر است."),
        ("bring about", "cause", "cause ساختار رسمی‌تر و دقیق‌تری دارد."),
    ],
    4: [
        ("really important", "crucial", "crucial آکادمیک‌تر است."),
        ("bad", "detrimental", "detrimental رسمی‌تر و دقیق‌تر است."),
        ("good", "beneficial", "beneficial رسمی‌تر است."),
        ("clear", "evident", "evident در متون رسمی طبیعی‌تر است."),
    ],
    5: [
        ("helped", "facilitated", "facilitated سطح واژگانی بالاتری دارد."),
        ("used", "utilized", "utilized رسمی‌تر است."),
        ("tried", "attempted", "attempted واژه‌ای رسمی‌تر است."),
        ("started", "initiated", "initiated در متن آکادمیک مناسب‌تر است."),
    ]
}

formal_sentence_patterns = [
    "Many {bad} the new system during the project.",
    "Researchers {bad} better results after the experiment.",
    "The policy can {bad} social progress.",
    "The school should {bad} students more effectively.",
    "These changes are {bad} for long-term growth."
]

def generate_formal_question(skill):
    pair = random.choice(formal_templates[skill])
    bad, good, reason = pair
    pattern = random.choice(formal_sentence_patterns)
    sentence = pattern.format(bad=bad)
    return {
        "sentence": sentence,
        "bad_word": bad,
        "good_word": good,
        "reason": reason
    }

linker_bank = {
    1: [
        ("I was tired; ___, I finished my homework.", ["however", "therefore", "for example"], "however", "رابط تضاد لازم است."),
        ("She studied hard; ___, she passed the exam.", ["however", "therefore", "meanwhile"], "therefore", "رابط نتیجه لازم است."),
    ],
    2: [
        ("Many students enjoy science. ___, physics can be exciting.", ["For example", "However", "Therefore"], "For example", "اینجا مثال آورده شده است."),
        ("The task was difficult; ___, they completed it successfully.", ["nevertheless", "for instance", "because"], "nevertheless", "رابط تضاد لازم است."),
    ],
    3: [
        ("The city invested in transport; ___, traffic decreased.", ["as a result", "in contrast", "for example"], "as a result", "رابط نتیجه مناسب است."),
        ("Online learning is flexible. ___, it may reduce face-to-face interaction.", ["On the other hand", "Therefore", "For instance"], "On the other hand", "اینجا دیدگاه مخالف آمده است."),
    ],
    4: [
        ("The device is inexpensive; ___, it is highly efficient.", ["moreover", "thus", "however"], "moreover", "اینجا اضافه‌کردن نکته مثبت داریم."),
        ("The proposal seemed practical; ___, several experts opposed it.", ["nevertheless", "for example", "similarly"], "nevertheless", "تضاد و مخالفت مطرح شده است."),
    ],
    5: [
        ("The findings were limited; ___, they offered valuable insights.", ["nonetheless", "for instance", "consequently"], "nonetheless", "رابط تضاد پیشرفته لازم است."),
        ("The policy was poorly implemented; ___, public trust declined.", ["consequently", "likewise", "namely"], "consequently", "رابط نتیجه دقیق‌ترین گزینه است."),
    ]
}

def generate_linker_question(skill):
    q = random.choice(linker_bank[skill])
    sentence, options, answer, explanation = q
    random.shuffle(options)
    return {
        "sentence": sentence,
        "options": options,
        "answer": answer,
        "explanation": explanation
    }

paraphrase_bank = {
    1: [
        ("Technology has changed the way people communicate.",
         "The way people communicate has been changed by technology.",
         ["People communicate in the same way because of technology.",
          "The way people communicate has been changed by technology.",
          "Technology is not related to communication."],
         "معنی حفظ شده و ساختار جمله تغییر کرده است."),
    ],
    2: [
        ("Students should learn how to think critically.",
         "Critical thinking is a skill students should develop.",
         ["Students should avoid difficult ideas.",
          "Critical thinking is a skill students should develop.",
          "Teachers do all the thinking for students."],
         "همان پیام اصلی با بیان متفاوت منتقل شده است."),
    ],
    3: [
        ("Reading regularly improves vocabulary.",
         "Vocabulary can be improved through regular reading.",
         ["Reading sometimes destroys vocabulary.",
          "Vocabulary can be improved through regular reading.",
          "Regular reading is only for children."],
         "ساختار passive باعث paraphrase طبیعی شده است."),
    ],
    4: [
        ("Governments must take action to reduce pollution.",
         "Measures should be implemented by governments to curb pollution.",
         ["Governments should ignore pollution.",
          "Measures should be implemented by governments to curb pollution.",
          "Pollution has nothing to do with governments."],
         "واژگان رسمی‌تر و ساختار متفاوت استفاده شده است."),
    ],
    5: [
        ("The internet enables people to access information instantly.",
         "Instant access to information is made possible by the internet.",
         ["The internet prevents access to information.",
          "Instant access to information is made possible by the internet.",
          "Information should not be available online."],
         "بازنویسی پیشرفته با حفظ کامل معنا انجام شده است."),
    ]
}

def generate_paraphrase_question(skill):
    original, answer, options, explanation = random.choice(paraphrase_bank[skill])
    random.shuffle(options)
    return {
        "original": original,
        "options": options,
        "answer": answer,
        "explanation": explanation
    }

punc_bank = {
    1: [
        ("When I arrived home ___ I saw my brother.", ",", "بعد از عبارت مقدماتی از comma استفاده می‌کنیم."),
        ("After lunch ___ we went back to class.", ",", "عبارت آغازین نیاز به comma دارد."),
    ],
    2: [
        ("I wanted to go out ___ it was raining heavily.", ";", "دو جمله مستقلِ مرتبط را با semicolon می‌توان وصل کرد."),
        ("She prepared carefully ___ she still felt nervous.", ";", "اینجا دو جمله مستقل داریم."),
    ],
    3: [
        ("My favorite subjects are math ___ science ___ and history.", ", ,", "برای فهرست از comma استفاده می‌کنیم."),
        ("The bag contained pens ___ notebooks ___ and a ruler.", ", ,", "لیست سه‌تایی نیاز به comma دارد."),
    ],
    4: [
        ("He said ___ practice makes progress.", ":", "colon برای معرفی نقل‌قول یا توضیح استفاده می‌شود."),
        ("There was only one solution ___ teamwork.", ":", "اینجا colon چیزی را معرفی می‌کند."),
    ],
    5: [
        ("The results were surprising ___ however ___ more research is needed.", "; ,", "قبل از however در این ساختار semicolon و بعدش comma می‌آید."),
        ("She trained daily ___ therefore ___ her performance improved.", "; ,", "در اتصال دو جمله مستقل با linker این الگو طبیعی است."),
    ]
}

def generate_punctuation_question(skill):
    sentence, answer, explanation = random.choice(punc_bank[skill])
    return {
        "sentence": sentence,
        "answer": answer,
        "explanation": explanation
    }

fa_topics = {
    1: "Should students wear school uniforms?",
    2: "Should homework be reduced for teenagers?",
    3: "Should schools replace printed books with tablets?",
    4: "Should social media use be limited for teens?",
    5: "Should AI tools be allowed in school writing tasks?"
}

fa_orders = {
    1: {
        "blocks": {
            "A": "In conclusion, uniforms can be useful in schools.",
            "B": "On the other hand, some students feel they limit individuality.",
            "C": "School uniforms are a common feature in many schools.",
            "D": "Firstly, they can reduce social pressure among students."
        },
        "answer": "CDBA"
    },
    2: {
        "blocks": {
            "A": "In conclusion, lighter homework may support balance.",
            "B": "However, some argue homework builds responsibility.",
            "C": "Homework is a major part of student life.",
            "D": "Firstly, too much homework can cause stress."
        },
        "answer": "CDBA"
    },
    3: {
        "blocks": {
            "A": "In conclusion, digital learning offers benefits despite some concerns.",
            "B": "On the other hand, screens may distract learners.",
            "C": "Many schools are considering digital textbooks.",
            "D": "Firstly, tablets can provide interactive learning tools."
        },
        "answer": "CDBA"
    },
    4: {
        "blocks": {
            "A": "Overall, some restrictions may be beneficial.",
            "B": "However, others believe social media helps communication.",
            "C": "Teenagers spend a great deal of time on social media.",
            "D": "Firstly, excessive use can affect mental health."
        },
        "answer": "CDBA"
    },
    5: {
        "blocks": {
            "A": "In conclusion, AI tools can be useful if used responsibly.",
            "B": "On the other hand, overreliance may weaken writing skills.",
            "C": "AI is becoming increasingly common in education.",
            "D": "Firstly, it can support idea generation and planning."
        },
        "answer": "CDBA"
    }
}

def generate_fa_question(skill):
    mode = random.choice(["order", "intro"])
    if mode == "order":
        data = fa_orders[skill]
        return {
            "type": "order",
            "blocks": data["blocks"],
            "answer": data["answer"],
            "topic": fa_topics[skill]
        }
    return {
        "type": "intro",
        "topic": fa_topics[skill]
    }

# =========================
# UI HEADER
# =========================
xp_in_level = st.session_state.xp % 100

st.markdown(f"""
<div class="status-shell">
    <div class="status-grid">
        <div class="stat-pill">🏆 Level: {st.session_state.level}</div>
        <div class="stat-pill">⚡ XP: {st.session_state.xp}</div>
        <div class="stat-pill">🖋️ PenCraft Academy</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.progress(xp_in_level / 100)
st.caption(f"{xp_in_level}/100 XP تا لول بعدی")

with st.expander("🏅 نشان‌ها | آمار | تنظیمات"):
    if st.session_state.badges:
        st.write(" | ".join(st.session_state.badges))
    else:
        st.write("هنوز نشانی کسب نشده.")

    st.write("### آمار بازی‌ها")
    for g, s in st.session_state.game_stats.items():
        st.write(f"**{g}** → ✅ {s['correct']} | ❌ {s['wrong']} | 🔥 streak: {s['streak']} | 🎯 difficulty: {st.session_state.game_skill[g]} ({get_skill_label(st.session_state.game_skill[g])})")

    if st.button("🔄 ریست کامل پیشرفت"):
        reset_progress()

# =========================
# GAME COMPONENTS
# =========================
def show_adaptive_panel(game_key):
    skill = st.session_state.game_skill[game_key]
    stats = st.session_state.game_stats[game_key]
    st.markdown(f"""
    <div class="score-box">
        <b>سطح فعلی:</b> {skill} - {get_skill_label(skill)}<br>
        <b>درست:</b> {stats["correct"]} |
        <b>غلط:</b> {stats["wrong"]} |
        <b>استریک:</b> {stats["streak"]}
    </div>
    """, unsafe_allow_html=True)

def formal_shift_game():
    st.subheader("🔍 Formal Shift")

    intro = [
        "در این بازی باید واژه یا عبارت غیررسمی را شناسایی کنی.",
        "بعد معادل رسمی‌تر آن را وارد می‌کنی.",
        "اگر چند بار درست جواب بدهی، عبارت‌ها سخت‌تر می‌شوند."
    ]
    if not mascot_dialogue("formal_intro", intro):
        return

    show_adaptive_panel("formal")
    ensure_question("formal", generate_formal_question)
    q = st.session_state.current_questions["formal"]

    st.markdown(f"""
    <div class="paragraph-box">{q["sentence"]}</div>
    """, unsafe_allow_html=True)

    st.write(f"واژه/عبارت غیررسمی را پیدا کن و نسخه رسمی‌ترش را بنویس.")

    found = st.text_input("عبارت غیررسمی:", key="formal_found")
    replacement = st.text_input("جایگزین رسمی:", key="formal_replacement")

    if not st.session_state.awaiting_next["formal"]:
        if st.button("بررسی پاسخ", key="formal_check"):
            correct_found = found.strip().lower() == q["bad_word"].lower()
            correct_repl = replacement.strip().lower() == q["good_word"].lower()
            if correct_found and correct_repl:
                add_xp(25 + st.session_state.game_skill["formal"] * 5)
                update_adaptive_level("formal", True)
                st.session_state.last_feedback["formal"] = f"✅ درست! {q['reason']}"
                if st.session_state.game_stats["formal"]["correct"] >= 5:
                    award_badge("Formal Hunter")
                st.session_state.awaiting_next["formal"] = True
                st.rerun()
            else:
                add_xp(-3)
                update_adaptive_level("formal", False)
                st.session_state.last_feedback["formal"] = f"❌ پاسخ بهتر: {q['bad_word']} → {q['good_word']} | {q['reason']}"
                st.session_state.awaiting_next["formal"] = True
                st.rerun()
    else:
        if st.session_state.last_feedback["formal"]:
            st.info(st.session_state.last_feedback["formal"])
        if st.button("سوال بعدی", key="formal_next"):
            next_question("formal", generate_formal_question)
            st.rerun()

def linker_chain_game():
    st.subheader("⛓️ Linker Chain")

    intro = [
        "در این بازی باید linker مناسب را انتخاب کنی.",
        "اگر خوب عمل کنی، گزینه‌ها و روابط معنایی پیچیده‌تر می‌شوند."
    ]
    if not mascot_dialogue("linker_intro", intro):
        return

    show_adaptive_panel("linker")
    ensure_question("linker", generate_linker_question)
    q = st.session_state.current_questions["linker"]

    st.markdown(f"""<div class='game-box'>{q["sentence"]}</div>""", unsafe_allow_html=True)
    choice = st.radio("انتخاب تو:", q["options"], key=f"linker_choice_dynamic_{q['sentence']}")

    if not st.session_state.awaiting_next["linker"]:
        if st.button("بررسی پاسخ", key="linker_check"):
            if choice == q["answer"]:
                add_xp(20 + st.session_state.game_skill["linker"] * 5)
                update_adaptive_level("linker", True)
                st.session_state.last_feedback["linker"] = f"✅ درست! {q['explanation']}"
                if st.session_state.game_stats["linker"]["correct"] >= 5:
                    award_badge("Link Master")
            else:
                add_xp(-3)
                update_adaptive_level("linker", False)
                st.session__feedback["linker"] = f"❌ درستش: {q['answer']} | {q['explanation']}"
            st.session_state.awaiting_next["linker"] = True
            st.rerun()
    else:
        st.info(st.session_state.last_feedback["linker"])
        if st.button("سوال بعدی", key="linker_next"):
            next