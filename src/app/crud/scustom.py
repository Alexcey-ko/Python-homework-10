"""SQL запросы для таблицы SCUSTOM."""

from sqlalchemy import select

from app.db import session
from app.db.models import Scustom


def get_scustom_by_email(email:str)->Scustom:
    """Выбор клиента по email."""
    stmt = select(Scustom).where(Scustom.email == email)
    result = session.execute(stmt)

    return result.scalar_one_or_none()

def create_scustom(email:str, phone_number:str, name:str)->Scustom:
    """Регистрация нового клиента."""
    scustom = Scustom(
        email=email, 
        phone_number=phone_number, 
        name=name 
    )
    session.add(scustom)
    session.flush()
    session.commit()
    
    return scustom