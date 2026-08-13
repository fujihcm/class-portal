import streamlit as st
import os, sys, importlib.util

st.set_page_config(page_title="【クラスA】ポータル", layout="wide")
st.title("🖥️ 【クラスA】 動作確認ポータル")
st.sidebar.markdown("[🔗 アーカイブ用ページへ](アーカイブ用のURLを記載)")

# ================================
# 設定（授業ごとにここを書き換えてGitHubにPush）
TARGET_LESSON = "lesson01"
# ================================

st.sidebar.markdown(f"**現在の対象: {TARGET_LESSON}**")

# クラスAの学生番号（例: 001〜050）
students = {f"student_{i:03d}": f"学生番号 {i:03d} 番" for i in range(1, 51)}
selected_student = st.sidebar.selectbox("学生を選んでください", options=list(students.keys()), format_func=lambda x: students[x])

target_app_path = os.path.join(TARGET_LESSON, selected_student, "app.py")

if os.path.exists(target_app_path):
    st.success(f"実行中: {students[selected_student]} のアプリ")
    st.divider()
    
    # 動的にアプリを読み込んで実行
    sys.path.insert(0, os.path.abspath(os.path.join(TARGET_LESSON, selected_student)))
    if "student_app" in sys.modules:
        del sys.modules["student_app"] # キャッシュクリア
    try:
        spec = importlib.util.spec_from_file_location("student_app", target_app_path)
        student_app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(student_app)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
    finally:
        sys.path.pop(0)
else:
    st.info("📌 まだ提出されていないか、同期されていません。")
