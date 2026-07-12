from sqlalchemy.orm import Session
from app.models.badge import Badge, UserBadge
from app.models.goal import Goal

class BadgeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_badges(self) -> list[Badge]:
        return self.db.query(Badge).all()

    def get_badge_by_id(self, badge_id: int) -> Badge | None:
        return self.db.query(Badge).filter(Badge.id == badge_id).first()

    def get_user_badges(self, user_id: int) -> list[UserBadge]:
        """Возвращает все полученные пользователем награды с информацией о самой награде."""
        return self.db.query(UserBadge).filter(UserBadge.user_id == user_id).all()

    def has_badge(self, user_id: int, badge_id: int) -> bool:
        return self.db.query(UserBadge).filter(
            UserBadge.user_id == user_id, UserBadge.badge_id == badge_id
        ).first() is not None

    def award_badge(self, user_id: int, badge_id: int) -> UserBadge:
        user_badge = UserBadge(user_id=user_id, badge_id=badge_id)
        self.db.add(user_badge)
        self.db.commit()
        self.db.refresh(user_badge)
        return user_badge

    # Подсчёт выполненных целей по периоду
    def get_completed_count_by_period(self, user_id: int, period: str) -> int:
        return self.db.query(Goal).filter(
            Goal.user_id == user_id,
            Goal.period == period,
            Goal.is_completed == True
        ).count()
