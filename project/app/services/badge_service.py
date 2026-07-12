from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.badge import Badge, UserBadge
from app.repositories.badge_repository import BadgeRepository

class BadgeService:
    def __init__(self, db: Session):
        self.repository = BadgeRepository(db)

    def list_badges(self) -> list[Badge]:
        return self.repository.get_all_badges()

    def get_badge(self, badge_id: int) -> Badge:
        badge = self.repository.get_badge_by_id(badge_id)
        if not badge:
            raise HTTPException(status_code=404, detail="Badge not found")
        return badge

    def get_user_badges(self, user_id: int) -> list[UserBadge]:
        """Получить все награды, которые заработал пользователь."""
        return self.repository.get_user_badges(user_id)

    def get_counters(self, user_id: int) -> dict:
        periods = ["day", "week", "month", "year"]
        counters = {}
        for p in periods:
            count = self.repository.get_completed_count_by_period(user_id, p)
            counters[f"{p}_count"] = count
        return counters

    def check_and_award_badges(self, user_id: int) -> list[Badge]:
        """Проверяет все награды и выдаёт те, условия которых выполнены и ещё не получены."""
        badges = self.repository.get_all_badges()
        new_badges = []
        for badge in badges:
            if badge.condition_type == "period_count":
                period = badge.condition_params.get("period")
                required = badge.condition_params.get("count")
                if not period or not required:
                    continue
                # если уже есть такая награда, пропускаем
                if self.repository.has_badge(user_id, badge.id):
                    continue
                # считаем текущий счётчик
                current_count = self.repository.get_completed_count_by_period(user_id, period)
                if current_count >= required:
                    self.repository.award_badge(user_id, badge.id)
                    new_badges.append(badge)
        return new_badges
