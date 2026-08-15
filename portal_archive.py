import os
import re
import streamlit as st
import streamlit.components.v1 as components

# 翻訳ポップアップを非表示
components.html(
    """
    <script>
    window.parent.document.documentElement.lang = 'ja';
    const meta = window.parent.document.createElement('meta');
    meta.name = 'google';
    meta.content = 'notranslate';
    window.parent.document.head.appendChild(meta);
    </script>
    """,
    width=0,
    height=0
)
st.markdown(
    """
    <style>
    [data-testid="stHeader"] {
        display: none !important;
    }
    footer {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 表紙の設定
st.set_page_config(
    page_title="総合アーカイブ 課題ポータル", page_icon="📚", layout="wide"
)

# 1. 授業回の選択（全回から選べるように設定）
lessons = {
    "lesson01": "第1回：はじめてのStreamlit",
    "lesson02": "第2回：グラフを描いてみよう",
    "lesson03": "第3回：入力フォームを使おう",
}


def top_page():
    st.title("📚 総合アーカイブ - Streamlit 課題ポータル")
    st.write(
        "左のメニューの各授業回セクションから、全クラスの学生の作品をプレビューできます。"
    )
    st.info("※ 提出済みの学生のファイルのみが自動的にリストアップされます。")


# ホームページの設定
intro_page = st.Page(top_page, title="ホーム", icon="🏠", default=True)

# st.navigationに渡す辞書（セクション分け用）
nav_dict = {"ホーム": [intro_page]}

# 各授業回のディレクトリを順番にチェック
for target_dir, lesson_title in lessons.items():
    pages = []

    # フォルダが存在するかチェック
    if os.path.exists(target_dir):
        files = sorted(os.listdir(target_dir))

        for file_name in files:
            # ① .py 以外のファイル（隠しファイル等）を除外
            if not file_name.endswith(".py"):
                continue

            # ② ファイル名の先頭にある出席番号を取り出す（例: "031_lesson01.py" -> 31）
            match = re.match(r"^(\d+)", file_name)

            if match:
                student_num = int(match.group(1))

                # アーカイブ用なので全クラス（1番 〜 100番）を対象にする
                if 1 <= student_num <= 100:
                    app_path = os.path.join(target_dir, file_name)

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

    # その授業回に1件でも提出ファイルが見つかった場合のみ、メニューのセクションとして追加
    if len(pages) > 0:
        nav_dict[lesson_title] = pages

# ナビゲーションの構築と実行
pg = st.navigation(nav_dict)
pg.run()
