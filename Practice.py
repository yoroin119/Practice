import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nash · Patient Portal",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── CSS — CLEAN WHITE THEME ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700;800;900&family=Lato:wght@300;400;700&display=swap');

html, body, * { font-family: 'Lato', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 2rem 2rem 2rem; background: #FFFFFF; }
.stApp { background: #FFFFFF !important; }
.stApp > div { background: #FFFFFF !important; }

:root {
    --rose:    #D94F45;
    --rose-lt: #FDF0EF;
    --rose-dk: #B03830;
    --teal:    #0D8A82;
    --teal-lt: #E8F6F5;
    --teal-dk: #096E68;
    --peach:   #E07840;
    --peach-lt:#FDF1E8;
    --cream:   #FFFFFF;
    --sand:    #F7F8FA;
    --text:    #111827;
    --text-sec:#4B5563;
    --success: #16A34A;
    --warning: #D97706;
    --danger:  #DC2626;
    --white:   #FFFFFF;
    --border:  #E5E7EB;
}

/* NAVBAR */
.nav-wrap {
    background: linear-gradient(120deg, #E8837A 0%, #F5A67D 50%, #F5C6A0 100%);
    border-radius: 20px;
    padding: 1.2rem 2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 8px 30px rgba(232,131,122,0.3);
}
.nav-logo {
    font-family: 'Nunito', sans-serif;
    font-size: 1.9rem;
    font-weight: 900;
    color: white;
    letter-spacing: -0.5px;
}
.nav-sub {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.85);
    font-weight: 400;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.nav-user {
    background: rgba(255,255,255,0.25);
    border-radius: 40px;
    padding: 0.5rem 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    color: white;
    font-size: 0.85rem;
    font-weight: 700;
}

/* SIDEBAR NAV PILLS */
.side-nav {
    background: white;
    border-radius: 16px;
    padding: 1.2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid var(--border);
}
.nav-pill {
    display: block;
    padding: 0.65rem 1rem;
    border-radius: 12px;
    font-weight: 600;
    font-size: 0.88rem;
    color: var(--text-sec);
    margin-bottom: 0.3rem;
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;
}
.nav-pill.active {
    background: var(--rose-lt);
    color: var(--rose-dk);
}
.nav-pill:hover { background: var(--sand); }

/* VITAL CARDS */
.vital-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 1.2rem 1.3rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1.5px solid var(--border);
    position: relative;
    overflow: hidden;
}
.vital-card-icon {
    font-size: 2rem;
    margin-bottom: 0.4rem;
}
.vital-label {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: var(--text-sec);
    margin-bottom: 0.2rem;
}
.vital-value {
    font-family: 'Nunito', sans-serif;
    font-size: 2.1rem;
    font-weight: 900;
    color: var(--text);
    line-height: 1;
}
.vital-unit { font-size: 0.82rem; font-weight: 400; color: var(--text-sec); }
.vital-badge {
    display: inline-block;
    padding: 0.18rem 0.6rem;
    border-radius: 20px;
    font-size: 0.68rem;
    font-weight: 700;
    margin-top: 0.35rem;
}
.badge-normal  { background: #E8F5ED; color: #3A8F5A; }
.badge-warning { background: #FEF8E7; color: #C07800; }
.badge-danger  { background: #FDECEC; color: #C03030; }
.vital-accent {
    position: absolute;
    top: 0; right: 0;
    width: 60px; height: 60px;
    border-radius: 0 18px 0 60px;
    opacity: 0.12;
}

/* SECTION HEADER */
.sec-head {
    font-family: 'Nunito', sans-serif;
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--text);
    margin: 1.4rem 0 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.sec-line {
    flex: 1;
    height: 2px;
    background: linear-gradient(90deg, var(--border), transparent);
    border-radius: 2px;
}

/* APPOINTMENT CARD */
.appt-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 1rem 1.2rem;
    border: 1.5px solid var(--border);
    margin-bottom: 0.7rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    display: flex;
    align-items: center;
    gap: 1rem;
}
.appt-avatar {
    width: 44px; height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0D8A82, #096E68);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
}
.appt-name { font-weight: 700; color: var(--text); font-size: 0.92rem; }
.appt-spec { font-size: 0.75rem; color: var(--text-sec); }
.appt-time { font-size: 0.78rem; color: var(--teal-dk); font-weight: 600; }

/* SUGGEST CARD */
.sug-card {
    background: #FFFFFF;
    border: 1.5px solid #E5E7EB;
    border-left: 4px solid var(--teal);
    border-radius: 16px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04);
}
.sug-rank { font-family:'Nunito',sans-serif; font-weight:900; font-size:1.5rem; color:var(--teal); }
.sug-spec { font-weight:700; color:var(--text); font-size:0.95rem; }
.sug-why  { font-size:0.75rem; color:var(--text-sec); margin-top:0.15rem; }

/* LIVE PULSE */
.live-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #F0FDF4;
    color: #16A34A;
    border: 1px solid #BBF7D0;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.8px;
}
.pulse-dot {
    width: 7px; height: 7px;
    background: #16A34A;
    border-radius: 50%;
    display: inline-block;
    animation: blink 1.4s infinite;
}
@keyframes blink {
    0%,100%{opacity:1;transform:scale(1)}
    50%{opacity:0.4;transform:scale(1.4)}
}

/* SUMMARY BOX */
.summary-box {
    background: var(--teal-lt);
    border: 1.5px solid var(--teal);
    border-radius: 14px;
    padding: 0.9rem 1.1rem;
    margin: 0.6rem 0;
}

/* REPORT CARD */
.report-row {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 0.8rem 1rem;
    border: 1px solid var(--border);
    margin-bottom: 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: #F3F4F6;
    border-radius: 14px;
    padding: 5px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 0.45rem 1.1rem;
    font-weight: 700;
    font-size: 0.85rem;
    color: var(--text-sec);
    font-family: 'Nunito', sans-serif;
}
.stTabs [aria-selected="true"] {
    background: var(--teal) !important;
    color: white !important;
}

/* PILL TAGS */
.pill { display:inline-block; padding:0.2rem 0.65rem; border-radius:20px; font-size:0.7rem; font-weight:700; margin:0.1rem; }
.pill-rose  { background:var(--rose-lt);  color:var(--rose-dk); }
.pill-teal  { background:var(--teal-lt);  color:var(--teal-dk); }
.pill-peach { background:var(--peach-lt); color:#B05A20; }
.pill-green { background:#E8F5ED; color:#3A8F5A; }
.pill-red   { background:#FDECEC; color:#C03030; }

/* DIVIDER */
.warm-div { height:2px; background:linear-gradient(90deg,var(--rose-lt),transparent); margin:1rem 0; border-radius:2px; }

/* PROFILE CARD */
.profile-card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 1.5rem;
    border: 1.5px solid var(--border);
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.profile-avatar {
    width: 72px; height: 72px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--teal), var(--teal-dk));
    margin: 0 auto 0.8rem auto;
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem;
}
.profile-name { font-family:'Nunito',sans-serif; font-weight:900; font-size:1.2rem; color:var(--text); }
.profile-meta { font-size:0.78rem; color:var(--text-sec); margin-top:0.2rem; }

button[kind="primary"], .stButton>button {
    background: linear-gradient(135deg, var(--teal-dk), var(--teal)) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-family: 'Nunito', sans-serif !important;
    padding: 0.5rem 1.2rem !important;
}
</style>
""", unsafe_allow_html=True)

# ─── MOCK DATA ─────────────────────────────────────────────────────────────────
def gen_vitals(days=14):
    dates = [datetime.now() - timedelta(days=i, hours=random.randint(0,10)) for i in range(days)]
    dates.reverse()
    return pd.DataFrame({
        "datetime":    dates,
        "temperature": [round(random.uniform(36.2, 38.6), 1) for _ in range(days)],
        "heart_rate":  [random.randint(60, 112) for _ in range(days)],
        "spo2":        [random.randint(93, 100)  for _ in range(days)],
        "bp_sys":      [random.randint(110, 148) for _ in range(days)],
        "bp_dia":      [random.randint(70, 95)   for _ in range(days)],
    })

vdf = gen_vitals()
latest = vdf.iloc[-1]

doctors = [
    {"name":"Dr. Priya Sharma",  "spec":"Cardiologist",      "exp":"12 yrs","rating":4.8,"slots":["10:00 AM","11:30 AM","3:00 PM"],"avatar":"👩‍⚕️"},
    {"name":"Dr. Arjun Mehta",   "spec":"Pulmonologist",     "exp":"9 yrs", "rating":4.6,"slots":["9:00 AM","2:00 PM","4:30 PM"], "avatar":"👨‍⚕️"},
    {"name":"Dr. Kavitha Rao",   "spec":"General Physician", "exp":"15 yrs","rating":4.9,"slots":["8:30 AM","12:00 PM","5:00 PM"],"avatar":"👩‍⚕️"},
    {"name":"Dr. Rohit Nair",    "spec":"Neurologist",       "exp":"11 yrs","rating":4.7,"slots":["10:30 AM","1:30 PM","3:30 PM"],"avatar":"👨‍⚕️"},
]

# ─── NAVBAR ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-wrap">
  <div>
    <div class="nav-logo">🌿 Nash · Patient Portal</div>
    <div class="nav-sub">Your Health. Your Control.</div>
  </div>
  <div class="nav-user">
    <span>👤</span>
    <span>Arjun Krishnan</span>
    <span style="background:rgba(255,255,255,0.3);border-radius:20px;padding:0.1rem 0.5rem;font-size:0.72rem;">P-1041</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Home", "📡 My Vitals", "🧠 Find Doctor", "📅 Appointments", "📋 My Reports"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    left, right = st.columns([1, 2.5])

    with left:
        # Profile card
        st.markdown("""
        <div class="profile-card">
          <div class="profile-avatar">👤</div>
          <div class="profile-name">Arjun Krishnan</div>
          <div class="profile-meta">Age 34 · Male · O+</div>
          <div class="profile-meta">🏥 Apollo Hospital, Bangalore</div>
          <div class="profile-meta">Ward 3B · Bed 12</div>
          <div style="margin-top:0.8rem;">
            <span class="pill pill-teal">No Allergies</span>
            <span class="pill pill-rose">Hypertension</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="warm-div"></div>', unsafe_allow_html=True)

        # Quick health summary
        st.markdown("""
        <div style="background:white;border-radius:16px;padding:1.1rem;border:1.5px solid #EDE8E1;box-shadow:0 2px 10px rgba(0,0,0,0.05);">
          <div style="font-family:Nunito,sans-serif;font-weight:800;font-size:0.95rem;color:#2D2D2D;margin-bottom:0.7rem;">📊 Health Summary</div>
          <div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #F5EFE6;">
            <span style="font-size:0.78rem;color:#7A7A8C;">Last Scan</span>
            <span style="font-size:0.78rem;font-weight:700;color:#2D2D2D;">2 mins ago</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #F5EFE6;">
            <span style="font-size:0.78rem;color:#7A7A8C;">Total Scans</span>
            <span style="font-size:0.78rem;font-weight:700;color:#2D2D2D;">14</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #F5EFE6;">
            <span style="font-size:0.78rem;color:#7A7A8C;">Upcoming Appt</span>
            <span style="font-size:0.78rem;font-weight:700;color:#4EADA8;">Tomorrow 10AM</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:0.4rem 0;">
            <span style="font-size:0.78rem;color:#7A7A8C;">Overall Status</span>
            <span style="font-size:0.78rem;font-weight:700;color:#C07800;">⚠️ Monitor</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        # Live status
        col_live, col_time = st.columns([1,1])
        with col_live:
            st.markdown('<div class="live-pill"><span class="pulse-dot"></span> NASH ROBOT ACTIVE</div>', unsafe_allow_html=True)
        with col_time:
            st.markdown(f'<div style="font-size:0.78rem;color:#7A7A8C;padding-top:0.4rem;">📅 {datetime.now().strftime("%A, %d %B %Y")}</div>', unsafe_allow_html=True)

        st.markdown('<div class="sec-head">📡 Latest Vitals <div class="sec-line"></div></div>', unsafe_allow_html=True)

        # Vitals row
        temp_s = "Normal" if 36.1<=latest['temperature']<=37.2 else ("Warning" if latest['temperature']<=38.5 else "danger")
        hr_s   = "Normal" if 60<=latest['heart_rate']<=100 else "Warning"
        spo2_s = "Normal" if latest['spo2']>=95 else ("Warning" if latest['spo2']>=92 else "danger")
        bp_s_  = "Normal" if latest['bp_sys']<120 else ("Warning" if latest['bp_sys']<140 else "danger")

        def vc(icon, label, val, unit, status, color):
            badge_cls = {"Normal":"badge-normal","Warning":"badge-warning","danger":"badge-danger"}.get(status,"badge-normal")
            return f"""
            <div class="vital-card">
              <div class="vital-accent" style="background:{color};"></div>
              <div class="vital-card-icon">{icon}</div>
              <div class="vital-label">{label}</div>
              <div class="vital-value">{val} <span class="vital-unit">{unit}</span></div>
              <div><span class="vital-badge {badge_cls}">{status}</span></div>
            </div>"""

        c1,c2,c3,c4,c5 = st.columns(5)
        with c1: st.markdown(vc("🌡️","Temp",latest['temperature'],"°C",temp_s,"#E8837A"), unsafe_allow_html=True)
        with c2: st.markdown(vc("💓","Heart Rate",int(latest['heart_rate']),"bpm",hr_s,"#E91E63"), unsafe_allow_html=True)
        with c3: st.markdown(vc("🫁","SpO₂",int(latest['spo2']),"%",spo2_s,"#4EADA8"), unsafe_allow_html=True)
        with c4: st.markdown(vc("🩺","BP Sys",int(latest['bp_sys']),"mmHg",bp_s_,"#F5A67D"), unsafe_allow_html=True)
        with c5: st.markdown(vc("📈","ECG","Sinus","Rhythm","Normal","#9C27B0"), unsafe_allow_html=True)

        st.markdown('<div class="warm-div"></div>', unsafe_allow_html=True)

        # Quick mini chart
        st.markdown('<div class="sec-head">📈 Heart Rate — Last 7 Days <div class="sec-line"></div></div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=vdf['datetime'][-7:], y=vdf['heart_rate'][-7:],
            mode='lines+markers',
            line=dict(color='#E8837A', width=2.5),
            marker=dict(size=6, color='#E8837A'),
            fill='tozeroy', fillcolor='rgba(232,131,122,0.1)'
        ))
        fig.add_hline(y=100, line_dash="dot", line_color="#F0A500", annotation_text="Max")
        fig.add_hline(y=60,  line_dash="dot", line_color="#5DB075", annotation_text="Min")
        fig.update_layout(
            height=200, plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=10,b=10),
            font=dict(family='Lato'), showlegend=False,
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(gridcolor='#F5EFE6')
        )
        st.plotly_chart(fig, use_container_width=True)

        # Upcoming appointment
        st.markdown('<div class="sec-head">📅 Next Appointment <div class="sec-line"></div></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="appt-card" style="border-color:#4EADA8;">
          <div class="appt-avatar">👩‍⚕️</div>
          <div style="flex:1;">
            <div class="appt-name">Dr. Priya Sharma</div>
            <div class="appt-spec">Cardiologist · Apollo Hospital</div>
            <div class="appt-time">⏰ Tomorrow · 10:00 AM · Room 204</div>
          </div>
          <span class="pill pill-green">Confirmed ✓</span>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MY VITALS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-head">📡 Live Vitals Feed <div class="sec-line"></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="live-pill" style="margin-bottom:0.8rem;"><span class="pulse-dot"></span> NASH SCANNING — REAL TIME</div>', unsafe_allow_html=True)

    v1,v2,v3,v4,v5 = st.columns(5)
    with v1: st.markdown(vc("🌡️","Temperature",latest['temperature'],"°C",temp_s,"#E8837A"), unsafe_allow_html=True)
    with v2: st.markdown(vc("💓","Heart Rate",int(latest['heart_rate']),"bpm",hr_s,"#E91E63"), unsafe_allow_html=True)
    with v3: st.markdown(vc("🫁","SpO₂",int(latest['spo2']),"%",spo2_s,"#4EADA8"), unsafe_allow_html=True)
    with v4: st.markdown(vc("🩺","BP",f"{int(latest['bp_sys'])}/{int(latest['bp_dia'])}","mmHg",bp_s_,"#F5A67D"), unsafe_allow_html=True)
    with v5: st.markdown(vc("📈","ECG","Normal","Sinus","Normal","#9C27B0"), unsafe_allow_html=True)

    st.markdown('<div class="warm-div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">📊 14-Day History Charts <div class="sec-line"></div></div>', unsafe_allow_html=True)

    ch1, ch2 = st.columns(2)
    def hex_to_rgba(hex_color, alpha=0.12):
        h = hex_color.lstrip('#')
        r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
        return f'rgba({r},{g},{b},{alpha})'

    def warm_chart(df, col, color, title, ymin=None, ymax=None, hlines=[]):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['datetime'], y=df[col],
            mode='lines+markers',
            line=dict(color=color, width=2.5),
            marker=dict(size=5, color=color),
            fill='tozeroy', fillcolor=hex_to_rgba(color)
        ))
        for val, lbl, lcolor in hlines:
            fig.add_hline(y=val, line_dash="dot", line_color=lcolor, annotation_text=lbl, annotation_font_size=10)
        fig.update_layout(
            title=dict(text=title, font=dict(family='Nunito', size=13, color='#2D2D2D')),
            height=220, plot_bgcolor='#FFFFFF', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=40,b=10),
            font=dict(family='Lato'), showlegend=False,
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor='#F5EFE6', range=[ymin,ymax] if ymin else None)
        )
        return fig

    with ch1:
        st.plotly_chart(warm_chart(vdf,'heart_rate','#E8837A','💓 Heart Rate (bpm)',
            hlines=[(100,'Max Normal','#F0A500'),(60,'Min Normal','#5DB075')]), use_container_width=True)
    with ch2:
        fig_bp = go.Figure()
        fig_bp.add_trace(go.Scatter(x=vdf['datetime'],y=vdf['bp_sys'],mode='lines+markers',
            name='Systolic',line=dict(color='#E8837A',width=2.5),marker=dict(size=5)))
        fig_bp.add_trace(go.Scatter(x=vdf['datetime'],y=vdf['bp_dia'],mode='lines+markers',
            name='Diastolic',line=dict(color='#4EADA8',width=2.5),marker=dict(size=5)))
        fig_bp.add_hline(y=120,line_dash="dot",line_color="#F0A500",annotation_text="Target")
        fig_bp.update_layout(title=dict(text='🩺 Blood Pressure (mmHg)',font=dict(family='Nunito',size=13,color='#2D2D2D')),
            height=220,plot_bgcolor='#FFFFFF',paper_bgcolor='white',
            margin=dict(l=10,r=10,t=40,b=10),font=dict(family='Lato'),
            xaxis=dict(showgrid=False),yaxis=dict(gridcolor='#F5EFE6'),
            legend=dict(orientation='h',yanchor='bottom',y=1.02,font=dict(size=10)))
        st.plotly_chart(fig_bp, use_container_width=True)

    ch3, ch4 = st.columns(2)
    with ch3:
        st.plotly_chart(warm_chart(vdf,'temperature','#F5A67D','🌡️ Temperature (°C)',
            hlines=[(37.2,'Fever Threshold','#E05C5C')]), use_container_width=True)
    with ch4:
        st.plotly_chart(warm_chart(vdf,'spo2','#4EADA8','🫁 SpO₂ (%)',ymin=88,ymax=102,
            hlines=[(95,'Min Normal','#F0A500')]), use_container_width=True)

    st.markdown('<div class="sec-head">🗂️ Scan History Log <div class="sec-line"></div></div>', unsafe_allow_html=True)
    disp = vdf.copy()
    disp['datetime'] = disp['datetime'].dt.strftime("%d %b %Y  %I:%M %p")
    disp.columns = ["Date & Time","Temp (°C)","Heart Rate","SpO₂ (%)","BP Sys","BP Dia"]
    st.dataframe(disp.iloc[::-1].reset_index(drop=True), use_container_width=True, height=260)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — FIND DOCTOR
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-head">🤒 How are you feeling? <div class="sec-line"></div></div>', unsafe_allow_html=True)

    symp_cols = st.columns(4)
    all_symptoms = ["Chest Pain","Shortness of Breath","Headache","Fatigue",
                    "Dizziness","Fever","Cough","Palpitations","Nausea","Joint Pain"]
    selected_symptoms = st.multiselect("Select your symptoms:", all_symptoms,
        default=["Chest Pain"] if latest['bp_sys'] > 130 else [])

    st.markdown('<div class="warm-div"></div>', unsafe_allow_html=True)

    sug_col, doc_col = st.columns([1,1.5])

    with sug_col:
        st.markdown('<div class="sec-head">🧠 AI Suggestion <div class="sec-line"></div></div>', unsafe_allow_html=True)

        suggestions = []
        if latest['bp_sys'] > 130 or "Chest Pain" in selected_symptoms or "Palpitations" in selected_symptoms:
            suggestions.append(("1","Cardiologist","👩‍⚕️",
                f"BP {int(latest['bp_sys'])}/{int(latest['bp_dia'])} mmHg is elevated" +
                (", chest pain reported" if "Chest Pain" in selected_symptoms else "")))
        if latest['spo2'] < 95 or "Shortness of Breath" in selected_symptoms or "Cough" in selected_symptoms:
            suggestions.append(("2","Pulmonologist","👨‍⚕️",
                f"SpO₂ {int(latest['spo2'])}% — respiratory assessment advised"))
        if "Headache" in selected_symptoms or "Dizziness" in selected_symptoms:
            suggestions.append(("3","Neurologist","👨‍⚕️",
                "Headache/dizziness — neurological evaluation recommended"))
        if "Fever" in selected_symptoms or latest['temperature'] > 37.5:
            suggestions.append(("2","General Physician","👩‍⚕️",
                f"Temp {latest['temperature']}°C — fever management needed"))
        if not suggestions:
            suggestions.append(("1","General Physician","👩‍⚕️",
                "Vitals are normal — routine check-up recommended"))

        for rank, spec, avatar, reason in suggestions[:3]:
            st.markdown(f"""
            <div class="sug-card">
              <div style="display:flex;align-items:center;gap:0.8rem;">
                <div class="sug-rank">#{rank}</div>
                <div style="font-size:1.5rem;">{avatar}</div>
                <div>
                  <div class="sug-spec">{spec}</div>
                  <div class="sug-why">🔍 {reason}</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

        # Vitals summary box
        st.markdown(f"""
        <div class="summary-box">
          <div style="font-size:0.72rem;color:#5A6A7A;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.5rem;">Current Vitals Summary</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.4rem;">
            <div style="font-size:0.78rem;">🌡️ Temp: <b>{latest['temperature']}°C</b></div>
            <div style="font-size:0.78rem;">💓 HR: <b>{int(latest['heart_rate'])} bpm</b></div>
            <div style="font-size:0.78rem;">🫁 SpO₂: <b>{int(latest['spo2'])}%</b></div>
            <div style="font-size:0.78rem;">🩺 BP: <b>{int(latest['bp_sys'])}/{int(latest['bp_dia'])}</b></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with doc_col:
        st.markdown('<div class="sec-head">📅 Book Appointment <div class="sec-line"></div></div>', unsafe_allow_html=True)

        suggested_spec = suggestions[0][1] if suggestions else "General Physician"
        matching = [d for d in doctors if d['spec'] == suggested_spec]
        if not matching: matching = [doctors[2]]

        sel_doc_name = st.selectbox("Choose Doctor:",
            [f"{d['avatar']} {d['name']} — {d['spec']} ({d['rating']}★)" for d in doctors])
        sel_doc = next((d for d in doctors if d['name'] in sel_doc_name), doctors[0])

        bc1, bc2 = st.columns(2)
        with bc1: appt_date = st.date_input("Date:", min_value=datetime.today())
        with bc2: slot = st.selectbox("Time Slot:", sel_doc['slots'])

        # Doctor info card
        st.markdown(f"""
        <div style="background:white;border-radius:14px;padding:1rem;border:1.5px solid #EDE8E1;margin:0.6rem 0;">
          <div style="display:flex;align-items:center;gap:0.8rem;">
            <div style="font-size:2rem;">{sel_doc['avatar']}</div>
            <div>
              <div style="font-weight:700;color:#2D2D2D;">{sel_doc['name']}</div>
              <div style="font-size:0.75rem;color:#7A7A8C;">{sel_doc['spec']} · {sel_doc['exp']} · ⭐ {sel_doc['rating']}</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        notes_input = st.text_area("Any notes for the doctor? (optional)", height=70,
            placeholder="Describe your symptoms or concerns...")

        if st.button("✅ Confirm Appointment & Set Reminder", use_container_width=True):
            st.success(f"🎉 Appointment confirmed with {sel_doc['name']} on {appt_date} at {slot}!")
            st.info("🔔 Push notification reminder will be sent 1 day & 1 hour before your appointment.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — APPOINTMENTS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-head">📅 Upcoming Appointments <div class="sec-line"></div></div>', unsafe_allow_html=True)

    upcoming = [
        {"doctor":"Dr. Priya Sharma","spec":"Cardiologist","date":"Tomorrow","time":"10:00 AM","room":"Room 204","status":"Confirmed","avatar":"👩‍⚕️"},
        {"doctor":"Dr. Kavitha Rao","spec":"General Physician","date":"12 May 2025","time":"8:30 AM","room":"Room 101","status":"Confirmed","avatar":"👩‍⚕️"},
    ]
    for a in upcoming:
        st.markdown(f"""
        <div class="appt-card">
          <div class="appt-avatar">{a['avatar']}</div>
          <div style="flex:1;">
            <div class="appt-name">{a['doctor']}</div>
            <div class="appt-spec">{a['spec']} · Apollo Hospital Bangalore</div>
            <div class="appt-time">📅 {a['date']} · ⏰ {a['time']} · 📍 {a['room']}</div>
          </div>
          <div style="text-align:right;">
            <span class="pill pill-green">{a['status']} ✓</span>
            <div style="font-size:0.7rem;color:#7A7A8C;margin-top:0.4rem;">🔔 Reminder set</div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="warm-div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">🗓️ Past Appointments <div class="sec-line"></div></div>', unsafe_allow_html=True)

    past = [
        {"doctor":"Dr. Priya Sharma","spec":"Cardiologist","date":"1 May 2025","diagnosis":"Hypertension Stage 1","avatar":"👩‍⚕️"},
        {"doctor":"Dr. Priya Sharma","spec":"Cardiologist","date":"24 Apr 2025","diagnosis":"Initial BP Assessment","avatar":"👩‍⚕️"},
        {"doctor":"Dr. Kavitha Rao", "spec":"General Physician","date":"10 Apr 2025","diagnosis":"Routine Check-up","avatar":"👩‍⚕️"},
    ]
    for p in past:
        st.markdown(f"""
        <div class="appt-card" style="opacity:0.85;">
          <div class="appt-avatar" style="background:linear-gradient(135deg,#C0C8D0,#9AA4AE);">{p['avatar']}</div>
          <div style="flex:1;">
            <div class="appt-name">{p['doctor']}</div>
            <div class="appt-spec">{p['spec']}</div>
            <div class="appt-time">📅 {p['date']}</div>
          </div>
          <div style="text-align:right;">
            <span class="pill pill-teal">{p['diagnosis']}</span>
            <div style="font-size:0.7rem;color:#7A7A8C;margin-top:0.3rem;">View Report →</div>
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — MY REPORTS
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="sec-head">📋 Medical Reports <div class="sec-line"></div></div>', unsafe_allow_html=True)

    reports = [
        {"date":"1 May 2025","doctor":"Dr. Priya Sharma","diagnosis":"Hypertension Stage 1","meds":"Amlodipine 5mg","status":"Final"},
        {"date":"24 Apr 2025","doctor":"Dr. Priya Sharma","diagnosis":"Initial BP Assessment","meds":"Lifestyle changes","status":"Final"},
        {"date":"10 Apr 2025","doctor":"Dr. Kavitha Rao", "diagnosis":"Routine Check-up","meds":"Vitamins B12","status":"Final"},
    ]
    for r in reports:
        st.markdown(f"""
        <div class="report-row">
          <div>
            <div style="font-weight:700;color:#2D2D2D;font-size:0.9rem;">📄 {r['diagnosis']}</div>
            <div style="font-size:0.75rem;color:#7A7A8C;">{r['doctor']} · {r['date']}</div>
            <div style="font-size:0.75rem;color:#4EADA8;margin-top:0.2rem;">💊 {r['meds']}</div>
          </div>
          <div style="text-align:right;">
            <span class="pill pill-green">{r['status']}</span>
            <div style="font-size:0.72rem;color:#7A7A8C;margin-top:0.3rem;">📥 Download PDF</div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="warm-div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-head">💊 Prescription History <div class="sec-line"></div></div>', unsafe_allow_html=True)

    prescriptions = [
        {"med":"Amlodipine 5mg","freq":"Once daily","dur":"30 days","doc":"Dr. Priya Sharma","date":"1 May 2025","inst":"After food. Monitor BP daily."},
        {"med":"Vitamin B12","freq":"Once daily","dur":"60 days","doc":"Dr. Kavitha Rao","date":"10 Apr 2025","inst":"With breakfast."},
    ]
    for p in prescriptions:
        st.markdown(f"""
        <div style="background:#FFFAF6;border-radius:14px;padding:1rem 1.2rem;
                    border:1.5px solid #F5EFE6;margin-bottom:0.6rem;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div>
              <div style="font-weight:700;color:#2D2D2D;font-size:0.92rem;">💊 {p['med']}</div>
              <div style="font-size:0.75rem;color:#7A7A8C;margin:0.2rem 0;">{p['doc']} · {p['date']}</div>
              <span class="pill pill-peach">{p['freq']}</span>
              <span class="pill pill-rose">{p['dur']}</span>
              <div style="font-size:0.73rem;color:#7A7A8C;margin-top:0.3rem;">📌 {p['inst']}</div>
            </div>
            <span style="font-size:0.7rem;color:#4EADA8;font-weight:700;cursor:pointer;">📄 View</span>
          </div>
        </div>""", unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div style="text-align:center;padding:1.5rem 0 0.5rem 0;
            font-size:0.72rem;color:#7A7A8C;border-top:1px solid #EDE8E1;margin-top:2rem;">
  🌿 Nash Patient Portal · Apollo Hospital Bangalore · Built with ❤️ for better healthcare
</div>
""", unsafe_allow_html=True)
