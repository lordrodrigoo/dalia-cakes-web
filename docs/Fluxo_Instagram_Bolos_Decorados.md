# 📸 Fluxo — Instagram → Bolos Decorados

## Visão Geral

Sempre que a Dalia postar uma foto de bolo no Instagram com uma hashtag de categoria, o site sincroniza automaticamente e organiza o post na seção correta.

---

## Fluxo Completo

```
Post no Instagram
com #feminino, #masculino, #neutro, #infantilmenina ou #infantilmenino
        │
        ▼
Sincronização automática
(job periódico busca novos posts via Instagram API)
        │
        ▼
Sistema lê as hashtags do caption
e identifica a subcategoria correspondente
        │
        ▼
Post salvo em instagram_posts
com subcategory (FK → decorated_cakes) e is_featured = true
        │
        ▼
Post aparece em "Últimos Bolos" na Home
e em Bolos Decorados (seção de destaque)
por 3 dias (featured_until = synced_at + 3 dias)
        │
        ▼  após 3 dias
Post sai do destaque (is_featured = false)
e passa a exibir apenas em:
bolos-decorados/{subcategoria}
ex: bolos-decorados/feminino
```

---

## Mapeamento de Hashtags

| Hashtag no Instagram | Subcategoria no site |
|---|---|
| `#feminino` | bolos-decorados/feminino |
| `#masculino` | bolos-decorados/masculino |
| `#neutro` | bolos-decorados/neutro |
| `#infantilmenina` | bolos-decorados/infantil/menina |
| `#infantilmenino` | bolos-decorados/infantil/menino |

> Se o post não tiver nenhuma hashtag de categoria reconhecida, ele é salvo sem subcategoria e não aparece em bolos decorados.

---

## Regras de Negócio

- `featured_until` = `synced_at + 3 dias`
- `is_featured` é atualizado automaticamente por um job agendado
- Um post pode ter múltiplas hashtags, mas apenas a primeira hashtag de categoria reconhecida é usada
- A sincronização roda a cada `INSTAGRAM_SYNC_INTERVAL_MINUTES` minutos (configurável via `.env`)
- O admin pode excluir ou forçar re-sincronização de posts pelo painel

---

## Envolvimento Técnico

| Componente | Responsabilidade |
|---|---|
| `instagram_usecase.py` | Lógica de sincronização e leitura de hashtags |
| `instagram_repository_impl.py` | Persistência no banco |
| `instagram_posts` (tabela) | Armazenamento dos posts sincronizados |
| `decorated_cakes` (tabela) | Referência das subcategorias válidas |
| Job agendado (APScheduler) | Atualiza `is_featured` e sincroniza novos posts |

---

*Dalia Bolos e Doces — v1.0 — Abril 2026*
