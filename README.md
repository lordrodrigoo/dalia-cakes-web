# Dalia Bolos e Doces — API

🇧🇷 Versão em Português · 🇺🇸 English version below

---

## 🇧🇷 Português

API REST da confeitaria artesanal **Dalia Bolos e Doces**, construída com FastAPI e Clean Architecture. Autenticação JWT, chatbot com Gemini AI, sincronização com Instagram, upload de imagens para S3 com otimização via Pillow, cobertura de testes de 100% e pipeline CI/CD com deploy automático na EC2.

![Python](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135%2B-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%2B-D71F00)
![Alembic](https://img.shields.io/badge/Alembic-migrations-6BA81E)
![Pytest](https://img.shields.io/badge/pytest-tested-0A9EDC?logo=pytest&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-compose-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-4169E1?logo=postgresql&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS-S3-FF9900?logo=amazonaws&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-2.5Flash-4285F4?logo=google&logoColor=white)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen?logo=codecov&logoColor=white)

---

## 📋 Índice

- [Tecnologias](#-tecnologias)
- [Funcionalidades](#-funcionalidades)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Começar](#-como-começar)
- [Rodando com Docker](#-rodando-com-docker)
- [Migrações](#-migrações)
- [Testes e Cobertura](#-testes-e-cobertura)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Documentação da API](#-documentação-da-api)
- [CI/CD e Deploy](#-cicd-e-deploy)

---

## 🛠 Tecnologias

- Python 3.12+
- FastAPI + Uvicorn
- SQLAlchemy 2.0+ (sync) + PostgreSQL 15+
- Alembic (migrações)
- Pytest + Coverage.py (100%)
- Docker & Docker Compose
- AWS S3 + boto3 (upload de imagens)
- Pillow (redimensionamento e conversão WebP)
- Google Gemini 2.5 Flash (chatbot IA)
- APScheduler (sincronização Instagram)
- python-jose (JWT)
- bcrypt (hash de senhas)
- structlog (logging estruturado)
- slowapi (rate limiting)
- Pydantic v2

---

## ✨ Funcionalidades

| Módulo | Descrição |
|--------|-----------|
| **Auth** | Login JWT, refresh token, logout |
| **Admin** | CRUD de administradores (OWNER/ADMIN) |
| **Categorias** | CRUD de categorias de produtos |
| **Produtos** | CRUD de produtos com imagem |
| **Upload** | Upload de imagens → processamento Pillow → S3 |
| **Bolos Decorados** | Subcategorias: feminino, masculino, neutro, infantil |
| **Instagram** | Sincronização automática de posts via Graph API |
| **Chatbot** | Assistente virtual com Gemini AI e histórico de sessão |

---

## 📁 Estrutura do Projeto

```
dalia-cakes-web/
├── .github/workflows/     — Pipeline CI/CD (GitHub Actions)
├── backend/
│   └── src/
│       ├── api/
│       │   ├── controllers/   — Endpoints HTTP
│       │   └── dependencies.py
│       ├── config/            — Settings, JWT, bcrypt, rate limiter, logger
│       ├── domain/
│       │   ├── models/        — Entidades de domínio
│       │   └── repositories/  — Interfaces dos repositórios
│       ├── dto/
│       │   ├── request/       — Schemas de entrada (Pydantic)
│       │   └── response/      — Schemas de saída (Pydantic)
│       ├── exceptions/        — Exceções customizadas por módulo
│       ├── infra/
│       │   ├── db/
│       │   │   ├── entities/      — Modelos ORM (SQLAlchemy)
│       │   │   ├── repositories/  — Implementações concretas
│       │   │   └── settings/      — Configuração do banco
│       │   ├── gemini/        — Cliente HTTP Gemini AI
│       │   └── s3/            — Cliente AWS S3
│       ├── middlewares/       — Correlation ID e logging
│       ├── usecases/          — Lógica de negócio pura
│       └── tests/             — Testes unitários e de integração
├── migrations/            — Migrações Alembic
├── docs/                  — Documentação e diagramas
├── Dockerfile             — Build multi-stage
├── docker-compose.yml     — Ambiente local
├── Makefile               — Comandos prontos
└── .env.example           — Variáveis de ambiente necessárias
```

---

## 🚀 Como Começar

### Pré-requisitos

- Python 3.12+
- Docker & Docker Compose
- PostgreSQL 15+ (sem Docker)
- `openssl` (para gerar SECRET_KEY)

### Opção A — Makefile (recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/dalia-cakes-web.git
cd dalia-cakes-web

# 2. Copie o .env e configure
make init
code .env   # preencha os valores

# 3. Instale as dependências
make setup

# 4. Gere uma SECRET_KEY segura
make secret-key   # copie o valor para o .env

# 5. Aplique as migrações
make migrate

# 6. Inicie a aplicação
make run
```

Acesse em: http://localhost:8000/docs

### Opção B — Comandos manuais

```bash
# 1. Clone e configure o ambiente
git clone https://github.com/seu-usuario/dalia-cakes-web.git
cd dalia-cakes-web
cp .env.example .env

# 2. Gere a SECRET_KEY
openssl rand -hex 32

# 3. Crie e ative o virtualenv
python3 -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate       # Windows

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Aplique as migrações
alembic upgrade head

# 6. Inicie a aplicação
uvicorn backend.src.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🐳 Rodando com Docker

```bash
# Iniciar todos os containers (app + banco)
make up

# Parar todos os containers
make down

# Parar e remover volumes (apaga dados do banco)
make down-v

# Ver status dos containers
make ps

# Aplicar migrações dentro do container
make migrate-docker
```

---

## 🔄 Migrações

```bash
make migrate              # Aplicar todas as migrações pendentes
make migrate-down         # Reverter a última migração
make revision msg="..."   # Criar nova migração

# Manual
alembic upgrade head
alembic downgrade -1
alembic revision --autogenerate -m "descrição"
```

---

## 🧪 Testes e Cobertura

```bash
make test-unit          # Testes unitários
make test-all           # Todos os testes com relatório de cobertura

# Manual
pytest backend/src/tests/unit_tests/ -v
pytest --cov=backend/src --cov-report=term-missing
pytest --cov=backend/src --cov-report=html   # abre em htmlcov/index.html
```

Cobertura atual: **100%**

---

## 🔐 Variáveis de Ambiente

Copie `.env.example` para `.env` e preencha todos os valores:

```env
# Banco de Dados
DB_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/dalia_cakes_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dalia_cakes_db
ALEMBIC_DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/dalia_cakes_db

# JWT
SECRET_KEY=             # gere com: openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# AWS S3
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_BUCKET=
AWS_S3_REGION=us-east-1

# Google Gemini (Chatbot)
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash

# Informações do negócio (usadas pelo chatbot)
BUSINESS_NAME=Dalia Bolos e Doces
BUSINESS_PHONE=
BUSINESS_ADDRESS=
BUSINESS_CITY=
BUSINESS_HOURS=
BUSINESS_PAYMENT_METHODS=
BUSINESS_IFOOD_LINK=
BUSINESS_ORDER_ADVANCE_DAYS=

# Instagram
INSTAGRAM_ACCESS_TOKEN=

# Owner (criado automaticamente na primeira inicialização)
OWNER_USERNAME=owner
OWNER_PASSWORD=ChangeMe@2026
OWNER_EMAIL=owner@daliacakes.com
OWNER_FIRST_NAME=System
OWNER_LAST_NAME=Owner

# API
API_TITLE=dalia cakes API
API_VERSION=1.0.0
API_V1_PREFIX=/api/v1
ENV=development

# Logging
LOG_LEVEL=DEBUG
LOG_FORMAT=text
```

> ⚠️ Nunca faça commit do arquivo `.env`. Ele já está no `.gitignore`.

---

## 📬 Documentação da API

Com a aplicação rodando:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Roles de autenticação

| Role | Descrição |
|------|-----------|
| `OWNER` | Acesso total a todos os recursos |
| `ADMIN` | Gerencia produtos, categorias e Instagram |

---

## 🚀 CI/CD e Deploy

O pipeline é automatizado via GitHub Actions. A cada push na branch `main`:

1. Lint (pylint) + testes unitários rodam em paralelo
2. Imagem Docker é validada (build sem push) em todo PR
3. Imagem é publicada no GHCR com tag do commit SHA
4. Deploy via SSH na EC2 com health check automático
5. Em caso de falha, rollback automático para a versão anterior

### Secrets necessários no GitHub

| Secret | Descrição |
|--------|-----------|
| `EC2_HOST` | IP ou domínio da instância EC2 |
| `EC2_USER` | Usuário SSH (ex: `ubuntu`) |
| `EC2_SSH_KEY` | Chave privada SSH |
| `EC2_DEPLOY_PATH` | Caminho do projeto na EC2 |
| `CONTAINER_REGISTRY_TOKEN` | PAT do GitHub com permissão `packages:write` |
| `CONTAINER_REGISTRY_USERNAME` | Seu usuário GitHub |
| `SMTP_USERNAME` | Email para notificações de falha |
| `SMTP_PASSWORD` | Senha do email |
| `NOTIFY_EMAIL` | Email de destino das notificações |

---

---

## 🇺🇸 English

REST API for the artisan bakery **Dalia Bolos e Doces**, built with FastAPI and Clean Architecture. JWT authentication, AI chatbot powered by Gemini, Instagram synchronization, S3 image upload with Pillow optimization, 100% test coverage and CI/CD pipeline with automatic EC2 deployment.

### Quick Start

```bash
git clone https://github.com/your-username/dalia-cakes-web.git
cd dalia-cakes-web
make init && make setup
make migrate && make run
```

Access at: http://localhost:8000/docs

For full English documentation, the structure and commands mirror the Portuguese section above — all `make` commands and environment variable names are identical.

---

*Dalia Bolos e Doces — v1.0 — 2026*
