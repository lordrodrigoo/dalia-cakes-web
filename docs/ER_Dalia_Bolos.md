# 🎂 Dalia Bolos e Doces — Diagrama ER

## Tabelas

### users
| Campo | Tipo | Detalhe |
|---|---|---|
| id | UUID | PK |
| username | STRING | único |
| email | STRING | único |
| password | STRING | bcrypt |
| is_owner | BOOLEAN | |
| created_at | TIMESTAMP WITH TIME ZONE | |
| updated_at | TIMESTAMP WITH TIME ZONE | |

---

### categories
| Campo | Tipo | Detalhe |
|---|---|---|
| id | UUID | PK |
| name | STRING | |
| slug | STRING | único |
| image_url | STRING | nullable |
| created_at | TIMESTAMP WITH TIME ZONE | |
| updated_at | TIMESTAMP WITH TIME ZONE | |

---

### products
| Campo | Tipo | Detalhe |
|---|---|---|
| id | UUID | PK |
| name | STRING | |
| price | NUMERIC(10,2) | |
| image_url | STRING | nullable |
| category_id | UUID | FK → categories.id |
| created_at | TIMESTAMP WITH TIME ZONE | |
| updated_at | TIMESTAMP WITH TIME ZONE | |

---

### decorated_cakes
| Campo | Tipo | Detalhe |
|---|---|---|
| id | UUID | PK |
| slug | STRING | único |
| created_at | TIMESTAMP WITH TIME ZONE | |
| updated_at | TIMESTAMP WITH TIME ZONE | |

Valores de slug: `feminino`, `masculino`, `neutro`, `infantil-menina`, `infantil-menino`

---

### instagram_posts
| Campo | Tipo | Detalhe |
|---|---|---|
| id | UUID | PK |
| post_id | STRING | ID original do Instagram |
| image_url | STRING | |
| caption | STRING | legenda do post |
| permalink | STRING | link do post |
| hashtags | STRING | hashtags extraídas |
| subcategory | UUID | FK → decorated_cakes.id, nullable |
| is_featured | BOOLEAN | em destaque na home |
| featured_until | TIMESTAMP | created_at + 3 dias |
| synced_at | TIMESTAMP WITH TIME ZONE | |
| created_at | TIMESTAMP WITH TIME ZONE | |
| updated_at | TIMESTAMP WITH TIME ZONE | |

---

## Relacionamentos

```
categories       1 ──── N  products
decorated_cakes  1 ──── N  instagram_posts
users                       (independente, acesso via JWT)
```

---

*Dalia Bolos e Doces — v1.0 — Abril 2026*
