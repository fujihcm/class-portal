import os
import re
import streamlit as st

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


# ==========================================
# 🌟 追加：学生のページを描画する関数（タブと実行機能）
# ==========================================
def create_student_page(student_title, target_app_path):
    def render_page():
        st.markdown(f"🧑‍🎓 {student_title} の作品")
        tab1, tab2 = st.tabs(["🚀 アプリ", "💻 ソースコード"])
        
        # ソースコードの読み込み
        with open(target_app_path, "r", encoding="utf-8") as f:
            code = f.read()

        # 【タブ1】 アプリの実行
        with tab1:
            try:
                # ※ st.set_page_configが複数回呼ばれるとエラーになるため、
                # 学生のコード内に含まれていた場合は無効化(コメントアウト)して実行する安全対策
                safe_code = re.sub(r'st\.set_page_config\(.*?\)', '# st.set_page_config (disabled)', code, flags=re.DOTALL)
                
                # exec() を使うと、現在のタブ(tab1)の中に学生のアプリがレンダリングされます
                exec(safe_code, {"__name__": "__main__", "st": st})
            except Exception as e:
                st.error(f"アプリの実行中にエラーが発生しました: {e}")

        # 【タブ2】 ソースコードの表示
        with tab2:
            st.code(code, language="python")
            
    return render_page
# ==========================================


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

            # ② ファイル名の先頭にある出席番号を取り出す
            match = re.match(r"^(\d+)", file_name)

            if match:
                student_num = int(match.group(1))

                # アーカイブ用なので全クラス（1番 〜 100番）を対象にする
                if 1 <= student_num <= 100:
                    app_path = os.path.join(target_dir, file_name)

                    # ③ サイドバー表示名と URLパスを生成
                    title_name = f"student_{student_num:03d}"
                    url_path_name = os.path.splitext(file_name)[0]

                    if os.path.isfile(app_path):
                        # 🌟 変更点：ファイルパスではなく、描画関数を生成して渡す
                        page_func = create_student_page(title_name, app_path)
                        
                        page = st.Page(
                            page_func,  # <- 関数を渡す
                            title=title_name,
                            icon="🧑‍🎓",
                            url_path=url_path_name,
                        )
                        pages.append(page)

    # その授業回に1件でも提出ファイルが見つかった場合のみ追加
    if len(pages) > 0:
        nav_dict[lesson_title] = pages

# ナビゲーションの構築と実行
pg = st.navigation(nav_dict)
pg.run()
