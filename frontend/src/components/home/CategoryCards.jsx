import { Link } from "react-router-dom"
import { categoryCardsStyles as s } from "../../styles/categoryCards.styles"

const categories = [
  { id: 1,
    name: "Bolos Decorados",
    slug: "bolos-decorados",
    description: "Bolos personalizados para todas as ocasiões.",
    image: "/assets/images/categoria-bolos.jpg" 
},
  { id: 2,
    name: "Bolos com cobertura",
    slug: "bolos-com-cobertura",
    description: "Bolos com diferentes tipos de cobertura para todos os gostos.",
    image: "/assets/images/categoria-doces.jpg"
  },
  { id: 3,
    name: "Bolos da vovó",
    slug: "bolos-da-vovo",
    description: "Bolos caseiros e tradicionais.",
    image: "/assets/images/categoria-bolos-da-vovo.jpg"
  },
  { id: 4,
    name: "Doces e Sobremesas",
    slug: "doces-e-sobremesas",
    description: "Sobremesas individuais deliciosas para qualquer ocasião.",
    image: "/assets/images/categoria-sobremesas.jpg"
  },
  { id: 5,
    name: "Sobremesas Tamanho Família",
    slug: "sobremesas-tamanho-familia",
    description: "Sobremesas deliciosas em porções maiores para compartilhar.",
    image: "/assets/images/categoria-tematicos.jpg"
  },
  { id: 6,
    name: "Bolos de pote",
    slug: "bolos-de-pote",
    description: "Bolos deliciosos em potes individuais.",
    image: "/assets/images/categoria-bolos-de-pote.jpg"
  },
  { id: 7,
    name: "Cones recheados",
    slug: "cones-recheados",
    description: "Cones deliciosos recheados para qualquer ocasião.",
    image: "/assets/images/categoria-cones-recheados.jpg"
  },
  { id: 8,
    name: "Copos da felicidade",
    slug: "copos-da-felicidade",
    description: "Copos deliciosos recheados para qualquer ocasião.",
    image: "/assets/images/categoria-copos-da-felicidade.jpg"
 },
]
    
export default function CategoryCards() {
  return (
    <section className={s.section}>
      <h2 className={s.title}>Categorias</h2>
      <div className={s.grid}>
        {categories.map((cat) => (
          <Link key={cat.id} to={`/cardapio/${cat.slug}`} className={s.card}>
            <img src={cat.image} alt={cat.name} className={s.cardImg} />
            <div className={s.cardContent}>
              <h3 className={s.cardTitle}>{cat.name}</h3>
              <p className={s.cardDesc}>{cat.description}</p>
              <span className={s.cardBtn}>Ver produtos</span>
            </div>
          </Link>
        ))}
      </div>
    </section>
  )
}
