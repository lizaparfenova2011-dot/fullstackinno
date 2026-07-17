from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.goal import Goal
from app.repositories.goals_repository import GoalsRepository
from app.repositories.counter_repository import CounterRepository
from app.schemas.goals import GoalCreate, GoalUpdate

class GoalService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = GoalsRepository(db)
        self.counter_repo = CounterRepository(db)

    # ---------- CRUD ----------
    def list_goals(self, user_id: int) -> list[Goal]:
        return self.repository.get_all(user_id)

    def get_goal(self, goal_id: int) -> Goal:
        goal = self.repository.get_by_id(goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        return goal

    def create_goal(self, user_id: int, schema: GoalCreate) -> Goal:
        goal = Goal(
            user_id=user_id,
            name=schema.name,
            period=schema.period,
            is_pinned=schema.is_pinned,
            created_at=date.today(),
            is_completed=False,
        )
        return self.repository.create(goal)

    def update_goal(self, user_id: int, goal_id: int, schema: GoalUpdate) -> Goal:
        goal = self.get_goal(goal_id)
        if goal.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not your goal")
        update_data = schema.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(goal, field, value)
        return self.repository.update(goal)

    def delete_goal(self, user_id: int, goal_id: int) -> None:
        goal = self.get_goal(goal_id)
        if goal.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not your goal")
        self.repository.delete(goal)

    # ---------- Дополнительные функции ----------
    def list_goals_by_period(self, user_id: int, period: str) -> list[Goal]:
        if period not in ("day", "week", "month", "year"):
            raise HTTPException(status_code=422, detail="Invalid period")
        return self.repository.get_by_period(user_id, period)

    def delete_goals_by_period(self, user_id: int, period: str) -> dict:
        if period not in ("day", "week", "month", "year"):
            raise HTTPException(status_code=422, detail="Invalid period")
        deleted_count = self.repository.delete_by_period(user_id, period)
        return {"deleted_count": deleted_count, "message": f"Deleted {deleted_count} goals with period '{period}'"}

    def toggle_completed(self, user_id: int, goal_id: int) -> Goal:
        goal = self.get_goal(goal_id)
        if goal.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not your goal")

    # Переключаем статус
        goal.is_completed = not goal.is_completed

        if goal.is_completed:
            goal.completed_at = date.today()
            self.counter_repo.increment_counter(user_id, goal.period)    # увеличиваем
        else:
            goal.completed_at = None
            self.counter_repo.decrement_counter(user_id, goal.period)    # уменьшаем

        return self.repository.update(goal)

    def toggle_pinned(self, user_id: int, goal_id: int) -> Goal:
        goal = self.get_goal(goal_id)
        if goal.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not your goal")
        goal.is_pinned = not goal.is_pinned
        return self.repository.update(goal)