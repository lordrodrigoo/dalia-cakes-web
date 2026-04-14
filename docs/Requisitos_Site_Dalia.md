# Documento de Requisitos — Site Dalia Bolos e Doces

**Versão:** 1.0  
**Data:** Abril de 2026  
**Baseado em:** Pesquisa com usuários (4 respondentes) + definições do projeto

---

## 1. Visão Geral

Site institucional e de cardápio para a confeitaria artesanal **Dalia Bolos e Doces**, com foco em apresentar os produtos, facilitar o contato via WhatsApp e oferecer integração com iFood. O site deve ser mobile-first, rápido e visualmente atrativo, com ênfase em fotos de qualidade dos produtos e preços em destaque.

---

## 2. Público-Alvo

Clientes em potencial que buscam bolos personalizados, doces e salgados artesanais. Acessam majoritariamente pelo celular e valorizam facilidade de uso e rapidez.

---

## 3. Requisitos Funcionais

### 3.1 Cardápio Online

- Exibir todos os produtos com foto, nome, descrição e preço.
- Organizar produtos por categoria (ex: bolos, doces, salgados).
- Exibir bolos decorados separadamente por subcategoria (feminino, masculino, neutro, infantil menina, infantil menino).
- Mostrar recheios disponíveis por produto ou de forma geral.
- Indicar o peso mínimo dos bolos (a partir de X kg).

### 3.2 Integração com WhatsApp

- Botão flutuante do WhatsApp visível em todas as páginas.
- Ao clicar, abrir conversa com mensagem pré-preenchida (ex: "Olá, tenho interesse em fazer um pedido!").
- Seção de contato com link direto para o WhatsApp da confeitaria.

### 3.3 Integração com iFood

- Link ou botão visível na página inicial e/ou de contato redirecionando para o perfil no iFood.

### 3.4 Informações da Confeitaria

- **Sobre nós:** história da confeitaria, apresentação da Dalia.
- **Horário de funcionamento:** dias e horários de atendimento.
- **Formas de pagamento:** métodos aceitos (Pix, cartão, dinheiro etc.).
- **Endereço / Localização:** mesmo sendo porta fechada, indicar o bairro/cidade.
- **Canal de comunicação:** WhatsApp como canal principal de pedidos.

### 3.5 Chatbot

- Widget flutuante acessível em todas as páginas.
- Responde dúvidas sobre produtos, preços, recheios, pedidos e horários.
- Integrado ao catálogo real de produtos via backend (Gemini 2.5 Flash).

### 3.6 Bolos Decorados — Feed Instagram

- Exibir fotos reais dos bolos sincronizadas automaticamente do Instagram.
- Posts em destaque (até 3 dias após publicação) aparecem na página inicial.
- Navegação por subcategoria (feminino, masculino, neutro, infantil menina, infantil menino).

### 3.7 Compartilhamento de Produtos

- Botão para compartilhar produto via link ou redes sociais.

---

## 4. Requisitos Não Funcionais

### 4.1 Mobile-First (Prioridade Máxima)

- **100% dos respondentes** indicaram que o site deve ser fácil de usar no celular.
- Layout responsivo, pensado primeiro para telas de 375px+.
- Botões e elementos de toque com tamanho adequado (mínimo 44px).
- Menus simples e navegação intuitiva.

### 4.2 Performance

- Carregamento rápido (indicado por 25% dos respondentes como importante).
- Imagens otimizadas (lazy loading, formatos modernos como WebP).
- Mínimo de requisições bloqueantes.

### 4.3 Design

- Design bonito e moderno, com identidade visual da confeitaria.
- Fotos de qualidade dos produtos em destaque (**75% dos respondentes** consideraram essencial).
- Preços visíveis e em destaque (**75% dos respondentes**).
- Identidade visual a definir (pendente retorno do formulário de branding).

### 4.4 Acessibilidade

- Textos com contraste adequado.
- Alt text em todas as imagens.
- Navegação funcional via teclado.

### 4.5 SEO

- Títulos e meta descriptions por página.
- URL amigáveis (ex: `/cardapio/bolos-decorados`).
- Open Graph para compartilhamento em redes sociais.

---

## 5. Páginas e Conteúdo

| Página | Rota | Conteúdo Principal |
|--------|------|--------------------|
| Home | `/` | Banner, produtos em destaque, feed Instagram, categorias, CTA WhatsApp/iFood |
| Cardápio | `/cardapio` | Listagem geral de categorias |
| Bolos Decorados | `/cardapio/bolos-decorados` | Feed Instagram por subcategoria |
| Produtos | `/cardapio/produtos` | Todos os produtos por categoria |
| Categoria | `/cardapio/produtos/:categoria` | Produtos filtrados por categoria |
| Sobre | `/sobre` | História, horário, formas de pagamento |
| Contato | `/contato` | Endereço, WhatsApp, iFood, localização |

---

## 6. Componentes Globais

| Componente | Descrição |
|------------|-----------|
| Header | Logo + menu de navegação (hamburger no mobile) |
| Footer | Links úteis, redes sociais, contato rápido |
| Botão WhatsApp flutuante | Fixo no canto inferior, todas as páginas |
| Widget Chatbot | Fixo no canto inferior, todas as páginas |

---

## 7. Fora do Escopo (v1.0)

- Sistema de avaliações e depoimentos (poderá ser adicionado futuramente).
- **Carrinho de compras e vendas pelo site — não existirão.** Todos os pedidos são feitos via WhatsApp ou iFood.
- Pagamento online integrado ao site.
- Sistema de cadastro de clientes.
- Painel de pedidos para o cliente.

---

## 8. Observações do Negócio

- Trabalha com **iFood e encomendas via WhatsApp**.
- **Não há vendas pelo site** — o site é vitrine e canal de contato.
- **Não atende presencialmente** (porta fechada).
- Bolos personalizados: cliente deve entrar em contato via WhatsApp.
- Antecedência mínima para pedidos: 3 dias (pedidos simples a partir de 24h).

---

## 9. Stack Técnica

| Camada | Tecnologia |
|--------|-----------|
| Frontend | React JS (Vite) |
| Deploy Frontend | Vercel |
| Backend | FastAPI + PostgreSQL |
| Deploy Backend | Railway / Render |
| Chatbot IA | Google Gemini 2.5 Flash |
| Sincronização Instagram | Instagram Graph API + APScheduler |
