from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.badge import Badge, UserBadge
from app.repositories.badge_repository import BadgeRepository
from app.repositories.counter_repository import CounterRepository

class BadgeService:
    def __init__(self, db: Session):
        self.repository = BadgeRepository(db)
        self.counter_repo = CounterRepository(db)

    def list_badges(self) -> list[Badge]:
        return self.repository.get_all_badges()

    def get_badge(self, badge_id: int) -> Badge:
        badge = self.repository.get_badge_by_id(badge_id)
        if not badge:
            raise HTTPException(status_code=404, detail="Badge not found")
        return badge

    def get_user_badges(self, user_id: int) -> list[UserBadge]:
        return self.repository.get_user_badges(user_id)

    def get_counters(self, user_id: int) -> dict:
        # Вот это место было ошибочным – теперь используем счётчики из отдельной таблицы
        return self.counter_repo.get_counters(user_id)

    def check_and_award_badges(self, user_id: int) -> list[Badge]:
        badges = self.repository.get_all_badges()
        new_badges = []
        counters = self.counter_repo.get_counters(user_id)
        for badge in badges:
            if badge.condition_type == "period_count":
                period = badge.condition_params.get("period")
                required = badge.condition_params.get("count")
                if not period or not required:
                    continue
                if self.repository.has_badge(user_id, badge.id):
                    continue
                current_count = counters.get(f"{period}_count", 0)
                if current_count >= required:
                    self.repository.award_badge(user_id, badge.id)
                    new_badges.append(badge)
        return new_badges