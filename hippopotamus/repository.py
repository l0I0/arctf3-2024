from sqlalchemy.orm import Session
from models import TestItem
from datetime import datetime

class TestItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str) -> TestItem:
        db_item = TestItem(name=name)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def get_all(self, skip: int = 0, limit: int = 10) -> list[TestItem]:
        return self.db.query(TestItem).offset(skip).limit(limit).all()

    def check_health(self) -> dict:
        try:
            # Проверяем подключение
            self.db.execute("SELECT 1")
            
            # Проверяем возможность записи
            test_item = TestItem(name="health_check")
            self.db.add(test_item)
            self.db.commit()
            
            # Проверяем возможность чтения
            self.db.query(TestItem).filter_by(name="health_check").first()
            
            # Проверяем возможность удаления
            self.db.delete(test_item)
            self.db.commit()
            
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow(),
                "details": {
                    "connection": "ok",
                    "write": "ok",
                    "read": "ok",
                    "delete": "ok"
                }
            }
        except Exception:
            return {
                "status": "unhealthy",
                "timestamp": datetime.utcnow(),
                "details": {
                    "connection": "error",
                    "write": "error",
                    "read": "error",
                    "delete": "error"
                }
            } 