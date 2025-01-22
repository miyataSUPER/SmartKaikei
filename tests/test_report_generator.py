"""
レポート生成機能のテスト

Author: Hiroshi Miyata
Date: 2024/12/27
"""

import pytest
from datetime import datetime
import pandas as pd
from database.models import Receipt
from utils.report_generator import ReportGenerator

@pytest.fixture
def sample_receipts():
    """サンプル領収書データのリスト"""
    return [
        Receipt(
            id=1,
            date=datetime(2024, 1, 15),
            vendor='テスト商店A',
            amount=1000,
            description='テスト購入1',
            issuer='テスト商店A'
        ),
        Receipt(
            id=2,
            date=datetime(2024, 1, 20),
            vendor='テスト商店B',
            amount=2000,
            description='テスト購入2',
            issuer='テスト商店B'
        ),
        Receipt(
            id=3,
            date=datetime(2024, 2, 1),
            vendor='テスト商店A',
            amount=3000,
            description='テスト購入3',
            issuer='テスト商店A'
        )
    ]

@pytest.fixture
def report_generator(sample_receipts):
    """ReportGeneratorのフィクスチャ"""
    return ReportGenerator(sample_receipts)

def test_to_dataframe(report_generator):
    """データフレーム変換のテスト"""
    df = report_generator.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert '日付' in df.columns
    assert '金額' in df.columns

def test_generate_monthly_report(report_generator):
    """月次レポート生成のテスト"""
    report = report_generator.generate_monthly_report(2024, 1)
    assert report['期間'] == '2024年1月'
    assert report['総支出額'] == 3000  # 1月の合計: 1000 + 2000
    assert report['取引件数'] == 2
    assert len(report['取引先別集計']) == 2

def test_generate_annual_report(report_generator):
    """年次レポート生成のテスト"""
    report = report_generator.generate_annual_report(2024)
    assert report['年度'] == '2024年'
    assert report['年間総支出額'] == 6000  # 全体の合計: 1000 + 2000 + 3000
    assert len(report['月別支出額']) == 2  # 1月と2月のデータ
    assert len(report['取引先別集計']) == 2  # 2つの取引先

def test_export_to_csv(report_generator, tmp_path):
    """CSV出力のテスト"""
    output_path = tmp_path / "test_report.csv"
    report_generator.export_to_csv(str(output_path))
    assert output_path.exists()
    df = pd.read_csv(output_path)
    assert len(df) == 3

def test_export_to_excel(report_generator, tmp_path):
    """Excel出力のテスト"""
    output_path = tmp_path / "test_report.xlsx"
    report_generator.export_to_excel(str(output_path))
    assert output_path.exists()
    df = pd.read_excel(output_path)
    assert len(df) == 3 
