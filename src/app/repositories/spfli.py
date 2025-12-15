"""SQL запросы для таблицы Spfli."""

from app.entities.spfli import SpfliData
from app.models import Spfli
from app.repositories.base import Repository


class SpfliRepository(Repository):
    """SQL запросы для таблицы Spfli."""

    def create_spfli(self, spfli: SpfliData) -> Spfli:
        """Создание записи в таблице Spfli."""
        new_spfli = Spfli(
            carrid = spfli.carrid,
            connid = spfli.connid,
            airpfrom = spfli.airpfrom,
            airpto = spfli.airpto,
            fltime = spfli.fltime,
        )

        return new_spfli
    
    def create_spfli_single(self, spfli: SpfliData) -> Spfli:
        """Создание одной записи в таблице Spfli."""
        new_spfli = self.create_spfli(spfli)
        self.session.add(new_spfli)

        return new_spfli

    def create_spfli_list(self, spfli_list: list[SpfliData]) -> list[Spfli]:
        """Создание одной записи в таблице Spfli."""
        result_list = [self.create_spfli(new_spfli) for new_spfli in spfli_list]
        self.session.add_all(result_list)

        return result_list