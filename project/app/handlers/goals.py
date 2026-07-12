from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.goals import (
    GoalCreate, GoalUpdate, GoalResponse,
    DeleteByPeriodRequest, ToggleCompletedResponse, TogglePinnedResponse
)
from app.services.goals_service import GoalService

router = APIRouter(prefix="/goals", tags=["goals"])

def get_current_user_id() -> int:
    return 1

def get_goal_service(db: Session = Depends(get_db)) -> GoalService:
    return GoalService(db)

@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(
    schema: GoalCreate,
    service: GoalService = Depends(get_goal_service),
    user_id: int = Depends(get_current_user_id)
):
    return service.create_goal(user_id, schema)

@router.get("/", response_model=list[GoalResponse])
def get_goals(
    service: GoalService = Depends(get_goal_service),
    user_id: int = Depends(get_current_user_id)
):
    return service.list_goals(user_id)

@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(
    goal_id: int,
    service: GoalService = Depends(get_goal_service),
    user_id: int = Depends(get_current_user_id)
):
    goal = service.get_goal(goal_id)
    if goal.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your goal")
    return goal

@router.patch("/{goal_id}", response_model=GoalResponse)
def update_goal(
    goal_id: int,
    schema: GoalUpdate,
    service: GoalService = Depends(get_goal_service),
    user_id: int = Depends(get_current_user_id)
):
    return service.update_goal(user_id, goal_id, schema)

@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(
    goal_id: int,
    service: GoalService = Depends(get_goal_service),
    user_id: int = Depends(get_current_user_id)
):
    service.delete_goal(user_id, goal_id)

@router.get("/period/{period}", response_model=list[GoalResponse])
def get_goals_by_period(
    period: str,
    service: GoalService = Depends(get_goal_service),
    user_id: int = Depends(get_current_user_id)
):
    return service.list_goals_by_period(user_id, period)

@router.delete("/period/{period}", response_model=dict)
def delete_goals_by_period(
    period: str,
    service: GoalService = Depends(get_goal_service),
    user_id: int = Depends(get_current_user_id)
):
    return service.delete_goals_by_period(user_id, period)

@router.patch("/{goal_id}/toggle-completed", response_model=ToggleCompletedResponse)
def toggle_completed(
    goal_id: int,
    service: GoalService = Depends(get_goal_service),
    user_id: int = Depends(get_current_user_id)
):
    goal = service.toggle_completed(user_id, goal_id)
    return ToggleCompletedResponse(
        goal_id=goal.id,
        is_completed=goal.is_completed,
        message="Goal marked as completed" if goal.is_completed else "Goal marked as not completed"
    )

@router.patch("/{goal_id}/toggle-pinned", response_model=TogglePinnedResponse)
def toggle_pinned(
    goal_id: int,
    service: GoalService = Depends(get_goal_service),
    user_id: int = Depends(get_current_user_id)
):
    goal = service.toggle_pinned(user_id, goal_id)
    return TogglePinnedResponse(
        goal_id=goal.id,
        is_pinned=goal.is_pinned,
        message="Goal pinned" if goal.is_pinned else "Goal unpinned"
    )