from .db import Session


class BaseRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def flush(self):
        await self.session.flush()

    async def __aenter__(self):
        return await self.session.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.session.__aexit__(exc_type, exc_val, exc_tb)
