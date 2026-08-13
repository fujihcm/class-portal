import streamlit as st
import os, sys, importlib.util

st.set_page_config(page_title="【総合アーカイブ】ポータル", layout="wide")
st.title("📚 【総合アーカイブ】 学生アプリ 確認ポータル")

# 1. 授業回の選択（全回から選べる）
lessons = {
    "lesson01": "第1回：はじめてのStreamlit",
    "lesson02": "第2回：グラフを描いてみよう",
    "lesson03": "第3回：入力フォームを使おう"
}
selected_lesson = st.sidebar.selectbox("授業回を選んでください", options=list(lessons.keys()), format_func=lambda x: lessons[x])

# 2. 全学生の選択（1〜100番まで全て）
students = {f"student_{i:03d}": f"学生番号 {i:03d} 番" for i in range(1, 101)}
selected_student = st.sidebar.selectbox("学生を選んでください", options=list(students.keys()), format_func=lambda x: students[x])

target_app_path = os.path.join(selected_lesson, selected_student, "app.py")

if os.path.exists(target_app_path):
    st.success(f"実行中: 【{lessons[selected_lesson]}】 {students[selected_student]}")
    st.divider()
    
    sys.path.insert(0, os.path.abspath(os.path.join(selected_lesson, selected_student)))
    if "student_app" in sys.modules:
        del sys.modules["student_app"]
    try:
        spec = importlib.util.spec_from_file_location("student_app", target_app_path)
        student_app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(student_app)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
    finally:
        sys.path.pop(0)
else:
    st.info("📌 この回の提出ファイルはまだ同期されていません。")
