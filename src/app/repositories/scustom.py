"""SQL запросы для таблицы Scustom."""

from sqlalchemy import select

from app.entities import ScustomData
from app.models import Scustom
from app.repositories.base import Repository


class ScustomRepository(Repository):
    """SQL запросы для таблицы Scustom."""

    async def get_scustom_by_email(self, email:str)->Scustom:
        """Выбор клиента по email."""
        query = select(Scustom).where(Scustom.email == email)
        stmt = await self.session.execute(query)
        result = stmt.scalar_one_or_none()

        return result

    def create_scustom(self, scustom:ScustomData)->Scustom:
        """Добавление нового клиента."""
        new_scustom = Scustom(
            email = scustom.email, 
            phone_number = scustom.phone_number, 
            name = scustom.name 
        )
        self.session.add(new_scustom)

        return new_scustom
    
    def create_scustom_single(self, scustom:ScustomData)->Scustom:
        """Добавление одного нового клиента."""
        new_scustom = self.create_scustom(scustom)

        return new_scustom

    def create_scustom_list(self, scustom_list: list[ScustomData]) -> list[Scustom]:
        """Создание одной записи в таблице Scustom."""
        result_list = [self.create_scustom(new_scustom) for new_scustom in scustom_list]

        return result_list