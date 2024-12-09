from celery_app import celery_app
from sqlalchemy import update
from models import User, UserPriceMultiplier
from database import async_session_maker
from redis_client import reset_cheat_counter

@celery_app.task
async def process_donation(user_id: int, donated_amount: int):
    async with async_session_maker() as db:
        # Обновляем пользователя атомарно
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(
                coin_balance=0,
                is_cheater=False
            )
            .returning(User.coin_balance)
        )
        result = await db.execute(stmt)
        
        # Сбрасываем множитель цен атомарно
        multiplier_stmt = (
            update(UserPriceMultiplier)
            .where(UserPriceMultiplier.user_id == user_id)
            .values(multiplier=1.0)
        )
        await db.execute(multiplier_stmt)
        
        # Сбрасываем счетчик читера в Redis
        await reset_cheat_counter(user_id)
        
        await db.commit()
        
        return {
            "donated_amount": donated_amount,
            "new_balance": 0
        } 