import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go  # Added for Graphical Analysis

# --- SET PAGE CONFIG ---
st.set_page_config(page_title="AyurSafe - The Digital Vaidya", page_icon="🌿", layout="wide")

# --- CUSTOM CSS FOR AYURVEDIC THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #FDFBF7; }
    h1, h2, h3 { color: #2D5A27 !important; font-family: 'serif'; }
    .ayur-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #2D5A27;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        color: #333333;
    }
    .warning-card {
        background-color: #FFF5F5;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E53E3E;
        color: #C53030;
        font-weight: bold;
    }
    .success-card {
        background-color: #F0FFF4;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #38A169;
        color: #2F855A;
    }
    [data-testid="stSidebar"] { background-color: #E8F0E6; }
    .stButton>button {
        background-color: #2D5A27;
        color: white;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('wellness_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS profiles 
                 (id INTEGER PRIMARY KEY, name TEXT, date TEXT, 
                 dosha_result TEXT, safety_warning TEXT)''')
    conn.commit()
    conn.close()

def save_profile(name, dosha, warning):
    conn = sqlite3.connect('wellness_data.db')
    c = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO profiles (name, date, dosha_result, safety_warning) VALUES (?,?,?,?)",
              (name, date_str, dosha, warning))
    conn.commit()
    conn.close()

# --- AYURVEDIC KNOWLEDGE BASE ---
HERB_INTERACTIONS = {
    "Ashwagandha": ["Antidepressants", "Thyroid meds", "Immunosuppressants"],
    "Guggul": ["Blood thinners", "Birth control", "BP medication"],
    "Brahmi": ["Sedatives", "Alzheimer's drugs"],
    "Triphala": ["Blood thinners", "Diabetes medication"],
    "Turmeric (High Dose)": ["Blood thinners", "Diabetes medication"]
}

init_db()

# --- HEADER SECTION ---
col_h1, col_h2 = st.columns([1, 4])
with col_h1:
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913520.png", width=120)
with col_h2:
    st.title("AyurSafe: The Modern Vaidya")
    st.markdown("*Decoding Ancient Wisdom for the Modern World*")

st.markdown("---")

# --- MAIN FORM ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("📋 Phase 1: Clinical Context")
    st.markdown('<div class="ayur-card">', unsafe_allow_html=True)
    name = st.text_input("Patient Name", placeholder="e.g. Rahul Sharma")
    age = st.number_input("Age", 1, 100, 25)
    
    c1, c2 = st.columns(2)
    with c1:
        season = st.selectbox("Current Season", ["Select", "Summer (Grishma)", "Monsoon (Varsha)", "Autumn (Sharad)", "Winter (Hemant)", "Spring (Vasanta)"])
    with c2:
        climate = st.selectbox("Environment", ["Select", "Dry/Arid", "Humid/Coastal", "Cold/Mountainous", "Urban/Polluted"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("⚠️ Phase 2: Safety Screen")
    st.markdown('<div class="ayur-card">', unsafe_allow_html=True)
    modern_meds = st.multiselect(
        "Current Modern Medications (BP, Sugar, etc.):",
        ["BP medication", "Diabetes medication", "Antidepressants", "Blood thinners", "Thyroid meds", "None"]
    )
    ayurvedic_interest = st.multiselect(
        "Ayurvedic Herbs you wish to take:",
        list(HERB_INTERACTIONS.keys())
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.subheader("🔍 Phase 3: Physical Investigation")
    st.markdown('<div class="ayur-card">', unsafe_allow_html=True)
    st.write("Select current symptoms:")
    
    v_score, p_score, k_score = 0, 0, 0
    
    with st.expander("💨 Vata Symptoms (Air/Space)", expanded=True):
        if st.checkbox("Dry skin / Brittle hair"): v_score += 1
        if st.checkbox("Anxiety / Racing thoughts"): v_score += 1
        if st.checkbox("Constipation / Bloating"): v_score += 1

    with st.expander("🔥 Pitta Symptoms (Fire/Water)", expanded=True):
        if st.checkbox("Acidity / Heartburn"): p_score += 1
        if st.checkbox("Irritability / Anger"): p_score += 1
        if st.checkbox("Skin rashes / Inflammation"): p_score += 1

    with st.expander("⛰️ Kapha Symptoms (Earth/Water)", expanded=True):
        if st.checkbox("Lethargy / Excessive Sleep"): k_score += 1
        if st.checkbox("Congestion / Heavy limbs"): k_score += 1
        if st.checkbox("Slow digestion / Weight gain"): k_score += 1
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANALYSIS LOGIC ---
if st.button("GENERATE CLINICAL CONCLUSION"):
    if not name or season == "Select":
        st.error("Please complete the Patient Name and Season details.")
    else:
        st.markdown("---")
        st.header(f"Wellness Report for {name}")
        
        # 1. SAFETY ANALYSIS
        st.subheader("🛡️ Drug-Herb Interaction Analysis")
        warnings = []
        for herb in ayurvedic_interest:
            for med in modern_meds:
                if med in HERB_INTERACTIONS[herb]:
                    warnings.append(f"{herb} + {med}")
        
        if warnings:
            for w in warnings:
                st.markdown(f'<div class="warning-card">⚠️ CRITICAL: {w} interacts. Consult a doctor.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-card"> No dangerous interactions detected for the selected combinations.</div>', unsafe_allow_html=True)

        # 2. DOSHA ANALYSIS & GRAPHING
        st.subheader("Bio-Energy (Dosha) Profile")
        
        scores = {"Vata": v_score, "Pitta": p_score, "Kapha": k_score}
        dominant_dosha = max(scores, key=scores.get)
        
        # Creating Columns for Analysis and Graph
        col_res1, col_res2 = st.columns([2, 3])
        
        with col_res1:
            st.markdown(f"""
            <div class="ayur-card">
                <h3 style="margin-top:0;">Current Imbalance (Vikriti)</h3>
                <h1 style='color:#D4AF37; margin:0;'>{dominant_dosha}</h1>
                <p>Based on your environment in <b>{season}</b>, your <b>{dominant_dosha}</b> energy is currently aggravated.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Text Recommendations
            with st.expander("See Recommended Lifestyle"):
                if dominant_dosha == "Vata":
                    st.info("Warm, oily foods. Use Ghee. Practice Abhyanga.")
                elif dominant_dosha == "Pitta":
                    st.info("Cooling foods, coconut water. Avoid midday sun.")
                else:
                    st.info("Light, dry, spicy foods. Vigorous morning exercise.")

        with col_res2:
            # --- PLOTLY RADAR CHART ---
            categories = ['Vata (💨)', 'Pitta (🔥)', 'Kapha (⛰️)']
            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=[v_score, p_score, k_score, v_score], # Close the loop
                theta=categories + [categories[0]],
                fill='toself',
                name='Your Profile',
                line_color='#2D5A27',
                fillcolor='rgba(45, 90, 39, 0.4)'
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, max(scores.values()) + 1]),
                    bgcolor="rgba(0,0,0,0)"
                ),
                showlegend=False,
                margin=dict(l=40, r=40, t=20, b=20),
                height=350,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig, use_container_width=True)

        # Save to Database
        save_profile(name, dominant_dosha, "; ".join(warnings))
        st.toast("Report saved to archive.")

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.markdown("### 🏺 Patient Archive")
    if st.checkbox("Show Past Records"):
        conn = sqlite3.connect('wellness_data.db')
        df = pd.read_sql_query("SELECT name, dosha_result, date FROM profiles", conn)
        st.dataframe(df)
        conn.close()
    
    st.markdown("---")
    st.caption("Shariram Aadyam Khalu Dharma Saadhanam")
    st.caption("The body is the primary instrument of life.")