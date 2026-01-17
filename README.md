# FastAPI Sample - Service Layer & Repository Pattern

A sample FastAPI application demonstrating best practices in application architecture using **Service Layer** and **Repository Pattern**, with experimental testing of **AsyncIO TaskGroup** and **Semaphore** for concurrent operations.

## Architecture Overview

This project follows clean architecture principles with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Routes                           │
├─────────────────────────────────────────────────────────────┤
│                  Service Layer                              │
│  (Business Logic & Orchestration)                           │
├─────────────────────────────────────────────────────────────┤
│              Repository Layer                               │
│  (Data Access & Persistence)                                │
├─────────────────────────────────────────────────────────────┤
│            SQLAlchemy ORM & Database                        │
└─────────────────────────────────────────────────────────────┘
```

## Key Patterns & Concepts

### 1. Service Layer Pattern

The **Service Layer** encapsulates business logic and acts as an intermediary between routes and repositories. This provides:

- **Separation of Concerns**: Business logic is decoupled from HTTP handling
- **Reusability**: Services can be used by multiple endpoints
- **Testability**: Services can be easily unit tested
- **Transaction Management**: Services coordinate database transactions

**Example:**
```python
class VolumeActionsService:
    async def create(self, volume: VolumeSchema):
        volume_db = VolumeDB(id=volume.id, name=volume.name, size=volume.size)
        async with async_session_factory() as session:
            repo = VolumeRepository(session)
            async with repo:
                await repo.create_volume(volume_db)
                await repo.commit()
```

### 2. Repository Pattern

The **Repository Pattern** abstracts data access logic and provides a collection-like interface to the domain model:

- **Data Abstraction**: Isolates domain objects from persistence details
- **Query Consolidation**: All database queries are centralized
- **Testability**: Easy to mock repositories in unit tests
- **Consistency**: Uniform interface for all data operations

**Example:**
```python
class VolumeRepository(BaseRepository):
    async def create_volume(self, volume: VolumeDB):
        self.session.add(volume)
        await self.session.flush()
    
    async def expand_volume(self, volume_id: int, current_size: int):
        stmt = update(VolumeDB).where(VolumeDB.id == volume_id).values({"size": current_size + 123})
        await self.session.execute(stmt)
```

### 3. AsyncIO TaskGroup & Semaphore (Experimental)

This project includes experimental testing of concurrent operations using:

- **TaskGroup**: Groups multiple async tasks and ensures all complete before returning
- **Semaphore**: Limits the number of concurrent operations to prevent resource exhaustion

**Use Case: Bulk Volume Expansion**

```python
async def expand_volumes(self):
    volumes = await self.list_volumes()
    async with TaskGroup() as tg:
        for volume in volumes:
            tg.create_task(self.expand_volume_task(volume))

async def expand_volume_task(self, volume: VolumeDB) -> None:
    async with self.semaphore:  # Limits to max_concurrent (default: 10)
        async with async_session_factory() as session:
            repo = VolumeRepository(session)
            async with repo:
                await repo.expand_volume(volume.id, volume.size)
                await repo.commit()
```

**Benefits:**
- **Concurrency**: Multiple volumes expanded simultaneously
- **Rate Limiting**: Semaphore prevents overwhelming the database
- **Isolation**: Each task has its own database session
- **Error Resilience**: Failures in one task don't block others

## Project Structure

```
fastapi-sample/
├── sample/
│   ├── __init__.py
│   ├── routes.py                 # API endpoints
│   ├── volumesRouter.py          # Volume-specific routes
│   ├── snapshotRouter.py         # Snapshot-specific routes
│   ├── contrib/                  # Shared utilities
│   │   └── paginated_response.py
│   ├── database/                 # Data access layer
│   │   ├── base_repository.py    # Base repository class
│   │   ├── data_models.py        # SQLAlchemy ORM models
│   │   └── db.py                 # Database configuration
│   ├── volumes/
│   │   ├── models/               # Pydantic schemas
│   │   │   └── volumes.py
│   │   ├── repository/           # Volume repository
│   │   │   └── volume_repository.py
│   │   ├── services/             # Business logic
│   │   │   └── volume_actions_service.py
│   │   ├── v0_volumes.py         # API v0 endpoints
│   │   └── v1_volumes.py         # API v1 endpoints
│   └── snapshots/                # Similar structure for snapshots
├── main.py                       # Application entry point
└── docker-compose.yaml           # PostgreSQL container config
```

## Database Setup

The application uses **PostgreSQL** with **SQLAlchemy async support**.

### Prerequisites

- PostgreSQL running (or use Docker)
- Python 3.10+
- FastAPI, SQLAlchemy, asyncpg

### Starting PostgreSQL

```bash
docker-compose up -d
```

### Running the Application

```bash
pip install -r requirements.txt
python main.py
```

## Key Features

### Session Management

- **ScopedSession**: Ensures one session per async task
- **Context Managers**: Automatic transaction handling
- **Error Handling**: Automatic rollback on exceptions

### Dependency Injection

FastAPI's `Depends()` is used for:
- Repository injection into services
- Service injection into routes
- Database session injection

### Async/Await

Full async support using:
- `AsyncSession` from SQLAlchemy
- `asyncpg` database driver
- Async context managers for resource management

## Testing Concurrent Operations

The semaphore + TaskGroup implementation is tested in the `VolumeService.expand_volumes()` method:

```bash
# Test expanding multiple volumes concurrently
POST /api/v1/volumes/expand
```

**Observing Concurrent Behavior:**
- Check logs to see tasks starting/completing
- Use `max_concurrent` parameter to adjust semaphore size
- Monitor database to see multiple updates happening

## Best Practices Implemented

✅ **Separation of Concerns**: Routes, Services, Repositories are independent  
✅ **Dependency Injection**: Loose coupling via FastAPI's Depends  
✅ **Error Handling**: Proper exception handling in services  
✅ **Transaction Management**: Explicit commit/rollback control  
✅ **Resource Management**: Context managers for cleanup  
✅ **Concurrent Operations**: Safe concurrent database access with TaskGroup + Semaphore  
✅ **Type Hints**: Full type annotation for better IDE support  
✅ **Async First**: Built for high-concurrency scenarios  

## Future Improvements

- [ ] Add comprehensive error handling and logging
- [ ] Implement caching layer
- [ ] Add pagination support
- [ ] Implement database migrations
- [ ] Add unit/integration tests
- [ ] Add API documentation with OpenAPI

## License

This project is provided as a learning resource.
