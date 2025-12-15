"""SQL запросы для таблицы Sairport."""

from sqlalchemy import select

from app.entities.sairport import SairportData
from app.models import Sairport
from app.repositories.base import Repository


class SairportRepository(Repository):
    """SQL запросы для таблицы Sairport."""

    async def get_city_list_distinct(self) -> list[str]:
        """Выбор всех городов."""
        query = select(Sairport.city).distinct()
        stmt = await self.session.execute(query)
        result = stmt.scalars().all()
        return result

    def create_sairport(self, sairport: SairportData) -> Sairport:
        """Создание записи в таблице Sairport."""
        new_sairport = Sairport(
            id = sairport.id,
            name = sairport.name,
            timezone = sairport.timezone,
            country = sairport.country,
            city = sairport.city,
        )

        return new_sairport
    
    def create_sairport_single(self, sairport: SairportData) -> Sairport:
        """Создание одной записи в таблице Sairport."""
        new_sairport = self.create_sairport(sairport)
        self.session.add(new_sairport)

        return new_sairport

    def create_sairport_list(self, sairport_list: list[SairportData]) -> list[Sairport]:
        """Создание одной записи в таблице Sairport."""
        result_list = [self.create_sairport(new_sairport) for new_sairport in sairport_list]
        self.session.add_all(result_list)

        return result_list   