# 🎂 Dalia Bolos e Doces — Estrutura do Projeto

## Monorepo

```
dalia-bolos/
├── backend/
├── frontend/               ← a definir
├── docker-compose.yml
└── README.md
```

---

## Backend — FastAPI + PostgreSQL

```
backend/
├── src/
│   ├── api/
│   │   ├── controllers/
│   │   │   ├── auth_controller.py
│   │   │   ├── product_controller.py
│   │   │   ├── category_controller.py
│   │   │   ├── review_controller.py
│   │   │   ├── instagram_controller.py
│   │   │   └── chatbot_controller.py
│   │   ├── __init__.py
│   │   └── dependencies.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── correlation.py       ← correlation ID
│   │   ├── limiter.py           ← rate limiting
│   │   ├── logger.py            ← structlog
│   │   ├── oauth2.py            ← JWT (criação e validação)
│   │   ├── owner.py             ← seeder do owner via .env
│   │   ├── security.py          ← bcrypt (hash de senha)
│   │   └── settings.py          ← variáveis de ambiente (pydantic-settings)
│   │
│   ├── domain/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   ├── category.py
│   │   │   ├── review.py
│   │   │   └── instagram_post.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── user_repository.py
│   │   │   ├── product_repository.py
│   │   │   ├── category_repository.py
│   │   │   ├── review_repository.py
│   │   │   └── instagram_repository.py
│   │   └── __init__.py
│   │
│   ├── dto/
│   │   ├── __init__.py
│   │   ├── auth_dto.py
│   │   ├── product_dto.py
│   │   ├── category_dto.py
│   │   ├── review_dto.py
│   │   └── instagram_dto.py
│   │
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── base_exception.py
│   │   ├── not_found_exception.py
│   │   ├── unauthorized_exception.py
│   │   └── conflict_exception.py
│   │
│   ├── infra/
│   │   ├── db/
│   │   │   ├── entities/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base_entity.py          ← id (UUID), created_at, updated_at
│   │   │   │   ├── user_entity.py
│   │   │   │   ├── category_entity.py
│   │   │   │   ├── product_entity.py
│   │   │   │   ├── review_entity.py
│   │   │   │   └── instagram_post_entity.py
│   │   │   ├── repositories/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user_repository_impl.py
│   │   │   │   ├── product_repository_impl.py
│   │   │   │   ├── category_repository_impl.py
│   │   │   │   ├── review_repository_impl.py
│   │   │   │   └── instagram_repository_impl.py
│   │   │   ├── settings/
│   │   │   │   ├── __init__.py
│   │   │   │   └── database.py             ← engine, session, Base
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── middlewares/
│   │   ├── __init__.py
│   │   ├── correlation_middleware.py
│   │   ├── logging_middleware.py
│   │   └── middlewares.py
│   │
│   ├── tests/
│   │   ├── config_tests/
│   │   ├── fixtures/
│   │   ├── functional_tests/
│   │   ├── integration_tests/
│   │   ├── unit_tests/
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   └── test_helpers.py
│   │
│   └── usecases/
│       ├── __init__.py
│       ├── auth_usecase.py
│       ├── product_usecase.py
│       ├── category_usecase.py
│       ├── review_usecase.py
│       └── instagram_usecase.py
│
├── migrations/                  ← Alembic
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── .env.example
├── Dockerfile
└── requirements.txt
```

---

## Variáveis de Ambiente (.env)

| Variável | Descrição |
|---|---|
| `APP_ENV` | Ambiente: development / production |
| `DATABASE_URL` | URL de conexão PostgreSQL async |
| `SECRET_KEY` | Chave secreta JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração do token JWT |
| `OWNER_NAME` | Nome do owner (seeder) |
| `OWNER_EMAIL` | E-mail do owner (seeder) |
| `OWNER_PASSWORD` | Senha do owner (seeder) |
| `INSTAGRAM_ACCESS_TOKEN` | Token de acesso Instagram API |
| `INSTAGRAM_USER_ID` | ID do usuário Instagram |
| `INSTAGRAM_SYNC_INTERVAL_MINUTES` | Intervalo de sincronização |
| `RATE_LIMIT_PER_MINUTE` | Limite de requisições por minuto |
| `ALLOWED_ORIGINS` | Origens permitidas (CORS) |

---

## Dependências Principais

| Pacote | Uso |
|---|---|
| `fastapi` | Framework web |
| `uvicorn` | ASGI server |
| `sqlalchemy` | ORM async |
| `asyncpg` | Driver PostgreSQL async |
| `alembic` | Migrations |
| `pydantic-settings` | Variáveis de ambiente |
| `python-jose` | JWT |
| `passlib[bcrypt]` | Hash de senhas |
| `slowapi` | Rate limiting |
| `structlog` | Logging estruturado |
| `httpx` | Cliente HTTP (Instagram API) |
| `asgi-correlation-id` | Correlation ID |
| `pytest + pytest-asyncio` | Testes |

---

## Fluxo de uma Requisição

```
Request HTTP
    │
    ▼
Middlewares (correlation_id → logging)
    │
    ▼
Controller (api/controllers/)
    │
    ▼
Dependencies (auth, session)
    │
    ▼
UseCase (regra de negócio)
    │
    ▼
Repository Interface (domain/repositories/)
    │
    ▼
Repository Impl (infra/db/repositories/)
    │
    ▼
PostgreSQL
```

---

## Seeder — Owner

Ao iniciar a aplicação, o sistema verifica se o owner já existe no banco.
Se não existir, cria automaticamente com base nas variáveis de ambiente.

```
startup event → create_owner_if_not_exists()
    │
    ├── owner existe? → nenhuma ação
    └── owner não existe? → cria com hash bcrypt da senha
```

---

*Dalia Bolos e Doces — v1.0 — Abril 2026*
