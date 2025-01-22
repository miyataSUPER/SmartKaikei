"""
OCR処理モジュールのテスト

Author: Hiroshi Miyata
Date: 2024/12/27
"""

import pytest
from unittest.mock import Mock, patch
from PIL import Image
from ocr.processor import OCRProcessor, ReceiptData

@pytest.fixture
def ocr_processor():
    """OCRProcessorのフィクスチャ"""
    with patch('ocr.processor.easyocr.Reader') as mock_reader:
        # EasyOCRのモック設定
        mock_reader.return_value.readtext.return_value = ['テスト領収書']
        with patch('ocr.processor.genai.GenerativeModel') as mock_genai:
            # Gemini APIのモック設定
            mock_genai.return_value.generate_content.return_value.text = {
                'date': '2024-01-01',
                'vendor': 'テスト商店',
                'amount': 1000,
                'description': 'テスト購入',
                'issuer': 'テスト商店'
            }
            processor = OCRProcessor()
            yield processor

@pytest.fixture
def sample_image(tmp_path):
    """サンプル画像の作成"""
    image_path = tmp_path / "sample_receipt.png"
    # テスト用の空の画像を作成
    img = Image.new('RGB', (800, 1000), color='white')
    img.save(image_path)
    return str(image_path)

def test_process_document(ocr_processor, sample_image):
    """ドキュメント処理のテスト"""
    with patch('pytesseract.image_to_string', return_value='テスト領収書'):
        result = ocr_processor.process_document(sample_image)
        assert isinstance(result, ReceiptData)
        assert hasattr(result, 'date')
        assert hasattr(result, 'amount')
        assert hasattr(result, 'vendor')

def test_process_image(ocr_processor, sample_image):
    """画像処理のテスト"""
    with patch('pytesseract.image_to_string', return_value='テスト領収書'):
        image = Image.open(sample_image)
        text = ocr_processor._process_image(image)
        assert isinstance(text, str)
        assert len(text) > 0
        assert 'テスト領収書' in text 
