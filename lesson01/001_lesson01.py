import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("📊 地図上に3Dグラフを描画する")

# サンプルデータ（緯度、経度、人口に見立てた数値）
df = pd.DataFrame({
    'lat': [35.6812, 35.6586, 35.6277],
    'lon': [139.7671, 139.7454, 139.7786],
    'value': [500, 800, 300],  # 棒の高さや円の大きさになる数値
    'name': ['エリアA', 'エリアB', 'エリアC']
})

# Pydeckを使った地図の設定
view_state = pdk.ViewState(latitude=35.66, longitude=139.76, zoom=11, pitch=50)

layer = pdk.Layer(
    'ColumnLayer',  # 3Dの棒グラフを描画するレイヤー
    df,
    get_position='[lon, lat]',
    get_elevation='value',  # 数値に応じて棒の高さを変える
    elevation_scale=2,      # 高さの倍率
    radius=200,             # 棒の太さ
    get_fill_color='[255, 165, 0, 200]', # オレンジ色（RGBA）
    pickable=True
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{name}\n数値: {value}"}
))
