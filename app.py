import streamlit as st
import pandas as pd
import random
from collections import Counter
import requests

# --- 網頁設定 ---
st.set_page_config(page_title="台灣威力彩 AI 分析儀", page_icon="💰", layout="wide")

# --- CSS 美化 ---
st.markdown("""
<style>
    .ball { display: inline-block; width: 45px; height: 45px; line-height: 45px; border-radius: 50%; text-align: center; font-weight: bold; font-size: 18px; margin: 5px; color: white; box-shadow: 2px 2px 5px rgba(0,0,0,0.2); }
    .zone1 { background-color: #28a745; border: 2px solid #1e7e34; }
    .zone2 { background-color: #dc3545; border: 2px solid #bd2130; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #FF4B4B; color: white; }
</style>
""", unsafe_allow_html=True)

# --- 核心函數 ---
def generate_mock_data(rounds=100):
    data = []
    for _ in range(rounds):
        data.append({
            'z1': sorted(random.sample(range(1, 39), 6)),
            'z2': random.choice(range(1, 9))
        })
    return data

# --- 介面主程式 ---
st.title("💰 台灣威力彩 (Super Lotto) 戰情室")
st.markdown("Streamlit Cloud 雲端版 - 永久免費部署")

# 側邊欄
with st.sidebar:
    st.header("關於")
    st.info("這是一個部署在 Streamlit Cloud 上的樂透分析工具。")

# 模擬數據處理
history_data = generate_mock_data(100)
flat_z1 = [n for d in history_data for n in d['z1']]
flat_z2 = [d['z2'] for d in history_data]
c1 = Counter(flat_z1)
c2 = Counter(flat_z2)

# 儀表板
col1, col2 = st.columns(2)
with col1:
    st.subheader("🔥 第一區熱門號碼")
    chart_data = pd.DataFrame(c1.most_common(5), columns=["號碼", "次數"])
    st.bar_chart(chart_data.set_index("號碼"))

with col2:
    st.subheader("❄️ 冷門號碼")
    st.table(pd.DataFrame(c1.most_common()[:-6:-1], columns=["號碼", "次數"]))

st.divider()
st.header("🎲 AI 智慧選號產生器")

if st.button("開始計算並生成最佳注單"):
    top_10_hot = [n for n, _ in c1.most_common(10)]
    pick_hot = random.sample(top_10_hot, 3)
    remaining = [n for n in range(1, 39) if n not in pick_hot]
    pick_rand = random.sample(remaining, 3)
    final_z1 = sorted(pick_hot + pick_rand)
    final_z2 = c2.most_common(1)[0][0]
    
    html_str = "<div style='text-align:center; margin-top: 20px;'>"
    for num in final_z1:
        html_str += f"<span class='ball zone1'>{num:02d}</span>"
    html_str += f"<span style='font-size:30px; margin:0 10px;'>+</span>"
    html_str += f"<span class='ball zone2'>{final_z2:02d}</span>"
    html_str += "</div>"
    st.markdown(html_str, unsafe_allow_html=True)
    st.success("已生成最佳組合！")
