import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nash · Doctor Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── CSS — PROFESSIONAL DARK THEME ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, * { font-family: 'Space Grotesk', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 2rem 2rem 2rem; background: #0F1117; }

:root {
    --bg:       #0F1117;
    --surface:  #1A1D27;
    --surface2: #222536;
    --surface3: #2A2E42;
    --teal:     #00C9B1;
    --teal-dk:  #009E8C;
    --teal-dim: rgba(0,201,177,0.12);
    --navy:     #141829;
    --accent:   #4F8EF7;
    --accent-dim: rgba(79,142,247,0.12);
    --gold:     #F5C842;
    --gold-dim: rgba(245,200,66,0.12);
    --red:      #FF5C5C;
    --red-dim:  rgba(255,92,92,0.12);
    --green:    #4EC97E;
    --green-dim:rgba(78,201,126,0.12);
    --orange:   #FF9B4E;
    --text:     #E8EAF0;
    --text-sec: #8890A4;
    --border:   #2A2E42;
    --border2:  #353A52;
}

/* Override streamlit background */
.stApp { background: #0F1117; }
.stApp > div { background: #0F1117; }

/* NAVBAR */
.doc-nav {
    background: linear-gradient(135deg, #141829 0%, #1A1D27 50%, #1E2235 100%);
    border: 1px solid #2A2E42;
    border-radius: 16px;
    padding: 1.1rem 1.8rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 30px rgba(0,0,0,0.4);
}
.doc-logo {
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--teal);
    letter-spacing: -0.5px;
}
.doc-logo span { color: var(--text); }
.doc-sub {
    font-size: 0.72rem;
    color: var(--text-sec);
    letter-spacing: 2px;
    text-transform: uppercase;
}
.doc-badge {
    background: var(--teal-dim);
    border: 1px solid var(--teal);
    color: var(--teal);
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* STAT CARDS */
.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    position: relative;
    overflow: hidden;
}
.stat-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
}
.stat-card.teal::after  { background: var(--teal); }
.stat-card.blue::after  { background: var(--accent); }
.stat-card.red::after   { background: var(--red); }
.stat-card.green::after { background: var(--green); }
.stat-icon { font-size: 1.4rem; margin-bottom: 0.4rem; }
.stat-val {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
    font-family: 'JetBrains Mono', monospace;
}
.stat-lbl { font-size: 0.72rem; color: var(--text-sec); margin-top: 0.3rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; }

/* SECTION HEADERS */
.sec-hd {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--teal);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 1.3rem 0 0.7rem 0;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.sec-line { flex:1; height:1px; background:var(--border); }

/* PATIENT QUEUE ROW */
.q-row {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.45rem;
    cursor: pointer;
    transition: border-color 0.2s;
}
.q-row:hover { border-color: var(--teal); }
.q-row.active { border-color: var(--teal); background: var(--teal-dim); }
.q-name { font-weight: 600; color: var(--text); font-size: 0.9rem; }
.q-meta { font-size: 0.72rem; color: var(--text-sec); margin-top: 0.15rem; }
.q-vital { font-size: 0.7rem; font-weight: 600; }

/* VITAL MINI CARDS */
.mini-vital {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
    margin-bottom: 0.5rem;
}
.mv-label { font-size: 0.65rem; color: var(--text-sec); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
.mv-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.4rem;
    font-weight: 600;
    color: var(--teal);
    line-height: 1.2;
}
.mv-unit { font-size: 0.72rem; color: var(--text-sec); }

/* PILLS */
.pill { display:inline-block; padding:0.18rem 0.65rem; border-radius:20px; font-size:0.68rem; font-weight:600; margin:0.1rem; }
.pill-teal   { background:var(--teal-dim);   border:1px solid var(--teal);   color:var(--teal);  }
.pill-red    { background:var(--red-dim);    border:1px solid var(--red);    color:var(--red);   }
.pill-green  { background:var(--green-dim);  border:1px solid var(--green);  color:var(--green); }
.pill-orange { background:rgba(255,155,78,.15);border:1px solid var(--orange);color:var(--orange);}
.pill-blue   { background:var(--accent-dim); border:1px solid var(--accent); color:var(--accent);}
.pill-gold   { background:var(--gold-dim);   border:1px solid var(--gold);   color:var(--gold);  }

/* STATUS BADGE */
.status-waiting { color: var(--orange); font-size:0.7rem; font-weight:700; }
.status-consult { color: var(--teal);   font-size:0.7rem; font-weight:700; }
.status-pending { color: var(--text-sec);font-size:0.7rem; font-weight:700; }

/* REPORT FORM */
.form-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
}
.form-label {
    font-size: 0.72rem;
    color: var(--teal);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.4rem;
}

/* PRESCRIPTION ROW */
.rx-row {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.rx-name { font-weight: 600; color: var(--text); font-size: 0.88rem; }
.rx-detail { font-size: 0.72rem; color: var(--text-sec); margin-top: 0.1rem; }

/* PROGRESS VISIT */
.visit-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--teal);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
}
.visit-num  { font-family:'JetBrains Mono',monospace; color:var(--teal); font-weight:600; font-size:0.78rem; }
.visit-date { font-size:0.72rem; color:var(--text-sec); }
.visit-note { font-size:0.78rem; color:var(--text); margin-top:0.3rem; }

/* ALERT CARD */
.alert-card {
    background: var(--red-dim);
    border: 1px solid var(--red);
    border-radius: 12px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
}
.alert-title { font-weight:600; color:var(--red); font-size:0.85rem; }
.alert-detail { font-size:0.75rem; color:var(--text-sec); margin-top:0.15rem; }

/* DIVIDER */
.dark-div { height:1px; background:var(--border); margin:1rem 0; }

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: var(--surface);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 0.4rem 1rem;
    font-weight: 600;
    font-size: 0.82rem;
    color: var(--text-sec);
    font-family: 'Space Grotesk', sans-serif;
}
.stTabs [aria-selected="true"] {
    background: var(--teal) !important;
    color: #0F1117 !important;
}

/* INPUTS */
.stTextArea textarea, .stTextInput input, .stSelectbox > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
}
.stTextArea label, .stTextInput label, .stSelectbox label,
.stDateInput label, .stMultiSelect label {
    color: var(--text-sec) !important;
    font-size: 0.78rem !important;
}

/* BUTTONS */
.stButton>button {
    background: linear-gradient(135deg, var(--teal-dk), var(--teal)) !important;
    color: #0F1117 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* LIVE BADGE */
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: var(--green-dim);
    border: 1px solid var(--green);
    color: var(--green);
    padding: 0.28rem 0.75rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.8px;
}
.pulse { width:6px;height:6px;background:var(--green);border-radius:50%;display:inline-block;animation:p 1.4s infinite; }
@keyframes p{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.4;transform:scale(1.5)}}

/* DATAFRAME */
.stDataFrame { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ─── MOCK DATA ─────────────────────────────────────────────────────────────────
def gen_vitals(days=14, seed=42):
    random.seed(seed)
    dates = [datetime.now() - timedelta(days=i, hours=random.randint(0,8)) for i in range(days)]
    dates.reverse()
    return pd.DataFrame({
        "datetime":    dates,
        "temperature": [round(random.uniform(36.2, 38.4), 1) for _ in range(days)],
        "heart_rate":  [random.randint(62, 110) for _ in range(days)],
        "spo2":        [random.randint(93, 100)  for _ in range(days)],
        "bp_sys":      [random.randint(112, 148) for _ in range(days)],
        "bp_dia":      [random.randint(72, 94)   for _ in range(days)],
    })

patients_queue = [
    {"name":"Rahul Verma",   "age":45,"id":"P-1042","time":"09:00","vitals_flag":"BP High",  "status":"Waiting",        "ward":"3B","bed":"12"},
    {"name":"Meena Das",     "age":62,"id":"P-1043","time":"09:30","vitals_flag":"Normal",    "status":"In Consultation","ward":"4A","bed":"7"},
    {"name":"Suresh Kumar",  "age":38,"id":"P-1044","time":"10:00","vitals_flag":"SpO₂ Low",  "status":"Waiting",        "ward":"2C","bed":"3"},
    {"name":"Lakshmi Patel", "age":55,"id":"P-1045","time":"10:30","vitals_flag":"Normal",    "status":"Pending",        "ward":"3B","bed":"15"},
    {"name":"Anil Joshi",    "age":70,"id":"P-1046","time":"11:00","vitals_flag":"HR Alert",  "status":"Pending",        "ward":"5D","bed":"9"},
]

alerts = [
    {"patient":"Suresh Kumar","id":"P-1044","msg":"SpO₂ dropped to 91% — immediate attention required","time":"2 min ago"},
    {"patient":"Anil Joshi",  "id":"P-1046","msg":"Heart rate irregular — 118 bpm recorded by Nash","time":"8 min ago"},
]

# ─── NAVBAR ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="doc-nav">
  <div>
    <div class="doc-logo">🏥 Nash<span> · Doctor Portal</span></div>
    <div class="doc-sub">Clinical Management System</div>
  </div>
  <div style="display:flex;align-items:center;gap:1rem;">
    <div class="live-badge"><span class="pulse"></span> NASH ONLINE</div>
    <div class="doc-badge">👨‍⚕️ Dr. Priya Sharma · Cardiologist</div>
    <div style="font-size:0.72rem;color:#8890A4;">{datetime.now().strftime('%a, %d %b %Y')}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Dashboard", "👥 Patients", "📋 Medical Reports", "💊 Prescriptions", "📈 Progress"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    # Stat cards
    s1,s2,s3,s4 = st.columns(4)
    stats = [
        ("5","Today's Patients","👥","teal"),
        ("2","Active Alerts","🚨","red"),
        ("1","In Consultation","🩺","blue"),
        ("12","This Week","📊","green"),
    ]
    for col,(val,lbl,icon,cls) in zip([s1,s2,s3,s4],stats):
        with col:
            st.markdown(f"""
            <div class="stat-card {cls}">
              <div class="stat-icon">{icon}</div>
              <div class="stat-val">{val}</div>
              <div class="stat-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="dark-div"></div>', unsafe_allow_html=True)

    left_col, right_col = st.columns([1.4, 1])

    with left_col:
        # Alerts
        st.markdown('<div class="sec-hd">🚨 Active Alerts <div class="sec-line"></div></div>', unsafe_allow_html=True)
        for a in alerts:
            st.markdown(f"""
            <div class="alert-card">
              <div class="alert-title">⚠️ {a['patient']} ({a['id']})</div>
              <div class="alert-detail">{a['msg']}</div>
              <div style="font-size:0.68rem;color:#8890A4;margin-top:0.3rem;">🕐 {a['time']}</div>
            </div>""", unsafe_allow_html=True)

        # Today's queue
        st.markdown('<div class="sec-hd">🗂️ Today\'s Queue <div class="sec-line"></div></div>', unsafe_allow_html=True)
        status_map = {"Waiting":"status-waiting","In Consultation":"status-consult","Pending":"status-pending"}
        vital_pill_map = {"Normal":"pill-green","BP High":"pill-red","SpO₂ Low":"pill-red","HR Alert":"pill-orange"}
        for p in patients_queue:
            pill_cls = vital_pill_map.get(p['vitals_flag'],'pill-green')
            status_cls = status_map.get(p['status'],'status-pending')
            st.markdown(f"""
            <div class="q-row">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                  <div class="q-name">{p['name']}</div>
                  <div class="q-meta">⏰ {p['time']} · Age {p['age']} · {p['id']} · Ward {p['ward']} Bed {p['bed']}</div>
                </div>
                <div style="text-align:right;">
                  <span class="pill {pill_cls}">{p['vitals_flag']}</span><br/>
                  <span class="{status_cls}">{p['status']}</span>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

    with right_col:
        # Today's vitals overview chart
        st.markdown('<div class="sec-hd">📡 Nash Feed — Live <div class="sec-line"></div></div>', unsafe_allow_html=True)
        vdf = gen_vitals()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=vdf['datetime'][-7:], y=vdf['bp_sys'][-7:],
            mode='lines+markers', name='Systolic',
            line=dict(color='#FF5C5C', width=2), marker=dict(size=5)
        ))
        fig.add_trace(go.Scatter(
            x=vdf['datetime'][-7:], y=vdf['heart_rate'][-7:],
            mode='lines+markers', name='Heart Rate',
            line=dict(color='#00C9B1', width=2), marker=dict(size=5)
        ))
        fig.update_layout(
            height=220, plot_bgcolor='#1A1D27', paper_bgcolor='#1A1D27',
            margin=dict(l=10,r=10,t=10,b=10),
            font=dict(family='Space Grotesk', color='#8890A4', size=10),
            xaxis=dict(showgrid=False, showticklabels=False, color='#2A2E42'),
            yaxis=dict(gridcolor='#2A2E42', color='#8890A4'),
            legend=dict(font=dict(size=10,color='#8890A4'),orientation='h',yanchor='bottom',y=1.02)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Doctor schedule
        st.markdown('<div class="sec-hd">📅 My Schedule <div class="sec-line"></div></div>', unsafe_allow_html=True)
        for p in patients_queue:
            pill_cls = vital_pill_map.get(p['vitals_flag'],'pill-green')
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.8rem;padding:0.5rem 0;border-bottom:1px solid #2A2E42;">
              <div style="font-family:JetBrains Mono,monospace;color:#00C9B1;font-size:0.82rem;width:48px;">{p['time']}</div>
              <div style="flex:1;">
                <div style="font-size:0.83rem;font-weight:600;color:#E8EAF0;">{p['name']}</div>
                <div style="font-size:0.68rem;color:#8890A4;">{p['id']}</div>
              </div>
              <span class="pill {pill_cls}" style="font-size:0.62rem;">{p['vitals_flag']}</span>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PATIENTS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    sel_patient = st.selectbox(
        "Select Patient:",
        [f"{p['time']} · {p['name']} ({p['id']})" for p in patients_queue],
        label_visibility="collapsed"
    )
    sel_idx = [f"{p['time']} · {p['name']} ({p['id']})" for p in patients_queue].index(sel_patient)
    sp = patients_queue[sel_idx]
    vdf = gen_vitals(seed=sel_idx*7+1)
    latest = vdf.iloc[-1]

    st.markdown(f"""
    <div style="background:var(--surface);border:1px solid var(--border);border-radius:16px;
                padding:1.2rem 1.5rem;margin-bottom:1rem;display:flex;align-items:center;gap:1.5rem;">
      <div style="width:56px;height:56px;background:linear-gradient(135deg,#009E8C,#00C9B1);
                  border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.5rem;">👤</div>
      <div style="flex:1;">
        <div style="font-size:1.15rem;font-weight:700;color:#E8EAF0;">{sp['name']}</div>
        <div style="font-size:0.78rem;color:#8890A4;">Age {sp['age']} · {sp['id']} · Ward {sp['ward']} · Bed {sp['bed']}</div>
        <div style="margin-top:0.4rem;">
          <span class="pill pill-teal">Hypertension</span>
          <span class="pill pill-orange">No Drug Allergies</span>
          <span class="pill pill-blue">Blood Group: O+</span>
        </div>
      </div>
      <div style="text-align:right;">
        <div class="live-badge"><span class="pulse"></span> Nash Active</div>
        <div style="font-size:0.7rem;color:#8890A4;margin-top:0.4rem;">Last scan: 3 min ago</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Vitals grid
    st.markdown('<div class="sec-hd">📡 Current Vitals <div class="sec-line"></div></div>', unsafe_allow_html=True)
    vc1,vc2,vc3,vc4,vc5 = st.columns(5)

    def dark_vital(col, icon, label, val, unit, color):
        col.markdown(f"""
        <div class="mini-vital" style="border-color:{color}22;border-left:3px solid {color};">
          <div class="mv-label">{icon} {label}</div>
          <div class="mv-val" style="color:{color};">{val}</div>
          <div class="mv-unit">{unit}</div>
        </div>""", unsafe_allow_html=True)

    dark_vital(vc1,"🌡️","Temp",   latest['temperature'],     "°C",    "#F5A67D")
    dark_vital(vc2,"💓","HR",     int(latest['heart_rate']), "bpm",   "#FF5C5C")
    dark_vital(vc3,"🫁","SpO₂",   int(latest['spo2']),       "%",     "#00C9B1")
    dark_vital(vc4,"🩺","BP Sys", int(latest['bp_sys']),     "mmHg",  "#4F8EF7")
    dark_vital(vc5,"📈","ECG",    "Sinus",                   "Rhythm","#F5C842")

    # Charts
    st.markdown('<div class="sec-hd">📊 14-Day Trend <div class="sec-line"></div></div>', unsafe_allow_html=True)

    def dark_chart(df, ycol, color, title, hlines=[]):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['datetime'], y=df[ycol],
            mode='lines+markers',
            line=dict(color=color, width=2.5),
            marker=dict(size=5, color=color),
            fill='tozeroy', fillcolor=color+'22'
        ))
        for val,lbl,lc in hlines:
            fig.add_hline(y=val,line_dash="dot",line_color=lc,annotation_text=lbl,annotation_font_size=9,annotation_font_color=lc)
        fig.update_layout(
            title=dict(text=title,font=dict(family='Space Grotesk',size=12,color='#8890A4')),
            height=200, plot_bgcolor='#1A1D27', paper_bgcolor='#1A1D27',
            margin=dict(l=10,r=10,t=35,b=10),
            font=dict(family='Space Grotesk',color='#8890A4',size=10), showlegend=False,
            xaxis=dict(showgrid=False,color='#2A2E42'),
            yaxis=dict(gridcolor='#2A2E42',color='#8890A4')
        )
        return fig

    dc1,dc2 = st.columns(2)
    with dc1: st.plotly_chart(dark_chart(vdf,'bp_sys','#FF5C5C','🩺 Blood Pressure (Systolic)',hlines=[(120,'Target','#F5C842')]), use_container_width=True)
    with dc2: st.plotly_chart(dark_chart(vdf,'heart_rate','#00C9B1','💓 Heart Rate (bpm)',hlines=[(100,'Max','#FF5C5C'),(60,'Min','#4EC97E')]), use_container_width=True)

    dc3,dc4 = st.columns(2)
    with dc3: st.plotly_chart(dark_chart(vdf,'spo2','#4F8EF7','🫁 SpO₂ (%)',hlines=[(95,'Min Normal','#FF9B4E')]), use_container_width=True)
    with dc4: st.plotly_chart(dark_chart(vdf,'temperature','#F5C842','🌡️ Temperature (°C)',hlines=[(37.2,'Fever','#FF5C5C')]), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — MEDICAL REPORTS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    r_left, r_right = st.columns([1.3, 1])

    with r_left:
        st.markdown('<div class="sec-hd">📋 Write Medical Report <div class="sec-line"></div></div>', unsafe_allow_html=True)

        sel_pat_r = st.selectbox("Patient:", [f"{p['name']} ({p['id']})" for p in patients_queue], key="r_pat")

        st.markdown('<div class="form-label">Chief Complaint</div>', unsafe_allow_html=True)
        complaint = st.text_area("", "Patient presents with chest tightness and exertional dyspnea for 3 days. Associated with mild headache.", height=80, key="complaint", label_visibility="collapsed")

        col_d, col_i = st.columns(2)
        with col_d:
            st.markdown('<div class="form-label">Diagnosis</div>', unsafe_allow_html=True)
            diagnosis = st.text_input("", "Hypertension Stage 1", key="diag", label_visibility="collapsed")
        with col_i:
            st.markdown('<div class="form-label">Investigations Ordered</div>', unsafe_allow_html=True)
            invest = st.text_input("", "ECG, Lipid Profile, Echo", key="inv", label_visibility="collapsed")

        st.markdown('<div class="form-label">Clinical Examination Notes</div>', unsafe_allow_html=True)
        exam = st.text_area("", "BP 142/92 mmHg on both arms. Heart sounds S1S2 normal. No murmurs. Lungs clear on auscultation. No pedal edema.", height=90, key="exam", label_visibility="collapsed")

        st.markdown('<div class="form-label">Treatment Plan</div>', unsafe_allow_html=True)
        plan = st.text_area("", "Start Amlodipine 5mg OD. Low sodium diet. Daily BP monitoring. Follow up in 2 weeks.", height=70, key="plan", label_visibility="collapsed")

        bc1, bc2 = st.columns(2)
        with bc1:
            if st.button("💾 Save Report", use_container_width=True, key="save_r"):
                st.success("✅ Report saved & shared with patient!")
        with bc2:
            if st.button("📄 Export PDF", use_container_width=True, key="exp_r"):
                st.info("📄 Generating PDF report...")

    with r_right:
        st.markdown('<div class="sec-hd">🗂️ Past Reports <div class="sec-line"></div></div>', unsafe_allow_html=True)
        past_reports = [
            {"date":"1 May 2025","patient":"Rahul Verma","diag":"Hypertension Stage 1","type":"Follow-up"},
            {"date":"24 Apr 2025","patient":"Rahul Verma","diag":"Initial BP Assessment","type":"First Visit"},
            {"date":"20 Apr 2025","patient":"Meena Das",  "diag":"Type 2 Diabetes Review","type":"Follow-up"},
            {"date":"15 Apr 2025","patient":"Suresh Kumar","diag":"Respiratory Infection","type":"Acute"},
            {"date":"10 Apr 2025","patient":"Rahul Verma","diag":"Routine Cardiac Check","type":"Routine"},
        ]
        for r in past_reports:
            st.markdown(f"""
            <div class="visit-card">
              <div style="display:flex;justify-content:space-between;">
                <div>
                  <div style="font-weight:600;color:#E8EAF0;font-size:0.88rem;">{r['patient']}</div>
                  <div style="font-size:0.75rem;color:#00C9B1;margin:0.15rem 0;">{r['diag']}</div>
                  <div style="font-size:0.7rem;color:#8890A4;">📅 {r['date']}</div>
                </div>
                <div>
                  <span class="pill pill-blue">{r['type']}</span>
                  <div style="font-size:0.68rem;color:#8890A4;margin-top:0.3rem;text-align:right;">View →</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

        # Vitals at current visit
        st.markdown('<div class="sec-hd">📡 Vitals at This Visit <div class="sec-line"></div></div>', unsafe_allow_html=True)
        vdf2 = gen_vitals()
        lat2 = vdf2.iloc[-1]
        vitals_at_visit = [
            ("🌡️","Temperature",f"{lat2['temperature']}°C"),
            ("💓","Heart Rate",  f"{int(lat2['heart_rate'])} bpm"),
            ("🫁","SpO₂",        f"{int(lat2['spo2'])}%"),
            ("🩺","Blood Pressure",f"{int(lat2['bp_sys'])}/{int(lat2['bp_dia'])} mmHg"),
        ]
        gr1, gr2 = st.columns(2)
        for i,(icon,label,val) in enumerate(vitals_at_visit):
            col = gr1 if i%2==0 else gr2
            col.markdown(f"""
            <div class="mini-vital">
              <div class="mv-label">{icon} {label}</div>
              <div style="font-family:JetBrains Mono,monospace;font-size:1.1rem;font-weight:600;color:#00C9B1;">{val}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — PRESCRIPTIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    p_left, p_right = st.columns([1.3, 1])

    with p_left:
        st.markdown('<div class="sec-hd">💊 Write Prescription <div class="sec-line"></div></div>', unsafe_allow_html=True)

        sel_pat_p = st.selectbox("Patient:", [f"{p['name']} ({p['id']})" for p in patients_queue], key="p_pat")

        st.markdown('<div class="form-label">Medicine Name</div>', unsafe_allow_html=True)
        med_name = st.text_input("", "Amlodipine 5mg", key="m1", label_visibility="collapsed")

        mc1,mc2,mc3 = st.columns(3)
        with mc1:
            st.markdown('<div class="form-label">Dosage</div>', unsafe_allow_html=True)
            dosage = st.text_input("", "5mg", key="d1", label_visibility="collapsed")
        with mc2:
            st.markdown('<div class="form-label">Frequency</div>', unsafe_allow_html=True)
            freq = st.selectbox("", ["Once daily","Twice daily","Thrice daily","SOS","Weekly"], key="f1", label_visibility="collapsed")
        with mc3:
            st.markdown('<div class="form-label">Duration</div>', unsafe_allow_html=True)
            dur = st.text_input("", "30 days", key="dur1", label_visibility="collapsed")

        st.markdown('<div class="form-label">Special Instructions</div>', unsafe_allow_html=True)
        inst = st.text_input("", "Take after food. Monitor BP daily. Avoid grapefruit juice.", key="inst1", label_visibility="collapsed")

        # Current Rx preview
        st.markdown(f"""
        <div style="background:#1A1D27;border:1px dashed #00C9B1;border-radius:12px;padding:0.9rem 1.1rem;margin:0.8rem 0;">
          <div style="font-size:0.68rem;color:#8890A4;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.5rem;">Prescription Preview</div>
          <div style="font-weight:600;color:#E8EAF0;">{med_name}</div>
          <div style="display:flex;gap:0.4rem;margin:0.3rem 0;">
            <span class="pill pill-teal">{dosage}</span>
            <span class="pill pill-blue">{freq}</span>
            <span class="pill pill-gold">{dur}</span>
          </div>
          <div style="font-size:0.73rem;color:#8890A4;">📌 {inst}</div>
        </div>""", unsafe_allow_html=True)

        pc1, pc2 = st.columns(2)
        with pc1:
            if st.button("➕ Add Medicine", use_container_width=True, key="add_m"):
                st.success("Medicine added to prescription!")
        with pc2:
            if st.button("📄 Generate & Share PDF", use_container_width=True, key="gen_pdf"):
                st.success("📄 Prescription PDF shared with patient!")

    with p_right:
        st.markdown('<div class="sec-hd">📜 Prescription History <div class="sec-line"></div></div>', unsafe_allow_html=True)
        rx_history = [
            {"pat":"Rahul Verma",   "med":"Amlodipine 5mg",    "freq":"Once daily", "dur":"30 days","date":"1 May 2025"},
            {"pat":"Meena Das",     "med":"Metformin 500mg",    "freq":"Twice daily","dur":"90 days","date":"20 Apr 2025"},
            {"pat":"Suresh Kumar",  "med":"Azithromycin 500mg", "freq":"Once daily", "dur":"5 days", "date":"15 Apr 2025"},
            {"pat":"Rahul Verma",   "med":"Atorvastatin 10mg",  "freq":"Once daily", "dur":"60 days","date":"10 Apr 2025"},
            {"pat":"Lakshmi Patel", "med":"Aspirin 75mg",       "freq":"Once daily", "dur":"Ongoing","date":"5 Apr 2025"},
        ]
        for rx in rx_history:
            st.markdown(f"""
            <div class="rx-row">
              <div>
                <div class="rx-name">💊 {rx['med']}</div>
                <div class="rx-detail">{rx['pat']} · {rx['date']}</div>
                <div style="margin-top:0.3rem;">
                  <span class="pill pill-teal" style="font-size:0.62rem;">{rx['freq']}</span>
                  <span class="pill pill-blue" style="font-size:0.62rem;">{rx['dur']}</span>
                </div>
              </div>
              <span style="color:#8890A4;font-size:0.72rem;cursor:pointer;">📄 View</span>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — PROGRESS TRACKER
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="sec-hd">📈 Patient Progress Tracker <div class="sec-line"></div></div>', unsafe_allow_html=True)

    sel_prog = st.selectbox("Track Patient:", [f"{p['name']} ({p['id']})" for p in patients_queue], key="prog_sel")
    prog_idx = [f"{p['name']} ({p['id']})" for p in patients_queue].index(sel_prog)
    pvdf = gen_vitals(seed=prog_idx*5+3)

    # BP + HR trends side by side
    pg1, pg2 = st.columns(2)

    with pg1:
        fig_prog = go.Figure()
        fig_prog.add_trace(go.Scatter(
            x=pvdf['datetime'], y=pvdf['bp_sys'],
            mode='lines+markers', name='Systolic',
            line=dict(color='#FF5C5C', width=2.5), marker=dict(size=6)
        ))
        fig_prog.add_trace(go.Scatter(
            x=pvdf['datetime'], y=pvdf['bp_dia'],
            mode='lines+markers', name='Diastolic',
            line=dict(color='#4F8EF7', width=2.5), marker=dict(size=6)
        ))
        fig_prog.add_hline(y=120,line_dash="dot",line_color="#F5C842",annotation_text="Target Sys",annotation_font_size=9,annotation_font_color="#F5C842")
        fig_prog.update_layout(
            title=dict(text='🩺 Blood Pressure Progress',font=dict(family='Space Grotesk',size=13,color='#8890A4')),
            height=260, plot_bgcolor='#1A1D27', paper_bgcolor='#1A1D27',
            margin=dict(l=10,r=10,t=40,b=10), font=dict(family='Space Grotesk',color='#8890A4',size=10),
            xaxis=dict(showgrid=False,color='#2A2E42'),
            yaxis=dict(gridcolor='#2A2E42',color='#8890A4'),
            legend=dict(orientation='h',yanchor='bottom',y=1.02,font=dict(size=10,color='#8890A4'))
        )
        st.plotly_chart(fig_prog, use_container_width=True)

    with pg2:
        fig_spo = go.Figure()
        fig_spo.add_trace(go.Scatter(
            x=pvdf['datetime'], y=pvdf['spo2'],
            mode='lines+markers', name='SpO₂',
            line=dict(color='#00C9B1', width=2.5), marker=dict(size=6),
            fill='tozeroy', fillcolor='rgba(0,201,177,0.1)'
        ))
        fig_spo.add_hline(y=95,line_dash="dot",line_color="#FF9B4E",annotation_text="Min Normal",annotation_font_size=9,annotation_font_color="#FF9B4E")
        fig_spo.update_layout(
            title=dict(text='🫁 SpO₂ Progress',font=dict(family='Space Grotesk',size=13,color='#8890A4')),
            height=260, plot_bgcolor='#1A1D27', paper_bgcolor='#1A1D27',
            margin=dict(l=10,r=10,t=40,b=10), font=dict(family='Space Grotesk',color='#8890A4',size=10),
            xaxis=dict(showgrid=False,color='#2A2E42'),
            yaxis=dict(gridcolor='#2A2E42',color='#8890A4',range=[88,102]), showlegend=False
        )
        st.plotly_chart(fig_spo, use_container_width=True)

    st.markdown('<div class="dark-div"></div>', unsafe_allow_html=True)

    prog_left, prog_right = st.columns([1, 1.4])

    with prog_left:
        st.markdown('<div class="sec-hd">🗓️ Visit Timeline <div class="sec-line"></div></div>', unsafe_allow_html=True)
        visits = [
            {"v":"Visit 3","date":"7 May 2025", "bp":"132/86","hr":"84","spo2":"97","note":"Good progress. BP improving steadily. Continue medication."},
            {"v":"Visit 2","date":"1 May 2025", "bp":"138/90","hr":"88","spo2":"96","note":"Moderate improvement. Medication response positive."},
            {"v":"Visit 1","date":"24 Apr 2025","bp":"148/96","hr":"95","spo2":"94","note":"Initial diagnosis. BP elevated. Started Amlodipine 5mg."},
        ]
        for vis in visits:
            st.markdown(f"""
            <div class="visit-card">
              <div style="display:flex;justify-content:space-between;margin-bottom:0.3rem;">
                <span class="visit-num">{vis['v']}</span>
                <span class="visit-date">📅 {vis['date']}</span>
              </div>
              <div style="display:flex;gap:0.5rem;margin-bottom:0.3rem;">
                <span class="pill pill-red"  style="font-size:0.62rem;">BP {vis['bp']}</span>
                <span class="pill pill-teal" style="font-size:0.62rem;">HR {vis['hr']}</span>
                <span class="pill pill-blue" style="font-size:0.62rem;">SpO₂ {vis['spo2']}%</span>
              </div>
              <div class="visit-note">{vis['note']}</div>
            </div>""", unsafe_allow_html=True)

    with prog_right:
        st.markdown('<div class="sec-hd">📝 Doctor\'s Notes <div class="sec-line"></div></div>', unsafe_allow_html=True)
        notes = st.text_area("",
            "Patient Rahul Verma showing consistent improvement on Amlodipine 5mg. BP has reduced from 148/96 to 132/86 over 3 visits. Target <120/80. Continue current medication. Review lipid profile. Consider ACE inhibitor if BP not at target in next 2 weeks.",
            height=130, key="dnotes", label_visibility="collapsed")

        st.markdown('<div class="form-label" style="margin-top:0.8rem;">Next Follow-up</div>', unsafe_allow_html=True)
        fu_date = st.date_input("", min_value=datetime.today(), key="fu_d", label_visibility="collapsed")
        fu_note = st.text_input("", "Follow-up BP check + lipid profile review", key="fu_n", label_visibility="collapsed")

        if st.button("💾 Save Progress Notes & Schedule Follow-up", use_container_width=True, key="save_prog"):
            st.success(f"✅ Notes saved. Follow-up scheduled for {fu_date}. Patient notified via push notification!")

        # Progress summary
        st.markdown("""
        <div style="background:var(--surface);border:1px solid var(--border);
                    border-left:3px solid #4EC97E;border-radius:12px;padding:0.9rem 1.1rem;margin-top:0.8rem;">
          <div style="font-size:0.68rem;color:#4EC97E;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.5rem;">📊 Progress Summary</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;">
            <div style="font-size:0.78rem;color:#8890A4;">BP Sys Reduction</div>
            <div style="font-family:JetBrains Mono,monospace;font-size:0.82rem;color:#4EC97E;font-weight:600;">-16 mmHg ↓</div>
            <div style="font-size:0.78rem;color:#8890A4;">BP Dia Reduction</div>
            <div style="font-family:JetBrains Mono,monospace;font-size:0.82rem;color:#4EC97E;font-weight:600;">-10 mmHg ↓</div>
            <div style="font-size:0.78rem;color:#8890A4;">HR Improvement</div>
            <div style="font-family:JetBrains Mono,monospace;font-size:0.82rem;color:#4EC97E;font-weight:600;">-11 bpm ↓</div>
            <div style="font-size:0.78rem;color:#8890A4;">Overall Trend</div>
            <div style="font-size:0.78rem;color:#4EC97E;font-weight:700;">✅ Improving</div>
          </div>
        </div>""", unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div style="text-align:center;padding:1.5rem 0 0.5rem 0;
            font-size:0.7rem;color:#8890A4;border-top:1px solid #2A2E42;margin-top:2rem;">
  🏥 Nash Doctor Portal · Apollo Hospital Bangalore · Clinical Management System v1.0
</div>
""", unsafe_allow_html=True)
