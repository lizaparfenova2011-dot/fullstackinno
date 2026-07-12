from app.database import Base, SessionLocal, engine
from app.models.goal import Goal
from app.repositories.goals_repository import GoalsRepository

Base.metadata.create_all(bind=engine)

db = SessionLocal()

repository = GoalsRepository(db)

goal = Goal(
    title="Сделать ремонт",
    time="month",
)

repository.create(goal)

goals = repository.get_all()

for goal in goals:
    print(goal.id, goal.title, goal.time)

db.close()