"""
レポート生成モジュール

このモジュールは、データベースから取得した領収書データを
CSVやPDF形式のレポートに変換します。

Author: Hiroshi Miyata
Date: 2024/12/27
"""

from datetime import datetime
from typing import List, Dict
import pandas as pd
from database.models import Receipt


class ReportGenerator:
    """レポート生成クラス"""

    def __init__(self, receipts: List[Receipt]):
        """
        初期化

        Args:
            receipts (List[Receipt]): 領収書データのリスト
        """
        self.receipts = receipts


    def to_dataframe(self) -> pd.DataFrame:
        """
        領収書データをPandasデータフレームに変換

        Returns:
            pd.DataFrame: 変換されたデータフレーム
        """
        data = []
        for receipt in self.receipts:
            data.append({
                '日付': receipt.date,
                '取引先': receipt.vendor,
                '金額': receipt.amount,
                '内容': receipt.description,
                '発行者': receipt.issuer,
                '宛名': receipt.recipient or '',
                '収入印紙': '有' if receipt.has_revenue_stamp else '無'
            })
        return pd.DataFrame(data)


    def generate_monthly_report(self, year: int, month: int) -> Dict:
        """
        月次レポートの生成

        Args:
            year (int): 対象年
            month (int): 対象月

        Returns:
            Dict: レポート集計データ
        """
        df = self.to_dataframe()
        monthly_data = df[
            (df['日付'].dt.year == year) & 
            (df['日付'].dt.month == month)
        ]

        return {
            '期間': f'{year}年{month}月',
            '総支出額': monthly_data['金額'].sum(),
            '取引件数': len(monthly_data),
            '取引先別集計': monthly_data.groupby('取引先')['金額'].sum().to_dict(),
            'データ': monthly_data
        }


    def generate_annual_report(self, year: int) -> Dict:
        """
        年次レポートの生成

        Args:
            year (int): 対象年

        Returns:
            Dict: レポート集計データ
        """
        df = self.to_dataframe()
        annual_data = df[df['日付'].dt.year == year]
        monthly_totals = annual_data.groupby(
            annual_data['日付'].dt.month
        )['金額'].sum()

        return {
            '年度': f'{year}年',
            '年間総支出額': annual_data['金額'].sum(),
            '月別支出額': monthly_totals.to_dict(),
            '取引先別集計': annual_data.groupby('取引先')['金額'].sum().to_dict(),
            'データ': annual_data
        }


    def export_to_csv(self, filepath: str) -> None:
        """
        CSVファイルとしてエクスポート

        Args:
            filepath (str): 出力先ファイルパス
        """
        df = self.to_dataframe()
        df.to_csv(filepath, index=False, encoding='utf-8-sig')


    def export_to_excel(self, filepath: str) -> None:
        """
        Excelファイルとしてエクスポート

        Args:
            filepath (str): 出力先ファイルパス
        """
        df = self.to_dataframe()
        df.to_excel(filepath, index=False, engine='openpyxl') 
