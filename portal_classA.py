import streamlit as st
import os

# 表紙の設定
st.set_page_config(page_title="クラスA 課題ポータル", page_icon="🏫", layout="wide")

# ディレクトリの設定（今回は lesson01 を対象にする）
TARGET_DIR = "lesson01"
pages = []

# フォルダが存在するかチェック
if os.path.exists(TARGET_DIR):
    # lesson01 の中にあるフォルダ（student_031 など）を順番に取得
    student_folders = sorted(os.listdir(TARGET_DIR))
    
    for folder_name in student_folders:
        # app.py のパスを作る（例: lesson01/student_031/app.py）
        app_path = os.path.join(TARGET_DIR, folder_name, "app.py")
        
        # もし app.py が存在したら、ポータルのメニュー（ページ）として登録する
        if os.path.isfile(app_path):
            # メニューに表示する名前を設定（例: 「🧑‍🎓 student_031」）
            page = st.Page(app_path, title=f"{folder_name}", icon="🧑‍🎓")
            pages.append(page)

# ページが1つでも見つかったら、ナビゲーション（サイドバー）を作って実行
if len(pages) > 0:
    # --- ポータルの表紙となるページも一番上に作っておく ---
    def top_page():
        st.title("🌟 クラスA - Streamlit 課題ポータル")
        st.write("左のメニューから、学生の作品を選んでプレビューできます。")
        st.info("※ このポータルはGitHubのフォルダ構成から自動生成されています。")
        
    intro_page = st.Page(top_page, title="ホーム", icon="🏠", default=True)
    
    # ホーム画面 ＋ 学生のアプリ一覧 をメニューにセット
    all_pages = [intro_page] + pages
    
    # ナビゲーションメニューを起動！
    pg = st.navigation(all_pages)
    pg.run()
    
else:
    st.title("🌟 クラスA - Streamlit 課題ポータル")
    st.warning(f"「{TARGET_DIR}」フォルダ内に、学生の app.py がまだ見つかりません。")