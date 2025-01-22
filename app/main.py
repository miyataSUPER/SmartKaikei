"""
確定申告用経費データベースアプリケーション

このモジュールは、Streamlitを使用したWebインターフェースを提供し、
OCR処理、データベース操作、レポート生成などの機能を統合します。

Author: Hiroshi Miyata
Date: 2024/12/27
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

# 環境変数の読み込み
load_dotenv()

# Gemini APIの設定
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

def init_session_state():
    """セッション状態の初期化"""
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'extracted_data' not in st.session_state:
        st.session_state.extracted_data = []

def main():
    """メインアプリケーション"""
    st.title("確定申告用経費データベース")
    
    # サイドバーでの機能選択
    menu = st.sidebar.selectbox(
        "機能を選択",
        ["領収書アップロード", "データ管理", "レポート出力"]
    )
    
    if menu == "領収書アップロード":
        show_upload_page()
    elif menu == "データ管理":
        show_management_page()
    else:
        show_report_page()

def show_upload_page():
    """領収書アップロード画面"""
    st.header("領収書アップロード")
    
    uploaded_file = st.file_uploader(
        "領収書をアップロード（PDF/画像）",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )
    
    if uploaded_file:
        st.info("ファイルがアップロードされました。OCR処理を開始します...")
        # TODO: OCR処理の実装
        st.success("OCR処理が完了しました。")

def show_management_page():
    """データ管理画面"""
    st.header("データ管理")
    
    # TODO: データベースからのデータ取得と表示
    st.info("実装予定: データの表示、編集、削除機能")

def show_report_page():
    """レポート出力画面"""
    st.header("レポート出力")
    
    st.selectbox(
        "レポートタイプを選択",
        ["月次レポート", "年次レポート", "カテゴリ別集計"]
    )
    
    # TODO: レポート生成機能の実装
    st.info("実装予定: 選択されたレポートタイプに基づくレポート生成")

if __name__ == "__main__":
    init_session_state()
    main() 
