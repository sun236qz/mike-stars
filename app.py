import streamlit as st
import time
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Mike's Hero Quest", page_icon="🥁", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 25px; height: 3.5em; font-size: 18px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.05); background-color: #FFD700; }
    .task-card { padding: 18px; border-radius: 20px; background-color: #ffffff; margin-bottom: 12px; border-left: 8px solid #4CAF50; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    .star-display { font-size: 50px; color: #FFA500; text-align: center; font-weight: 900; text-shadow: 2px 2px #ffe4b5; }
    </style>
    """, unsafe_allow_html=True)

# --- Database Setup (Google Sheets or Local) ---
use_gsheets = False
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Sheet1", usecols=[0], nrows=1)
    if 'stars' not in st.session_state:
        st.session_state.stars = int(df.iloc[0, 0])
    use_gsheets = True
except Exception as e:
    # Fallback if Google Sheets is not configured yet
    if 'stars' not in st.session_state:
        st.session_state.stars = 0

def update_stars(new_total):
    st.session_state.stars = new_total
    if use_gsheets:
        try:
            new_df = pd.DataFrame({'stars': [new_total]})
            conn.update(worksheet="Sheet1", data=new_df)
        except:
            pass

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Parent Console")
    new_stars = st.number_input("Adjust Stars Manually", value=st.session_state.stars, step=1)
    if st.button("Update Total"):
        update_stars(new_stars)
        st.rerun()
    st.divider()
    st.write("💡 **Tips for Mike:**")
    st.caption("Provide immediate positive feedback! Give stars right after the task is done.")

# --- Main UI ---
st.title("🛡️ Mike's Hero Quest")
st.markdown(f"<div class='star-display'>My Energy Stars: {st.session_state.stars} ⭐</div>", unsafe_allow_html=True)

progress = min(st.session_state.stars / 100, 1.0)
st.progress(progress)
st.caption(f"✨ Only {max(100 - st.session_state.stars, 0)} stars away from the next big milestone!")

st.subheader("🚀 Daily Hero Missions")

daily_tasks = [
    ("🥁 Practice Drums", 1),
    ("🎹 Practice Piano", 1),
    ("🦁 Beast Academy", 1),
    ("📐 Mathplore", 1),
    ("📚 Reading", 1),
    ("🐉 Wukong Chinese", 1),
    ("🍚 Eat Well", 1),
    ("🪥 Brush Teeth", 1),
    ("🧹 Do Chores", 1),
    ("🏃 Exercise (30 mins)", 2),
    ("💯 Perfect Score in School", 3)
]

for task_name, star_val in daily_tasks:
    cols = st.columns([4, 1.2])
    with cols[0]:
        st.markdown(f"<div class='task-card'>{task_name}</div>", unsafe_allow_html=True)
    with cols[1]:
        if st.button(f"+{star_val} ⭐", key=task_name):
            update_stars(st.session_state.stars + star_val)
            if star_val >= 3:
                st.snow()
            else:
                st.balloons()
            st.toast(f"Awesome! You got {star_val} star(s)!")
            time.sleep(0.5)
            st.rerun()

st.markdown("---")
st.subheader("🎁 Treasure Shop")

rewards = [
    {"level": "🌈 Level 1 Reward", "cost": 10, "items": ["15 mins iPad", "Play Lego", "Other games"], "icon": "🎮"},
    {"level": "🎡 Level 2 Reward", "cost": 80, "items": ["A small gift", "Go out for a day"], "icon": "🎈"},
    {"level": "✈️ Level 3 Reward", "cost": 300, "items": ["A family trip!"], "icon": "🗺️"}
]

for r in rewards:
    with st.expander(f"{r['icon']} {r['level']} (Cost: {r['cost']} ⭐)"):
        st.markdown("**Choose your reward:**")
        for item in r['items']:
            st.write(f"• {item}")
        
        if st.session_state.stars >= r['cost']:
            if st.button(f"Claim {r['level']}", key=r['level']):
                update_stars(st.session_state.stars - r['cost'])
                st.balloons()
                st.success("Reward claimed! Great job, Mike!")
                time.sleep(1)
                st.rerun()
        else:
            st.warning(f"You need {r['cost'] - st.session_state.stars} more stars. Keep going!")
