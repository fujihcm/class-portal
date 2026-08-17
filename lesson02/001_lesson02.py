import streamlit as st
import pandas as pd
import numpy as np

st.title("🗺️ 地図プロットのデモアプリ")

# 1. サンプルデータ（緯度・経度）を作成（例：東京駅周辺）
df = pd.DataFrame({
    'latitude': [35.6812, 35.6838, 35.6795],
    'longitude': [139.7671, 139.7744, 139.7580],
    '名前': ['東京駅', '日本橋', '有楽町']
})

st.subheader("シンプルマップ")
# 2. 地図にプロット（これだけで地図が表示されます）
st.map(df)

# データの表も一緒に表示
st.subheader("プロットしたデータ一覧")
st.dataframe(df)
