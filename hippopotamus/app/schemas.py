from pydantic import BaseModel, constr, StringConstraints, computed_field
import re
from typing import Annotated, Optional
from datetime import datetime


# Регулярное выражение для проверки username
# Разрешаем только латинские буквы, цифры, точку, дефис и нижнее подчеркивание
USERNAME_PATTERN = r"^[a-zA-Z0-9._-]+$"

class UserCreate(BaseModel):
    username: Annotated[
        str, 
        StringConstraints(
            pattern=USERNAME_PATTERN,
            min_length=1,
            max_length=32
        )
    ]
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe123",
                "password": "secretpassword"
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class CoinEarn(BaseModel):
    amount: int

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 1
            }
        }

class ShopItemBase(BaseModel):
    name: str
    description: str
    price: int

class ShopItemCreate(ShopItemBase):
    content: str
    pass

class ShopItem(ShopItemBase):
    id: int

    class Config:
        from_attributes = True

class ShopItemWithContent(ShopItem):
    content: str

    class Config:
        from_attributes = True

class PurchaseResponse(BaseModel):
    message: str
    item_content: str
    remaining_balance: int

class UserPurchaseResponse(BaseModel):
    id: int
    item_name: str
    description: str
    content: str
    purchase_date: datetime

    @computed_field
    def formatted_date(self) -> str:
        return self.purchase_date.strftime("%d.%m.%Y %H:%M")

    class Config:
        from_attributes = True

class SellResponse(BaseModel):
    message: str
    sold_item: str
    earned_amount: int
    new_balance: int

class CandidateInfo(BaseModel):
    id: int
    name: str
    votes: int
    
    class Config:
        from_attributes = True

class ElectionInfo(BaseModel):
    id: Optional[int] = None
    election_start: Optional[datetime]
    election_end: Optional[datetime]
    time_left: Optional[str]
    winner: Optional[CandidateInfo] = None
    candidates: list[CandidateInfo] = []
    
    class Config:
        from_attributes = True

