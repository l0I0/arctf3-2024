"""items

Revision ID: 3c811526e7fa
Revises: 547f17d21642
Create Date: 2024-11-28 02:21:49.324536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c811526e7fa'
down_revision: Union[str, None] = '547f17d21642'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None




def upgrade() -> None:
    op.execute("""
        INSERT INTO shop_items (name, description, price, content) VALUES
        (
            'Бегемот с флагом',
            'Редкий бегемот, держащий загадочный флаг. Говорят, в нем скрыт секрет...',
            500000,
            'arctf{h1pp0_w1th_fl4g-2025}'
        ),
        (
            'Морковка для бегемота',
            'Базовая еда для вашего бегемота. +1 к счастью',
            50,
            'Ваш бегемот доволен морковкой! 🥕'
        ),
        (
            'Шляпа бегемота',
            'Модная шляпа для вашего бегемота. Чисто косметический предмет',
            200,
            'Ваш бегемот выглядит потрясающе в этой шляпе! 🎩'
        ),
        (
            'Загадочная коробка',
            'Содержит случайные предметы, связанные с бегемотами. Может быть пустой!',
            500,
            'Вы получили... ничего особенного! Повезёт в следующий раз! 📦'
        ),
        (
            'Золотая статуэтка бегемота',
            'Редкий декоративный предмет, показывающий ваше богатство',
            5000,
            'Вы получили блестящую золотую статуэтку бегемота! ✨'
        ),
        (
            'Бесполезный трофей',
            'Дорогой, но совершенно бесполезный трофей',
            10000,
            'Поздравляем с пустой тратой монет! 🏆'
        ),
        (
            'Сломанный калькулятор',
            'Калькулятор, который показывает только неправильные результаты',
            750,
            'По этому калькулятору 2 + 2 = 5! 🔢'
        ),
        (
            'Пустая коробка',
            'Просто пустая коробка. Внутри ничего нет',
            100,
            'Вау! Она действительно пустая! 📭'
        ),
        (
            'Невидимый бегемот',
            'Бегемот, которого никто не видит. Возможно, его не существует',
            15000,
            'Вы его не видите? Всё правильно! 👻'
        ),
        (
            'Квадратный круг',
            'Математически невозможный предмет',
            3000,
            'Ошибка: не удалось загрузить текстуру ⭕️'
        )
    """)


def downgrade() -> None:
    op.execute("""
        DELETE FROM shop_items
        WHERE name IN (
            'Flag Item',
            'Морковка для бегемота',
            'Шляпа бегемота',
            'Загадочная коробка',
            'Золотая статуэтка бегемота',
            'Бесполезный трофей',
            'Сломанный калькулятор',
            'Пустая коробка',
            'Невидимый бегемот',
            'Квадратный круг'
        );
    """)