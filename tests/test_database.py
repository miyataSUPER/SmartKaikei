"""
データベース操作のテスト

Author: Hiroshi Miyata
Date: 2024/12/27
"""

import pytest
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from database.models import Receipt, DatabaseManager, init_db, Base

@pytest.fixture(scope="session")
def engine():
    """テスト用データベースエンジンの作成"""
    return init_db('sqlite:///:memory:')

@pytest.fixture(scope="function")
def db_session(engine):
    """テスト用データベースセッションの作成"""
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def db_manager(db_session):
    """DatabaseManagerのフィクスチャ"""
    return DatabaseManager(db_session)

@pytest.fixture
def sample_receipt_data():
    """サンプル領収書データ"""
    return {
        'date': datetime.now(),
        'vendor': 'テスト商店',
        'amount': 1000,
        'description': 'テスト購入',
        'issuer': 'テスト商店',
        'recipient': 'テスト太郎',
        'has_revenue_stamp': False
    }

def test_add_receipt(db_manager, sample_receipt_data):
    """領収書追加のテスト"""
    receipt = db_manager.add_receipt(sample_receipt_data)
    assert isinstance(receipt, Receipt)
    assert receipt.vendor == sample_receipt_data['vendor']
    assert receipt.amount == sample_receipt_data['amount']

def test_get_receipt(db_manager, sample_receipt_data):
    """領収書取得のテスト"""
    receipt = db_manager.add_receipt(sample_receipt_data)
    retrieved = db_manager.get_receipt(receipt.id)
    assert retrieved is not None
    assert retrieved.id == receipt.id
    assert retrieved.vendor == receipt.vendor

def test_update_receipt(db_manager, sample_receipt_data):
    """領収書更新のテスト"""
    receipt = db_manager.add_receipt(sample_receipt_data)
    update_data = {'amount': 2000}
    success = db_manager.update_receipt(receipt.id, update_data)
    assert success
    updated = db_manager.get_receipt(receipt.id)
    assert updated.amount == 2000

def test_delete_receipt(db_manager, sample_receipt_data):
    """領収書削除のテスト"""
    receipt = db_manager.add_receipt(sample_receipt_data)
    success = db_manager.delete_receipt(receipt.id)
    assert success
    deleted = db_manager.get_receipt(receipt.id)
    assert deleted is None

def test_search_receipts(db_manager, sample_receipt_data):
    """領収書検索のテスト"""
    # テストデータの追加
    db_manager.add_receipt(sample_receipt_data)
    db_manager.add_receipt({
        **sample_receipt_data,
        'amount': 2000,
        'vendor': '別のテスト商店'
    })
    
    db_manager.session.flush()  # セッションをフラッシュ

    # 金額での検索テスト
    results = db_manager.search_receipts(min_amount=1500)
    assert len(results) == 1
    assert results[0].amount == 2000

    # 販売者名での検索テスト
    results = db_manager.search_receipts(vendor='別の')
    assert len(results) == 1
    assert results[0].vendor == '別のテスト商店'

    # 複合条件での検索テスト
    results = db_manager.search_receipts(
        min_amount=500,
        vendor='テスト'
    )
    assert len(results) == 2 
