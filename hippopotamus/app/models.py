from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, UniqueConstraint
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)
    telegram_id = Column(String, nullable=True)
    coin_balance = Column(Integer, default=0)
    is_cheater = Column(Boolean, default=False)

class ShopItem(Base):
    __tablename__ = "shop_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Integer)
    content = Column(String) 
    
class UserPurchase(Base):
    __tablename__ = "user_purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("shop_items.id"))
    purchase_date = Column(DateTime, default=datetime.utcnow)

class UserPriceMultiplier(Base):
    __tablename__ = "user_price_multipliers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    multiplier = Column(Float, default=1.0)  # Множитель цены для пользователя
    last_update = Column(DateTime, default=datetime.utcnow)

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    election_id = Column(Integer, ForeignKey("elections.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    votes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    election = relationship("Election", back_populates="candidates", foreign_keys=[election_id])
    user = relationship("User")

class Election(Base):
    __tablename__ = "elections"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    winner_id = Column(Integer, ForeignKey("candidates.id"), nullable=True)
    finished = Column(Boolean, default=False)
    
    candidates = relationship("Candidate", back_populates="election", 
                            foreign_keys=[Candidate.election_id])
    winner = relationship("Candidate", foreign_keys=[winner_id],
                         primaryjoin="Election.winner_id == Candidate.id")

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    election_id = Column(Integer, ForeignKey('elections.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    
    __table_args__ = (
        UniqueConstraint('election_id', 'user_id', name='one_vote_per_election'),
    )
