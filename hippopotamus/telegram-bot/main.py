from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from environs import Env
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, Column, Integer, String, Boolean, update, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Загружаем переменные окружения
env = Env()
env.read_env()

# Конфигурация
BOT_TOKEN = env("TELEGRAM_BOT_TOKEN")
DATABASE_URL = env("POSTGRES_URL_ASYNC")

# Инициализация базы данных
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Модели
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)
    telegram_id = Column(String, nullable=True)

class Election(Base):
    __tablename__ = "elections"
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    winner_id = Column(Integer, ForeignKey('candidates.id'), nullable=True)
    finished = Column(Boolean, default=False)

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True)
    election_id = Column(Integer)
    user_id = Column(Integer)
    name = Column(String)
    votes = Column(Integer, default=0)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем клавиатуру с обычными кнопками
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            # [KeyboardButton(text="👥 Список пользователей")],
            [KeyboardButton(text="✅ Верификация")],
            [KeyboardButton(text="🗳 Мои кандидаты")],
            [KeyboardButton(text="🏆 Получить приз")]
        ],
        resize_keyboard=True
    )
    return keyboard

@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я бот для верификации пользователей.\n"
        "Чтобы пройти верификацию, нажмите кнопку '✅ Верификация' "
        "и введите код, который вы получили при регистрации.",
        reply_markup=get_main_keyboard()
    )

@dp.message(lambda message: message.text == "✅ Верификация") 
async def start_verification(message: types.Message):
    await message.reply(
        "Для верификации введите команду /verify и ваш код.\n"
        "Например: /verify ABC123"
    )

@dp.message(Command(commands=['verify']))
async def verify_user(message: types.Message):
    try:
        # Получаем код из сообщения
        code = message.text.split()[1]
        telegram_id = str(message.from_user.id)
        
        async with async_session() as session:
            # Проверяем, не использовался ли уже этот Telegram ID
            existing_user = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            if existing_user.scalar_one_or_none():
                await message.reply(
                    "❌ Этот Telegram аккаунт уже привязан к другому пользователю.\n"
                    "Один Telegram аккаунт можно использовать только для одной верификации."
                )
                return
            
            # Ищем пользователя с таким кодом верификации
            result = await session.execute(
                select(User).where(User.verification_code == code)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                await message.reply(
                    "❌ Неверный код верификации.\n"
                    "Проверьте код и попробуйте снова."
                )
                return
            
            if user.is_verified:
                await message.reply("✅ Этот аккаунт уже верифицирован!")
                return
            
            # Обновляем пользователя
            stmt = (
                update(User)
                .where(User.id == user.id)
                .values(
                    is_verified=True,
                    telegram_id=telegram_id,
                    verification_code=None  # Очищаем код после использования
                )
            )
            await session.execute(stmt)
            await session.commit()
            
            await message.reply(
                "🎉 Поздравляем! Верификация успешно пройдена!\n"
                "Теперь у вас есть доступ ко всем функциям."
            )
            
    except IndexError:
        await message.reply(
            "❌ Неправильный формат команды.\n"
            "Используйте: /verify КОД_ВЕРИФИКАЦИИ"
        )
    except Exception as e:
        print(f"Error: {e}")  # Для отладки
        await message.reply("Произошла ошибка. Попробуйте позже.")

@dp.message(Command(commands=['users']))
async def show_users(message: types.Message):
    async with async_session() as session:
        # Получаем всех пользователей
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        if not users:
            await message.reply("Пока нет зарегистрированных пользователей.")
            return
        
        # Формируем сообщение со списком пользователей
        users_text = "Список пользователей:\n\n"
        for user in users:
            verified_status = "✅" if user.is_verified else "❌"
            users_text += f"ID: {user.id}\n"
            users_text += f"Имя: {user.username}\n"
            users_text += f"Верификация: {verified_status}\n"
            users_text += f"Telegram ID: {user.telegram_id or 'Не привязан'}\n"
            users_text += "-------------------\n"
        
        await message.reply(users_text)

# @dp.message(lambda message: message.text == "👥 Список пользователей")
# async def handle_users_button(message: types.Message):
#     await show_users(message)

@dp.message(lambda message: message.text == "🗳 Мои кандидаты")
async def show_my_candidates(message: types.Message):
    async with async_session() as session:
        # Получаем пользователя по telegram_id
        result = await session.execute(
            select(User).where(User.telegram_id == str(message.from_user.id))
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await message.reply("Вы не привязали свой аккаунт к боту.")
            return
            
        # Получаем всех кандидатов пользователя
        result = await session.execute(
            select(Candidate).where(Candidate.user_id == user.id)
            .order_by(Candidate.election_id.desc())
        )
        candidates = result.scalars().all()
        
        if not candidates:
            await message.reply("У вас пока нет выдвинутых кандидатов.")
            return
            
        # Формируем сообщение со списком кандидатов
        text = "Ваши кандидаты:\n\n"
        for candidate in candidates:
            text += f"ID выборов: {candidate.election_id}\n"
            text += f"Имя кандидата: {candidate.name}\n"
            text += f"Голосов: {candidate.votes}\n"
            text += "-------------------\n"
            
        await message.reply(text)

@dp.message(lambda message: message.text == "🏆 Получить приз")
async def get_prize(message: types.Message):
    async with async_session() as session:
        # Получаем пользователя по telegram_id
        result = await session.execute(
            select(User).where(User.telegram_id == str(message.from_user.id))
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await message.reply("Вы не привязали свой аккаунт к боту.")
            return
            
        # Получаем последнего победившего кандидата пользователя
        result = await session.execute(
            select(Candidate)
            .join(Election, Election.winner_id == Candidate.id)
            .where(
                Candidate.user_id == user.id,
                Election.finished == True
            )
            .order_by(Election.end_time.desc())
            .limit(1)
        )
        winning_candidate = result.scalar_one_or_none()
        
        if not winning_candidate:
            await message.reply("У вас пока нет победивших кандидатов.")
            return
            
        # Отправляем приз
        await message.reply(
            "🎉 Поздравляем с победой!\n"
            "Ваш приз: arctf{w1nn3r_0f_th3_3l3ct10n}\n\n"
            f"Победивший кандидат: {winning_candidate.name}"
        )

async def main():
    # Создаем таблицы при запуске (если они еще не существуют)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())