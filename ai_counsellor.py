import streamlit as st
from groq import Groq
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import os
from dotenv import load_dotenv
from gtts import gTTS
import tempfile

load_dotenv()

# ────────────────────── Professional modern styling ──────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap');

    .main {background-color: #F8FAFC;}
    h1, h2, h3 {font-family: 'Playfair Display', sans-serif; color: #0F4C81;}
    
    .stButton > button {
        background: linear-gradient(90deg, #0F4C81, #00A676);
        color: white !important;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(15,76,129,0.25);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,166,118,0.35);
    }

    .chat-user {
        background: #E0F2FE;
        border-radius: 20px 20px 4px 20px;
        padding: 16px 20px;
        margin: 12px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    .chat-assistant {
        background: #F1F5F9;
        border-radius: 20px 20px 20px 4px;
        padding: 16px 20px;
        margin: 12px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }

    .metric-card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(15,76,129,0.15);
    }

    .fade-in {animation: fadeIn 0.7s ease forwards;}
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(30px);}
        to {opacity: 1; transform: translateY(0);}
    }

    .stProgress > div > div > div > div {
        background-color: #00A676 !important;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="AI Counsellor", page_icon="🧠", layout="wide")

# ────────────── Groq client ──────────────
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# ────────────── Database connection ──────────────
# ────────────── Database connection (safe, no connection refused) ──────────────
def get_db_connection():
    import psycopg2
    from psycopg2.extras import RealDictCursor
    import streamlit as st

    # Use 127.0.0.1 explicitly to avoid localhost resolution issues
    db_config = {
        "host": "127.0.0.1",               # Force IPv4
        "port": 5432,                      # Default PostgreSQL port
        "dbname": st.secrets["db"]["dbname"],
        "user": st.secrets["db"]["user"],
        "password": st.secrets["db"]["password"],
        "connect_timeout": 5,              # Quick fail if server not reachable
        "cursor_factory": RealDictCursor
    }

    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except psycopg2.OperationalError as e:
        st.error(f"⚠️ PostgreSQL connection failed: {e}\n\nMake sure your server is running and host is 127.0.0.1.")
        st.stop()


# ────────────── Initialize tables ──────────────
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        full_name VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS profiles (
        user_id INTEGER PRIMARY KEY REFERENCES users(id),
        education_level VARCHAR(100),
        degree VARCHAR(200),
        grad_year INTEGER,
        gpa FLOAT,
        target_degree VARCHAR(100),
        field VARCHAR(200),
        intake_year INTEGER,
        countries TEXT[],
        budget INTEGER,
        funding VARCHAR(100),
        ielts VARCHAR(50),
        gre VARCHAR(50),
        sop VARCHAR(50),
        onboarding_completed BOOLEAN DEFAULT FALSE
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS shortlisted (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        university_name VARCHAR(200),
        country VARCHAR(100),
        annual_cost INTEGER,
        acceptance VARCHAR(50),
        risk VARCHAR(50),
        level VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, university_name)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS locked (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        university_name VARCHAR(200),
        country VARCHAR(100),
        annual_cost INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, university_name)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        task_text TEXT,
        done BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    cur.close()
    conn.close()

if "db_init" not in st.session_state:
    init_db()
    st.session_state.db_init = True

# ────────────── Universities list ──────────────
UNIVERSITIES = [
    {"name": "MIT", "country": "USA", "annual_cost_usd": 60000, "acceptance": "Very Low", "risk": "High", "level": "Dream"},
    {"name": "Stanford University", "country": "USA", "annual_cost_usd": 62000, "acceptance": "Very Low", "risk": "High", "level": "Dream"},
    {"name": "University of Toronto", "country": "Canada", "annual_cost_usd": 42000, "acceptance": "Medium", "risk": "Medium", "level": "Target"},
    {"name": "University of British Columbia", "country": "Canada", "annual_cost_usd": 38000, "acceptance": "Medium", "risk": "Low", "level": "Target"},
    {"name": "Imperial College London", "country": "UK", "annual_cost_usd": 52000, "acceptance": "Low", "risk": "High", "level": "Dream"},
    {"name": "UCL", "country": "UK", "annual_cost_usd": 48000, "acceptance": "Medium", "risk": "Medium", "level": "Target"},
    {"name": "Technical University of Munich", "country": "Germany", "annual_cost_usd": 8000, "acceptance": "Medium", "risk": "Low", "level": "Safe"},
    {"name": "ETH Zurich", "country": "Switzerland", "annual_cost_usd": 25000, "acceptance": "Low", "risk": "Medium", "level": "Dream"},
    {"name": "University of Melbourne", "country": "Australia", "annual_cost_usd": 45000, "acceptance": "Medium", "risk": "Medium", "level": "Target"},
    {"name": "NUS", "country": "Singapore", "annual_cost_usd": 38000, "acceptance": "Low", "risk": "High", "level": "Dream"},
    {"name": "University of Sydney", "country": "Australia", "annual_cost_usd": 42000, "acceptance": "Medium", "risk": "Medium", "level": "Target"},
    {"name": "University of Manchester", "country": "UK", "annual_cost_usd": 42000, "acceptance": "Medium", "risk": "Low", "level": "Safe"},
    {"name": "University of Waterloo", "country": "Canada", "annual_cost_usd": 36000, "acceptance": "Medium", "risk": "Medium", "level": "Target"},
    {"name": "Georgia Tech", "country": "USA", "annual_cost_usd": 48000, "acceptance": "Medium", "risk": "Medium", "level": "Target"},
    {"name": "RWTH Aachen", "country": "Germany", "annual_cost_usd": 6000, "acceptance": "High", "risk": "Low", "level": "Safe"},
    {"name": "University of Oxford", "country": "UK", "annual_cost_usd": 55000, "acceptance": "Very Low", "risk": "High", "level": "Dream"},
    {"name": "UC Berkeley", "country": "USA", "annual_cost_usd": 58000, "acceptance": "Low", "risk": "High", "level": "Dream"},
    {"name": "Monash University", "country": "Australia", "annual_cost_usd": 38000, "acceptance": "High", "risk": "Low", "level": "Safe"},
]

# ────────────── DB helper functions ──────────────
def create_or_get_user(email, full_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (email, full_name) VALUES (%s, %s) ON CONFLICT (email) DO UPDATE SET full_name = EXCLUDED.full_name RETURNING id", (email, full_name))
    user_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()
    return user_id

def save_profile(user_id, profile):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO profiles (user_id, education_level, degree, grad_year, gpa, target_degree, field, intake_year, countries, budget, funding, ielts, gre, sop, onboarding_completed)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
        ON CONFLICT (user_id) DO UPDATE SET
            education_level=EXCLUDED.education_level, degree=EXCLUDED.degree, grad_year=EXCLUDED.grad_year,
            gpa=EXCLUDED.gpa, target_degree=EXCLUDED.target_degree, field=EXCLUDED.field,
            intake_year=EXCLUDED.intake_year, countries=EXCLUDED.countries, budget=EXCLUDED.budget,
            funding=EXCLUDED.funding, ielts=EXCLUDED.ielts, gre=EXCLUDED.gre,
            sop=EXCLUDED.sop, onboarding_completed=TRUE
    """, (user_id, profile["education_level"], profile["degree"], profile["grad_year"], profile["gpa"],
          profile["target_degree"], profile["field"], profile["intake_year"], profile["countries"],
          profile["budget"], profile["funding"], profile["ielts"], profile["gre"], profile["sop"]))
    conn.commit()
    cur.close()
    conn.close()

def load_profile(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM profiles WHERE user_id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return dict(row) if row else None

def save_shortlisted(user_id, uni):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO shortlisted (user_id, university_name, country, annual_cost, acceptance, risk, level)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id, university_name) DO NOTHING
    """, (user_id, uni["name"], uni["country"], uni["annual_cost_usd"], uni["acceptance"], uni["risk"], uni["level"]))
    conn.commit()
    cur.close()
    conn.close()

def load_shortlisted(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM shortlisted WHERE user_id = %s", (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"name": r["university_name"], "country": r["country"], "annual_cost_usd": r["annual_cost"],
             "acceptance": r.get("acceptance",""), "risk": r.get("risk",""), "level": r.get("level","")} for r in rows]

def save_locked(user_id, uni):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO locked (user_id, university_name, country, annual_cost)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (user_id, university_name) DO NOTHING
    """, (user_id, uni["name"], uni["country"], uni["annual_cost_usd"]))
    conn.commit()
    cur.close()
    conn.close()

def load_locked(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM locked WHERE user_id = %s", (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"name": r["university_name"], "country": r["country"], "annual_cost_usd": r["annual_cost"]} for r in rows]

def save_tasks(user_id, tasks):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE user_id = %s", (user_id,))
    for task in tasks:
        cur.execute("INSERT INTO tasks (user_id, task_text, done) VALUES (%s, %s, %s)", (user_id, task["task"], task["done"]))
    conn.commit()
    cur.close()
    conn.close()

def load_tasks(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT task_text as task, done FROM tasks WHERE user_id = %s ORDER BY id", (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"task": r["task"], "done": r["done"]} for r in rows]

# ────────────── Session state ──────────────
if "user_id" not in st.session_state: st.session_state.user_id = None
if "email" not in st.session_state: st.session_state.email = None
if "current_stage" not in st.session_state: st.session_state.current_stage = 1
if "messages" not in st.session_state: st.session_state.messages = []
if "shortlisted" not in st.session_state: st.session_state.shortlisted = []
if "locked" not in st.session_state: st.session_state.locked = []
if "tasks" not in st.session_state: st.session_state.tasks = []
if "user_profile" not in st.session_state: st.session_state.user_profile = {}

stages = ["Login / Onboarding", "Dashboard", "AI Counsellor", "University Discovery", "Lock University", "Application Tasks"]

# ────────────── Sidebar ──────────────
with st.sidebar:
    st.markdown('<div style="text-align:center;"><h2 style="color:white;">🧠 AI Counsellor</h2></div>', unsafe_allow_html=True)
    st.markdown("**Your Professional Study Abroad Guide**")
    if st.session_state.user_id:
        st.success(f"👤 {st.session_state.get('email', 'User')}")
        st.progress((st.session_state.current_stage - 1) / 5)
        st.markdown(f"**Stage {st.session_state.current_stage}/6**")
    if st.button("🔄 Reset Everything"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ────────────── Main title ──────────────
st.title("AI Counsellor - Study Abroad Platform")
st.markdown('<p class="fade-in" style="color:#64748B; font-size:18px;">Your empathetic AI companion for confident study-abroad decisions</p>', unsafe_allow_html=True)

# ────────────── Stage 1: Login / Onboarding ──────────────
if st.session_state.current_stage == 1:
    st.subheader("Welcome – Login or Create Account")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        if st.button("Login"):
            if email:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("SELECT id, email FROM users WHERE email = %s", (email,))
                row = cur.fetchone()
                if row:
                    st.session_state.user_id = row["id"]
                    st.session_state.email = row["email"]
                    profile = load_profile(row["id"])
                    if profile:
                        st.session_state.user_profile = profile
                        st.session_state.current_stage = 2
                    st.session_state.shortlisted = load_shortlisted(row["id"])
                    st.session_state.locked = load_locked(row["id"])
                    st.session_state.tasks = load_tasks(row["id"])
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("No account found. Please sign up.")
                cur.close()
                conn.close()

    with tab2:
        name = st.text_input("Full Name")
        email = st.text_input("Email", key="signup_email")
        if st.button("Create Account & Start"):
            if name and email:
                user_id = create_or_get_user(email, name)
                st.session_state.user_id = user_id
                st.session_state.email = email
                st.success("Account created! Please complete onboarding below.")
                st.rerun()

    if st.session_state.user_id and not st.session_state.user_profile:
        st.subheader("Mandatory Onboarding")
        with st.form("onboarding_form"):
            education_level = st.selectbox("Current Education Level", ["Bachelor's", "Master's", "PhD"])
            degree = st.text_input("Degree / Major")
            grad_year = st.number_input("Expected Graduation Year", 2025, 2035, 2026)
            gpa = st.number_input("GPA (optional)", 0.0, 10.0, 7.5, 0.1)
            target_degree = st.selectbox("Intended Degree", ["Bachelor's", "Master's", "MBA", "PhD"])
            field = st.text_input("Field of Study", "Computer Science")
            intake_year = st.number_input("Target Intake Year", 2026, 2030, 2026)
            countries = st.multiselect("Preferred Countries", ["USA", "Canada", "UK", "Germany", "Australia", "Singapore"], default=["Canada", "Germany"])
            budget = st.slider("Annual Budget (USD)", 5000, 80000, 35000, 1000)
            funding = st.selectbox("Funding Plan", ["Self-funded", "Scholarship", "Loan"])
            ielts = st.selectbox("IELTS/TOEFL Status", ["Not started", "In progress", "Completed"])
            gre = st.selectbox("GRE/GMAT Status", ["Not started", "In progress", "Completed"])
            sop = st.selectbox("SOP Status", ["Not started", "Draft", "Ready"])

            if st.form_submit_button("Complete Onboarding"):
                profile = {
                    "education_level": education_level,
                    "degree": degree,
                    "grad_year": int(grad_year),
                    "gpa": float(gpa),
                    "target_degree": target_degree,
                    "field": field,
                    "intake_year": int(intake_year),
                    "countries": countries,
                    "budget": int(budget),
                    "funding": funding,
                    "ielts": ielts,
                    "gre": gre,
                    "sop": sop
                }
                st.session_state.user_profile = profile
                save_profile(st.session_state.user_id, profile)
                st.session_state.current_stage = 2
                st.success("Onboarding completed!")
                st.rerun()

elif st.session_state.current_stage == 2:
    st.subheader("Dashboard")
    profile = st.session_state.user_profile
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card fade-in">', unsafe_allow_html=True)
        st.metric("Profile Strength", "Strong" if profile.get("gpa", 0) >= 7.5 else "Average")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card fade-in">', unsafe_allow_html=True)
        st.metric("Budget", f"${profile.get('budget', 0):,}/year")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card fade-in">', unsafe_allow_html=True)
        st.metric("Locked Universities", len(st.session_state.locked))
        st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Go to AI Counsellor", type="primary"):
        st.session_state.current_stage = 3
        st.rerun()

elif st.session_state.current_stage == 3:
    st.markdown('<h2 class="fade-in">💬 Conversation with Saanvi</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748B;">Your warm & empathetic AI study-abroad counsellor</p>', unsafe_allow_html=True)

    for i, msg in enumerate(st.session_state.messages):
        avatar = "👤" if msg["role"] == "user" else "🧠"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                if st.button("🔊 Listen", key=f"tts_{i}"):
                    try:
                        tts = gTTS(text=msg["content"], lang="en", slow=False)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                            tts.write_to_fp(fp)
                            st.audio(fp.name, format="audio/mp3")
                    except Exception as e:
                        st.error(f"Audio failed: {e}")

    prompt = st.chat_input("Ask Saanvi anything...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("Saanvi is thinking..."):
                if client:
                    system = f"""You are Saanvi, a warm, empathetic study-abroad counsellor.
User profile: {json.dumps(st.session_state.user_profile)}
Stage: {stages[st.session_state.current_stage-1]}
Shortlisted: {len(st.session_state.shortlisted)}
Locked: {len(st.session_state.locked)}
Be supportive, clear, structured and encouraging."""
                    resp = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": system}] + st.session_state.messages[-10:],
                        temperature=0.7,
                        max_tokens=800
                    )
                    reply = resp.choices[0].message.content
                else:
                    reply = "I'm here to listen. Tell me more about your plans…"

                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

                # Voice button for latest reply
                if st.button("🔊 Hear Saanvi's reply", key="tts_latest"):
                    try:
                        tts = gTTS(text=reply, lang="en", slow=False)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                            tts.write_to_fp(fp)
                            st.audio(fp.name, format="audio/mp3")
                    except Exception as e:
                        st.error(f"Audio failed: {e}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Discover Universities"):
            st.session_state.current_stage = 4
            st.rerun()
    with col2:
        if st.button("View Application Tasks"):
            st.session_state.current_stage = 6
            st.rerun()

elif st.session_state.current_stage == 4:
    st.subheader("University Discovery")
    profile = st.session_state.user_profile
    budget = profile.get("budget", 40000)
    countries = profile.get("countries", [])
    filtered = [u for u in UNIVERSITIES if u["country"] in countries and u["annual_cost_usd"] <= budget * 1.2]
    for uni in filtered:
        with st.expander(f"⭐ {uni['name']} ({uni['country']}) – {uni['level']}"):
            st.write(f"**Annual Cost**: ${uni['annual_cost_usd']:,}")
            st.write(f"**Acceptance chance**: {uni['acceptance']}")
            st.write(f"**Risk level**: {uni['risk']}")
            if st.button("Shortlist this university", key=f"short_{uni['name']}"):
                save_shortlisted(st.session_state.user_id, uni)
                st.session_state.shortlisted = load_shortlisted(st.session_state.user_id)
                st.success(f"Added {uni['name']} to shortlist!")
    if st.button("Proceed to Locking", type="primary"):
        st.session_state.current_stage = 5
        st.rerun()

elif st.session_state.current_stage == 5:
    st.subheader("Lock Your Choices")
    st.info("You must lock at least one university to proceed to application guidance.")
    for uni_dict in st.session_state.shortlisted:
        uni = {"name": uni_dict["name"], "country": uni_dict["country"], "annual_cost_usd": uni_dict["annual_cost_usd"]}
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{uni['name']}** – ${uni['annual_cost_usd']:,}/year")
        with col2:
            if uni["name"] not in [l.get("name") for l in st.session_state.locked]:
                if st.button("Lock", key=f"lock_{uni['name']}"):
                    save_locked(st.session_state.user_id, uni)
                    st.session_state.locked = load_locked(st.session_state.user_id)
                    st.success(f"{uni['name']} locked!")
    if len(st.session_state.locked) >= 1 and st.button("Continue to Application Guidance", type="primary"):
        st.session_state.current_stage = 6
        st.rerun()

elif st.session_state.current_stage == 6:
    st.subheader("Application Guidance & Checklist")
    if not st.session_state.tasks:
        st.session_state.tasks = [
            {"task": "Complete IELTS / TOEFL", "done": False},
            {"task": "Draft Statement of Purpose (SOP)", "done": False},
            {"task": f"Gather documents for {st.session_state.locked[0]['name'] if st.session_state.locked else 'chosen university'}", "done": False},
            {"task": "Submit applications before deadline", "done": False}
        ]
        save_tasks(st.session_state.user_id, st.session_state.tasks)

    for i, task in enumerate(st.session_state.tasks):
        done = st.checkbox(task["task"], value=task["done"], key=f"task_{i}")
        if done != task["done"]:
            task["done"] = done
            save_tasks(st.session_state.user_id, st.session_state.tasks)

    if st.button("Finish Journey"):
        st.balloons()
        st.success("Congratulations! You're on track for a successful study abroad journey.")

st.caption("AI Counsellor • Professional Edition • PostgreSQL + Groq + Voice Output • Hackathon Ready")