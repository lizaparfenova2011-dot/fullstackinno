from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.badge import BadgeResponse, UserBadgeResponse, CountersResponse
from app.services.badge_service import BadgeService
from app.auth import get_current_user   # используем твою зависимость

router = APIRouter(prefix="/badges", tags=["badges"])

@router.get("/", response_model=list[BadgeResponse])
def get_all_badges(db: Session = Depends(get_db)):
    """Список всех существующих наград (условия получения)."""
    service = BadgeService(db)
    return service.list_badges()

@router.get("/{badge_id}", response_model=BadgeResponse)
def get_badge(badge_id: int, db: Session = Depends(get_db)):
    """Информация о конкретной награде."""
    service = BadgeService(db)
    return service.get_badge(badge_id)

@router.get("/me/earned", response_model=list[UserBadgeResponse])
def get_my_badges(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Просмотр наград, полученных текущим пользователем."""
    service = BadgeService(db)
    return service.get_user_badges(current_user.id)

# Счётчики
@router.get("/me/counters", response_model=CountersResponse)
def get_my_counters(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Просмотр счётчиков выполненных целей по периодам (никогда не обнуляются)."""
    service = BadgeService(db)
    counters = service.get_counters(current_user.id)
    return counters
