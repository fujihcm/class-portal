import streamlit as st
import os
import re  # 数字を抽出するために追加

# 表紙の設定
st.set_page_config(page_title="クラスB 課題ポータル", page_icon="🏫", layout="wide")

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
            # 学生番号が 51番 〜 100番 の場合のみ処理を続ける
            if 51 <= student_num <= 100:
                app_path = os.path.join(TARGET_DIR, folder_name, "app.py")
                
                # app.py が存在したらメニューに追加
                if os.path.isfile(app_path):
                    page = st.Page(app_path, title=f"{folder_name}", icon="🧑‍🎓", url_path=folder_name)
                    pages.append(page)

# ページが1つでも見つかったら、ナビゲーションを作る
if len(pages) > 0:
    def top_page():
        st.title("🌟 クラスB - Streamlit 課題ポータル")
        st.write("左のメニューから、クラスB（出席番号51〜100）の学生の作品をプレビューできます。")
        st.info("※ クラスA（1番〜50番）の学生は表示されません。")
        
    intro_page = st.Page(top_page, title="ホーム", icon="🏠", default=True)
    all_pages = [intro_page] + pages
    
    pg = st.navigation(all_pages)
    pg.run()
    
else:
    st.title("🌟 クラスB - Streamlit 課題ポータル")
    st.warning(f"「{TARGET_DIR}」フォルダ内に、クラスBの提出物がまだ見つかりません。")