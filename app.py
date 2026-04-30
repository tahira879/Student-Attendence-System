import streamlit as st
#import face_recognition
import numpy as np
import sqlite3
import os
import pandas as pd
from datetime import datetime
from PIL import Image
import json

# ──────────────────────────────────────────────
#  PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="FaceAttend Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
#  PREMIUM CSS  — all buttons styled dark
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg-deep:    #020b18;
    --bg-card:    #071428;
    --bg-card2:   #0d1e35;
    --border:     rgba(59,130,246,0.18);
    --blue:       #3b82f6;
    --blue-light: #60a5fa;
    --cyan:       #06b6d4;
    --green:      #10b981;
    --red:        #ef4444;
    --gold:       #f59e0b;
    --text:       #e2e8f0;
    --text-muted: #64748b;
    --glow:       rgba(59,130,246,0.35);
}

html, body, .stApp {
    background: var(--bg-deep) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 4rem 2rem !important; max-width: 1300px !important; }

/* ── hero ── */
.hero { text-align: center; padding: 3rem 1rem 2rem; }
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 5vw, 4rem);
    font-weight: 800; color: #fff;
    letter-spacing: -1px; margin: 0; line-height: 1.1;
}
.hero h1 span { color: var(--blue-light); }
.hero p { color: var(--text-muted); font-size: 1.05rem; margin: .8rem auto 0; max-width: 520px; }

/* ── cards ── */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px; padding: 2rem;
    transition: box-shadow .2s;
}
.card:hover { box-shadow: 0 0 30px rgba(59,130,246,.12); }

.dash-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px; padding: 1.8rem 1.5rem;
    transition: all .25s;
}
.dash-card:hover {
    border-color: var(--blue);
    box-shadow: 0 0 35px var(--glow);
    transform: translateY(-3px);
}
.dash-card .icon {
    width: 48px; height: 48px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem; margin-bottom: 1.2rem;
}
.dash-card h3 { font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:700; margin:0 0 .4rem; color:#fff; }
.dash-card p  { font-size:.85rem; color:var(--text-muted); margin:0 0 1rem; line-height:1.5; }

/* ── section titles ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem; font-weight: 800;
    color: var(--blue-light); margin: 0 0 .3rem;
}
.section-sub { color: var(--text-muted); font-size: .9rem; margin-bottom: 2rem; }

/* ── stat pill ── */
.stat-row { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:1.5rem; }
.stat-pill {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 50px; padding: 8px 18px;
    font-size: .82rem; color: var(--text-muted);
}
.stat-pill b { color: var(--blue-light); }

/* ── badges ── */
.badge-present {
    background:rgba(16,185,129,.15); color:var(--green);
    border:1px solid rgba(16,185,129,.4);
    padding:4px 14px; border-radius:50px;
    font-size:.8rem; font-weight:700; letter-spacing:.5px;
}
.badge-absent {
    background:rgba(239,68,68,.15); color:var(--red);
    border:1px solid rgba(239,68,68,.4);
    padding:4px 14px; border-radius:50px;
    font-size:.8rem; font-weight:700; letter-spacing:.5px;
}

/* ── table ── */
.att-table { width:100%; border-collapse:collapse; }
.att-table th {
    color:var(--text-muted); font-size:.78rem;
    letter-spacing:1px; text-transform:uppercase;
    padding:10px 14px; border-bottom:1px solid var(--border);
    text-align:left; font-family:'Syne',sans-serif;
}
.att-table td {
    padding:13px 14px;
    border-bottom:1px solid rgba(59,130,246,.07);
    font-size:.88rem; color:var(--text); vertical-align:middle;
}
.att-table tr:hover td { background:rgba(59,130,246,.04); }
.avatar-circle {
    display:inline-flex; width:32px; height:32px;
    background:var(--blue); border-radius:50%;
    align-items:center; justify-content:center;
    font-family:'Syne',sans-serif; font-weight:700;
    font-size:.85rem; color:#fff;
    margin-right:10px; vertical-align:middle;
}

/* ── message boxes ── */
.msg-success {
    background:rgba(16,185,129,.12); border:1px solid rgba(16,185,129,.35);
    color:var(--green); padding:14px 18px; border-radius:12px;
    font-weight:600; margin-bottom:1rem;
}
.msg-error {
    background:rgba(239,68,68,.12); border:1px solid rgba(239,68,68,.35);
    color:var(--red); padding:14px 18px; border-radius:12px;
    font-weight:600; margin-bottom:1rem;
}
.msg-info {
    background:rgba(59,130,246,.1); border:1px solid rgba(59,130,246,.3);
    color:var(--blue-light); padding:14px 18px; border-radius:12px;
    margin-bottom:1rem;
}
.msg-warn {
    background:rgba(245,158,11,.1); border:1px solid rgba(245,158,11,.3);
    color:var(--gold); padding:14px 18px; border-radius:12px;
    margin-bottom:1rem;
}

/* ════════════════════════════════
   BUTTON OVERRIDES — ALL DARK
   ════════════════════════════════ */

/* Base reset — kill Streamlit's white default */
.stButton > button {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: .88rem !important;
    padding: 10px 22px !important;
    transition: all .2s !important;
    width: 100%;
}
.stButton > button:hover {
    border-color: var(--blue) !important;
    color: #fff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 0 18px var(--glow) !important;
}
.stButton > button:focus {
    box-shadow: 0 0 0 2px var(--blue) !important;
    outline: none !important;
}

/* PRIMARY blue button */
.stButton > button[kind="primary"] {
    background: var(--blue) !important;
    border: none !important;
    color: #fff !important;
    box-shadow: 0 0 18px var(--glow) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #2563eb !important;
    box-shadow: 0 0 28px var(--glow) !important;
}

/* DANGER button wrapper */
.danger-btn .stButton > button {
    background: rgba(239,68,68,.12) !important;
    border: 1px solid rgba(239,68,68,.4) !important;
    color: var(--red) !important;
}
.danger-btn .stButton > button:hover {
    background: rgba(239,68,68,.22) !important;
    border-color: var(--red) !important;
    box-shadow: 0 0 18px rgba(239,68,68,.3) !important;
}

/* Nav buttons */
.nav-btn-wrap .stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text-muted) !important;
    border-radius: 10px !important;
}
.nav-btn-wrap.active .stButton > button {
    background: var(--blue) !important;
    border-color: var(--blue) !important;
    color: #fff !important;
    box-shadow: 0 0 18px var(--glow) !important;
}

/* Download button */
.stDownloadButton > button {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}
.stDownloadButton > button:hover {
    border-color: var(--blue) !important;
    color: #fff !important;
}

/* Input fields */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stDateInput input {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}
.stSelectbox > div > div > div { color: var(--text) !important; }

div[data-testid="stCameraInput"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}

.hdiv { border:none; border-top:1px solid var(--border); margin:1.5rem 0; }
.cam-label {
    font-family:'Syne',sans-serif; font-size:.78rem; font-weight:600;
    color:var(--text-muted); letter-spacing:1px;
    text-transform:uppercase; margin-bottom:.4rem;
}

/* Tips box */
.tips-box {
    background: var(--bg-card2);
    border: 1px solid rgba(245,158,11,.25);
    border-radius: 14px; padding: 1.2rem 1.4rem;
    margin-top: 1rem;
}
.tips-box h4 { font-family:'Syne',sans-serif; font-size:.85rem; color:var(--gold); margin:0 0 .6rem; }
.tips-box ul { margin:0; padding-left:1.2rem; color:var(--text-muted); font-size:.83rem; line-height:1.8; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  DATABASE LAYER  (SQLite)
# ──────────────────────────────────────────────
DB_FILE = "faceattend.db"

def get_conn():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll        TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            dept        TEXT DEFAULT '',
            encoding    TEXT NOT NULL,
            registered_at TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            roll    TEXT NOT NULL,
            name    TEXT NOT NULL,
            dept    TEXT DEFAULT '',
            date    TEXT NOT NULL,
            time    TEXT NOT NULL,
            day     TEXT NOT NULL,
            status  TEXT DEFAULT 'PRESENT',
            UNIQUE(roll, date)
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ── DB helpers ──
def db_get_students() -> dict:
    conn = get_conn()
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return {r["roll"]: {
        "name": r["name"], "roll": r["roll"], "dept": r["dept"],
        "encoding": json.loads(r["encoding"]),
        "registered_at": r["registered_at"]
    } for r in rows}

def db_add_student(roll, name, dept, encoding, registered_at):
    conn = get_conn()
    conn.execute(
        "INSERT INTO students (roll,name,dept,encoding,registered_at) VALUES (?,?,?,?,?)",
        (roll, name, dept, json.dumps(encoding), registered_at)
    )
    conn.commit(); conn.close()

def db_delete_student(roll):
    conn = get_conn()
    conn.execute("DELETE FROM students WHERE roll=?", (roll,))
    conn.commit(); conn.close()

def db_get_attendance() -> list:
    conn = get_conn()
    rows = conn.execute("SELECT * FROM attendance ORDER BY date DESC, time DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def db_mark_attendance(roll, name, dept, date, time_s, day):
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO attendance (roll,name,dept,date,time,day,status) VALUES (?,?,?,?,?,?,'PRESENT')",
            (roll, name, dept, date, time_s, day)
        )
        conn.commit()
        result = True
    except sqlite3.IntegrityError:
        result = False   # already marked today
    conn.close()
    return result

def db_clear_attendance():
    conn = get_conn()
    conn.execute("DELETE FROM attendance")
    conn.commit(); conn.close()

def db_delete_student_attendance(roll):
    conn = get_conn()
    conn.execute("DELETE FROM attendance WHERE roll=?", (roll,))
    conn.commit(); conn.close()

def db_already_marked(roll, date) -> bool:
    conn = get_conn()
    row = conn.execute(
        "SELECT 1 FROM attendance WHERE roll=? AND date=?", (roll, date)
    ).fetchone()
    conn.close()
    return row is not None

# ──────────────────────────────────────────────
#  FACE HELPERS
# ──────────────────────────────────────────────
def pil_to_np(img: Image.Image) -> np.ndarray:
    return np.array(img.convert("RGB"))

def encode_face(img_np: np.ndarray):
    """
    Returns (encoding, n_faces_found)
    Uses model='hog' for speed; upgrade to 'cnn' if GPU available.
    """
    locs = face_recognition.face_locations(img_np, model="hog")
    if not locs:
        return None, 0
    encs = face_recognition.face_encodings(img_np, known_face_locations=locs)
    return (encs[0] if encs else None), len(locs)

# ──────────────────────────────────────────────
#  SESSION STATE
# ──────────────────────────────────────────────
for key, default in [("page","dashboard"),("reg_msg",None),("att_msg",None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ──────────────────────────────────────────────
#  HERO
# ──────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>Face<span>Attend</span> Pro</h1>
  <p>Biometric attendance system — powered by SQLite, fast & persistent.</p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  NAV
# ──────────────────────────────────────────────
pages = {
    "dashboard":  ("🏠", "Dashboard"),
    "register":   ("📸", "Register"),
    "attendance": ("✅", "Attendance"),
    "records":    ("📋", "Records"),
}

nav_cols = st.columns(len(pages))
for i, (key, (icon, label)) in enumerate(pages.items()):
    active = "active" if st.session_state.page == key else ""
    with nav_cols[i]:
        st.markdown(f"<div class='nav-btn-wrap {active}'>", unsafe_allow_html=True)
        if st.button(f"{icon} {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.session_state.reg_msg = None
            st.session_state.att_msg = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr class='hdiv'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════
if st.session_state.page == "dashboard":
    students   = db_get_students()
    attendance = db_get_attendance()
    today_str  = datetime.now().strftime("%Y-%m-%d")
    today_recs = [r for r in attendance if r["date"] == today_str]

    st.markdown("""
    <div class="section-title">Dashboard</div>
    <div class="section-sub">Overview of your attendance system</div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-pill">👤 Registered: <b>{len(students)}</b></div>
        <div class="stat-pill">✅ Present Today: <b>{len(today_recs)}</b></div>
        <div class="stat-pill">📊 Total Logs: <b>{len(attendance)}</b></div>
        <div class="stat-pill">📆 <b>{datetime.now().strftime('%A, %d %b %Y')}</b></div>
        <div class="stat-pill">🗄️ Database: <b>SQLite</b></div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="dash-card">
          <div class="icon" style="background:rgba(59,130,246,.15);color:#3b82f6;">📸</div>
          <h3>Register Face</h3>
          <p>Enlist new students by capturing their unique facial features and roll number.</p>
        </div><br>""", unsafe_allow_html=True)
        if st.button("Open Registration", key="dash_reg", use_container_width=True, type="primary"):
            st.session_state.page = "register"; st.rerun()

    with c2:
        st.markdown("""
        <div class="dash-card">
          <div class="icon" style="background:rgba(6,182,212,.15);color:#06b6d4;">✅</div>
          <h3>Take Attendance</h3>
          <p>Mark daily attendance instantly using face recognition — no manual entry needed.</p>
        </div><br>""", unsafe_allow_html=True)
        if st.button("Mark Attendance", key="dash_att", use_container_width=True, type="primary"):
            st.session_state.page = "attendance"; st.rerun()

    with c3:
        st.markdown("""
        <div class="dash-card">
          <div class="icon" style="background:rgba(16,185,129,.15);color:#10b981;">📋</div>
          <h3>View Records</h3>
          <p>Track and export attendance history with detailed logs, filters, and CSV export.</p>
        </div><br>""", unsafe_allow_html=True)
        if st.button("View Records", key="dash_rec", use_container_width=True, type="primary"):
            st.session_state.page = "records"; st.rerun()

    if today_recs:
        st.markdown("<hr class='hdiv'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title' style='font-size:1.2rem'>Today's Attendance Snapshot</div>", unsafe_allow_html=True)
        df = pd.DataFrame(today_recs)[["name","roll","time","day","status"]]
        st.dataframe(df, use_container_width=True)


# ══════════════════════════════════════════════
#  REGISTER
# ══════════════════════════════════════════════
elif st.session_state.page == "register":
    st.markdown("""
    <div class="section-title">Register Face</div>
    <div class="section-sub">Capture a clear photo to enroll in the system.</div>
    """, unsafe_allow_html=True)

    students = db_get_students()
    col_cam, col_form = st.columns([1.2, 1])

    with col_cam:
        st.markdown("<div class='cam-label'>📷 Live Camera</div>", unsafe_allow_html=True)
        img_file = st.camera_input("", key="reg_cam", label_visibility="collapsed")

        # Photo tips
        st.markdown("""
        <div class="tips-box">
            <h4>📸 Tips for Best Results</h4>
            <ul>
                <li>Face the camera <b>directly</b></li>
                <li>Ensure <b>good, even lighting</b> — no backlighting</li>
                <li>Keep your face <b>centered</b> in the frame</li>
                <li>Remove glasses or hats if possible</li>
                <li>Take the photo in a <b>bright room</b></li>
                <li>Only <b>one face</b> should be in frame</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        st.markdown("#### Student Details")
        name = st.text_input("Full Name")
        roll = st.text_input("Roll Number *(required)*")
        dept = st.text_input("Department (optional)")

        if st.session_state.reg_msg:
            kind, text = st.session_state.reg_msg
            css = "msg-success" if kind == "ok" else "msg-error"
            st.markdown(f"<div class='{css}'>{text}</div>", unsafe_allow_html=True)

        if st.button("📸 Register Now", type="primary", use_container_width=True):
            if not name.strip():
                st.session_state.reg_msg = ("err", "⚠️ Please enter the student's full name.")
                st.rerun()
            elif not roll.strip():
                st.session_state.reg_msg = ("err", "⚠️ Roll Number is required.")
                st.rerun()
            elif roll.strip() in students:
                st.session_state.reg_msg = ("err", f"⚠️ Roll {roll.strip()} is already registered.")
                st.rerun()
            elif img_file is None:
                st.session_state.reg_msg = ("err", "⚠️ Please capture a photo first.")
                st.rerun()
            else:
                with st.spinner("Detecting face and encoding…"):
                    img    = Image.open(img_file)
                    img_np = pil_to_np(img)
                    enc, n_faces = encode_face(img_np)

                if n_faces == 0:
                    st.session_state.reg_msg = ("err",
                        "❌ No face detected. Try: better lighting, face camera directly, remove glasses.")
                elif n_faces > 1:
                    st.session_state.reg_msg = ("err",
                        f"⚠️ {n_faces} faces detected. Only ONE person should be in frame.")
                elif enc is None:
                    st.session_state.reg_msg = ("err", "❌ Face encoding failed. Please retake the photo.")
                else:
                    reg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    db_add_student(roll.strip(), name.strip(), dept.strip(), enc.tolist(), reg_time)
                    st.session_state.reg_msg = ("ok",
                        f"✅ {name.strip()} (Roll: {roll.strip()}) registered successfully!")
                    st.rerun()

    # Registered list
    students = db_get_students()
    if students:
        st.markdown("<hr class='hdiv'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-title' style='font-size:1.2rem'>Registered Students ({len(students)})</div>", unsafe_allow_html=True)

        table_html = """
        <div class='card' style='padding:0;overflow:hidden;'>
        <table class='att-table'>
          <thead><tr>
            <th>Student</th><th>Roll No.</th><th>Department</th><th>Registered At</th>
          </tr></thead><tbody>
        """
        for r_id, s in students.items():
            initial = s["name"][0].upper()
            table_html += f"""
            <tr>
              <td><span class='avatar-circle'>{initial}</span>{s['name']}</td>
              <td>{s['roll']}</td>
              <td>{s.get('dept','—') or '—'}</td>
              <td>{s.get('registered_at','—')}</td>
            </tr>"""
        table_html += "</tbody></table></div>"
        st.markdown(table_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("🗑️ Delete a Student"):
            roll_options = {f"{s['name']} (Roll: {s['roll']})": r for r, s in students.items()}
            selected = st.selectbox("Select student to delete", list(roll_options.keys()))
            st.markdown("<div class='danger-btn'>", unsafe_allow_html=True)
            if st.button("Delete Student", use_container_width=True, key="del_stu"):
                rid = roll_options[selected]
                db_delete_student(rid)
                st.success(f"Deleted {selected}")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAKE ATTENDANCE
# ══════════════════════════════════════════════
elif st.session_state.page == "attendance":
    st.markdown("""
    <div class="section-title">Take Attendance</div>
    <div class="section-sub">Position your face clearly in the frame for instant recognition.</div>
    """, unsafe_allow_html=True)

    students = db_get_students()

    if not students:
        st.markdown("<div class='msg-info'>⚠️ No students registered yet. Please register students first.</div>", unsafe_allow_html=True)
    else:
        col_cam2, col_status = st.columns([1.2, 1])

        with col_cam2:
            st.markdown("<div class='cam-label'>📷 Face Recognition Camera</div>", unsafe_allow_html=True)
            att_img = st.camera_input("", key="att_cam", label_visibility="collapsed")

            st.markdown("""
            <div class="tips-box">
                <h4>📸 Recognition Tips</h4>
                <ul>
                    <li>Same lighting as registration gives <b>best results</b></li>
                    <li>Face camera <b>directly</b>, don't tilt head</li>
                    <li>Stay <b>still</b> for a moment before clicking</li>
                    <li>Keep face <b>centered</b> in frame</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col_status:
            st.markdown("#### 📡 Status Feed")

            if st.session_state.att_msg:
                kind, text = st.session_state.att_msg
                css_map = {"ok": "msg-success", "err": "msg-error", "info": "msg-info", "warn": "msg-warn"}
                css = css_map.get(kind, "msg-info")
                st.markdown(f"<div class='{css}'>{text}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='msg-info'>📷 Ready to scan. Capture photo then click Mark Attendance.</div>", unsafe_allow_html=True)

            if st.button("✅ Mark My Attendance", type="primary", use_container_width=True):
                if att_img is None:
                    st.session_state.att_msg = ("err", "⚠️ Please capture a photo first.")
                    st.rerun()
                else:
                    with st.spinner("Scanning face…"):
                        img    = Image.open(att_img)
                        img_np = pil_to_np(img)
                        enc, n_faces = encode_face(img_np)

                    if n_faces == 0:
                        st.session_state.att_msg = ("err",
                            "❌ No face detected. Improve lighting and face camera directly.")
                        st.rerun()
                    elif n_faces > 1:
                        st.session_state.att_msg = ("err",
                            f"⚠️ {n_faces} faces detected. Only one person at a time please.")
                        st.rerun()
                    elif enc is None:
                        st.session_state.att_msg = ("err", "❌ Face encoding failed. Retake photo.")
                        st.rerun()
                    else:
                        known_encs  = [np.array(s["encoding"]) for s in students.values()]
                        known_rolls = list(students.keys())

                        distances = face_recognition.face_distance(known_encs, enc)
                        best_idx  = int(np.argmin(distances))
                        best_dist = float(distances[best_idx])

                        # Confidence score (0–100%)
                        confidence = max(0, round((1 - best_dist) * 100, 1))
                        THRESHOLD  = 0.52   # lower = stricter

                        if best_dist > THRESHOLD:
                            st.session_state.att_msg = ("err",
                                f"❌ Face not recognised (confidence: {confidence}%). Are you registered?")
                            st.rerun()
                        else:
                            matched_roll = known_rolls[best_idx]
                            matched_name = students[matched_roll]["name"]
                            matched_dept = students[matched_roll].get("dept","")

                            now      = datetime.now()
                            date_str = now.strftime("%Y-%m-%d")
                            time_str = now.strftime("%I:%M %p")
                            day_str  = now.strftime("%A")

                            marked = db_mark_attendance(
                                matched_roll, matched_name, matched_dept,
                                date_str, time_str, day_str
                            )

                            if not marked:
                                st.session_state.att_msg = ("info",
                                    f"ℹ️ {matched_name} — attendance already marked today.")
                            else:
                                st.session_state.att_msg = ("ok",
                                    f"✅ **{matched_name}** (Roll: {matched_roll}) marked PRESENT at {time_str} — {day_str}. Confidence: {confidence}%")
                            st.rerun()

        # Today's attendance table
        attendance = db_get_attendance()
        today_str  = datetime.now().strftime("%Y-%m-%d")
        today_recs = [r for r in attendance if r["date"] == today_str]
        present_rolls = {r["roll"] for r in today_recs}

        st.markdown("<hr class='hdiv'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-title' style='font-size:1.2rem'>Today — {datetime.now().strftime('%A, %d %B %Y')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-row'><div class='stat-pill'>✅ Present: <b>{len(present_rolls)}</b></div><div class='stat-pill'>❌ Absent: <b>{len(students)-len(present_rolls)}</b></div></div>", unsafe_allow_html=True)

        table_html = """
        <div class='card' style='padding:0;overflow:hidden;'>
        <table class='att-table'>
          <thead><tr>
            <th>Student</th><th>Roll No.</th><th>Date</th><th>Day</th><th>Time</th><th>Status</th>
          </tr></thead><tbody>
        """
        for roll_id, s in students.items():
            initial = s["name"][0].upper()
            if roll_id in present_rolls:
                rec   = next(r for r in today_recs if r["roll"] == roll_id)
                badge = "<span class='badge-present'>PRESENT</span>"
                t_td  = rec["time"]; d_td = rec["day"]; dt_td = rec["date"]
            else:
                badge = "<span class='badge-absent'>ABSENT</span>"
                t_td  = "—"; d_td = datetime.now().strftime("%A"); dt_td = today_str

            table_html += f"""
            <tr>
              <td><span class='avatar-circle'>{initial}</span>{s['name']}</td>
              <td>{s['roll']}</td><td>{dt_td}</td><td>{d_td}</td><td>{t_td}</td>
              <td>{badge}</td>
            </tr>"""
        table_html += "</tbody></table></div>"
        st.markdown(table_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  RECORDS
# ══════════════════════════════════════════════
elif st.session_state.page == "records":
    st.markdown("""
    <div class="section-title">Attendance Records</div>
    <div class="section-sub">Full history stored in SQLite database.</div>
    """, unsafe_allow_html=True)

    attendance = db_get_attendance()

    col_filters, col_table = st.columns([1, 3])

    with col_filters:
        st.markdown("#### 🔍 Filters")
        search_q    = st.text_input("Name or Roll", placeholder="Search…")
        date_filter = st.date_input("Filter by Date", value=None)

        filtered = attendance.copy()
        if search_q:
            q = search_q.lower()
            filtered = [r for r in filtered if q in r["name"].lower() or q in r["roll"].lower()]
        if date_filter:
            filtered = [r for r in filtered if r["date"] == str(date_filter)]

        st.markdown(f"<br><div class='stat-pill'>Total Logs: <b>{len(attendance)}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-pill'>Showing: <b>{len(filtered)}</b></div>", unsafe_allow_html=True)

    with col_table:
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if attendance:
                df = pd.DataFrame(attendance)
                csv_bytes = df.to_csv(index=False).encode()
                st.download_button(
                    "⬇️ Export CSV",
                    data=csv_bytes,
                    file_name=f"attendance_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
        with btn_c2:
            st.markdown("<div class='danger-btn'>", unsafe_allow_html=True)
            if st.button("🗑️ Clear All Records", use_container_width=True, key="clear_all"):
                db_clear_attendance()
                st.success("All attendance records cleared.")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        if not filtered:
            st.markdown("<div class='msg-info'>No records found matching your filters.</div>", unsafe_allow_html=True)
        else:
            table_html = """
            <div class='card' style='padding:0;overflow:hidden;margin-top:1rem;'>
            <table class='att-table'>
              <thead><tr>
                <th>Student</th><th>Roll No.</th><th>Department</th>
                <th>Date</th><th>Day</th><th>Time</th><th>Status</th>
              </tr></thead><tbody>
            """
            for rec in filtered:
                initial = rec["name"][0].upper()
                badge   = "<span class='badge-present'>PRESENT</span>" if rec["status"]=="PRESENT" else "<span class='badge-absent'>ABSENT</span>"
                dept    = rec.get("dept","—") or "—"
                table_html += f"""
                <tr>
                  <td><span class='avatar-circle'>{initial}</span>{rec['name']}</td>
                  <td>{rec['roll']}</td><td>{dept}</td>
                  <td>{rec['date']}</td><td>{rec.get('day','—')}</td>
                  <td>{rec['time']}</td><td>{badge}</td>
                </tr>"""
            table_html += "</tbody></table></div>"
            st.markdown(table_html, unsafe_allow_html=True)

        if attendance:
            st.markdown("<hr class='hdiv'>", unsafe_allow_html=True)
            with st.expander("🗑️ Delete Records for a Specific Student"):
                student_names = list({f"{r['name']} (Roll: {r['roll']})" for r in attendance})
                del_target = st.selectbox("Select Student", student_names)
                st.markdown("<div class='danger-btn'>", unsafe_allow_html=True)
                if st.button("Delete Their Records", use_container_width=True, key="del_rec"):
                    roll_to_del = del_target.split("Roll: ")[-1].rstrip(")")
                    db_delete_student_attendance(roll_to_del)
                    st.success(f"Records deleted for {del_target}")
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
