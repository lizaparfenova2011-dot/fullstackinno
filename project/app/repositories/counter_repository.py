from sqlalchemy.orm import Session
from app.models.user_counter import UserCounter

class CounterRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_counters(self, user_id: int) -> dict:
        counters = {}
        for period in ("day", "week", "month", "year"):
            uc = self.db.query(UserCounter).filter_by(user_id=user_id, period=period).first()
            counters[f"{period}_count"] = uc.count if uc else 0
        return counters

    def increment_counter(self, user_id: int, period: str) -> None:
        uc = self.db.query(UserCounter).filter_by(user_id=user_id, period=period).first()
        if not uc:
            uc = UserCounter(user_id=user_id, period=period, count=1)
            self.db.add(uc)
        else:
            uc.count += 1
        self.db.commit()

    def decrement_counter(self, user_id: int, period: str) -> None:
        uc = self.db.query(UserCounter).filter_by(user_id=user_id, period=period).first()
        if uc and uc.count > 0:
            uc.count -= 1
            self.db.commit()