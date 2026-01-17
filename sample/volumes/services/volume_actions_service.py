from typing import Annotated
from fastapi import Depends
from sample.volumes.repository.volume_repository import VolumeRepository
from sample.volumes.models.volumes import VolumeModel
from sample.database.data_models import VolumeDB
from sample.database.db import async_session_factory


class VolumeActionsService:
    def __init__(
        self,
        volume_repository: Annotated[VolumeRepository, Depends()],
    ):
        self.volume_repository = volume_repository
    
    async def resize(self, volume: VolumeModel):
        async with async_session_factory() as session:
            repo = VolumeRepository(session)
            async with repo:
                await repo.expand_volume(volume.id, volume.size)
                await repo.session.commit()

    async def get_volumes(self, repo: VolumeRepository = None):
        if not repo:
            repo = self.volume_repository
        return await repo.list_all_volumes()

    async def create(self, volume: VolumeModel):
        volume_db = VolumeDB(id=volume.id, name=volume.name, size=volume.size)
        
        async with async_session_factory() as session:
            repo = VolumeRepository(session)

            async with repo:
                volumes_in_db = await self.get_volumes(repo)
                # print([volume.id for volume in volumes_in_db])
                await repo.create_volume(volume_db)
                await repo.session.commit()

    