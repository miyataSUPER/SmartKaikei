# ベースイメージとしてPython 3.9を使用
FROM python:3.9-slim

# 日本語フォントとTesseract OCRのインストール
RUN apt-get update && apt-get install -y \
    fonts-noto-cjk \
    tesseract-ocr \
    tesseract-ocr-jpn \
    libgl1-mesa-glx \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの設定
WORKDIR /app

# 依存パッケージのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY . .

# 環境変数の設定
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Streamlitのポート設定
EXPOSE 8501

# アプリケーションの起動
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"] 
