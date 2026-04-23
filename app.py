import streamlit as st
import cv2
import face_recognition
import numpy as np
import json
import os
import pandas as pd
from datetime import datetime
from PIL import Image
import io

st.set_page_config(page_title="FaceAttend Pro", page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
:root {
    --bg-deep:#020b18; --bg-card:#071428; --bg-card2:#0d1e35;
    --border:rgba(59,130,246,0.25); --blue:#3b82f6; --blue-light:#60a5fa;
    --cyan:#06b6d4; --green:#10b981; --red:#ef4444;
    --text:#e2e8f0; --text-muted:#64748b;
    --neon-glow:0 0 20px rgba(59,130,246,0.55),0 0 45px rgba(59,130,246,0.2);
}
html,body,.stApp { background:var(--bg-deep) !important; font-family:'DM Sans',sans-serif; color:var(--text); }
#MainMenu,footer,header { visibility:hidden; }
.block-container { padding:0 2rem 4rem !important; max-width:1300px !important; }

/* ===== ALL BUTTONS — dark with neon border ===== */
.stButton > button {
    background: rgba(13,30,53,0.9) !important;
    border: 1.5px solid rgba(59,130,246,0.45) !important;
    border-radius: 12px !important;
    color: var(--blue-light) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: .88rem !important;
    padding: 10px 20px !important;
    transition: all .22s ease !important;
    box-shadow: 0 0 10px rgba(59,130,246,0.1) !important;
    width: 100% !important;
    letter-spacing:.3px !important;
}
.stButton > button:hover {
    background: rgba(59,130,246,0.15) !important;
    border-color: var(--blue) !important;
    color: #fff !important;
    box-shadow: var(--neon-glow) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active { transform:translateY(0) !important; }

/* primary filled blue */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg,#1d4ed8,#3b82f6) !important;
    border: none !important;
    color: #fff !important;
    box-shadow: var(--neon-glow) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg,#1e40af,#2563eb) !important;
    box-shadow: 0 0 35px rgba(59,130,246,0.8) !important;
}

/* nav active */
.nav-active .stButton > button {
    background: linear-gradient(135deg,#1d4ed8,#3b82f6) !important;
    border-color: transparent !important;
    color: #fff !important;
    box-shadow: var(--neon-glow) !important;
}

/* danger */
.danger-btn .stButton > button {
    background: rgba(239,68,68,0.08) !important;
    border: 1.5px solid rgba(239,68,68,0.4) !important;
    color: #ef4444 !important;
    box-shadow: none !important;
}
.danger-btn .stButton > button:hover {
    background: rgba(239,68,68,0.18) !important;
    border-color: #ef4444 !important;
    color: #fff !important;
    box-shadow: 0 0 20px rgba(239,68,68,0.45) !important;
}

/* download button */
.stDownloadButton > button {
    background: linear-gradient(135deg,#1d4ed8,#3b82f6) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-family: 'Syne',sans-serif !important;
    font-weight:600 !important;
    padding:10px 20px !important;
    box-shadow: var(--neon-glow) !important;
    width:100% !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg,#1e40af,#2563eb) !important;
    box-shadow: 0 0 35px rgba(59,130,246,0.8) !important;
    transform:translateY(-2px) !important;
}

/* ===== HERO ===== */
.hero { text-align:center; padding:2.5rem 1rem 1.5rem; }
.hero h1 {
    font-family:'Syne',sans-serif; font-size:clamp(2rem,5vw,3.6rem);
    font-weight:800; color:#fff; letter-spacing:-1px; margin:0; line-height:1.1;
}
.hero h1 span {
    background:linear-gradient(90deg,#60a5fa,#06b6d4);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.hero p { color:var(--text-muted); font-size:.98rem; margin:.7rem auto 0; max-width:460px; }

/* ===== CARDS ===== */
.card {
    background:var(--bg-card); border:1px solid var(--border);
    border-radius:20px; padding:1.8rem; transition:box-shadow .2s;
}
.card:hover { box-shadow:0 0 25px rgba(59,130,246,.1); }
.dash-card {
    background:var(--bg-card); border:1.5px solid var(--border);
    border-radius:20px; padding:1.8rem 1.5rem 1.2rem;
    transition:all .25s; margin-bottom:.5rem; min-height:175px;
}
.dash-card:hover { border-color:var(--blue); box-shadow:var(--neon-glow); transform:translateY(-3px); }
.dash-card .icon {
    width:46px; height:46px; border-radius:13px;
    display:inline-flex; align-items:center; justify-content:center;
    font-size:1.3rem; margin-bottom:1rem;
}
.dash-card h3 { font-family:'Syne',sans-serif; font-size:1.05rem; font-weight:700; margin:0 0 .4rem; color:#fff; }
.dash-card p  { font-size:.83rem; color:var(--text-muted); margin:0; line-height:1.5; }

/* ===== SECTION TITLES ===== */
.section-title {
    font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800;
    background:linear-gradient(90deg,#60a5fa,#06b6d4);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0 0 .25rem;
}
.section-sub { color:var(--text-muted); font-size:.88rem; margin-bottom:1.8rem; }

/* ===== STAT PILLS ===== */
.stat-row { display:flex; gap:10px; flex-wrap:wrap; margin-bottom:1.5rem; }
.stat-pill {
    background:var(--bg-card2); border:1px solid var(--border);
    border-radius:50px; padding:7px 16px; font-size:.8rem; color:var(--text-muted);
}
.stat-pill b { color:var(--blue-light); }

/* ===== BADGES ===== */
.badge-present {
    background:rgba(16,185,129,.15); color:#10b981;
    border:1px solid rgba(16,185,129,.4); padding:4px 14px;
    border-radius:50px; font-size:.78rem; font-weight:700; letter-spacing:.5px;
}
.badge-absent {
    background:rgba(239,68,68,.15); color:#ef4444;
    border:1px solid rgba(239,68,68,.4); padding:4px 14px;
    border-radius:50px; font-size:.78rem; font-weight:700; letter-spacing:.5px;
}

/* ===== TABLE ===== */
.att-table { width:100%; border-collapse:collapse; }
.att-table th {
    color:var(--text-muted); font-size:.74rem; letter-spacing:1px;
    text-transform:uppercase; padding:10px 14px; border-bottom:1px solid var(--border);
    text-align:left; font-family:'Syne',sans-serif;
}
.att-table td {
    padding:12px 14px; border-bottom:1px solid rgba(59,130,246,.06);
    font-size:.86rem; color:var(--text); vertical-align:middle;
}
.att-table tr:hover td { background:rgba(59,130,246,.04); }
.av {
    display:inline-flex; width:30px; height:30px;
    background:linear-gradient(135deg,#2563eb,#06b6d4); border-radius:50%;
    align-items:center; justify-content:center;
    font-family:'Syne',sans-serif; font-weight:700; font-size:.82rem;
    color:#fff; margin-right:9px; vertical-align:middle;
}

/* ===== MESSAGES ===== */
.msg-ok  { background:rgba(16,185,129,.1); border:1px solid rgba(16,185,129,.4); color:#10b981; padding:13px 16px; border-radius:12px; font-weight:600; margin-bottom:1rem; font-size:.9rem; }
.msg-err { background:rgba(239,68,68,.1); border:1px solid rgba(239,68,68,.4); color:#ef4444; padding:13px 16px; border-radius:12px; font-weight:600; margin-bottom:1rem; font-size:.9rem; }
.msg-inf { background:rgba(59,130,246,.08); border:1px solid rgba(59,130,246,.3); color:var(--blue-light); padding:13px 16px; border-radius:12px; margin-bottom:1rem; font-size:.9rem; }

/* ===== INPUTS ===== */
.stTextInput > div > div > input {
    background:var(--bg-card2) !important; border:1.5px solid var(--border) !important;
    border-radius:10px !important; color:var(--text) !important;
}
.stTextInput > div > div > input:focus { border-color:var(--blue) !important; box-shadow:0 0 0 2px rgba(59,130,246,.2) !important; }
.stSelectbox > div > div { background:var(--bg-card2) !important; border:1.5px solid var(--border) !important; border-radius:10px !important; color:var(--text) !important; }
.stDateInput input { background:var(--bg-card2) !important; border:1.5px solid var(--border) !important; color:var(--text) !important; border-radius:10px !important; }
div[data-testid="stCameraInput"] { background:var(--bg-card) !important; border:1.5px solid var(--border) !important; border-radius:16px !important; }
div[data-testid="stCameraInput"]:hover { border-color:var(--blue) !important; box-shadow:var(--neon-glow) !important; }

.hdiv { border:none; border-top:1px solid var(--border); margin:1.5rem 0; }
.cam-label { font-family:'Syne',sans-serif; font-size:.74rem; font-weight:600; color:var(--text-muted); letter-spacing:1px; text-transform:uppercase; margin-bottom:.5rem; }
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:var(--bg-deep); }
::-webkit-scrollbar-thumb { background:rgba(59,130,246,.3); border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ── DATA ──
STUDENTS_FILE   = "students.json"
ATTENDANCE_FILE = "attendance.json"

def load_students():
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE) as f: return json.load(f)
    return {}

def save_students(d):
    with open(STUDENTS_FILE,"w") as f: json.dump(d,f,indent=2)

def load_attendance():
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE) as f: return json.load(f)
    return []

def save_attendance(d):
    with open(ATTENDANCE_FILE,"w") as f: json.dump(d,f,indent=2)

# ── SESSION ──
for k,v in [("page","dashboard"),("reg_msg",None),("att_msg",None)]:
    if k not in st.session_state: st.session_state[k]=v

# ── FACE HELPERS ──
def pil_to_np(img):
    arr = np.array(img.convert("RGB"))
    h,w = arr.shape[:2]
    if w < 640:
        scale = 640/w
        arr = cv2.resize(arr,(int(w*scale),int(h*scale)),interpolation=cv2.INTER_CUBIC)
    return arr

def encode_face(img_np):
    # Try normal first
    encs = face_recognition.face_encodings(img_np, num_jitters=3, model="small")
    if encs: return encs[0]
    # Upsample for small/blurry faces
    locs = face_recognition.face_locations(img_np, model="hog", number_of_times_to_upsample=2)
    if locs:
        encs = face_recognition.face_encodings(img_np, known_face_locations=locs, num_jitters=3)
        if encs: return encs[0]
    return None

def enc_to_list(e): return e.tolist()
def list_to_enc(l): return np.array(l)

# ── HERO ──
st.markdown("""
<div class="hero">
  <h1>Face<span>Attend</span> Pro</h1>
  <p>Premium biometric attendance — offline, fast &amp; persistent.</p>
</div>""", unsafe_allow_html=True)

# ── NAV ──
pages = {"dashboard":("🏠","Dashboard"),"register":("📸","Register"),
         "attendance":("✅","Attendance"),"records":("📋","Records")}
ncols = st.columns(4)
for i,(key,(icon,label)) in enumerate(pages.items()):
    with ncols[i]:
        active = st.session_state.page == key
        if active: st.markdown("<div class='nav-active'>",unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.page=key; st.session_state.reg_msg=None; st.session_state.att_msg=None; st.rerun()
        if active: st.markdown("</div>",unsafe_allow_html=True)

st.markdown("<hr class='hdiv'>",unsafe_allow_html=True)

# ══════════════════════════
#  DASHBOARD
# ══════════════════════════
if st.session_state.page=="dashboard":
    students=load_students(); att=load_attendance()
    today=datetime.now().strftime("%Y-%m-%d")
    today_recs=[r for r in att if r["date"]==today]
    st.markdown('<div class="section-title">Dashboard</div><div class="section-sub">Overview of your attendance system</div>',unsafe_allow_html=True)
    st.markdown(f"""<div class="stat-row">
        <div class="stat-pill">👤 Registered: <b>{len(students)}</b></div>
        <div class="stat-pill">✅ Present Today: <b style='color:#10b981'>{len(today_recs)}</b></div>
        <div class="stat-pill">❌ Absent Today: <b style='color:#ef4444'>{len(students)-len(today_recs)}</b></div>
        <div class="stat-pill">📊 Total Logs: <b>{len(att)}</b></div>
        <div class="stat-pill">📆 <b>{datetime.now().strftime('%A, %d %B %Y')}</b></div>
    </div>""",unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown('<div class="dash-card"><div class="icon" style="background:rgba(59,130,246,.15);color:#3b82f6;">📸</div><h3>Register Face</h3><p>Add new students with face capture and roll number.</p></div>',unsafe_allow_html=True)
        if st.button("Open Registration →",key="dr"): st.session_state.page="register"; st.rerun()
    with c2:
        st.markdown('<div class="dash-card"><div class="icon" style="background:rgba(6,182,212,.15);color:#06b6d4;">✅</div><h3>Take Attendance</h3><p>Mark daily attendance via face recognition instantly.</p></div>',unsafe_allow_html=True)
        if st.button("Mark Attendance →",key="da"): st.session_state.page="attendance"; st.rerun()
    with c3:
        st.markdown('<div class="dash-card"><div class="icon" style="background:rgba(16,185,129,.15);color:#10b981;">📋</div><h3>View Records</h3><p>Filter, export and manage all attendance logs.</p></div>',unsafe_allow_html=True)
        if st.button("View Records →",key="dv"): st.session_state.page="records"; st.rerun()
    if today_recs:
        st.markdown("<hr class='hdiv'><div class='section-title' style='font-size:1.1rem'>Today's Snapshot</div>",unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(today_recs)[["name","roll","dept","time","day","status"]],use_container_width=True,hide_index=True)

# ══════════════════════════
#  REGISTER
# ══════════════════════════
elif st.session_state.page=="register":
    st.markdown('<div class="section-title">Register Face</div><div class="section-sub">Capture student face — roll number is mandatory.</div>',unsafe_allow_html=True)
    students=load_students()
    cc,cf=st.columns([1.3,1])
    with cc:
        st.markdown("<div class='card'><div class='cam-label'>📷 Camera — face the lens clearly</div>",unsafe_allow_html=True)
        img_file=st.camera_input("",key="rcam",label_visibility="collapsed")
        if img_file: st.markdown("<div class='msg-inf' style='margin-top:.5rem;font-size:.82rem;'>✅ Photo captured. Fill details →</div>",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
    with cf:
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.markdown("#### 🎓 Student Details")
        name=st.text_input("Full Name",placeholder="e.g. Ahmed Khan")
        roll=st.text_input("🔴 Roll Number (Required)",placeholder="e.g. 2024-CS-001")
        dept=st.text_input("Department (Optional)",placeholder="e.g. Computer Science")
        if st.session_state.reg_msg:
            k2,t2=st.session_state.reg_msg
            css="msg-ok" if k2=="ok" else "msg-err"
            st.markdown(f"<div class='{css}'>{t2}</div>",unsafe_allow_html=True)
        reg_btn=st.button("📸  Register Now",type="primary",use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)
        if reg_btn:
            err=None
            if not name.strip(): err="⚠️ Full name is required."
            elif not roll.strip(): err="⚠️ Roll Number is required."
            elif roll.strip() in students: err=f"⚠️ Roll '{roll.strip()}' already registered."
            elif img_file is None: err="⚠️ Please capture a photo first."
            if err: st.session_state.reg_msg=("err",err); st.rerun()
            else:
                with st.spinner("🔍 Detecting face…"):
                    enc=encode_face(pil_to_np(Image.open(img_file)))
                if enc is None:
                    st.session_state.reg_msg=("err","❌ No face detected. Try better lighting and face camera directly.")
                else:
                    students[roll.strip()]={"name":name.strip(),"roll":roll.strip(),"dept":dept.strip(),
                        "encoding":enc_to_list(enc),"registered_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    save_students(students)
                    st.session_state.reg_msg=("ok",f"✅ {name.strip()} (Roll: {roll.strip()}) registered!")
                    st.rerun()
    if students:
        st.markdown("<hr class='hdiv'>",unsafe_allow_html=True)
        st.markdown(f"<div class='section-title' style='font-size:1.1rem'>Registered Students ({len(students)})</div>",unsafe_allow_html=True)
        rows="".join(f"<tr><td><span class='av'>{s['name'][0].upper()}</span>{s['name']}</td><td>{s['roll']}</td><td>{s.get('dept','—') or '—'}</td><td>{s.get('registered_at','—')}</td></tr>" for s in students.values())
        st.markdown(f"<div class='card' style='padding:0;overflow:hidden;'><table class='att-table'><thead><tr><th>Student</th><th>Roll No.</th><th>Dept</th><th>Registered At</th></tr></thead><tbody>{rows}</tbody></table></div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        with st.expander("🗑️ Delete a Student"):
            opts={f"{s['name']}  —  Roll: {s['roll']}":r for r,s in students.items()}
            sel=st.selectbox("Select",list(opts.keys()))
            _,cd=st.columns([3,1])
            with cd:
                st.markdown("<div class='danger-btn'>",unsafe_allow_html=True)
                if st.button("Delete",key="dst",use_container_width=True):
                    del students[opts[sel]]; save_students(students); st.success("Deleted."); st.rerun()
                st.markdown("</div>",unsafe_allow_html=True)

# ══════════════════════════
#  ATTENDANCE
# ══════════════════════════
elif st.session_state.page=="attendance":
    st.markdown('<div class="section-title">Take Attendance</div><div class="section-sub">70% face visibility is enough — partial/blurry photos accepted.</div>',unsafe_allow_html=True)
    students=load_students()
    if not students:
        st.markdown("<div class='msg-inf'>⚠️ No students registered. Go to <b>Register</b> first.</div>",unsafe_allow_html=True)
    else:
        ca,cs=st.columns([1.3,1])
        with ca:
            st.markdown("<div class='card'><div class='cam-label'>📷 Face Recognition Camera</div>",unsafe_allow_html=True)
            att_img=st.camera_input("",key="acam",label_visibility="collapsed")
            st.markdown("</div>",unsafe_allow_html=True)
        with cs:
            st.markdown("<div class='card'>",unsafe_allow_html=True)
            st.markdown("#### 📡 Status Feed")
            if st.session_state.att_msg:
                k2,t2=st.session_state.att_msg
                css="msg-ok" if k2=="ok" else "msg-err" if k2=="err" else "msg-inf"
                st.markdown(f"<div class='{css}'>{t2}</div>",unsafe_allow_html=True)
            else:
                st.markdown("<div class='msg-inf'>📷 Capture photo then click below.</div>",unsafe_allow_html=True)
            mark=st.button("✅  Mark My Attendance",type="primary",use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)
            if mark:
                if att_img is None:
                    st.session_state.att_msg=("err","⚠️ Please capture a photo first."); st.rerun()
                else:
                    with st.spinner("🔍 Scanning…"):
                        enc=encode_face(pil_to_np(Image.open(att_img)))
                    if enc is None:
                        st.session_state.att_msg=("err","❌ No face detected. Ensure good lighting."); st.rerun()
                    else:
                        known_encs=[list_to_enc(s["encoding"]) for s in students.values()]
                        known_rolls=list(students.keys())
                        dists=face_recognition.face_distance(known_encs,enc)
                        bi=int(np.argmin(dists)); bd=float(dists[bi])
                        THRESHOLD=0.62          # ~70% match accepted
                        conf=round((1-bd)*100)
                        if bd>THRESHOLD:
                            st.session_state.att_msg=("err",f"❌ Face not recognised (match: {conf}%). Try better lighting or re-register."); st.rerun()
                        else:
                            mr=known_rolls[bi]; mn=students[mr]["name"]
                            now=datetime.now()
                            ds=now.strftime("%Y-%m-%d"); ts=now.strftime("%I:%M %p"); dy=now.strftime("%A")
                            adata=load_attendance()
                            already=any(r["roll"]==mr and r["date"]==ds for r in adata)
                            if already:
                                st.session_state.att_msg=("inf",f"ℹ️ {mn} — already marked today.")
                            else:
                                adata.append({"name":mn,"roll":mr,"dept":students[mr].get("dept",""),
                                    "date":ds,"time":ts,"day":dy,"status":"PRESENT"})
                                save_attendance(adata)
                                st.session_state.att_msg=("ok",
                                    f"✅ Attendance marked!\n\n"
                                    f"👤 {mn}  |  🎫 Roll: {mr}\n\n"
                                    f"🕐 {ts}  |  📅 {ds}  |  📆 {dy}  |  🎯 Match: {conf}%")
                            st.rerun()

        adata=load_attendance(); today=datetime.now().strftime("%Y-%m-%d")
        today_recs=[r for r in adata if r["date"]==today]; pr={r["roll"] for r in today_recs}
        st.markdown(f"<hr class='hdiv'><div class='section-title' style='font-size:1.1rem'>Today — {datetime.now().strftime('%A, %d %B %Y')}</div>",unsafe_allow_html=True)
        st.markdown(f"<div class='stat-row'><div class='stat-pill'>✅ Present: <b style='color:#10b981'>{len(pr)}</b></div><div class='stat-pill'>❌ Absent: <b style='color:#ef4444'>{len(students)-len(pr)}</b></div></div>",unsafe_allow_html=True)
        rows=""
        for rid,s in students.items():
            init=s["name"][0].upper()
            if rid in pr:
                rec=next(r for r in today_recs if r["roll"]==rid)
                badge="<span class='badge-present'>● PRESENT</span>"; t=rec["time"]; d=rec["day"]; dt=rec["date"]
            else:
                badge="<span class='badge-absent'>● ABSENT</span>"; t="—"; d=datetime.now().strftime("%A"); dt=today
            rows+=f"<tr><td><span class='av'>{init}</span>{s['name']}</td><td>{s['roll']}</td><td>{dt}</td><td>{d}</td><td>{t}</td><td>{badge}</td></tr>"
        st.markdown(f"<div class='card' style='padding:0;overflow:hidden;'><table class='att-table'><thead><tr><th>Student</th><th>Roll</th><th>Date</th><th>Day</th><th>Time</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div>",unsafe_allow_html=True)

# ══════════════════════════
#  RECORDS
# ══════════════════════════
elif st.session_state.page=="records":
    st.markdown('<div class="section-title">Attendance Records</div><div class="section-sub">View, filter, export and manage all attendance logs.</div>',unsafe_allow_html=True)
    adata=load_attendance(); students=load_students()
    cf2,ct=st.columns([1,3.2])
    with cf2:
        st.markdown("<div class='card'>",unsafe_allow_html=True)
        st.markdown("#### 🔍 Filters")
        sq=st.text_input("Name or Roll",placeholder="Search…")
        df2=st.date_input("Filter by Date",value=None)
        filtered=adata.copy()
        if sq:
            q=sq.lower(); filtered=[r for r in filtered if q in r["name"].lower() or q in r["roll"].lower()]
        if df2: filtered=[r for r in filtered if r["date"]==str(df2)]
        st.markdown(f"<br><div class='stat-pill'>Total: <b>{len(adata)}</b></div><br><div class='stat-pill'>Showing: <b>{len(filtered)}</b></div>",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
    with ct:
        b1,b2=st.columns(2)
        with b1:
            if adata:
                csv=pd.DataFrame(adata).to_csv(index=False).encode()
                st.download_button("⬇️  Export CSV",data=csv,file_name=f"attendance_{datetime.now().strftime('%Y%m%d')}.csv",mime="text/csv",use_container_width=True)
        with b2:
            st.markdown("<div class='danger-btn'>",unsafe_allow_html=True)
            if st.button("🗑️  Clear All Records",use_container_width=True):
                save_attendance([]); st.success("Cleared."); st.rerun()
            st.markdown("</div>",unsafe_allow_html=True)
        if not filtered:
            st.markdown("<div class='msg-inf' style='margin-top:1rem;'>No records found.</div>",unsafe_allow_html=True)
        else:
            rows="".join(
                f"<tr><td><span class='av'>{r['name'][0].upper()}</span>{r['name']}</td>"
                f"<td>{r['roll']}</td><td>{r.get('dept','—') or '—'}</td>"
                f"<td>{r['date']}</td><td>{r.get('day','—')}</td><td>{r['time']}</td>"
                f"<td>{'<span class=badge-present>● PRESENT</span>' if r['status']=='PRESENT' else '<span class=badge-absent>● ABSENT</span>'}</td></tr>"
                for r in sorted(filtered,key=lambda x:(x["date"],x["time"]),reverse=True)
            )
            st.markdown(f"<div class='card' style='padding:0;overflow:hidden;margin-top:1rem;'><table class='att-table'><thead><tr><th>Student</th><th>Roll</th><th>Dept</th><th>Date</th><th>Day</th><th>Time</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div>",unsafe_allow_html=True)
        if adata:
            st.markdown("<hr class='hdiv'>",unsafe_allow_html=True)
            with st.expander("🗑️ Delete Records for a Specific Student"):
                opts={f"{r['name']} (Roll: {r['roll']})":r["roll"] for r in adata}
                sel=st.selectbox("Select",list(opts.keys()),key="drsel")
                st.markdown("<div class='danger-btn'>",unsafe_allow_html=True)
                if st.button("Delete Their Records",key="drb",use_container_width=True):
                    rd=opts[sel]; adata=[r for r in adata if r["roll"]!=rd]
                    save_attendance(adata); st.success(f"Deleted for {sel}"); st.rerun()
                st.markdown("</div>",unsafe_allow_html=True)
