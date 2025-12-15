"""SQL запросы для таблицы Scarr."""

from app.entities.scarr import ScarrData
from app.models import Scarr
from app.repositories.base import Repository


class ScarrRepository(Repository):
    """SQL запросы для таблицы Scarr."""

    def create_scarr(self, scarr: ScarrData) -> Scarr:
        """Создание записи в таблице Scarr."""
        new_scarr = Scarr(
            carrid = scarr.carrid,
            carrname = scarr.carrname,
            carrcode = scarr.carrcode,
            url = scarr.url,
        )
        self.session.add(new_scarr)

        return new_scarr
    
    def create_scarr_single(self, scarr: ScarrData) -> Scarr:
        """Создание одной записи в таблице Scarr."""
        new_scarr = self.create_scarr(scarr)

        return new_scarr

    def create_scarr_list(self, scarr_list: list[ScarrData]) -> list[Scarr]:
        """Создание одной записи в таблице Scarr."""
        result_list = [self.create_scarr(new_scarr) for new_scarr in scarr_list]
        
        return result_list        