import os
import re
import streamlit as st

# 表紙の設定
st.set_page_config(
    page_title="総合アーカイブ 課題ポータル", page_icon="📚", layout="wide"
)

st.markdown("""
<style>
    /* 1. 画面全体の上下のパディングを適度に減らす（システムツールバーを避けるため4rem） */
    .block-container {
        padding-top: 4rem !important; /* 前回の2remから4remに増やして隠れるのを防ぐ */
        padding-bottom: 1rem !important;
    }
    /* 2. カラム全体の垂直配置を中央揃えにする */
    [data-testid="column"] {
        display: flex;
        align-items: center; /* これでタイトルとスイッチの高さが完璧に揃います */
    }
    /* 3. タイトル（左カラム）の上下余白をゼロにして正確に配置する */
    [data-testid="column"] > div.stMarkdown,
    [data-testid="column"] > div.stMarkdown p {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    /* 4. st.divider()（区切り線）の上下の余白を極限まで削る（前回と同じ） */
    hr {
        margin-top: 0.5rem !important;
        margin-bottom: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

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
        # コードの読み込み
        with open(target_app_path, "r", encoding="utf-8") as f:
            code = f.read()

        # カラムを [左：右] = [3：1] の割合で分割
        col1, col2 = st.columns([3, 2], vertical_alignment="center")
        with col1:
            st.write(f"**🧑‍🎓 {student_title} の作品**")
        with col2:
            # 右上にスイッチを配置
            show_code = st.toggle("💻 ソースコード")

        st.divider() # 区切り線

        if show_code:
            # スイッチON：コードを表示
            st.code(code, language="python")
        else:
            # スイッチOFF：アプリを実行
            safe_code = re.sub(r'st\.set_page_config\(.*?\)', '# disabled', code, flags=re.DOTALL)
            try:
                exec(safe_code, {"__name__": "__main__", "st": st})
            except Exception as e:
                st.error(f"エラー: {e}")
                
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
