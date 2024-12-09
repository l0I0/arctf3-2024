from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from database import get_db
from models import User, UserPriceMultiplier
from auth import get_current_user
import random
from redis_client import reset_cheat_counter

router = APIRouter()

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Получение информации о текущем пользователе.
    """
    return {
        "username": current_user.username,
        "is_verified": current_user.is_verified,
        "telegram_id": current_user.telegram_id
    }

@router.post("/unlink-telegram")
async def unlink_telegram(
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    try:
        if not current_user.telegram_id:
            raise HTTPException(
                status_code=400,
                detail="Telegram account is not linked"
            )
        
        stmt = (
            update(User)
            .where(User.id == current_user.id)
            .values(
                telegram_id=None,
                is_verified=False
            )
        )
        await db.execute(stmt)
        await db.commit()
        
        return {
            "message": "Telegram account successfully unlinked",
            "username": current_user.username,
            "is_verified": False
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to unlink Telegram account: {str(e)}"
        )

@router.get("/balance")
async def get_balance(current_user: User = Depends(get_current_user)):
    return {
        "coin_balance": current_user.coin_balance
    }

@router.post("/generate-verification-code")
async def generate_verification_code(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Генерация нового 6-символьного кода подтверждения для пользователя.
    """
    try:
        if current_user.is_verified:
            raise HTTPException(
                status_code=400,
                detail="Пользователь уже подтвержден"
            )

        # Генерируем случайный 6-значный код из букв и цифр
        letters_and_digits = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        verification_code = ''.join(random.choices(letters_and_digits, k=6))

        # Обновляем код верификации пользователя
        stmt = (
            update(User)
            .where(User.id == current_user.id)
            .values(verification_code=verification_code)
        )
        await db.execute(stmt)
        await db.commit()

        return {
            "message": "Код подтверждения успешно сгенерирован",
            "verification_code": verification_code
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при генерации кода подтверждения: {str(e)}"
        )

@router.post("/donate", response_model=dict)
async def donate_coins(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Пожертвовать все монеты, снять статус читера и сбросить множитель цен
    """
    try:
        if current_user.coin_balance <= 0:
            raise HTTPException(
                status_code=400,
                detail="You don't have any coins to donate"
            )

        donated_amount = current_user.coin_balance

        # Обновляем пользователя: обнуляем баланс и убираем статус читера
        stmt = (
            update(User)
            .where(User.id == current_user.id)
            .values(
                coin_balance=0,
                is_cheater=False
            )
        )
        await db.execute(stmt)
        
        # Сбрасываем множитель цен
        multiplier_stmt = (
            update(UserPriceMultiplier)
            .where(UserPriceMultiplier.user_id == current_user.id)
            .values(multiplier=1.0)
        )
        await db.execute(multiplier_stmt)
        
        # Сбрасываем счетчик читера в Redis
        await reset_cheat_counter(current_user.id)
        
        await db.commit()

        return {
            "message": "Thank you for your donation! Your cheater status and price multiplier have been reset",
            "donated_amount": donated_amount,
            "new_balance": 0
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process donation: {str(e)}"
        )
