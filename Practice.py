import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nash — Autonomous Medical Robot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── BRAND COLORS & CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

* { font-family: 'DM Sans', sans-serif; }

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; padding-bottom: 1rem; }

/* Root variables */
:root {
    --teal: #0D7C7C;
    --teal-light: #14A6A6;
    --teal-dark: #085858;
    --teal-pale: #E6F4F4;
    --white: #FFFFFF;
    --silver: #C0C8D0;
    --surface: #F4F6F8;
    --text: #1A1A2E;
    --text-sec: #5A6A7A;
    --success: #2ECC71;
    --warning: #F39C12;
    --danger: #E74C3C;
}

/* NAVBAR */
.nash-nav {
    background: linear-gradient(135deg, #085858 0%, #0D7C7C 50%, #14A6A6 100%);
    padding: 1rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 8px 32px rgba(13, 124, 124, 0.3);
}
.nash-logo {
    font-family: 'Sora', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: white;
    letter-spacing: -1px;
}
.nash-tagline {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.75);
    font-weight: 300;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.nav-badge {
    background: rgba(255,255,255,0.2);
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
}

/* METRIC CARDS */
.metric-card {
    background: white;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    border: 1.5px solid #E6F4F4;
    box-shadow: 0 2px 12px rgba(13,124,124,0.08);
    position: relative;
    overflow: hidden;
    margin-bottom: 0.5rem;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #14A6A6, #0D7C7C);
    border-radius: 4px 0 0 4px;
}
.metric-card.warning::before { background: linear-gradient(180deg, #F39C12, #E67E22); }
.metric-card.danger::before  { background: linear-gradient(180deg, #E74C3C, #C0392B); }
.metric-card.normal::before  { background: linear-gradient(180deg, #2ECC71, #27AE60); }

.metric-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #5A6A7A;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-family: 'Sora', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #1A1A2E;
    line-height: 1;
}
.metric-unit {
    font-size: 0.8rem;
    color: #5A6A7A;
    font-weight: 400;
}
.metric-status {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 600;
    padding: 0.15rem 0.5rem;
    border-radius: 20px;
    margin-top: 0.4rem;
}
.status-normal  { background: #E8F8F0; color: #27AE60; }
.status-warning { background: #FEF5E7; color: #E67E22; }
.status-danger  { background: #FDEDEC; color: #C0392B; }

/* SECTION HEADERS */
.section-header {
    font-family: 'Sora', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #1A1A2E;
    margin: 1.2rem 0 0.8rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid #E6F4F4;
}

/* APPOINTMENT CARDS */
.appt-card {
    background: white;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    border: 1.5px solid #E6F4F4;
    margin-bottom: 0.6rem;
    box-shadow: 0 2px 8px rgba(13,124,124,0.06);
}
.appt-doctor { font-weight: 600; color: #0D7C7C; font-size: 0.95rem; }
.appt-spec   { font-size: 0.75rem; color: #5A6A7A; margin-bottom: 0.3rem; }
.appt-time   { font-size: 0.82rem; color: #1A1A2E; }

/* SUGGESTION CARDS */
.suggest-card {
    background: linear-gradient(135deg, #E6F4F4 0%, white 100%);
    border: 1.5px solid #14A6A6;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
}
.suggest-rank { font-family: 'Sora', sans-serif; font-weight: 800; color: #0D7C7C; font-size: 1.4rem; }
.suggest-spec { font-weight: 600; color: #1A1A2E; font-size: 1rem; }
.suggest-reason { font-size: 0.78rem; color: #5A6A7A; margin-top: 0.2rem; }

/* PATIENT ROW */
.patient-row {
    background: white;
    border-radius: 10px;
    padding: 0.8rem 1.1rem;
    margin-bottom: 0.5rem;
    border: 1px solid #E6F4F4;
    display: flex;
    align-items: center;
    gap: 1rem;
}

/* LANDING HERO */
.hero-section {
    background: linear-gradient(135deg, #085858 0%, #0D7C7C 60%, #14A6A6 100%);
    border-radius: 20px;
    padding: 3rem 2.5rem;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 12px 40px rgba(13,124,124,0.35);
}
.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -2px;
    margin-bottom: 0.5rem;
}
.hero-sub {
    font-size: 1.1rem;
    opacity: 0.85;
    font-weight: 300;
    margin-bottom: 1.5rem;
    max-width: 560px;
    margin-left: auto;
    margin-right: auto;
}

/* FEATURE CARDS */
.feat-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    border: 1.5px solid #E6F4F4;
    box-shadow: 0 4px 16px rgba(13,124,124,0.08);
    height: 100%;
}
.feat-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }
.feat-title { font-family: 'Sora', sans-serif; font-weight: 700; color: #0D7C7C; font-size: 1rem; margin-bottom: 0.4rem; }
.feat-desc  { font-size: 0.82rem; color: #5A6A7A; line-height: 1.5; }

/* VITAL RANGE BAR */
.range-bar-wrap { margin: 0.3rem 0 0.8rem 0; }
.range-label { font-size: 0.72rem; color: #5A6A7A; margin-bottom: 0.2rem; }

/* PILLS */
.pill {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    margin: 0.1rem;
}
.pill-teal   { background: #E6F4F4; color: #0D7C7C; }
.pill-green  { background: #E8F8F0; color: #27AE60; }
.pill-orange { background: #FEF5E7; color: #E67E22; }
.pill-red    { background: #FDEDEC; color: #C0392B; }

/* REPORT CARD */
.report-card {
    background: white;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    border: 1.5px solid #E6F4F4;
    box-shadow: 0 2px 10px rgba(13,124,124,0.07);
    margin-bottom: 1rem;
}
.report-title { font-family: 'Sora', sans-serif; font-weight: 700; color: #1A1A2E; font-size: 1rem; }
.report-meta  { font-size: 0.75rem; color: #5A6A7A; margin-bottom: 0.7rem; }

/* DIVIDER */
.teal-divider {
    height: 2px;
    background: linear-gradient(90deg, #0D7C7C, transparent);
    border-radius: 2px;
    margin: 1rem 0;
}

/* LIVE BADGE */
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #E8F8F0;
    color: #27AE60;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1px;
}
.live-dot {
    width: 8px; height: 8px;
    background: #2ECC71;
    border-radius: 50%;
    animation: pulse 1.5s infinite;
    display: inline-block;
}
@keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.5; transform: scale(1.3); }
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #F4F6F8;
    border-radius: 12px;
    padding: 6px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
    font-size: 0.9rem;
    color: #5A6A7A;
}
.stTabs [aria-selected="true"] {
    background: #0D7C7C !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ─── NAVBAR ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nash-nav">
  <div>
    <div class="nash-logo">🤖 Nash</div>
    <div class="nash-tagline">Autonomous Medical Robot Platform</div>
  </div>
  <div style="text-align:right;">
    <div class="nav-badge">🇮🇳 India</div>
    <div style="color:rgba(255,255,255,0.6);font-size:0.75rem;margin-top:0.3rem;">v1.0 Prototype</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── MOCK DATA ─────────────────────────────────────────────────────────────────
def generate_vitals_history(days=14):
    dates = [datetime.now() - timedelta(days=i, hours=random.randint(0,12)) for i in range(days)]
    dates.reverse()
    return pd.DataFrame({
        "datetime": dates,
        "temperature": [round(random.uniform(36.0, 38.8), 1) for _ in range(days)],
        "heart_rate":  [random.randint(58, 115) for _ in range(days)],
        "spo2":        [random.randint(92, 100) for _ in range(days)],
        "bp_sys":      [random.randint(108, 148) for _ in range(days)],
        "bp_dia":      [random.randint(68, 96)  for _ in range(days)],
    })

vitals_df = generate_vitals_history()
latest = vitals_df.iloc[-1]

doctors = [
    {"name": "Dr. Priya Sharma",    "spec": "Cardiologist",        "exp": "12 yrs", "rating": 4.8, "slots": ["10:00 AM", "11:30 AM", "3:00 PM"]},
    {"name": "Dr. Arjun Mehta",     "spec": "Pulmonologist",       "exp": "9 yrs",  "rating": 4.6, "slots": ["9:00 AM",  "2:00 PM",  "4:30 PM"]},
    {"name": "Dr. Kavitha Rao",     "spec": "General Physician",   "exp": "15 yrs", "rating": 4.9, "slots": ["8:30 AM", "12:00 PM", "5:00 PM"]},
    {"name": "Dr. Rohit Nair",      "spec": "Neurologist",         "exp": "11 yrs", "rating": 4.7, "slots": ["10:30 AM","1:30 PM",  "3:30 PM"]},
    {"name": "Dr. Sneha Iyer",      "spec": "Endocrinologist",     "exp": "8 yrs",  "rating": 4.5, "slots": ["9:30 AM", "11:00 AM", "4:00 PM"]},
]

patients_queue = [
    {"name": "Rahul Verma",   "age": 45, "id": "P-1042", "time": "09:00 AM", "vitals": "BP High",      "status": "Waiting"},
    {"name": "Meena Das",     "age": 62, "id": "P-1043", "time": "09:30 AM", "vitals": "Normal",        "status": "In Consultation"},
    {"name": "Suresh Kumar",  "age": 38, "id": "P-1044", "time": "10:00 AM", "vitals": "SpO₂ Low",      "status": "Waiting"},
    {"name": "Lakshmi Patel", "age": 55, "id": "P-1045", "time": "10:30 AM", "vitals": "Normal",        "status": "Pending"},
    {"name": "Anil Joshi",    "age": 70, "id": "P-1046", "time": "11:00 AM", "vitals": "HR Irregular",  "status": "Pending"},
]

# ─── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🏠  Nash — Home", "🧑‍⚕️  Patient Dashboard", "👨‍⚕️  Doctor Dashboard"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — LANDING PAGE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class="hero-section">
      <div class="hero-title">Meet Nash</div>
      <div class="hero-sub">India's first fully autonomous medical robot that comes to you — scanning vitals, connecting you to the right doctor, all in real time.</div>
      <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
        <span style="background:rgba(255,255,255,0.2);color:white;padding:0.4rem 1rem;border-radius:20px;font-size:0.85rem;font-weight:600;">🤖 Autonomous Navigation</span>
        <span style="background:rgba(255,255,255,0.2);color:white;padding:0.4rem 1rem;border-radius:20px;font-size:0.85rem;font-weight:600;">📡 Real-time Vitals</span>
        <span style="background:rgba(255,255,255,0.2);color:white;padding:0.4rem 1rem;border-radius:20px;font-size:0.85rem;font-weight:600;">🧠 AI Doctor Matching</span>
        <span style="background:rgba(255,255,255,0.2);color:white;padding:0.4rem 1rem;border-radius:20px;font-size:0.85rem;font-weight:600;">🏥 Hospital-grade EMR</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Features grid
    st.markdown('<div class="section-header">What Nash Does</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    feats = [
        ("🌡️", "5 Vital Parameters", "Temperature · Heart Rate · ECG · SpO₂ · Blood Pressure — collected autonomously by the robot."),
        ("🧠", "Smart Doctor Match", "AI engine analyses your vitals + symptoms to suggest the most relevant specialist."),
        ("📅", "Easy Appointments", "Book a slot with your suggested doctor in seconds. Reminders sent automatically."),
        ("📋", "Complete Medical EMR", "Doctors get full patient history, prescriptions, progress tracking across every visit."),
    ]
    for col, (icon, title, desc) in zip([c1,c2,c3,c4], feats):
        with col:
            st.markdown(f"""
            <div class="feat-card">
              <div class="feat-icon">{icon}</div>
              <div class="feat-title">{title}</div>
              <div class="feat-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="teal-divider"></div>', unsafe_allow_html=True)

    # How it works
    st.markdown('<div class="section-header">How Nash Works</div>', unsafe_allow_html=True)
    steps = [
        ("1", "🤖", "Nash Arrives", "The autonomous robot navigates to the patient's bedside or room."),
        ("2", "📡", "Vitals Scanned", "All 5 parameters collected in under 60 seconds, streamed live to the platform."),
        ("3", "🧠", "Doctor Suggested", "AI matches abnormal vitals + symptoms to the right specialist."),
        ("4", "📅", "Appointment Booked", "Patient picks a slot. Reminder notification sent automatically."),
        ("5", "👨‍⚕️", "Doctor Reviews", "Doctor sees full vitals history, writes report & prescription on the platform."),
    ]
    cols = st.columns(5)
    for col, (num, icon, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div style="text-align:center;padding:1rem;">
              <div style="width:40px;height:40px;background:#0D7C7C;color:white;border-radius:50%;
                          display:flex;align-items:center;justify-content:center;
                          font-family:Sora,sans-serif;font-weight:800;font-size:1rem;
                          margin:0 auto 0.6rem auto;">{num}</div>
              <div style="font-size:1.8rem;margin-bottom:0.4rem;">{icon}</div>
              <div style="font-family:Sora,sans-serif;font-weight:700;font-size:0.85rem;color:#1A1A2E;margin-bottom:0.3rem;">{title}</div>
              <div style="font-size:0.75rem;color:#5A6A7A;line-height:1.4;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="teal-divider"></div>', unsafe_allow_html=True)

    # Stats
    st.markdown('<div class="section-header">Nash by the Numbers</div>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    stats = [("2,840+", "Patients Scanned"), ("98.6%", "Vitals Accuracy"), ("12", "Specializations"), ("4.9★", "Doctor Rating")]
    for col, (val, lbl) in zip([s1,s2,s3,s4], stats):
        with col:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#E6F4F4,white);border-radius:14px;
                        padding:1.2rem;text-align:center;border:1.5px solid #C0C8D0;">
              <div style="font-family:Sora,sans-serif;font-size:2rem;font-weight:800;color:#0D7C7C;">{val}</div>
              <div style="font-size:0.8rem;color:#5A6A7A;font-weight:500;">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    # Vitals collected
    st.markdown('<div class="section-header" style="margin-top:1.5rem;">Vitals Collected by Nash Robot</div>', unsafe_allow_html=True)
    v1, v2, v3, v4, v5 = st.columns(5)
    vitals_info = [
        ("🌡️", "Temperature", "36.1–37.2°C", "#E74C3C"),
        ("💓", "Heart Rate",  "60–100 bpm",   "#E91E63"),
        ("📈", "ECG",         "Sinus Rhythm",  "#9C27B0"),
        ("🫁", "SpO₂",        "95–100%",       "#2196F3"),
        ("🩺", "Blood Pressure","<120/80 mmHg","#0D7C7C"),
    ]
    for col, (icon, name, range_, color) in zip([v1,v2,v3,v4,v5], vitals_info):
        with col:
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:1rem;text-align:center;
                        border-top:4px solid {color};box-shadow:0 2px 10px rgba(0,0,0,0.06);">
              <div style="font-size:2rem;">{icon}</div>
              <div style="font-weight:700;color:#1A1A2E;font-size:0.88rem;margin:0.3rem 0;">{name}</div>
              <div style="font-size:0.72rem;color:#5A6A7A;">{range_}</div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PATIENT DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    # Patient header
    col_info, col_live = st.columns([3,1])
    with col_info:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem;">
          <div style="width:52px;height:52px;background:linear-gradient(135deg,#0D7C7C,#14A6A6);
                      border-radius:50%;display:flex;align-items:center;justify-content:center;
                      font-size:1.4rem;">👤</div>
          <div>
            <div style="font-family:Sora,sans-serif;font-weight:700;font-size:1.2rem;color:#1A1A2E;">Arjun Krishnan</div>
            <div style="font-size:0.78rem;color:#5A6A7A;">Age: 34 · Blood Group: O+ · Patient ID: P-1041</div>
            <div style="font-size:0.75rem;color:#5A6A7A;">📍 Apollo Hospital, Bangalore · Ward 3B</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_live:
        st.markdown("""
        <div style="text-align:right;padding-top:0.5rem;">
          <div class="live-badge"><span class="live-dot"></span> NASH ACTIVE</div>
          <div style="font-size:0.72rem;color:#5A6A7A;margin-top:0.3rem;">Last scan: 2 mins ago</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="teal-divider"></div>', unsafe_allow_html=True)

    # ── LIVE VITALS ──
    st.markdown('<div class="section-header">📡 Latest Vitals from Nash Robot</div>', unsafe_allow_html=True)

    def vital_card(label, value, unit, status, icon):
        cls = {"Normal":"normal","Warning":"warning","High":"danger","Low":"danger"}.get(status,"normal")
        status_cls = {"Normal":"status-normal","Warning":"status-warning","High":"status-danger","Low":"status-danger"}.get(status,"status-normal")
        return f"""
        <div class="metric-card {cls}">
          <div class="metric-label">{icon} {label}</div>
          <div class="metric-value">{value} <span class="metric-unit">{unit}</span></div>
          <span class="metric-status {status_cls}">{status}</span>
        </div>"""

    temp_val = latest['temperature']
    hr_val   = latest['heart_rate']
    spo2_val = latest['spo2']
    bp_s     = latest['bp_sys']
    bp_d     = latest['bp_dia']

    temp_status = "Normal" if 36.1 <= temp_val <= 37.2 else ("High" if temp_val > 37.2 else "Low")
    hr_status   = "Normal" if 60 <= hr_val <= 100 else ("High" if hr_val > 100 else "Low")
    spo2_status = "Normal" if spo2_val >= 95 else ("Warning" if spo2_val >= 92 else "Low")
    bp_status   = "Normal" if bp_s < 120 else ("Warning" if bp_s < 130 else "High")

    cv1, cv2, cv3, cv4, cv5 = st.columns(5)
    with cv1: st.markdown(vital_card("Temperature", temp_val, "°C",   temp_status, "🌡️"), unsafe_allow_html=True)
    with cv2: st.markdown(vital_card("Heart Rate",  hr_val,   "bpm",  hr_status,   "💓"), unsafe_allow_html=True)
    with cv3: st.markdown(vital_card("SpO₂",        spo2_val, "%",    spo2_status, "🫁"), unsafe_allow_html=True)
    with cv4: st.markdown(vital_card("Blood Pressure", f"{bp_s}/{bp_d}", "mmHg", bp_status, "🩺"), unsafe_allow_html=True)
    with cv5: st.markdown(vital_card("ECG", "Normal", "Sinus", "Normal", "📈"), unsafe_allow_html=True)

    # ── VITALS HISTORY CHARTS ──
    st.markdown('<div class="section-header">📊 Vitals History (Last 14 Days)</div>', unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig_hr = go.Figure()
        fig_hr.add_trace(go.Scatter(
            x=vitals_df['datetime'], y=vitals_df['heart_rate'],
            mode='lines+markers', name='Heart Rate',
            line=dict(color='#0D7C7C', width=2.5),
            marker=dict(size=5, color='#0D7C7C'),
            fill='tozeroy', fillcolor='rgba(13,124,124,0.08)'
        ))
        fig_hr.add_hline(y=100, line_dash="dot", line_color="#E74C3C", annotation_text="Max Normal")
        fig_hr.add_hline(y=60,  line_dash="dot", line_color="#F39C12", annotation_text="Min Normal")
        fig_hr.update_layout(
            title="Heart Rate (bpm)", height=220,
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=35,b=10),
            font=dict(family='DM Sans'), showlegend=False,
            xaxis=dict(showgrid=False), yaxis=dict(gridcolor='#F4F6F8')
        )
        st.plotly_chart(fig_hr, use_container_width=True)

    with chart_col2:
        fig_bp = go.Figure()
        fig_bp.add_trace(go.Scatter(
            x=vitals_df['datetime'], y=vitals_df['bp_sys'],
            mode='lines+markers', name='Systolic',
            line=dict(color='#E74C3C', width=2.5), marker=dict(size=5)
        ))
        fig_bp.add_trace(go.Scatter(
            x=vitals_df['datetime'], y=vitals_df['bp_dia'],
            mode='lines+markers', name='Diastolic',
            line=dict(color='#14A6A6', width=2.5), marker=dict(size=5)
        ))
        fig_bp.add_hline(y=120, line_dash="dot", line_color="#F39C12")
        fig_bp.update_layout(
            title="Blood Pressure (mmHg)", height=220,
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=35,b=10),
            font=dict(family='DM Sans'),
            xaxis=dict(showgrid=False), yaxis=dict(gridcolor='#F4F6F8'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02)
        )
        st.plotly_chart(fig_bp, use_container_width=True)

    chart_col3, chart_col4 = st.columns(2)
    with chart_col3:
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=vitals_df['datetime'], y=vitals_df['temperature'],
            mode='lines+markers', line=dict(color='#F39C12', width=2.5),
            marker=dict(size=5), fill='tozeroy', fillcolor='rgba(243,156,18,0.08)'
        ))
        fig_temp.add_hline(y=37.2, line_dash="dot", line_color="#E74C3C")
        fig_temp.update_layout(
            title="Temperature (°C)", height=200,
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=35,b=10),
            font=dict(family='DM Sans'), showlegend=False,
            xaxis=dict(showgrid=False), yaxis=dict(gridcolor='#F4F6F8')
        )
        st.plotly_chart(fig_temp, use_container_width=True)

    with chart_col4:
        fig_spo2 = go.Figure()
        fig_spo2.add_trace(go.Scatter(
            x=vitals_df['datetime'], y=vitals_df['spo2'],
            mode='lines+markers', line=dict(color='#2196F3', width=2.5),
            marker=dict(size=5), fill='tozeroy', fillcolor='rgba(33,150,243,0.08)'
        ))
        fig_spo2.add_hline(y=95, line_dash="dot", line_color="#F39C12")
        fig_spo2.update_layout(
            title="SpO₂ (%)", height=200,
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=35,b=10),
            font=dict(family='DM Sans'), showlegend=False,
            xaxis=dict(showgrid=False), yaxis=dict(gridcolor='#F4F6F8', range=[88,102])
        )
        st.plotly_chart(fig_spo2, use_container_width=True)

    # ── DOCTOR SUGGESTION + BOOKING ──
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.markdown('<div class="section-header">🧠 AI Doctor Suggestions</div>', unsafe_allow_html=True)

        # Symptom input
        symptoms = st.multiselect(
            "Add your symptoms (optional):",
            ["Chest Pain", "Shortness of Breath", "Headache", "Fatigue",
             "Dizziness", "Fever", "Cough", "Palpitations"],
            default=["Chest Pain"] if bp_s > 130 else []
        )

        suggestions = []
        if bp_s > 130 or "Chest Pain" in symptoms or "Palpitations" in symptoms:
            suggestions.append(("1", "Cardiologist", f"BP {bp_s}/{bp_d} mmHg is elevated" + (", chest pain reported" if "Chest Pain" in symptoms else "")))
        if spo2_val < 95 or "Shortness of Breath" in symptoms:
            suggestions.append(("2", "Pulmonologist", f"SpO₂ at {spo2_val}% — respiratory review recommended"))
        if "Headache" in symptoms:
            suggestions.append(("3", "Neurologist", "Headache with elevated BP — neurological assessment advised"))
        if not suggestions:
            suggestions.append(("1", "General Physician", "Vitals are within normal range — routine check-up recommended"))

        for rank, spec, reason in suggestions[:3]:
            st.markdown(f"""
            <div class="suggest-card">
              <div style="display:flex;align-items:center;gap:0.8rem;">
                <div class="suggest-rank">#{rank}</div>
                <div>
                  <div class="suggest-spec">{spec}</div>
                  <div class="suggest-reason">🔍 {reason}</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="section-header">📅 Book Appointment</div>', unsafe_allow_html=True)

        selected_spec = suggestions[0][1] if suggestions else "General Physician"
        matching_docs = [d for d in doctors if d['spec'] == selected_spec]
        if not matching_docs:
            matching_docs = [doctors[2]]  # fallback to GP

        sel_doc = st.selectbox("Select Doctor", [d['name'] + " — " + d['spec'] for d in matching_docs] + [d['name'] + " — " + d['spec'] for d in doctors if d not in matching_docs])
        doc_obj = next((d for d in doctors if d['name'] in sel_doc), doctors[0])

        col_date, col_slot = st.columns(2)
        with col_date:
            appt_date = st.date_input("Date", min_value=datetime.today())
        with col_slot:
            slot = st.selectbox("Time Slot", doc_obj['slots'])

        st.markdown(f"""
        <div style="background:#E6F4F4;border-radius:10px;padding:0.8rem 1rem;margin:0.5rem 0;border:1px solid #14A6A6;">
          <div style="font-size:0.75rem;color:#5A6A7A;">Booking Summary</div>
          <div style="font-weight:600;color:#0D7C7C;">{doc_obj['name']}</div>
          <div style="font-size:0.8rem;color:#1A1A2E;">⭐ {doc_obj['rating']} · {doc_obj['exp']} experience</div>
          <div style="font-size:0.8rem;color:#1A1A2E;">📅 {appt_date} · ⏰ {slot}</div>
        </div>""", unsafe_allow_html=True)

        if st.button("✅ Confirm Appointment", use_container_width=True):
            st.success(f"🎉 Appointment confirmed with {doc_obj['name']} on {appt_date} at {slot}. Push notification will be sent 1 hour before!")

    # ── UPCOMING APPOINTMENTS ──
    st.markdown('<div class="section-header">📋 Upcoming Appointments</div>', unsafe_allow_html=True)
    upcoming = [
        {"doctor": "Dr. Priya Sharma", "spec": "Cardiologist",      "date": "Tomorrow",  "time": "10:00 AM", "status": "Confirmed"},
        {"doctor": "Dr. Kavitha Rao",  "spec": "General Physician",  "date": "12 May",    "time": "8:30 AM",  "status": "Confirmed"},
    ]
    for a in upcoming:
        pill_color = "pill-green" if a['status'] == "Confirmed" else "pill-orange"
        st.markdown(f"""
        <div class="appt-card">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
              <div class="appt-doctor">{a['doctor']}</div>
              <div class="appt-spec">{a['spec']}</div>
              <div class="appt-time">📅 {a['date']} · ⏰ {a['time']}</div>
            </div>
            <span class="pill {pill_color}">{a['status']}</span>
          </div>
        </div>""", unsafe_allow_html=True)

    # ── SCAN HISTORY TABLE ──
    st.markdown('<div class="section-header">🗂️ Scan History</div>', unsafe_allow_html=True)
    display_df = vitals_df.copy()
    display_df['datetime'] = display_df['datetime'].dt.strftime("%d %b %Y  %I:%M %p")
    display_df.columns = ["Date & Time", "Temp (°C)", "Heart Rate (bpm)", "SpO₂ (%)", "BP Sys", "BP Dia"]
    display_df = display_df.iloc[::-1].reset_index(drop=True)
    st.dataframe(display_df, use_container_width=True, height=250)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — DOCTOR DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    # Doctor header
    dcol1, dcol2 = st.columns([3,1])
    with dcol1:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem;">
          <div style="width:52px;height:52px;background:linear-gradient(135deg,#085858,#0D7C7C);
                      border-radius:50%;display:flex;align-items:center;justify-content:center;
                      font-size:1.4rem;">👨‍⚕️</div>
          <div>
            <div style="font-family:Sora,sans-serif;font-weight:700;font-size:1.2rem;color:#1A1A2E;">Dr. Priya Sharma</div>
            <div style="font-size:0.78rem;color:#5A6A7A;">Cardiologist · MBBS, MD · 12 yrs experience</div>
            <div style="font-size:0.75rem;color:#5A6A7A;">🏥 Apollo Hospital, Bangalore</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with dcol2:
        st.markdown("""
        <div style="text-align:right;padding-top:0.5rem;">
          <div style="background:#E6F4F4;color:#0D7C7C;padding:0.3rem 0.8rem;border-radius:20px;
                      font-size:0.75rem;font-weight:700;display:inline-block;">📅 Wednesday, 7 May 2025</div>
          <div style="font-size:0.72rem;color:#5A6A7A;margin-top:0.3rem;">5 patients today</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="teal-divider"></div>', unsafe_allow_html=True)

    # ── QUICK STATS ──
    ds1, ds2, ds3, ds4 = st.columns(4)
    quick_stats = [
        ("5", "Today's Patients",  "#0D7C7C", "👥"),
        ("2", "Alerts",            "#E74C3C", "🚨"),
        ("1", "In Consultation",   "#F39C12", "🩺"),
        ("12", "Total This Week",  "#2ECC71", "📊"),
    ]
    for col, (val, lbl, color, icon) in zip([ds1,ds2,ds3,ds4], quick_stats):
        with col:
            st.markdown(f"""
            <div style="background:white;border-radius:14px;padding:1rem 1.2rem;
                        border-left:4px solid {color};box-shadow:0 2px 10px rgba(0,0,0,0.06);">
              <div style="font-size:1.3rem;">{icon}</div>
              <div style="font-family:Sora,sans-serif;font-size:1.8rem;font-weight:800;color:{color};">{val}</div>
              <div style="font-size:0.75rem;color:#5A6A7A;font-weight:500;">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="teal-divider"></div>', unsafe_allow_html=True)

    # ── PATIENT QUEUE + DETAIL ──
    queue_col, detail_col = st.columns([1, 1.6])

    with queue_col:
        st.markdown('<div class="section-header">🗂️ Today\'s Patient Queue</div>', unsafe_allow_html=True)
        selected_patient = st.radio(
            "Select patient to view:",
            [f"{p['time']} · {p['name']} ({p['id']})" for p in patients_queue],
            label_visibility="collapsed"
        )
        sel_idx = [f"{p['time']} · {p['name']} ({p['id']})" for p in patients_queue].index(selected_patient)
        sel_p = patients_queue[sel_idx]

        status_colors = {"Waiting": "#F39C12", "In Consultation": "#0D7C7C", "Pending": "#C0C8D0"}
        for p in patients_queue:
            sc = status_colors.get(p['status'], '#C0C8D0')
            vitals_pill = "pill-red" if p['vitals'] != "Normal" else "pill-green"
            st.markdown(f"""
            <div style="background:{'#E6F4F4' if p == sel_p else 'white'};
                        border-radius:10px;padding:0.7rem 1rem;margin-bottom:0.4rem;
                        border:{'1.5px solid #0D7C7C' if p == sel_p else '1px solid #E6F4F4'};
                        cursor:pointer;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                  <div style="font-weight:600;color:#1A1A2E;font-size:0.88rem;">{p['name']}</div>
                  <div style="font-size:0.72rem;color:#5A6A7A;">⏰ {p['time']} · Age {p['age']}</div>
                </div>
                <div style="text-align:right;">
                  <span class="pill {vitals_pill}" style="font-size:0.65rem;">{p['vitals']}</span><br/>
                  <span style="font-size:0.68rem;color:{sc};font-weight:600;">{p['status']}</span>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

    with detail_col:
        st.markdown(f'<div class="section-header">👤 {sel_p["name"]} · {sel_p["id"]}</div>', unsafe_allow_html=True)

        # Tabs inside doctor detail
        dt1, dt2, dt3 = st.tabs(["📡 Vitals", "📋 Medical Report", "💊 Prescription"])

        with dt1:
            # Show mini vitals for selected patient
            pv = vitals_df.iloc[random.randint(0, len(vitals_df)-1)]
            vc1, vc2 = st.columns(2)
            vitals_display = [
                ("🌡️", "Temperature", f"{pv['temperature']}°C"),
                ("💓", "Heart Rate",   f"{int(pv['heart_rate'])} bpm"),
                ("🫁", "SpO₂",         f"{int(pv['spo2'])}%"),
                ("🩺", "Blood Pressure",f"{int(pv['bp_sys'])}/{int(pv['bp_dia'])} mmHg"),
            ]
            for i, (icon, name, val) in enumerate(vitals_display):
                col = vc1 if i % 2 == 0 else vc2
                with col:
                    st.markdown(f"""
                    <div style="background:#F4F6F8;border-radius:10px;padding:0.7rem 1rem;margin-bottom:0.5rem;">
                      <div style="font-size:0.7rem;color:#5A6A7A;font-weight:600;text-transform:uppercase;">{icon} {name}</div>
                      <div style="font-family:Sora,sans-serif;font-weight:700;font-size:1.3rem;color:#0D7C7C;">{val}</div>
                    </div>""", unsafe_allow_html=True)

            # Trend chart for this patient
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=vitals_df['datetime'][-7:], y=vitals_df['heart_rate'][-7:],
                mode='lines+markers', name='HR',
                line=dict(color='#0D7C7C', width=2)
            ))
            fig_trend.add_trace(go.Scatter(
                x=vitals_df['datetime'][-7:], y=vitals_df['bp_sys'][-7:],
                mode='lines+markers', name='BP Sys',
                line=dict(color='#E74C3C', width=2)
            ))
            fig_trend.update_layout(
                title="7-Day Vitals Trend", height=180,
                plot_bgcolor='white', paper_bgcolor='white',
                margin=dict(l=5,r=5,t=35,b=5),
                font=dict(family='DM Sans', size=10),
                xaxis=dict(showgrid=False), yaxis=dict(gridcolor='#F4F6F8'),
                legend=dict(orientation='h', yanchor='bottom', y=1.02, font=dict(size=10))
            )
            st.plotly_chart(fig_trend, use_container_width=True)

        with dt2:
            st.markdown("**Chief Complaint**")
            complaint = st.text_area("", "Patient complains of chest tightness and shortness of breath on exertion for the past 3 days.", height=70, key="complaint")

            st.markdown("**Clinical Examination Notes**")
            exam = st.text_area("", "BP elevated at 142/92 mmHg. Heart sounds normal. No murmurs. Lungs clear on auscultation.", height=70, key="exam")

            dcol_a, dcol_b = st.columns(2)
            with dcol_a:
                st.markdown("**Diagnosis**")
                diagnosis = st.text_input("", "Hypertension Stage 1", key="diag")
            with dcol_b:
                st.markdown("**Investigations**")
                invest = st.text_input("", "ECG, Lipid Profile, Echo", key="inv")

            if st.button("💾 Save Medical Report", use_container_width=True, key="save_report"):
                st.success("✅ Medical report saved and shared with patient!")

        with dt3:
            st.markdown("**Add Medicines**")
            med_col1, med_col2, med_col3 = st.columns([2,1,1])
            with med_col1: med_name = st.text_input("Medicine", "Amlodipine 5mg", key="med1")
            with med_col2: med_freq = st.selectbox("Frequency", ["Once daily", "Twice daily", "Thrice daily", "SOS"], key="freq1")
            with med_col3: med_dur  = st.text_input("Duration", "30 days", key="dur1")
            med_inst = st.text_input("Special Instructions", "Take after food. Monitor BP daily.", key="inst1")

            st.markdown("""
            <div style="background:#E6F4F4;border-radius:10px;padding:0.8rem 1rem;
                        border:1px dashed #14A6A6;margin:0.5rem 0;">
              <div style="font-size:0.72rem;color:#5A6A7A;margin-bottom:0.4rem;">Current Prescription</div>
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                  <span style="font-weight:600;color:#1A1A2E;">Amlodipine 5mg</span>
                  <span class="pill pill-teal">Once daily</span>
                  <span class="pill pill-teal">30 days</span>
                </div>
              </div>
              <div style="font-size:0.75rem;color:#5A6A7A;margin-top:0.3rem;">📌 Take after food. Monitor BP daily.</div>
            </div>
            """, unsafe_allow_html=True)

            pcol1, pcol2 = st.columns(2)
            with pcol1:
                if st.button("➕ Add Medicine", use_container_width=True): st.info("Medicine added to prescription!")
            with pcol2:
                if st.button("📄 Generate PDF", use_container_width=True): st.success("📄 Prescription PDF generated & shared with patient!")

    # ── PATIENT PROGRESS TRACKER ──
    st.markdown('<div class="section-header">📈 Patient Progress Tracker</div>', unsafe_allow_html=True)

    prog_col1, prog_col2 = st.columns([2,1])
    with prog_col1:
        fig_prog = go.Figure()
        fig_prog.add_trace(go.Scatter(
            x=vitals_df['datetime'], y=vitals_df['bp_sys'],
            mode='lines+markers', name='BP Systolic',
            line=dict(color='#E74C3C', width=2.5), marker=dict(size=6)
        ))
        fig_prog.add_trace(go.Scatter(
            x=vitals_df['datetime'], y=vitals_df['bp_dia'],
            mode='lines+markers', name='BP Diastolic',
            line=dict(color='#0D7C7C', width=2.5), marker=dict(size=6)
        ))
        fig_prog.add_hline(y=120, line_dash="dot", line_color="#F39C12", annotation_text="Target Systolic")
        fig_prog.update_layout(
            title="Blood Pressure Progress — Arjun Krishnan", height=260,
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=40,b=10),
            font=dict(family='DM Sans'),
            xaxis=dict(showgrid=False), yaxis=dict(gridcolor='#F4F6F8'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02)
        )
        st.plotly_chart(fig_prog, use_container_width=True)

    with prog_col2:
        st.markdown('<div style="margin-top:0.3rem;"></div>', unsafe_allow_html=True)
        visits = [
            {"visit": "Visit 1", "date": "24 Apr", "note": "Initial diagnosis. BP very high.", "bp": "148/96"},
            {"visit": "Visit 2", "date": "1 May",  "note": "BP improving. Medication response good.", "bp": "138/90"},
            {"visit": "Visit 3", "date": "7 May",  "note": "Good progress. Continue medication.", "bp": "132/86"},
        ]
        for v in visits:
            st.markdown(f"""
            <div style="background:white;border-radius:10px;padding:0.7rem 1rem;
                        margin-bottom:0.5rem;border:1px solid #E6F4F4;">
              <div style="display:flex;justify-content:space-between;">
                <span style="font-weight:700;color:#0D7C7C;font-size:0.85rem;">{v['visit']}</span>
                <span style="font-size:0.72rem;color:#5A6A7A;">{v['date']}</span>
              </div>
              <div style="font-size:0.75rem;color:#1A1A2E;margin:0.2rem 0;">BP: <b>{v['bp']}</b></div>
              <div style="font-size:0.72rem;color:#5A6A7A;">{v['note']}</div>
            </div>""", unsafe_allow_html=True)

    # ── DOCTOR NOTES ──
    st.markdown('<div class="section-header">📝 Doctor\'s Notes</div>', unsafe_allow_html=True)
    notes = st.text_area("", "Patient responding well to Amlodipine 5mg. BP trending down over 2 weeks. Schedule follow-up in 2 weeks. Consider adding ARB if BP does not reach target (<120/80).", height=90, key="doc_notes")
    if st.button("💾 Save Notes", key="save_notes"):
        st.success("Notes saved to patient record!")
