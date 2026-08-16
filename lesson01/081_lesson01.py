import streamlit as st

# タイトルを表示
st.title("はじめてのStreamlitアプリ 🚀")

# テキストと入力フォームのテスト
st.write("Pythonのコードで作成したWebアプリケーションです！")

name = st.text_input("あなたの名前を入力してください:", "ゲスト")
st.write(f"こんにちは、{name} さん!！")

# デバッグ用：変数の中身を確認したい時は print ではなく st.write を使います
x = 10 + 20
st.write("計算結果のテスト:", x)
