# AI-OCR 確定申告用経費データベース

## 概要
領収書をアップロードするだけで、OCRとAIで自動的に経費データを作成・管理できるアプリケーションです。
確定申告時の経費管理を効率化し、データの正確性を向上させます。

## 特徴
- 📱 **シンプルなUI**: ドラッグ＆ドロップでかんたん操作
- 🤖 **高精度なOCR**: Tesseract + EasyOCRによるマルチエンジン処理
- 🧠 **AI解析**: Google Gemini APIによる正確な情報抽出
- 🔍 **柔軟な検索**: 日付、金額、取引先など多様な検索オプション
- 📊 **レポート機能**: 月次・年次レポートの自動生成
- 🔒 **安全性**: ローカル保存でデータを安全に管理

## 動作環境
- Docker Desktop
- 8GB以上のRAM
- Google Gemini APIキー

## クイックスタート
```bash
# リポジトリのクローン
git clone https://github.com/yourusername/AI-OCR.git
cd AI-OCR

# 環境変数の設定
cp .env.sample .env
# .envファイルを編集してGemini APIキーを設定

# Dockerイメージのビルドと起動
docker build -t ai-ocr .
docker run -p 8501:8501 -v $(pwd)/data:/app/data ai-ocr

# ブラウザでアクセス
open http://localhost:8501
```

## 使い方

### 1. 領収書のアップロード
1. 「領収書アップロード」タブを選択
2. 領収書ファイルをドラッグ＆ドロップ（または選択）
3. 「処理開始」をクリック
4. AI解析結果を確認

対応フォーマット：
- PDF形式の領収書
- 画像形式（PNG, JPEG, JPG）の領収書

### 2. データの管理
- **検索**: 日付、金額、取引先で検索
- **編集**: データの修正・更新
- **削除**: 不要データの削除
- **一括処理**: 複数領収書の一括取り込み

### 3. レポート作成
- **月次レポート**: 月間支出・取引先別集計
- **年次レポート**: 年間推移・カテゴリ別分析
- **出力形式**: CSV, Excel（カスタムフォーマット対応）

## 開発者向け情報

### コンテナ内でのテスト実行
```bash
# コンテナ内でテストを実行
docker exec -it ai-ocr pytest tests/ -v

# カバレッジレポートの生成
docker exec -it ai-ocr pytest --cov=database --cov=ocr --cov=utils tests/ -v
```

現在のテストカバレッジ:
- データベース（models.py）: 92%
- OCR処理（processor.py）: 83%
- レポート生成（report_generator.py）: 100%
- 全体カバレッジ: 90%

### ディレクトリ構造
```
AI-OCR/
├── app/              # Streamlitアプリケーション
├── database/         # データベースモデルと操作
├── ocr/             # OCR・AI処理エンジン
├── utils/           # ユーティリティ機能
├── tests/           # テストコード
├── uploads/         # アップロードファイル
└── data/            # データベース
```

## トラブルシューティング

### OCR精度の改善
- 画像は300dpi以上を推奨
- 傾きのない画像を使用
- 十分な明るさと鮮明さを確保

### よくある問題
1. Dockerの問題
   - Dockerデーモンが起動しているか確認
   - メモリ割り当ての確認（8GB以上推奨）
   - ポート8501が利用可能か確認

2. OCR/APIエラー
   - 画像品質の確認
   - Gemini APIキーの確認
   - ネットワーク接続の確認

3. データ永続化の問題
   - ボリュームマウントの確認
   - データディレクトリの権限確認
   - ディスク容量の確認

## 注意事項
- コンテナ再起動時もデータは保持されます（`data/`ディレクトリに保存）
- AI解析結果は必ず目視確認してください
- 機密情報の取り扱いに注意してください

## ライセンス
MIT License

## 作者
Hiroshi Miyata  
Mail: miyata.aistart@gmail.com



