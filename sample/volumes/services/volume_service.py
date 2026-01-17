from asyncio import Semaphore, TaskGroup, sleep
from random import randint
from typing import Annotated
from fastapi import Depends
from sample.volumes.repository.volume_repository import VolumeRepository
from sample.volumes.services.volume_actions_service import VolumeActionsService
from sample.volumes.models.volumes import VolumeModel


class VolumeService:
    def __init__(
        self,
        volume_actions_service: Annotated[VolumeActionsService, Depends()],
        volume_repository: Annotated[VolumeRepository, Depends()],
        max_concurrent: int = 2
    ):
        self.volume_repository = volume_repository
        self.volume_actions_service = volume_actions_service
        self.semaphore = Semaphore(max_concurrent)

    async def list_volumes(self):
        return await self.volume_actions_service.get_volumes()
    
    async def create_volumes(self):
        def gen_rand_volumes():
            rand_number = randint(1000, 90000)
            return VolumeModel(
                id=rand_number,
                name="Volume %s" % rand_number,
                size=rand_number)

        volumes = [gen_rand_volumes() for _ in range(10)]
        async with TaskGroup() as tg:
            for volume in volumes:
                tg.create_task(self.create_volume_task(volume))

    async def create_volume_task(self, volume: VolumeModel) -> None:
        async with self.semaphore:
            await self.volume_actions_service.create(volume)
            await sleep(1)

    async def expand_volumes(self):
        volumes = await self.list_volumes()
        async with TaskGroup() as tg:
            for volume in volumes:
                tg.create_task(self.expand_volume_task(volume))

    async def expand_volume_task(self, volume: VolumeModel) -> None:
        async with self.semaphore:
            await self.volume_actions_service.resize(volume)
