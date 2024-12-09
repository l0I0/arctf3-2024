from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from database import get_db
from models import User, UserPriceMultiplier
from auth import get_current_user
from schemas import CoinEarn
from redis_client import get_last_tap_amount, set_last_tap_amount, increment_cheat_counter, reset_cheat_counter, is_user_cheater

router = APIRouter()

@router.post("/tap-hippo")
async def tap_hippo(
    coin_data: CoinEarn,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        if coin_data.amount > 1_000_000:
            raise HTTPException(
                status_code=400,
                detail="Maximum amount per tap is 1,000,000 coins"
            )

        last_amount = await get_last_tap_amount(current_user.id)
        suspicious_activity = False
        multiplier_value = 1.0
        balance_reset = False
        
        if coin_data.amount - last_amount > 1:
            suspicious_activity = True
            cheat_count = await increment_cheat_counter(current_user.id)
            
            if cheat_count >= 5:
                cheater_stmt = (
                    update(User)
                    .where(User.id == current_user.id)
                    .values(is_cheater=True)
                )
                await db.execute(cheater_stmt)
                await db.commit()
                current_user.is_cheater = True
            
            if cheat_count >= 10:
                balance_stmt = (
                    update(User)
                    .where(User.id == current_user.id)
                    .values(coin_balance=0)
                )
                await db.execute(balance_stmt)
                await reset_cheat_counter(current_user.id)
                balance_reset = True
                current_user.coin_balance = 0

            try:
                # Вычисляем новый баланс
                current_balance = current_user.coin_balance or 0
                requested_amount = coin_data.amount
                new_balance = min(current_balance + requested_amount, 9_223_372_036_854_775_807)
                
                # Получаем текущий множитель пользователя
                query = select(UserPriceMultiplier).where(
                    UserPriceMultiplier.user_id == current_user.id
                )
                result = await db.execute(query)
                multiplier = result.scalar_one_or_none()
                
                # Вычисляем множитель на основе запрошенной суммы и текущего баланса
                amount_ratio = requested_amount / max(current_balance, 1)
                balance_factor = (new_balance / 1000) ** 0.3
                
                # Комбинируем факторы для итогового множителя
                new_multiplier = max(
                    1.0,
                    balance_factor * (1.0 + amount_ratio)
                )
                
                # Ограничиваем максимальным значением
                new_multiplier = min(new_multiplier, 1_000_000.0)
                
                if not multiplier:
                    multiplier = UserPriceMultiplier(
                        user_id=current_user.id,
                        multiplier=new_multiplier
                    )
                    db.add(multiplier)
                else:
                    multiplier.multiplier = max(multiplier.multiplier, new_multiplier)
                
                multiplier_value = multiplier.multiplier
                await db.commit()
                
                # Обновляем баланс пользователя
                stmt = (
                    update(User)
                    .where(User.id == current_user.id)
                    .values(coin_balance=new_balance)
                    .returning(User.coin_balance)
                )
                result = await db.execute(stmt)
                new_balance = result.scalar_one()
                await db.commit()
            except Exception as calc_error:
                multiplier_value = 1.0

        else:
            await set_last_tap_amount(current_user.id, coin_data.amount)

        if not balance_reset:
            try:
                current_balance = current_user.coin_balance or 0
                new_balance = min(current_balance + coin_data.amount, 9_223_372_036_854_775_807)
                
                stmt = (
                    update(User)
                    .where(User.id == current_user.id)
                    .values(coin_balance=new_balance)
                    .returning(User.coin_balance)
                )
                result = await db.execute(stmt)
                new_balance = result.scalar_one()
                await db.commit()
            except Exception as balance_error:
                raise HTTPException(
                    status_code=400,
                    detail="Balance calculation error. Try a smaller amount."
                )
        else:
            new_balance = 0

        response = {
            "message": f"You earned {coin_data.amount} coins!",
            "new_balance": new_balance
        }

        if suspicious_activity:
            response.update({
                "warning": "Suspicious activity detected. Prices have been increased!"
            })
            if balance_reset:
                response["message"] = "Balance has been reset due to multiple cheating attempts!"
        
        return response
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update coin balance: {str(e)}"
        )
