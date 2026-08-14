import streamlit as st
import os

st.set_page_config(page_title="課題アーカイブ", page_icon="🗄️", layout="wide")

ARCHIVE_DIR = "archive"

# ==========================================
# 🔓 【教員用・公開設定】
# 公開したい授業回のフォルダ名をここに手動で追加してください。
# ここにリストアップされた回だけが、アーカイブポータルに表示されます。
# ==========================================
PUBLISHED_LESSONS = [
    "lesson01",
    # "lesson02",  # 公開準備ができたらコメントアウトを外す
    # "lesson03",
]

def archive_top():
    st.title("🗄️ 課題アーカイブ（過去の作品）")
    st.write("これまでに終了した、公開許可済みの授業回を閲覧できます。")
    if PUBLISHED_LESSONS:
        st.info(f"現在公開中の回: {', '.join(PUBLISHED_LESSONS)}")
    else:
        st.warning("現在公開されているアーカイブはありません。")

pages = [st.Page(archive_top, title="アーカイブTOP", icon="🏠", default=True)]

# アーカイブフォルダが存在する場合のみ処理
if os.path.exists(ARCHIVE_DIR):
    # 教員が公開設定（リストに登録）した授業回だけをループする
    for lesson in PUBLISHED_LESSONS:
        lesson_path = os.path.join(ARCHIVE_DIR, lesson)
        
        if os.path.isdir(lesson_path):
            # 該当レッスン内の学生フォルダを走査
            for student in sorted(os.listdir(lesson_path)):
                app_path = os.path.join(lesson_path, student, "app.py")
                
                if os.path.isfile(app_path):
                    # 例: LESSON01 - student_031
                    pages.append(st.Page(app_path, title=f"{lesson.upper()} - {student}", icon="📂"))

pg = st.navigation(pages)
pg.run()