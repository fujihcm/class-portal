import streamlit as st
import os
import re  # 数字を抽出するために追加

# 🎯 【教員設定】ポータルの公開フラグ（True: 通常公開 / False: 一時停止中）
PORTAL_ACTIVE = False

# 一時停止中の処理
if not PORTAL_ACTIVE:
    st.set_page_config(page_title="授業ポータル - 一時停止中", page_icon="🛑")
    st.warning("現在、課題ポータルは一時休止中です。次回の授業時間内にお開きください。")
    st.stop()  # ここで処理を中断し、下のポータル画面を描画しない

# 表紙の設定
st.set_page_config(page_title="クラスA 課題ポータル", page_icon="🏫", layout="wide")

# ディレクトリの設定（今回は lesson01 を対象にする）
TARGET_DIR = "lesson01"
pages = []

# フォルダが存在するかチェック
if os.path.exists(TARGET_DIR):
    student_folders = sorted(os.listdir(TARGET_DIR))
    
    for folder_name in student_folders:
        # フォルダ名から数字部分だけを探して取り出す（例: "student_031" -> 31）
        match = re.search(r'\d+', folder_name)
        
        if match:
            student_num = int(match.group()) # 見つけた数字を整数（数値）に変換
            
            # 🎯 ここがクラスの振り分け条件！
            # 学生番号が 1番 〜 50番 の場合のみ処理を続ける
            if 1 <= student_num <= 50:
                app_path = os.path.join(TARGET_DIR, folder_name, "app.py")
                
                # app.py が存在したらメニューに追加
                if os.path.isfile(app_path):
                    page = st.Page(app_path, title=f"{folder_name}", icon="🧑‍🎓", url_path=folder_name)
                    pages.append(page)

# ページが1つでも見つかったら、ナビゲーションを作る
if len(pages) > 0:
    def top_page():
        st.title("🌟 クラスA - Streamlit 課題ポータル")
        st.write("左のメニューから、クラスA（学生番号1〜50）の学生の作品をプレビューできます。")
        st.info("※ クラスB（51番〜）の学生は表示されません。")
        
    intro_page = st.Page(top_page, title="ホーム", icon="🏠", default=True)
    all_pages = [intro_page] + pages
    
    pg = st.navigation(all_pages)
    pg.run()
    
else:
    st.title("🌟 クラスA - Streamlit 課題ポータル")
    st.warning(f"「{TARGET_DIR}」フォルダ内に、クラスAの提出物がまだ見つかりません。")