# FastAPI Sample

Aplicação FastAPI demonstrando **Service Layer** e **Repository Pattern** com operações concorrentes usando **AsyncIO TaskGroup** e **Semaphore**.

## Arquitetura

```
Routes → Service Layer (Lógica de Negócio) → Repository (Acesso a Dados) → SQLAlchemy & PostgreSQL
```

## Padrões

- **Service Layer**: Encapsula lógica de negócio, desacoplada das rotas
- **Repository Pattern**: Abstrai acesso a dados, centraliza queries
- **AsyncIO + Semaphore**: Operações concorrentes com controle de rate limiting
- **Dependency Injection**: Usando `Depends()` do FastAPI

## Estrutura do Projeto

```
fastapi-sample/
├── sample/
│   ├── routes.py                    # Endpoints
│   ├── volumesRouter.py             # Rotas de volumes
│   ├── database/                    # Camada de dados
│   │   ├── base_repository.py       # Base repository
│   │   ├── data_models.py           # Modelos ORM
│   │   └── db.py                    # Configuração
│   └── volumes/
│       ├── models/                  # Schemas (Pydantic)
│       ├── repository/              # Data access
│       ├── services/                # Lógica de negócio
│       ├── v0_volumes.py            # API v0
│       └── v1_volumes.py            # API v1
├── main.py                          # Entry point
└── docker-compose.yaml              # PostgreSQL
```
