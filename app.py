import streamlit as st
import time

# --- 页面配置 ---
st.set_page_config(page_title="Mike 的英雄勋章挑战", page_icon="🥁", layout="centered")

# --- 视觉样式增强 ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 25px; height: 3.5em; font-size: 18px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.05); background-color: #FFD700; }
    .task-card { padding: 18px; border-radius: 20px; background-color: #ffffff; margin-bottom: 12px; border-left: 8px solid #4CAF50; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    .star-display { font-size: 50px; color: #FFA500; text-align: center; font-weight: 900; text-shadow: 2px 2px #ffe4b5; }
    .reward-section { background-color: #fff9e6; padding: 20px; border-radius: 20px; border: 2px dashed #ffcc00; }
    </style>
    """, unsafe_allow_html=True)

# --- 数据持久化模拟 ---
if 'stars' not in st.session_state:
    st.session_state.stars = 0

# --- 侧边栏：家长管理 ---
with st.sidebar:
    st.header("⚙️ 家长控制台")
    new_stars = st.number_input("手动调整星星数量", value=st.session_state.stars)
    if st.button("更新总数"):
        st.session_state.stars = new_stars
    st.divider()
    st.write("💡 **Tips for Mike:**")
    st.caption("ADHD孩子需要即时反馈，打鼓或刷牙完请立刻让他亲手点击加星！")

# --- 主界面 ---
st.title("🛡️ Mike 的英雄成长之路")
st.markdown(f"<div class='star-display'>我的能量星星: {st.session_state.stars} ⭐</div>", unsafe_allow_html=True)

# 进度条 (设定100颗星为一个大周期的里程碑)
progress = min(st.session_state.stars / 100, 1.0)
st.progress(progress)
st.caption(f"✨ 再拿 {max(100 - st.session_state.stars, 0)} 颗星就能解锁更高级的奖励了！")

# --- 任务挑战区 ---
st.subheader("🚀 每日英雄任务")

# 任务列表：名称, 星数
daily_tasks = [
    ("🥁 练习打鼓 (热身开始！)", 1),
    ("🎹 练习钢琴 (指尖魔法)", 1),
    ("🦁 Beast Academy (数学挑战)", 1),
    ("📐 Mathplore (思维训练)", 1),
    ("📚 Reading (阅读时光)", 1),
    ("🐉 悟空中文 (中文大作战)", 1),
    ("🍚 认真吃饭 (补充能量)", 1),
    ("🪥 保护牙齿 (刷牙白白)", 1),
    ("🧹 劳动模范 (做家务)", 1),
    ("🏃 运动 30 分钟 (活力全开)", 2),
    ("💯 学校练习得满分 (黄金挑战)", 3)
]

for task_name, star_val in daily_tasks:
    cols = st.columns([4, 1.2])
    with cols[0]:
        st.markdown(f"<div class='task-card'>{task_name}</div>", unsafe_allow_html=True)
    with cols[1]:
        if st.button(f"+{star_val} ⭐", key=task_name):
            st.session_state.stars += star_val
            # 不同分数触发不同特效
            if star_val >= 3:
                st.snow() # 满分撒雪花
            else:
                st.balloons() # 普通任务喷气球
            st.toast(f"太棒了, Mike! 增加了 {star_val} 颗星！")
            time.sleep(0.5)
            st.rerun()

# --- 奖励兑换区 ---
st.markdown("---")
st.subheader("🎁 英雄宝藏商店")

rewards = [
    {
        "level": "🌈 第一级奖励", 
        "cost": 10, 
        "items": ["15分钟玩iPad", "玩乐高(Lego)", "自选其他游戏"],
        "icon": "🎮"
    },
    {
        "level": "🎡 第二级奖励", 
        "cost": 80, 
        "items": ["精美小礼物一份", "全家出门游玩一天(Go out for a day)"],
        "icon": "🎈"
    },
    {
        "level": "✈️ 第三级奖励", 
        "cost": 300, 
        "items": ["全家梦幻旅行一次"],
        "icon": "🗺️"
    }
]

for r in rewards:
    with st.expander(f"{r['icon']} {r['level']} (需 {r['cost']} ⭐)"):
        st.markdown(f"**可选奖励：**")
        for item in r['items']:
            st.write(f"• {item}")
        
        if st.session_state.stars >= r['cost']:
            if st.button(f"兑换 {r['level']}", key=r['level']):
                st.session_state.stars -= r['cost']
                st.balloons()
                st.success(f"兑换成功！Mike太棒了，去享受奖励吧！")
                time.sleep(1)
                st.rerun()
        else:
            st.warning(f"还需要 {r['cost'] - st.session_state.stars} 颗星才能兑换哦，继续加油！")
