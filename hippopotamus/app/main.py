from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import pytz
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from sqlalchemy import select, update
from database import get_db
from routers.election import finish_election
from routers import router
from database import engine, Base
from models import Election
from config import ELECTION_INTERVAL_MINUTES

# Устанавливаем московскую временную зону
moscow_tz = pytz.timezone('Europe/Moscow')

app = FastAPI(
    title="Hippo Clicker API",
    description="API для игры Hippo Clicker с системой авторизации и магазином",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "system",
            "description": "Системные операции для проверки работоспособности"
        },
        {
            "name": "auth",
            "description": "Операции аутентификации и регистрации"
        },
        {
            "name": "users",
            "description": "Операции с пользователями и их данными"
        },
        {
            "name": "game",
            "description": "Игровая механика и экономика"
        },
        {
            "name": "shop",
            "description": "Магазин и покупки"
        },
        {
            "name": "election",
            "description": "Система выборов и голосования"
        }
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://176.98.173.11:39343"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Подключаем все роутеры
app.include_router(router)

@app.on_event("startup")
@repeat_every(seconds=10)
async def manage_elections() -> None:
    """
    Фоновая задача для управления выборами
    """
    async for db in get_db():
        try:
            now = datetime.utcnow()
            
            # Помечаем истекшие выборы как завершенные
            expired_query = select(Election).where(
                Election.end_time <= now,
                Election.finished == False
            )
            result = await db.execute(expired_query)
            expired_elections = result.scalars().all()
            
            for election in expired_elections:
                await finish_election(db, election)
                # Получаем победителя через relationship
                winner = election.winner
                winner_info = f"winner_id: {election.winner_id}" if election.winner_id else "no winner"
                print(f"Marking election {election.id} as finished, {winner_info}")
            
            # Проверяем наличие активных выборов
            active_query = select(Election).where(
                Election.start_time <= now,
                Election.end_time > now,
                Election.finished == False
            )
            result = await db.execute(active_query)
            active_election = result.scalar_one_or_none()
            
            # Создаем новые выборы если нет активных
            if not active_election:
                new_election = Election(
                    start_time=now,
                    end_time=now + timedelta(minutes=ELECTION_INTERVAL_MINUTES),
                    finished=False
                )
                db.add(new_election)
                await db.commit()
                print(f"Created new election at {now}")
                
        except Exception as e:
            print(f"Error in election management task: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)