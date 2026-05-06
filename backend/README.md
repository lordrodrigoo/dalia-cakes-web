# Dalia Bolos e Doces — Backend

> REST API da confeitaria artesanal **Dalia Bolos e Doces**, construída com FastAPI e Clean Architecture.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00)
![Pytest](https://img.shields.io/badge/Testes-400%20passed-brightgreen?logo=pytest)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS-S3-FF9900?logo=amazonaws&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-2.5Flash-4285F4?logo=google&logoColor=white)

---

## Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Módulos e Funcionalidades](#módulos-e-funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Começar](#como-começar)
- [Docker](#docker)
- [Migrações](#migrações)
- [Testes](#testes)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Documentação da API](#documentação-da-api)
- [Instagram — Lógica Detalhada](#instagram--lógica-detalhada)
- [CI/CD](#cicd)

---

## Visão Geral

API REST completa para gerenciamento do site da confeitaria. Permite que a proprietária administre produtos, categorias, bolos decorados e posts do Instagram via painel administrativo, enquanto clientes acessam o cardápio, a galeria e o chatbot de atendimento.

**Destaques técnicos:**
- Clean Architecture com separação clara entre domínio, aplicação e infraestrutura
- Sincronização automática com Instagram a cada 6 horas via APScheduler
- Classificação inteligente de posts por palavras-chave nas captions
- Chatbot com memória de sessão alimentado pelo Google Gemini 2.5 Flash
- Upload de imagens com processamento Pillow e armazenamento no AWS S3
- 100% de cobertura de testes (unitários + integração)
- Pipeline CI/CD com deploy automático na EC2 e rollback automático

---

## Arquitetura

O projeto segue os princípios da **Clean Architecture**, organizando o código em camadas com dependências apontando sempre para dentro:

```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                            │
│           (controllers, DTOs, dependencies)                 │
├─────────────────────────────────────────────────────────────┤
│                     Application Layer                       │
│                       (usecases)                            │
├─────────────────────────────────────────────────────────────┤
│                      Domain Layer                           │
│              (models, repository interfaces)                │
├─────────────────────────────────────────────────────────────┤
│                   Infrastructure Layer                      │
│         (ORM entities, repositories, S3, Gemini,           │
│          Instagram client, scheduler)                       │
└─────────────────────────────────────────────────────────────┘
```

**Regra principal:** o domínio não conhece nenhuma dependência externa. Os usecases dependem apenas de interfaces (repositórios abstratos), nunca de implementações concretas.

---

## Tecnologias

| Categoria | Tecnologia |
|-----------|-----------|
| Framework | FastAPI 0.135 + Uvicorn |
| ORM | SQLAlchemy 2.0 (sync) |
| Banco de dados | PostgreSQL 15+ |
| Migrações | Alembic |
| Auth | JWT (python-jose) + bcrypt |
| Upload | AWS S3 + boto3 + Pillow |
| IA | Google Gemini 2.5 Flash |
| Scheduler | APScheduler 3 |
| Rate limiting | slowapi |
| Logging | structlog |
| Validação | Pydantic v2 |
| Testes | Pytest + Coverage.py + testcontainers |
| Lint | Pylint |
| Infra | Docker + Docker Compose |

---

## Módulos e Funcionalidades

### Auth
- Login com JWT (access token + refresh token)
- Refresh automático de token
- Logout com invalidação
- Proteção de rotas por role (`OWNER`, `ADMIN`)

### Administradores
- CRUD de admins pelo proprietário (`OWNER`)
- Dois níveis de permissão: `OWNER` (acesso total) e `ADMIN` (gerencia conteúdo)
- Criação automática do owner na primeira inicialização via variáveis de ambiente

### Categorias e Produtos
- CRUD completo de categorias e produtos
- Produtos vinculados a categorias
- Upload de imagem por produto/categoria (processado e salvo no S3)
- Imagens convertidas para WebP e redimensionadas automaticamente

### Upload de Imagens
- Aceita `JPEG`, `JPG`, `PNG`, `WebP`
- Limite de 15MB por arquivo
- Redimensionamento automático por tipo (`products`: 800×800, `categories`: 1200×600)
- Conversão automática para WebP para otimização de banda
- Deleção de imagem antiga ao substituir

### Instagram
Veja a seção detalhada [Instagram — Lógica Detalhada](#instagram--lógica-detalhada).

### Chatbot
- Assistente virtual com Google Gemini 2.5 Flash
- Memória de sessão por `session_id`
- Contexto do negócio injetado no prompt (nome, endereço, horários, formas de pagamento, link iFood)
- Produtos do cardápio disponíveis automaticamente como contexto
- Rate limiting para evitar abuso

---

## Estrutura do Projeto

```
backend/
└── src/
    ├── api/
    │   ├── controllers/          # Endpoints HTTP por módulo
    │   │   ├── auth_controller.py
    │   │   ├── admin_controller.py
    │   │   ├── category_controller.py
    │   │   ├── product_controller.py
    │   │   ├── instagram_controller.py
    │   │   ├── decorated_cakes_controller.py
    │   │   ├── upload_controller.py
    │   │   ├── chatbot_controller.py
    │   │   └── health_controller.py
    │   ├── dependencies.py       # Injeção de dependências (FastAPI Depends)
    │   └── routers.py            # Registro de todos os routers
    │
    ├── config/
    │   ├── settings.py           # Variáveis de ambiente (pydantic-settings)
    │   ├── jwt.py                # Geração e validação de tokens
    │   ├── bcrypt.py             # Hash de senhas
    │   ├── rate_limiter.py       # Configuração do slowapi
    │   └── logger.py             # Configuração do structlog
    │
    ├── domain/
    │   ├── models/               # Entidades puras de domínio (dataclasses)
    │   │   ├── admin.py
    │   │   ├── category.py
    │   │   ├── product.py
    │   │   ├── instagram_post.py
    │   │   └── decorated_cake.py
    │   └── repositories/         # Interfaces abstratas dos repositórios
    │
    ├── dto/
    │   ├── request/              # Schemas de entrada (Pydantic)
    │   └── response/             # Schemas de saída (Pydantic)
    │
    ├── exceptions/               # Exceções customizadas por módulo
    │
    ├── infra/
    │   ├── db/
    │   │   ├── entities/         # Modelos ORM (SQLAlchemy)
    │   │   ├── repositories/     # Implementações concretas dos repositórios
    │   │   └── settings/         # Configuração da sessão e conexão
    │   ├── gemini/               # Cliente HTTP para Gemini AI
    │   ├── instagram/
    │   │   ├── instagram_client.py   # Fetch de posts via Graph API
    │   │   └── scheduler.py          # Jobs APScheduler
    │   └── s3/                   # Cliente AWS S3
    │
    ├── middlewares/              # Correlation ID e logging de requests
    ├── usecases/                 # Lógica de negócio pura
    │
    └── tests/
        ├── unit_tests/           # Testes com mocks (sem banco)
        └── integration_tests/    # Testes com banco real (testcontainers)

migrations/
└── versions/                    # Histórico de migrações Alembic
```

---

## Como Começar

### Pré-requisitos

- Python 3.12+
- PostgreSQL 15+ (ou Docker)
- `openssl` (para gerar SECRET_KEY)
- Conta AWS S3
- Chave Google Gemini API
- Token de acesso Instagram Graph API

### Setup com Makefile (recomendado)

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd dalia-cakes-web

# 2. Setup completo em um comando
make quickstart

# 3. Configure o .env (gerado automaticamente)
code .env

# 4. Gere uma SECRET_KEY segura
make secret-key   # copie o valor para SECRET_KEY no .env

# 5. Aplique as migrações
make migrate

# 6. Inicie o servidor
make run
# → http://localhost:8000/docs
```

### Setup manual

```bash
# Ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Dependências
pip install -r requirements.txt

# Configuração
cp .env.example .env
# edite o .env com seus valores

# SECRET_KEY
openssl rand -hex 32

# Migrações
alembic upgrade head

# Servidor
uvicorn backend.src.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Docker

```bash
# Subir todos os containers (app + banco)
make up

# Parar tudo
make down

# Parar e apagar volumes (reseta o banco)
make down-v

# Status dos containers
make ps

# Logs da aplicação
make logs

# Shell dentro do container
make shell

# Aplicar migrações dentro do container
make migrate-docker
```

O `docker-compose.yml` sobe dois serviços:
- `app` — API FastAPI na porta `8000`
- `database` — PostgreSQL na porta `5432`

---

## Migrações

```bash
# Aplicar todas as migrações pendentes
make migrate

# Reverter a última migração
make migrate-down

# Criar nova migração (autogenerate)
make revision msg="descrição da mudança"

# Manual
alembic upgrade head
alembic downgrade -1
alembic revision --autogenerate -m "descrição"
```

### Histórico de migrações

| Revisão | Descrição |
|---------|-----------|
| `5384aa5898d8` | Schema inicial (admins, auth) |
| `44affdf3e706` | Tabela de categorias |
| `eb0736fb43be` | Renomeia tabela de admins |
| `aea0e3d8bcbc` | Tabela de produtos |
| `a081b98c66d6` | Tabela de bolos decorados + subcategorias iniciais |
| `b83406813ee1` | Tabela de posts do Instagram |
| `3d1dbac93437` | `media_url` e `permalink` como Text |
| `14eb944bc6c2` | Tabela `app_config` (token Instagram persistido) |
| `2f8c1a9e4b7d` | Corrige hashtags + adiciona categoria Outros |

---

## Testes

```bash
# Unitários (rápidos, sem banco)
make test-unit

# Integração (requer Docker para testcontainers)
make test-integration

# Todos com relatório de cobertura
make test-all
# → relatório HTML em htmlcov/index.html
```

### Estratégia de testes

| Tipo | Escopo | Ferramenta |
|------|--------|-----------|
| **Unitários** | Usecases com mocks de repositório | pytest + MagicMock |
| **Integração** | Repositórios com banco PostgreSQL real | pytest + testcontainers |

Os testes de integração sobem um container PostgreSQL temporário via **testcontainers** — não é necessário ter um banco rodando localmente. O container é criado e destruído automaticamente a cada execução.

**Cobertura atual: 100%** em todos os usecases, repositórios, modelos e DTOs.

---

## Variáveis de Ambiente

Copie `.env.example` para `.env` e preencha os valores:

```env
# ── Banco de Dados ──────────────────────────────────────────
DB_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/dalia_cakes_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dalia_cakes_db
ALEMBIC_DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/dalia_cakes_db

# ── JWT ─────────────────────────────────────────────────────
SECRET_KEY=               # gere com: openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# ── AWS S3 ──────────────────────────────────────────────────
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_BUCKET=
AWS_S3_REGION=us-east-1

# ── Google Gemini ────────────────────────────────────────────
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash

# ── Dados do Negócio (contexto do chatbot) ───────────────────
BUSINESS_NAME=Dalia Bolos e Doces
BUSINESS_PHONE=
BUSINESS_ADDRESS=
BUSINESS_CITY=
BUSINESS_HOURS=
BUSINESS_PAYMENT_METHODS=
BUSINESS_IFOOD_LINK=
BUSINESS_ORDER_ADVANCE_DAYS=

# ── Instagram ────────────────────────────────────────────────
INSTAGRAM_ACCESS_TOKEN=

# ── Owner (criado na primeira inicialização) ─────────────────
OWNER_USERNAME=owner
OWNER_PASSWORD=ChangeMe@2026
OWNER_EMAIL=owner@daliacakes.com
OWNER_FIRST_NAME=System
OWNER_LAST_NAME=Owner

# ── API ──────────────────────────────────────────────────────
API_TITLE=dalia cakes API
API_VERSION=1.0.0
API_V1_PREFIX=/api/v1
ENV=development

# ── Logging ──────────────────────────────────────────────────
LOG_LEVEL=DEBUG
LOG_FORMAT=text
```

> **Nunca faça commit do `.env`.** Ele está no `.gitignore`.

---

## Documentação da API

Com a aplicação rodando, acesse:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Endpoints resumidos

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| `POST` | `/api/v1/auth/login` | — | Login |
| `POST` | `/api/v1/auth/refresh` | — | Renova access token |
| `POST` | `/api/v1/auth/logout` | JWT | Logout |
| `GET` | `/api/v1/categories` | — | Lista categorias |
| `POST` | `/api/v1/categories` | ADMIN | Cria categoria |
| `GET` | `/api/v1/products` | — | Lista produtos |
| `GET` | `/api/v1/products/category/{id}` | — | Produtos por categoria |
| `POST` | `/api/v1/products` | ADMIN | Cria produto |
| `GET` | `/api/v1/instagram-posts/featured` | — | Posts em destaque (com fallback) |
| `GET` | `/api/v1/instagram-posts` | — | Todos os posts |
| `POST` | `/api/v1/instagram-posts/sync` | ADMIN | Sincroniza manualmente |
| `PATCH` | `/api/v1/instagram-posts/{id}/subcategory` | ADMIN | Classifica post |
| `PATCH` | `/api/v1/instagram-posts/{id}/featured` | ADMIN | Alterna destaque |
| `GET` | `/api/v1/decorated-cakes` | — | Lista subcategorias |
| `GET` | `/api/v1/decorated-cakes/{id}/posts` | — | Posts por subcategoria |
| `POST` | `/api/v1/chatbot/message` | — | Envia mensagem ao chatbot |
| `POST` | `/api/v1/upload` | ADMIN | Upload de imagem |

### Roles de autenticação

| Role | Permissões |
|------|-----------|
| `OWNER` | Acesso total, incluindo gerenciar outros admins |
| `ADMIN` | Gerencia produtos, categorias, posts e Instagram |

---

## Instagram — Lógica Detalhada

### Ciclo de sincronização

O scheduler APScheduler executa dois jobs automaticamente:

| Job | Intervalo | O que faz |
|-----|-----------|-----------|
| `sync_instagram_job` | A cada 6h | Busca posts, classifica, renova URLs, reclassifica posts sem categoria |
| `refresh_token_job` | A cada 50 dias | Renova o token Instagram (válido por 60 dias) |

### Fluxo completo do sync

```
Instagram Graph API (v21.0)
  ↓ fetch_instagram_posts() — até 10 páginas com paginação
  ↓
Para cada post:
  ├── Post já existe no banco?
  │   ├── Sim → atualiza media_url e permalink (URLs do CDN expiram!)
  │   │   ├── Já tem subcategoria → retorna (sem reclassificar)
  │   │   └── Sem subcategoria → tenta classificar agora
  │   └── Não → classifica e salva com is_featured=True, featured_until=now+3dias
  ↓
refresh_featured_status()   — expira posts com featured_until < now
  ↓
reclassify_unclassified_posts()  — reclassifica todos os posts sem subcategoria
```

### Classificação por palavra-chave

Cada subcategoria tem um campo `hashtag` com uma palavra-chave curta. O sistema faz busca de substring case-insensitive na caption do post.

**Exemplos de match para a palavra-chave `feminino`:**

| Caption do post | Match? |
|-----------------|--------|
| `Bolo feminino especial` | ✅ |
| `#bolofeminino` | ✅ |
| `#FEMININO` | ✅ |
| `BOLOSFEMININOS lindos` | ✅ |
| `Bolo masculino` | ❌ |

**Subcategorias padrão:**

| Nome | Palavra-chave |
|------|---------------|
| Feminino | `feminino` |
| Masculino | `masculino` |
| Neutro | `neutro` |
| Infantil Menina | `infantilmenina` |
| Infantil Menino | `infantilmenino` |
| Outros | *(catch-all automático)* |

### Categoria Outros (catch-all)

Posts que não contêm nenhuma palavra-chave conhecida na caption são automaticamente atribuídos à categoria **Outros**. Isso garante que qualquer post (doces, caixinhas, bastidores, etc.) sempre apareça em alguma categoria no site.

### Posts em destaque

- Novos posts entram com `is_featured=True` por **3 dias**
- Após 3 dias, `is_featured` expira e o post permanece na subcategoria mas sai do carousel da Home
- **Fallback:** se não há nenhum post em destaque ativo, o endpoint `/featured` retorna os **12 posts mais recentes** automaticamente — o carousel da Home nunca fica vazio

### URLs do CDN do Instagram

As URLs `media_url` retornadas pela API do Instagram expiram após alguns dias. A cada sincronização, o sistema atualiza `media_url` e `permalink` de todos os posts existentes com os valores frescos retornados pela API.

---

## CI/CD

O pipeline é automatizado via **GitHub Actions** (`.github/workflows/backend.yml`).

### Estágios

```
[Source]          [Build]           [Deploy]
lint          →   build-image   →   publish-image  →  deploy-ec2
test-unit
```

| Etapa | Trigger | O que faz |
|-------|---------|-----------|
| `lint` | PR + push main | Pylint no código-fonte |
| `test-unit` | PR + push main | Todos os testes unitários |
| `build-image` | PR + push main | Build da imagem Docker (sem push) |
| `publish-image` | Push main | Publica imagem no GHCR com tag `sha-{commit}` |
| `deploy-ec2` | Push main | Deploy via SSH na EC2 com health check e rollback |

### Rollback automático

Se o health check falhar após o deploy, o pipeline reverte automaticamente para a imagem anterior.

### Secrets necessários no GitHub

| Secret | Descrição |
|--------|-----------|
| `EC2_HOST` | IP ou domínio da instância EC2 |
| `EC2_USER` | Usuário SSH |
| `EC2_SSH_KEY` | Chave privada SSH |
| `EC2_DEPLOY_PATH` | Caminho do projeto na EC2 |
| `CONTAINER_REGISTRY_TOKEN` | GitHub PAT com `packages:write` |
| `CONTAINER_REGISTRY_USERNAME` | Usuário GitHub |
| `SMTP_USERNAME` | Email para notificações de falha |
| `SMTP_PASSWORD` | Senha do email |
| `NOTIFY_EMAIL` | Destinatário das notificações |

---

*Dalia Bolos e Doces — API v1.0 — 2026*
