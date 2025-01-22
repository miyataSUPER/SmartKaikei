"""
データベースモデル定義

このモジュールは、SQLAlchemyを使用して領収書データの
データベースモデルを定義します。

Author: Hiroshi Miyata
Date: 2024/12/27
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session

Base = declarative_base()


class Receipt(Base):
    """領収書データモデル"""
    __tablename__ = 'receipts'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    vendor = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(1000))
    issuer = Column(String(255), nullable=False)
    recipient = Column(String(255))
    has_revenue_stamp = Column(Boolean)
    
    # メタデータ
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    file_path = Column(String(1000))  # 元の領収書ファイルへのパス
    ocr_text = Column(String)  # OCRで抽出された生テキスト


def init_db(db_url: str = 'sqlite:///receipts.db'):
    """
    データベースの初期化

    Args:
        db_url (str): データベース接続URL
    """
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine


class DatabaseManager:
    """データベース操作マネージャー"""

    def __init__(self, session: Session):
        """
        初期化

        Args:
            session: SQLAlchemyのセッション
        """
        self.session = session


    def add_receipt(self, receipt_data: dict) -> Receipt:
        """
        領収書データの追加

        Args:
            receipt_data (dict): 領収書データ

        Returns:
            Receipt: 追加された領収書レコード
        """
        receipt = Receipt(**receipt_data)
        self.session.add(receipt)
        self.session.commit()
        return receipt


    def get_receipt(self, receipt_id: int) -> Optional[Receipt]:
        """
        領収書データの取得

        Args:
            receipt_id (int): 領収書ID

        Returns:
            Optional[Receipt]: 取得された領収書レコード
        """
        return self.session.query(Receipt).filter(Receipt.id == receipt_id).first()


    def update_receipt(self, receipt_id: int, update_data: dict) -> bool:
        """
        領収書データの更新

        Args:
            receipt_id (int): 領収書ID
            update_data (dict): 更新データ

        Returns:
            bool: 更新成功の場合True
        """
        receipt = self.get_receipt(receipt_id)
        if receipt:
            for key, value in update_data.items():
                setattr(receipt, key, value)
            self.session.commit()
            return True
        return False


    def delete_receipt(self, receipt_id: int) -> bool:
        """
        領収書データの削除

        Args:
            receipt_id (int): 領収書ID

        Returns:
            bool: 削除成功の場合True
        """
        receipt = self.get_receipt(receipt_id)
        if receipt:
            self.session.delete(receipt)
            self.session.commit()
            return True
        return False


    def search_receipts(self, **filters) -> List[Receipt]:
        """
        領収書データの検索

        Args:
            **filters: 検索フィルター
                - date_from (datetime): 開始日
                - date_to (datetime): 終了日
                - vendor (str): 販売者名（部分一致）
                - min_amount (float): 最小金額
                - max_amount (float): 最大金額

        Returns:
            list[Receipt]: 検索結果のリスト
        """
        query = self.session.query(Receipt)
        
        if 'date_from' in filters:
            query = query.filter(Receipt.date >= filters['date_from'])
        if 'date_to' in filters:
            query = query.filter(Receipt.date <= filters['date_to'])
        if 'vendor' in filters:
            query = query.filter(Receipt.vendor.ilike(f"%{filters['vendor']}%"))
        if 'min_amount' in filters:
            query = query.filter(Receipt.amount >= filters['min_amount'])
        if 'max_amount' in filters:
            query = query.filter(Receipt.amount <= filters['max_amount'])
        
        # 結果をコミット前に取得
        results = query.all()
        self.session.commit()
        return results 
