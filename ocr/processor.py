"""
OCR処理モジュール

このモジュールは、TesseractとEasyOCRを使用して領収書から
テキスト情報を抽出し、Gemini APIを使用して構造化データに変換します。

Author: Hiroshi Miyata
Date: 2024/12/27
"""

import os
from typing import Dict, List, Union, Optional
import pytesseract
import easyocr
from PIL import Image
import pdf2image
import google.generativeai as genai
from pydantic import BaseModel


class ReceiptData(BaseModel):
    """領収書データモデル"""
    date: str
    vendor: str
    amount: float
    description: str
    issuer: str
    recipient: Optional[str] = None
    has_revenue_stamp: Optional[bool] = None


class OCRProcessor:
    """OCR処理クラス"""
    
    def __init__(self):
        """OCRエンジンの初期化"""
        self.reader = easyocr.Reader(['ja', 'en'])
        self.model = genai.GenerativeModel('gemini-pro-vision')


    def process_document(self, file_path: str) -> ReceiptData:
        """
        ドキュメントを処理し、領収書データを抽出する

        Args:
            file_path (str): 処理対象のファイルパス

        Returns:
            ReceiptData: 抽出された領収書データ
        """
        # 画像の読み込みと前処理
        if file_path.lower().endswith('.pdf'):
            images = self._convert_pdf_to_images(file_path)
            text = self._process_images(images)
        else:
            image = Image.open(file_path)
            text = self._process_image(image)

        # Gemini APIを使用してデータを構造化
        structured_data = self._structure_data_with_gemini(text)
        
        return ReceiptData(**structured_data)


    def _convert_pdf_to_images(self, pdf_path: str) -> List[Image.Image]:
        """PDFを画像に変換"""
        return pdf2image.convert_from_path(pdf_path)


    def _process_image(self, image: Image.Image) -> str:
        """
        単一画像のOCR処理

        Args:
            image (Image.Image): 処理対象の画像

        Returns:
            str: 抽出されたテキスト
        """
        # Tesseract OCRでの処理
        tesseract_text = pytesseract.image_to_string(
            image, lang='jpn', config='--psm 6'
        )

        # EasyOCRでの処理
        easyocr_result = self.reader.readtext(
            image, detail=0, paragraph=True
        )
        easyocr_text = '\n'.join(easyocr_result)

        # 両方の結果を組み合わせて返す
        return f"{tesseract_text}\n{easyocr_text}"


    def _process_images(self, images: List[Image.Image]) -> str:
        """複数画像の処理"""
        texts = []
        for image in images:
            texts.append(self._process_image(image))
        return '\n'.join(texts)


    def _structure_data_with_gemini(self, text: str) -> Dict:
        """
        Gemini APIを使用してテキストを構造化データに変換

        Args:
            text (str): OCRで抽出されたテキスト

        Returns:
            Dict: 構造化されたデータ
        """
        prompt = f"""
        以下の領収書テキストから必要な情報を抽出し、JSONフォーマットで返してください:
        
        {text}
        
        必要な情報:
        - date: 取引日付
        - vendor: 取引先名
        - amount: 金額（数値のみ）
        - description: 取引内容
        - issuer: 発行者名
        - recipient: 宛名（あれば）
        - has_revenue_stamp: 収入印紙の有無（確認できる場合のみtrue/false）
        """

        response = self.model.generate_content(prompt)
        # TODO: レスポンスのパースと検証
        return response.text


if __name__ == "__main__":
    # テスト用コード
    processor = OCRProcessor()
    # result = processor.process_document("test_receipt.pdf")
    # print(result) 
