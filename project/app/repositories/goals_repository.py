from sqlalchemy.orm import Session
from app.models.goal import Goal
from datetime import date

class GoalsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, user_id: int):
        return self.db.query(Goal).filter(Goal.user_id == user_id).all()

    def get_by_id(self, goal_id: int) -> Goal | None:
        return self.db.query(Goal).filter(Goal.id == goal_id).first()

    def create(self, goal: Goal) -> Goal:
        self.db.add(goal)
        self.db.commit()
        self.db.refresh(goal)
        return goal

    def update(self, goal: Goal) -> Goal:
        self.db.commit()
        self.db.refresh(goal)
        return goal

    def delete(self, goal: Goal) -> None:
        self.db.delete(goal)
        self.db.commit()

    def get_by_period(self, user_id: int, period: str) -> list[Goal]:
        return self.db.query(Goal).filter(
            Goal.user_id == user_id, Goal.period == period
        ).all()

    def delete_by_period(self, user_id: int, period: str) -> int:
        deleted_count = self.db.query(Goal).filter(
            Goal.user_id == user_id, Goal.period == period
        ).delete()
        self.db.commit()
        return deleted_count
