# AI-OCR 確定申告用経費データベース

作成日: 2024/12/27
更新日: 2024/01/22

## 概要
領収書をアップロードするだけで、OCRとAIで自動的に経費データを作成・管理できるアプリです。
確定申告の経費管理をラクにします。

## 主な機能

### 1. 領収書の自動読み取り
- **対応フォーマット**
  - PDF形式の領収書
  - 画像形式（PNG, JPEG, JPG）の領収書
- **OCR機能**
  - Tesseract OCRと EasyOCRを組み合わせた高精度な日本語認識
  - 画像の自動前処理（傾き補正、ノイズ除去）
- **AI解析**
  - Google Gemini APIによる情報抽出
  - 以下の項目を自動認識：
    - 取引日付
    - 取引先名
    - 金額
    - 取引内容
    - 発行者名
    - 宛名（オプション）
    - 収入印紙の有無

### 2. データベース管理
- **保存機能**
  - SQLiteデータベースによる安全な保存
  - OCRテキストの原文も保持
- **検索・編集機能**
  - 日付範囲による検索
  - 取引先名によるあいまい検索
  - 金額範囲による絞り込み
  - データの編集・削除
- **一括処理**
  - 複数領収書の一括取り込み
  - 一括エクスポート

### 3. レポート機能
- **月次レポート**
  - 月間支出合計
  - 取引先別集計
  - 取引件数集計
- **年次レポート**
  - 年間支出合計
  - 月別推移グラフ
  - 取引先別年間集計
- **出力形式**
  - CSV形式（UTF-8）
  - Excel形式（.xlsx）
  - カスタムフォーマット対応

## セットアップ手順

### 1. 必要な環境
- Python 3.9以上
- Docker Desktop（オプション）
- Google Gemini APIアカウント
- 8GB以上のRAM推奨

### 2. インストール
```bash
# リポジトリのクローン
git clone https://github.com/yourusername/AI-OCR.git
cd AI-OCR

# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt

# 環境変数の設定
cp .env.sample .env
# .envファイルを編集してGemini APIキーを設定
```

### 3. 起動方法
#### ローカル実行
```bash
# アプリケーションの起動
streamlit run app/main.py

# ブラウザでアクセス
open http://localhost:8501
```

#### Docker実行
```bash
# Dockerイメージのビルド
docker build -t ai-ocr .

# コンテナの起動
docker run -p 8501:8501 -v $(pwd)/data:/app/data ai-ocr
```

## テスト実行
```bash
# 全テストの実行
pytest tests/ -v

# カバレッジレポートの生成
pytest --cov=database --cov=ocr --cov=utils tests/ -v
```

### テストカバレッジ
- データベース（models.py）: 92%
- OCR処理（processor.py）: 83%
- レポート生成（report_generator.py）: 100%
- 全体カバレッジ: 90%

## 環境設定詳細

### 1. 環境変数（.env）
```
# API設定
GEMINI_API_KEY=your_api_key_here  # Google Gemini APIキー

# データベース設定
DATABASE_URL=sqlite:///receipts.db  # SQLiteデータベースのパス

# OCR設定
TESSERACT_PATH=/usr/bin/tesseract  # Tesseractの実行パス
TESSERACT_LANG=jpn                 # 日本語モデルを使用

# アプリケーション設定
DEBUG=false                        # デバッグモードの有効/無効
UPLOAD_FOLDER=./uploads           # アップロードファイルの保存先
MAX_CONTENT_LENGTH=16777216       # 最大アップロードサイズ（16MB）
```

### 2. ディレクトリ構造
```
AI-OCR/
├── app/              # メインアプリケーション
│   └── main.py      # Streamlitアプリケーション
├── database/         # データベース関連
│   └── models.py    # SQLAlchemyモデル
├── ocr/             # OCR処理モジュール
│   └── processor.py # OCR処理クラス
├── utils/           # ユーティリティ
│   └── report_generator.py # レポート生成
├── tests/           # テストコード
├── uploads/         # アップロードファイル保存先
├── data/            # データベースファイル
├── Dockerfile       # Dockerビルド設定
├── requirements.txt # Python依存パッケージ
└── README.md        # このファイル
```

## 使用方法

### 1. 領収書のアップロード
1. ブラウザで`http://localhost:8501`にアクセス
2. 「領収書アップロード」タブを選択
3. ファイルをドラッグ＆ドロップまたは選択
4. 「処理開始」ボタンをクリック

### 2. データの確認・編集
1. 「データ管理」タブを選択
2. 一覧から対象データを選択
3. 必要に応じて編集・削除

### 3. レポート出力
1. 「レポート出力」タブを選択
2. レポートタイプ（月次/年次）を選択
3. 期間を指定
4. 出力形式を選択してダウンロード

## 注意事項
- **OCRの精度について**
  - 画像は300dpi以上推奨
  - 傾きのない画像が最適
  - 手書き文字は認識精度が低下する可能性あり
- **データの確認**
  - AI解析結果は必ずご確認ください
  - 特に金額は要確認
- **バックアップ**
  - 定期的なデータベースのバックアップを推奨

## トラブルシューティング
1. OCRが正しく動作しない場合
   - 画像の品質を確認
   - Tesseractの日本語モデルが正しくインストールされているか確認

2. APIエラーが発生する場合
   - Gemini APIキーの設定を確認
   - APIの利用制限を確認

## 開発状況
- [x] データベース機能
- [x] OCR処理機能
- [x] レポート生成機能
- [x] 基本的なテスト実装
- [ ] エラーケースのテスト追加
- [ ] UI/UXの改善
- [ ] パフォーマンスの最適化

## ライセンス
MIT License

## 作者
Hiroshi Miyata
Mail: miyata.aistart@gmail.com

