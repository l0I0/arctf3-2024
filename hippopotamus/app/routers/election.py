from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, timedelta
import pytz
from database import get_db
from models import Election, Candidate, User, Vote
from schemas import ElectionInfo, CandidateInfo
from typing import Optional
from config import ELECTION_INTERVAL_MINUTES
from auth import get_current_user

router = APIRouter(prefix="/election")

# Устанавливаем московскую временную зону
moscow_tz = pytz.timezone('Europe/Moscow')

async def get_current_election(db: AsyncSession):
    """
    Получает текущие активные выборы
    """
    now = datetime.utcnow()
    
    # Проверяем наличие активных выборов
    query = select(Election).where(
        Election.start_time <= now,
        Election.end_time > now,
        Election.finished == False
    ).order_by(Election.start_time.desc())
    
    result = await db.execute(query)
    return result.scalar_one_or_none()

@router.get("/current", response_model=Optional[ElectionInfo])
async def get_current_election_info(db: AsyncSession = Depends(get_db)):
    """
    Получение информации о текущих выборах и оставшемся времени
    """
    election = await get_current_election(db)
    if not election:
        return ElectionInfo(
            id=election.id,
            election_start=None,
            election_end=None,
            time_left=None,
            candidates=[]
        )

    now = datetime.utcnow()
    if now >= election.end_time:
        return ElectionInfo(
            id=election.id,
            election_start=None,
            election_end=None,
            time_left=None,
            candidates=[]
        )

    # Конвертируем в московское время
    msk_start = moscow_tz.fromutc(election.start_time)
    msk_end = moscow_tz.fromutc(election.end_time)
    
    # Вычисляем оставшееся время
    time_left = election.end_time - now
    minutes = time_left.seconds // 60
    seconds = time_left.seconds % 60
    time_left_str = f"{minutes} минут {seconds} секунд"

    # Получаем кандидатов
    query = select(Candidate).where(
        Candidate.election_id == election.id
    ).order_by(Candidate.votes.desc())
    result = await db.execute(query)
    candidates = result.scalars().all()

    return ElectionInfo(
        id=election.id,
        election_start=msk_start,
        election_end=msk_end,
        time_left=time_left_str,
        candidates=[CandidateInfo(
            id=c.id,
            name=c.name,
            votes=c.votes
        ) for c in candidates]
    )

async def finish_election(db: AsyncSession, election: Election) -> None:
    """
    Завершает выборы и определяет победителя.
    Для победы нужно набрать минимум 10 голосов.
    """
    query = select(Candidate).where(
        Candidate.election_id == election.id
    ).order_by(Candidate.votes.desc())
    
    result = await db.execute(query)
    candidates = result.scalars().all()
    
    # Фильтруем кандидатов, у которых минимум 10 голосов
    eligible_candidates = [c for c in candidates if c.votes >= 10]
    
    if eligible_candidates:
        max_votes = eligible_candidates[0].votes
        winners = [c for c in eligible_candidates if c.votes == max_votes]
        
        import random
        winner = random.choice(winners)
        
        stmt = (
            update(Election)
            .where(Election.id == election.id)
            .values(
                winner_id=winner.id,
                finished=True
            )
        )
        await db.execute(stmt)
    else:
        # Если нет кандидатов с достаточным количеством голосов
        stmt = (
            update(Election)
            .where(Election.id == election.id)
            .values(
                winner_id=None,
                finished=True
            )
        )
        await db.execute(stmt)
    
    await db.commit()

@router.get("/history", response_model=list[ElectionInfo])
async def get_election_history(db: AsyncSession = Depends(get_db)):
    """
    Получение истории прошедших выборов
    """
    # Получаем все завершенные выборы с победителями
    query = (
        select(Election, Candidate)
        .outerjoin(Candidate, Election.winner_id == Candidate.id)
        .where(Election.finished == True)
        .order_by(Election.end_time.desc())
    )
    
    result = await db.execute(query)
    elections_with_winners = result.unique().all()
    
    history = []
    for election_row in elections_with_winners:
        election = election_row[0]
        winner_candidate = election_row[1]
        
        # Получаем всех кандидатов для этих выборов
        candidates_query = select(Candidate).where(
            Candidate.election_id == election.id
        ).order_by(Candidate.votes.desc())
        
        candidates_result = await db.execute(candidates_query)
        candidates = candidates_result.scalars().all()
        
        msk_start = moscow_tz.fromutc(election.start_time)
        msk_end = moscow_tz.fromutc(election.end_time)
        
        winner = None
        if winner_candidate:
            winner = CandidateInfo(
                id=winner_candidate.id,
                name=winner_candidate.name,
                votes=winner_candidate.votes
            )
        
        history.append(ElectionInfo(
            id=election.id,
            election_start=msk_start,
            election_end=msk_end,
            time_left=None,
            winner=winner,
            candidates=[CandidateInfo(
                id=c.id,
                name=c.name,
                votes=c.votes
            ) for c in candidates]
        ))
    
    return history

@router.post("/nominate")
async def nominate_candidate(
    name: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Выдвинуть кандидата на текущие выборы
    """
    # Проверяем верификацию пользователя
    if not current_user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Только верифицированные пользователи могут выдвигать кандидатов"
        )
        
    # Получаем текущие выборы
    election = await get_current_election(db)
    if not election:
        raise HTTPException(
            status_code=400,
            detail="Нет активных выборов"
        )
    
    # Проверяем, не выдвигал ли уже пользователь кандидата
    query = select(Candidate).where(
        Candidate.election_id == election.id,
        Candidate.user_id == current_user.id
    )
    result = await db.execute(query)
    existing_candidate = result.scalar_one_or_none()
    
    if existing_candidate:
        raise HTTPException(
            status_code=400,
            detail="Вы уже выдвинули кандидата на эти выборы"
        )
    
    # Проверяем баланс
    if current_user.coin_balance < 200000:
        raise HTTPException(
            status_code=400,
            detail="Недостаточно монет для выдвижения кандидата (требуется 200000)"
        )
    
    try:
        # Списываем монеты
        stmt = (
            update(User)
            .where(User.id == current_user.id)
            .values(coin_balance=User.coin_balance - 200000)
            .returning(User.coin_balance)
        )
        result = await db.execute(stmt)
        new_balance = result.scalar_one()
        
        # Создаем кандидата
        new_candidate = Candidate(
            election_id=election.id,
            user_id=current_user.id,
            name=name,
            votes=0
        )
        db.add(new_candidate)
        await db.commit()
        
        return {
            "message": f"Кондидат {name} успешно выдвинут",
            "new_balance": new_balance
        }
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при выдвижении кандидата: {str(e)}"
        )

@router.post("/vote/{candidate_id}")
async def vote_for_candidate(
    candidate_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Голосование за кандидата
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Только верифицированные пользователи могут голосовать"
        )

    # Получаем кандидата
    result = await db.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Кандидат не найден"
        )

    if candidate.user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Нельзя голосовать за себя"
        )

    # Получаем текущие выборы
    election = await get_current_election(db)
    if not election or election.id != candidate.election_id:
        raise HTTPException(
            status_code=400,
            detail="Эти выборы уже завершены"
        )

    # Проверяем, не голосовал ли уже пользователь
    vote_exists = await db.execute(
        select(Vote).where(
            Vote.election_id == election.id,
            Vote.user_id == current_user.id
        )
    )
    if vote_exists.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Вы уже проголосовали в этих выборах"
        )

    try:
        # Создаем запись о голосе
        new_vote = Vote(
            election_id=election.id,
            user_id=current_user.id,
            candidate_id=candidate_id
        )
        db.add(new_vote)

        # Увеличиваем количество голосов
        stmt = (
            update(Candidate)
            .where(Candidate.id == candidate_id)
            .values(votes=Candidate.votes + 1)
            .returning(Candidate.votes)
        )
        result = await db.execute(stmt)
        new_votes = result.scalar_one()
        
        await db.commit()

        return {
            "message": f"Голос за кандидата {candidate.name} успешно учтен",
            "new_votes": new_votes
        }

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при голосовании: {str(e)}"
        )
