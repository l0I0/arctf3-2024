from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from database import get_db
from models import User, ShopItem as ShopItemModel, UserPurchase, UserPriceMultiplier
from schemas import ShopItem, ShopItemCreate, PurchaseResponse, UserPurchaseResponse, SellResponse
from auth import get_current_user
from redis_client import get_cheat_counter
from datetime import datetime

router = APIRouter()

@router.get("/items", response_model=list[ShopItem])
async def get_shop_items(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получение списка товаров в магазине с учетом множителя цен пользователя.
    """
    try:
        # Проверяем, является ли пользователь читером
        cheat_count = await get_cheat_counter(current_user.id)
        is_cheater = cheat_count >= 5
        
        # Получаем множитель цен для пользователя
        query = select(UserPriceMultiplier).where(
            UserPriceMultiplier.user_id == current_user.id
        )
        result = await db.execute(query)
        multiplier = result.scalar_one_or_none()
        
        # Если пользователь читер, устанавливаем максимальный множитель
        if is_cheater:
            price_multiplier = 1_000_000.0
        else:
            price_multiplier = multiplier.multiplier if multiplier else 1.0

        # Получаем все товары
        query = select(ShopItemModel)
        result = await db.execute(query)
        items = result.scalars().all()

        # Применяем множитель к ценам
        for item in items:
            item.price = int(item.price * price_multiplier)

        return items
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get shop items: {str(e)}"
        )

@router.post("/buy/{item_id}", response_model=PurchaseResponse)
async def buy_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Покупка товара из магазина.
    """
    # Проверяем, является ли пользователь читером
    if current_user.is_cheater:
        raise HTTPException(
            status_code=403,
            detail="Cheaters are not allowed to make purchases"
        )

    try:
        # Получаем товар
        query = select(ShopItemModel).where(ShopItemModel.id == item_id)
        result = await db.execute(query)
        item = result.scalar_one_or_none()

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        # Получаем множитель цен для пользователя
        query = select(UserPriceMultiplier).where(
            UserPriceMultiplier.user_id == current_user.id
        )
        result = await db.execute(query)
        multiplier = result.scalar_one_or_none()
        final_price = int(item.price * (multiplier.multiplier if multiplier else 1.0))

        # Проверяем достаточно ли монет
        if current_user.coin_balance < final_price:
            raise HTTPException(
                status_code=400,
                detail="Not enough coins"
            )

        # Создаем запись о покупке
        purchase = UserPurchase(
            user_id=current_user.id,
            item_id=item.id,
            purchase_date=datetime.utcnow()
        )
        db.add(purchase)

        # Обновляем баланс пользователя
        current_user.coin_balance -= final_price
        await db.commit()

        return PurchaseResponse(
            message="Purchase successful",
            item_content=item.content,
            remaining_balance=current_user.coin_balance
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process purchase: {str(e)}"
        )

@router.get("/my-purchases", response_model=list[UserPurchaseResponse])
async def get_user_purchases(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получение списка покупок пользователя.
    """
    try:
        query = (
            select(
                UserPurchase.id,
                ShopItemModel.name.label("item_name"),
                ShopItemModel.description,
                ShopItemModel.content,
                UserPurchase.purchase_date
            )
            .join(ShopItemModel, UserPurchase.item_id == ShopItemModel.id)
            .where(UserPurchase.user_id == current_user.id)
            .order_by(UserPurchase.purchase_date.desc())
        )
        result = await db.execute(query)
        return result.all()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get purchases: {str(e)}"
        )

@router.post("/sell/{purchase_id}", response_model=SellResponse)
async def sell_item(
    purchase_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Продажа ранее купленного товара.
    """
    try:
        # Получаем информацию о покупке
        query = (
            select(UserPurchase, ShopItemModel)
            .join(ShopItemModel, UserPurchase.item_id == ShopItemModel.id)
            .where(
                UserPurchase.id == purchase_id,
                UserPurchase.user_id == current_user.id
            )
        )
        result = await db.execute(query)
        purchase_info = result.first()

        if not purchase_info:
            raise HTTPException(
                status_code=404,
                detail="Purchase not found or doesn't belong to you"
            )

        purchase, item = purchase_info

        # Вычисляем сумму возврата (50% от цены)
        refund_amount = item.price // 2

        # Удаляем запись о покупке
        await db.execute(
            delete(UserPurchase).where(UserPurchase.id == purchase_id)
        )

        # Обновляем баланс пользователя
        current_user.coin_balance += refund_amount
        await db.commit()

        return SellResponse(
            message="Item sold successfully",
            sold_item=item.name,
            earned_amount=refund_amount,
            new_balance=current_user.coin_balance
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to sell item: {str(e)}"
        )
