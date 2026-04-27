import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { getCategories } from "../../services/categories"
import { categoryCardsStyles as s } from "../../styles/categoryCards.styles"


export default function CategoryCards() {
  const [categories, setCategories] = useState([])

  useEffect(() => {
    getCategories()
      .then(res => setCategories(res.data))
      .catch(() => setCategories([]))
  }, [])

  return (
    <section className={s.section}>
      <h2 className={s.title}>Categorias</h2>
      <div className={s.grid}>
        {categories.map((cat) => (
          <Link key={cat.id} to={`/cardapio/${cat.slug}`} className={s.card}>
            <img src={cat.image_url} alt={cat.name} className={s.cardImg} />
            <div className={s.cardContent}>
              <h3 className={s.cardTitle}>{cat.name}</h3>
              <span className={s.cardBtn}>Ver produtos</span>
            </div>
          </Link>
        ))}
      </div>
    </section>
  )
}
