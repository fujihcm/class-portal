import streamlit as st
import os
import re  # 数字を抽出するために追加

# 表紙の設定
st.set_page_config(page_title="総合アーカイブ 課題ポータル", page_icon="📚", layout="wide")

# 1. 授業回の選択（全回から選べるように設定）
# ※授業が進むごとに教員がここを書き足してGitHubに保存（コミット）します
lessons = {
    "lesson01": "第1回：はじめてのStreamlit",
    "lesson02": "第2回：グラフを描いてみよう",
    "lesson03": "第3回：入力フォームを使おう"
}

def top_page():
    st.title("📚 総合アーカイブ - Streamlit 課題ポータル")
    st.write("左のメニューの各授業回セクションから、全クラスの学生の作品をプレビューできます。")
    st.info("※ 提出済みの学生のファイルのみが自動的にリストアップされます。")

# ホームページの設定
intro_page = st.Page(top_page, title="ホーム", icon="🏠", default=True)

# st.navigationに渡す辞書（セクション分け用）
# キーがセクション名、値がページのリストになります
nav_dict = {"ホーム": [intro_page]}

# 各授業回のディレクトリを順番にチェック
for target_dir, lesson_title in lessons.items():
    pages = []
    
    # フォルダが存在するかチェック
    if os.path.exists(target_dir):
        student_folders = sorted(os.listdir(target_dir))
        
        for folder_name in student_folders:
            # フォルダ名から数字部分だけを探して取り出す（例: "student_031" -> 31）
            match = re.search(r'\d+', folder_name)
            
            if match:
                student_num = int(match.group())
                
                # 🎯 ここがクラスの振り分け条件！
                # アーカイブ用なので、クラスA・B全員（1番 〜 100番）を対象にする
                if 1 <= student_num <= 100:
                    app_path = os.path.join(target_dir, folder_name, "app.py")
                    
                    # app.py が存在したらメニューに追加
                    if os.path.isfile(app_path):
                        page = st.Page(app_path, title=f"{folder_name}", icon="🧑‍🎓")
                        pages.append(page)
    
    # その授業回に1件でも提出ファイルが見つかった場合のみ、メニューのセクションとして追加
    if len(pages) > 0:
        nav_dict[lesson_title] = pages

# ナビゲーションの構築と実行
pg = st.navigation(nav_dict)
pg.run()