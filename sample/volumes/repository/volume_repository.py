from sqlalchemy import (
    select,
    update
)

from sample.database.base_repository import BaseRepository
from sample.database.data_models import VolumeDB


class VolumeRepository(BaseRepository):
    async def list_all_volumes(self):
        stmt = (
            select(VolumeDB)
        )
        result = await self.session.scalars(stmt)
        return result.all()

    async def expand_volume(self, volume_id: int, current_size: int):
        stmt = (
            update(VolumeDB)
            .where(VolumeDB.id == volume_id)
            .values({
                "size": current_size+123
            })
        )
        await self.session.execute(stmt)

    async def create_volume(self, volume: VolumeDB):
        self.session.add(volume)
