import os
import re
import streamlit as st

# 🎯 【教員設定】ポータルの公開フラグ（True: 通常公開 / False: 一時停止中）
PORTAL_ACTIVE = True

# 一時停止中の処理
if not PORTAL_ACTIVE:
    st.set_page_config(page_title="授業ポータル - 一時停止中", page_icon="🛑")
    st.warning(
        "現在、課題ポータルは一時休止中です。次回の授業時間内にお開きください。"
    )
    st.stop()

# 表紙の設定
st.set_page_config(page_title="クラスA 課題ポータル", page_icon="🏫", layout="wide")

# ディレクトリの設定（対象の授業回フォルダ）
TARGET_DIR = "lesson01"
pages = []

# フォルダが存在するかチェック
if os.path.exists(TARGET_DIR):
    files = sorted(os.listdir(TARGET_DIR))

    for file_name in files:
        # ① .py 以外のファイル（隠しファイル等）を除外
        if not file_name.endswith(".py"):
            continue

        # ② ファイル名の先頭にある出席番号を取り出す（例: "031_lesson01.py" -> 31）
        match = re.match(r"^(\d+)", file_name)

        if match:
            student_num = int(match.group(1))

            # 🎯 クラスAの振り分け条件（出席番号 1番 〜 50番）
            if 1 <= student_num <= 50:
                app_path = os.path.join(TARGET_DIR, file_name)

                # ③ サイドバー表示名（student_031 形式）と URLパス（031_lesson01 形式）を生成
                title_name = f"student_{student_num:03d}"
                url_path_name = os.path.splitext(file_name)[0]

                if os.path.isfile(app_path):
                    page = st.Page(
                        app_path,
                        title=title_name,
                        icon="🧑‍🎓",
                        url_path=url_path_name,
                    )
                    pages.append(page)

# ページが見つかったらナビゲーションを生成
if len(pages) > 0:

    def top_page():
        st.title("🌟 クラスA - Streamlit 課題ポータル")
        st.write(
            "左のメニューから、クラスA（学生番号1〜50）の学生の作品をプレビューできます。"
        )
        st.info("※ クラスB（51番〜）の学生は表示されません。")

    intro_page = st.Page(top_page, title="ホーム", icon="🏠", default=True)
    all_pages = [intro_page] + pages

    pg = st.navigation(all_pages)
    pg.run()

else:
    st.title("🌟 クラスA - Streamlit 課題ポータル")
    st.warning(
        f"「{TARGET_DIR}」フォルダ内に、クラスAの提出物がまだ見つかりません。"
    )
