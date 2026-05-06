# Dalia Bolos e Doces — Frontend

> Interface web da confeitaria artesanal **Dalia Bolos e Doces**, construída com React 19 e Tailwind CSS.

![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-4-06B6D4?logo=tailwindcss&logoColor=white)
![React Router](https://img.shields.io/badge/React_Router-7-CA4245?logo=reactrouter&logoColor=white)
![Axios](https://img.shields.io/badge/Axios-1.15-5A29E4)
![Node](https://img.shields.io/badge/Node-20+-339933?logo=node.js&logoColor=white)

---

## Índice

- [Visão Geral](#visão-geral)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Páginas e Rotas](#páginas-e-rotas)
- [Painel Administrativo](#painel-administrativo)
- [Cliente HTTP e Autenticação](#cliente-http-e-autenticação)
- [Como Começar](#como-começar)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Build e Deploy](#build-e-deploy)
- [CI/CD](#cicd)

---

## Visão Geral

SPA (Single Page Application) que serve como vitrine digital da confeitaria. Apresenta o cardápio, a galeria de bolos decorados e informações de contato para os clientes — e oferece um painel administrativo completo para a proprietária gerenciar todo o conteúdo do site sem precisar de conhecimento técnico.

**Destaques:**
- Galeria de bolos decorados com categorias (Feminino, Masculino, Infantil, etc.) alimentada pelo Instagram
- Carousel de posts em destaque na Home com fallback automático
- Painel admin protegido por JWT com refresh automático de token
- Integração completa com a API: produtos, categorias, Instagram e upload de imagens
- SEO configurado por página com `useSEO` hook customizado
- Design responsivo com Tailwind CSS

---

## Tecnologias

| Categoria | Tecnologia |
|-----------|-----------|
| Framework | React 19 |
| Build tool | Vite 8 |
| Estilo | Tailwind CSS 4 |
| Roteamento | React Router DOM 7 |
| HTTP client | Axios 1.15 |
| Notificações | react-hot-toast |
| Slider | keen-slider |
| Lint | ESLint 9 |
| Deploy | Docker + Nginx |

---

## Estrutura do Projeto

```
frontend/
├── src/
│   ├── assets/
│   │   ├── icons/              # Ícones (WhatsApp, Instagram, iFood, Facebook)
│   │   └── images/             # Imagens estáticas (logo, caricatura)
│   │
│   ├── components/
│   │   ├── admin/
│   │   │   └── AdminLayout.jsx     # Sidebar + estrutura do painel admin
│   │   ├── home/
│   │   │   ├── CategoryCards.jsx   # Cards de categorias na Home
│   │   │   ├── HeroBanner.jsx      # Banner principal
│   │   │   ├── InstagramFeed.jsx   # Carousel de posts em destaque
│   │   │   ├── WhatsAppButton.jsx  # Botão flutuante WhatsApp
│   │   │   ├── FacebookButton.jsx
│   │   │   ├── IfoodButton.jsx
│   │   │   └── InstagramButton.jsx
│   │   ├── Header.jsx          # Navegação principal
│   │   ├── Footer.jsx
│   │   ├── Layout.jsx          # Wrapper com Header + Footer
│   │   ├── Login.jsx           # Formulário de login
│   │   └── ProtectedRoute.jsx  # Guard para rotas admin
│   │
│   ├── hooks/
│   │   └── useSEO.js           # Hook para title/description por página
│   │
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Cardapio.jsx
│   │   ├── Produtos.jsx
│   │   ├── BolosDecorados.jsx
│   │   ├── Sobre.jsx
│   │   ├── Contato.jsx
│   │   ├── LoginPage.jsx
│   │   └── admin/
│   │       ├── dashboard.jsx
│   │       ├── Categorias.jsx
│   │       ├── Produtos.jsx
│   │       ├── BolosDecorados.jsx
│   │       └── Instagram.jsx
│   │
│   ├── services/               # Camada de acesso à API
│   │   ├── api.js              # Instância Axios + interceptors
│   │   ├── auth.js             # Login, refresh, logout
│   │   ├── categories.js
│   │   ├── products.js
│   │   ├── instagram.js
│   │   ├── decoratedCakes.js
│   │   ├── upload.js
│   │   └── chatbot.js
│   │
│   ├── styles/                 # Objetos de classes Tailwind por componente
│   │   ├── adminInstagram.styles.js
│   │   ├── bolosDecorados.styles.js
│   │   └── ... (um arquivo por página/componente)
│   │
│   ├── utils/
│   │   └── whatsapp.js         # Gera links do WhatsApp com mensagem pré-preenchida
│   │
│   ├── data/
│   │   └── instagramMock.js    # Dados mock para desenvolvimento sem API
│   │
│   ├── App.jsx                 # Definição de rotas
│   └── main.jsx                # Entry point
│
├── public/
├── index.html
├── vite.config.js
├── .env.example
└── package.json
```

---

## Páginas e Rotas

### Rotas públicas

Todas as rotas públicas usam o `Layout` com Header e Footer.

| Rota | Componente | Descrição |
|------|-----------|-----------|
| `/` | `Home` | Página principal com hero banner, categorias e carousel do Instagram |
| `/cardapio` | `Cardapio` | Listagem de todas as categorias do cardápio |
| `/cardapio/:categoriaSlug` | `Produtos` | Produtos de uma categoria específica |
| `/bolos-decorados` | `BolosDecorados` | Galeria de bolos por subcategoria com lightbox |
| `/sobre` | `Sobre` | História e informações da confeitaria |
| `/contato` | `Contato` | Formulário de contato, endereço e mapa |
| `/login` | `LoginPage` | Página de login (sem Header/Footer) |

### Detalhe das páginas principais

**Home (`/`)**
- HeroBanner com call-to-action para WhatsApp e iFood
- CategoryCards mostrando as categorias do cardápio
- InstagramFeed: carousel de posts em destaque. Se não houver posts novos há mais de 3 dias, exibe automaticamente os 12 mais recentes — o carousel nunca fica vazio

**Bolos Decorados (`/bolos-decorados`)**
- Tabs de navegação por subcategoria (Feminino, Masculino, Infantil Menina, etc.)
- Grid de imagens com hover effect
- Lightbox com navegação prev/next
- Botão para pedir bolo similar pelo WhatsApp com link direto para o post do Instagram

---

## Painel Administrativo

Acessível em `/admin` — protegido por JWT. Requer login com role `ADMIN` ou `OWNER`.

### Dashboard (`/admin`)
Visão geral com cards de resumo: total de posts, posts em destaque, posts sem subcategoria, subcategorias cadastradas.

### Categorias (`/admin/categorias`)
- Listagem de todas as categorias do cardápio
- Criar, editar e excluir categorias
- Upload de imagem por categoria

### Produtos (`/admin/produtos`)
- Listagem e busca de produtos
- Criar, editar e excluir produtos
- Associação com categoria
- Upload de imagem por produto

### Bolos Decorados (`/admin/bolos-decorados`)
- Gerenciar subcategorias (criar, editar, excluir)
- Cada subcategoria tem: nome, slug e palavra-chave para matching automático com Instagram

### Instagram (`/admin/instagram`)
A tela mais completa do painel.

**Funcionalidades:**

| Ação | Descrição |
|------|-----------|
| **Sincronizar** | Dispara o sync manual com o Instagram e atualiza a tela |
| **Nova foto** | Upload manual de imagem para criar um post sem Instagram |
| **Classificar** | Atribui manualmente um post a uma subcategoria |
| **Destacar na Home** | Marca/desmarca um post como featured (aparece no carousel) |
| **Excluir** | Remove o post do banco |
| **Filtrar** | Filtra a grade por subcategoria |

**Indicadores visuais:**
- Badge `⭐ Destaque` nos posts atualmente em destaque
- Nome da subcategoria exibido sobre a imagem no hover
- Quando a imagem do CDN do Instagram expirou, exibe ícone 📷 em vez do texto da caption

---

## Cliente HTTP e Autenticação

Todo acesso à API passa pela instância Axios configurada em `services/api.js`.

### Interceptor de request
Injeta automaticamente o header `Authorization: Bearer <token>` em todas as requisições se houver um `access_token` no `localStorage`.

```js
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})
```

### Interceptor de response — refresh automático
Quando a API retorna `401 Unauthorized`:
1. Tenta renovar o access token usando o `refresh_token` armazenado
2. Se bem-sucedido, repete a requisição original com o novo token transparentemente
3. Se o refresh também falhar (token expirado/inválido), limpa o storage e redireciona para `/login`

Esse mecanismo garante que a administradora nunca seja interrompida no meio do trabalho por um token expirado.

### Serviços disponíveis

| Arquivo | Operações |
|---------|-----------|
| `auth.js` | login, refresh, logout |
| `categories.js` | listar, buscar por slug/id, criar, atualizar, deletar |
| `products.js` | listar, buscar por id/categoria, criar, atualizar, deletar |
| `instagram.js` | posts featured, todos, não classificados, sync, toggle featured, deletar, upload manual, classificar |
| `decoratedCakes.js` | listar subcategorias, posts por subcategoria, criar, atualizar, deletar subcategoria |
| `upload.js` | upload de imagem |
| `chatbot.js` | enviar mensagem ao assistente virtual |

---

## Como Começar

### Pré-requisitos

- Node.js 20+
- npm
- Backend rodando (ver `backend/README.md`)

### Instalação

```bash
cd frontend

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env
# edite o .env com a URL da API e dados do negócio

# Iniciar em modo desenvolvimento
npm run dev
# → http://localhost:5173
```

### Scripts disponíveis

```bash
npm run dev       # Servidor de desenvolvimento com HMR
npm run build     # Build de produção em dist/
npm run preview   # Preview local do build de produção
npm run lint      # ESLint em todo o src/
```

---

## Variáveis de Ambiente

Copie `.env.example` para `.env`:

```env
# URL base da API — sem barra final
VITE_API_URL=http://localhost:8000/api/v1

# Contato e negócio
VITE_BUSINESS_PHONE=+5511999999999
VITE_WHATSAPP_NUMBER=5511999999999

# Links externos
VITE_IFOOD_URL=https://www.ifood.com.br/...
VITE_ADDRESS=Rua Exemplo, 123 - Vila Carrão, São Paulo
VITE_MAPS_LINK=https://maps.google.com/?q=...
VITE_MAPS_EMBED=https://www.google.com/maps/embed?...
```

> Todas as variáveis devem começar com `VITE_` para serem expostas pelo Vite ao código do cliente.

> **Nunca faça commit do `.env`.** Ele está no `.gitignore`.

---

## Build e Deploy

### Build de produção

```bash
npm run build
# Saída em frontend/dist/
```

### Docker

O `Dockerfile.frontend` usa **multi-stage build**:

1. **Stage build** — instala dependências e executa `vite build`
2. **Stage produção** — copia `dist/` para uma imagem Nginx Alpine mínima

O `nginx.conf` configura:
- `try_files $uri /index.html` para suporte às rotas do React Router (SPA)
- Cache de longa duração para assets com hash no nome

```bash
# Build da imagem
docker build -f Dockerfile.frontend -t dalia-cakes-frontend .

# Rodar localmente
docker run -p 80:80 dalia-cakes-frontend
# → http://localhost:80
```

---

## CI/CD

O pipeline é automatizado via **GitHub Actions** (`.github/workflows/frontend.yml`).

### Estágios

```
[Source]     [Build]           [Deploy]
lint     →   build-image   →   publish-image  →  deploy-ec2
```

| Etapa | Trigger | O que faz |
|-------|---------|-----------|
| `lint` | PR + push main | ESLint em todo o código |
| `build-image` | PR + push main | Build da imagem Docker (sem push, valida que compila) |
| `publish-image` | Push main | Publica imagem no GHCR com tag `sha-{commit}` e `latest` |
| `deploy-ec2` | Push main | Deploy via SSH na EC2 com health check e rollback automático |

### Rollback automático

Se `curl http://localhost:80` falhar após o deploy, o pipeline reverte automaticamente para a imagem anterior e registra o evento.

### Secrets necessários no GitHub

| Secret | Descrição |
|--------|-----------|
| `EC2_HOST` | IP ou domínio da instância EC2 |
| `EC2_USER` | Usuário SSH (ex: `ubuntu`) |
| `EC2_SSH_KEY` | Chave privada SSH |
| `EC2_DEPLOY_PATH` | Caminho do projeto na EC2 |
| `CONTAINER_REGISTRY_TOKEN` | GitHub PAT com permissão `packages:write` |
| `CONTAINER_REGISTRY_USERNAME` | Usuário GitHub |

---

*Dalia Bolos e Doces — Frontend v1.0 — 2026*
