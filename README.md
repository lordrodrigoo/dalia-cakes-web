<div align="center">

<img src="frontend/src/assets/images/logo_home.png" alt="Dalia Bolos e Doces" width="140" />

# Dalia Bolos e Doces

### Plataforma web completa para confeitaria artesanal

*API REST · Painel Administrativo · Vitrine para Clientes*

[![Backend CI](https://github.com/lordrodrigoo/dalia-cakes-web/actions/workflows/backend.yml/badge.svg)](https://github.com/lordrodrigoo/dalia-cakes-web/actions/workflows/backend.yml)
[![Frontend CI](https://github.com/lordrodrigoo/dalia-cakes-web/actions/workflows/frontend.yml/badge.svg)](https://github.com/lordrodrigoo/dalia-cakes-web/actions/workflows/frontend.yml)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](backend/README.md)
[![Tests](https://img.shields.io/badge/tests-400%20passed-brightgreen)](backend/README.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

</div>

---

## O Projeto

Sistema completo desenvolvido para a confeitaria artesanal Dalia Bolos e Doces, cobrindo desde a vitrine para os clientes até o gerenciamento interno de conteúdo pela proprietária.

O site integra diretamente com o Instagram — a cada 6 horas sincroniza os posts automaticamente e os organiza por categoria de bolo usando palavras-chave da legenda. A Dalia só precisa postar normalmente e o site se atualiza sozinho.

O chatbot é alimentado pelo Google Gemini e conhece o cardápio, os preços, o horário de funcionamento e os canais de venda em tempo real — respondendo dúvidas dos clientes 24h por dia sem nenhuma intervenção manual.

O painel administrativo foi desenhado para ser usado sem nenhum conhecimento técnico: gerenciamento completo de produtos, categorias, bolos decorados e posts do Instagram com poucos cliques.

Tecnicamente, o projeto usa Clean Architecture no backend, 100% de cobertura de testes, imagens convertidas automaticamente para WebP e armazenadas no S3, autenticação JWT com refresh automático e CI/CD com deploy automático na AWS EC2.

---

## Stack

### Backend

<div>

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-6BA81E?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-100%25_coverage-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

</div>

<div>

![AWS S3](https://img.shields.io/badge/AWS_S3-Storage-FF9900?style=for-the-badge&logo=amazons3&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-Image_Processing-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-Chatbot-4285F4?style=for-the-badge&logo=google&logoColor=white)
![APScheduler](https://img.shields.io/badge/APScheduler-Background_Jobs-FF6B35?style=for-the-badge)
![Instagram API](https://img.shields.io/badge/Instagram_Graph_API-E4405F?style=for-the-badge&logo=instagram&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-499848?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)

</div>

### Frontend

<div>

![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![React Router](https://img.shields.io/badge/React_Router-7-CA4245?style=for-the-badge&logo=reactrouter&logoColor=white)
![Axios](https://img.shields.io/badge/Axios-1.15-5A29E4?style=for-the-badge)
![ESLint](https://img.shields.io/badge/ESLint-9-4B32C3?style=for-the-badge&logo=eslint&logoColor=white)

</div>

### Infraestrutura

<div>

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![AWS EC2](https://img.shields.io/badge/AWS_EC2-Deploy-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white)
![GHCR](https://img.shields.io/badge/GHCR-Container_Registry-181717?style=for-the-badge&logo=github&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-Frontend_Server-009639?style=for-the-badge&logo=nginx&logoColor=white)

</div>

---

## Screenshots

### Vitrine Pública

| | |
|:---:|:---:|
| ![Home com chatbot](docs/screenshot/desktop/home_chatbot_aberto.png) | ![Bolos Decorados](docs/screenshot/desktop/bolos_decorados.png) |
| *Página inicial com chatbot Bel Doçura* | *Bolos decorados por categoria* |
| ![Categorias](docs/screenshot/desktop/categorias.png) | ![Contato](docs/screenshot/desktop/contato.png) |
| *Cardápio por categorias* | *Contato, mapa e horários* |

### Painel Administrativo

| | |
|:---:|:---:|
| ![Dashboard](docs/screenshot/desktop/dashboard.png) | ![Instagram Admin](docs/screenshot/desktop/dashboard_com_detalhe_na_imagem.png) |
| *Dashboard principal* | *Gerenciamento do Instagram* |
| ![Bolos Decorados Admin](docs/screenshot/desktop/admin_bolos_decorados.png) | ![API Docs](docs/screenshot/api/api_pt1.png) |
| *Gerenciamento de bolos decorados* | *Documentação da API (Swagger)* |

### Mobile

<div align="center">
  <img src="docs/screenshot/mobile/home.png" width="18%" alt="Home" />
  <img src="docs/screenshot/mobile/bolos_decorados.png" width="18%" alt="Bolos Decorados" />
  <img src="docs/screenshot/mobile/home_chatbot_aberto.png" width="18%" alt="Chatbot" />
  <img src="docs/screenshot/mobile/dashboard.png" width="18%" alt="Admin" />
  <img src="docs/screenshot/mobile/login.png" width="18%" alt="Login" />
</div>

---

## Funcionalidades

| Módulo | Descrição |
|--------|-----------|
| **Vitrine** | Cardápio por categorias, galeria de bolos decorados, sobre e contato |
| **Instagram** | Sync automático a cada 6h, classificação por palavra-chave na caption, categoria catch-all |
| **Carousel** | Posts em destaque com fallback automático — nunca fica vazio |
| **Chatbot** | Assistente virtual com Gemini AI, contexto do negócio e histórico de sessão |
| **Upload** | Imagens convertidas para WebP e otimizadas, armazenadas no S3 |
| **Auth** | JWT com refresh automático, roles OWNER e ADMIN |
| **Admin** | Painel completo para gerenciar produtos, categorias e posts sem conhecimento técnico |
| **CI/CD** | Deploy automático na EC2 com rollback em caso de falha |

---

## Arquitetura

```
┌──────────────┐     HTTPS      ┌─────────────────────────────────┐
│   React SPA  │ ─────────────► │          Nginx (EC2)            │
│   (Vite)     │                │                                 │
└──────────────┘                │  ┌──────────────────────────┐   │
                                │  │     FastAPI + Uvicorn    │   │
                                │  │   (Clean Architecture)   │   │
                                │  └────────────┬─────────────┘   │
                                │               │                  │
                                │  ┌────────────▼─────────────┐   │
                                │  │      PostgreSQL 15        │   │
                                │  └──────────────────────────┘   │
                                └─────────────────────────────────┘
                                              │
                              ┌───────────────┼───────────────┐
                              ▼               ▼               ▼
                          AWS S3        Instagram        Google
                         (imagens)      Graph API        Gemini AI
```

**Backend segue Clean Architecture** com 4 camadas:

```
API (controllers, DTOs)
    ↓
Application (usecases)
    ↓
Domain (models, repository interfaces)
    ↓
Infrastructure (ORM, S3, Gemini, Instagram, Scheduler)
```

---

## Início Rápido

### Pré-requisitos

- Python 3.12+ · Node.js 20+ · Docker & Docker Compose
- Conta AWS S3 · Chave Google Gemini · Token Instagram Graph API

### Com Docker (recomendado)

```bash
git clone <url-do-repositorio>
cd dalia-cakes-web

# Configurar variáveis de ambiente
cp .env.example .env
# edite o .env

# Subir tudo
make up

# Aplicar migrações
make migrate-docker

# → API:  http://localhost:8000/docs
# → Site: http://localhost:80
```

### Desenvolvimento local

```bash
# Backend
make quickstart     # cria venv + instala dependências + copia .env
make migrate        # aplica migrações
make run            # → http://localhost:8000

# Frontend (outro terminal)
cd frontend
npm install
npm run dev         # → http://localhost:5173
```

---

## Documentação Detalhada

| Módulo | README |
|--------|--------|
| Backend — API, arquitetura, testes, Instagram, CI/CD | [backend/README.md](backend/README.md) |
| Frontend — páginas, admin, autenticação, build | [frontend/README.md](frontend/README.md) |

---

## Estrutura do Repositório

```
dalia-cakes-web/
├── backend/               # API FastAPI (Clean Architecture)
│   └── src/
│       ├── api/           # Controllers e DTOs
│       ├── domain/        # Modelos e interfaces
│       ├── usecases/      # Lógica de negócio
│       └── infra/         # Banco, S3, Gemini, Instagram
├── frontend/              # SPA React + Tailwind
│   └── src/
│       ├── pages/         # Páginas públicas e admin
│       ├── components/    # Componentes reutilizáveis
│       └── services/      # Camada de acesso à API
├── migrations/            # Histórico Alembic
├── .github/workflows/     # Pipelines CI/CD
├── Dockerfile             # Backend
├── Dockerfile.frontend    # Frontend (multi-stage)
├── docker-compose.yml
├── Makefile               # Comandos prontos
└── .env.example
```

---

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais informações.

---

<div align="center">

Feito com muito carinho e dedicação para a **Confeitaria da Dalia** · 2026

</div>
