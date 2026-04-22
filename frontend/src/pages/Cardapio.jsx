import { useState, useEffect } from 'react'
import { getCategories } from '../services/categories'
import { getProductsByCategory } from '../services/products'
import { cardapioStyles as s } from '../styles/cardapio.styles'

const WHATSAPP_NUMBER = import.meta.env.VITE_BUSINESS_PHONE.replace(/\D/g, '')
const IFOOD_URL = import.meta.env.VITE_IFOOD_URL

function buildWhatsAppLink(productName) {
  const message = encodeURIComponent(`Olá! Tenho interesse no produto: ${productName} 🎂`)
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${message}`
}

export default function Cardapio() {
  const [sections, setSections] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedProduct, setSelectedProduct] = useState(null)

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const catRes = await getCategories()
        const categories = catRes.data

        const sectionsData = await Promise.all(
          categories.map(async (cat) => {
            const prodRes = await getProductsByCategory(cat.id)
            return { category: cat, products: prodRes.data }
          })
        )

        setSections(sectionsData.filter(s => s.products.length > 0))
      } catch {
        setSections([])
      } finally {
        setLoading(false)
      }
    }

    fetchAll()
  }, [])

  if (loading) return <p className={s.empty}>Carregando...</p>
  if (sections.length === 0) return <p className={s.empty}>Nenhum produto encontrado.</p>

  return (
    <div className={s.wrapper}>
      {sections.map(({ category, products }) => (
        <section key={category.id} className={s.section}>
          <h2 className={s.categoryTitle}>{category.name}</h2>
          <div className={s.grid}>
            {products.map(product => (
              <div
                key={product.id}
                className={s.card}
                onClick={() => setSelectedProduct(product)}
              >
                <div className="overflow-hidden">
                  <img src={product.image_url} alt={product.name} className={s.cardImg} />
                </div>
                <div className={s.cardBody}>
                  <span className={s.cardName}>{product.name}</span>
                  <span className={s.cardPrice}>R$ {Number(product.price).toFixed(2)}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      ))}

      {/* Modal */}
      {selectedProduct && (
        <div className={s.modalOverlay} onClick={() => setSelectedProduct(null)}>
          <div className={`${s.modal} relative`} onClick={e => e.stopPropagation()}>
            <button className={s.modalClose} onClick={() => setSelectedProduct(null)}>✕</button>
            <img src={selectedProduct.image_url} alt={selectedProduct.name} className={s.modalImg} />
            <div className={s.modalBody}>
              <h2 className={s.modalName}>{selectedProduct.name}</h2>
              <span className={s.modalPrice}>R$ {Number(selectedProduct.price).toFixed(2)}</span>
              {selectedProduct.description && (
                <p className={s.modalDesc}>{selectedProduct.description}</p>
              )}
              <div className={s.modalActions}>
                <a
                  href={buildWhatsAppLink(selectedProduct.name)}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={s.whatsappBtn}
                >
                  🟢 Encomendar pelo WhatsApp
                </a>
                <a
                  href={IFOOD_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={s.ifoodBtn}
                >
                  🛵 Ver no iFood
                </a>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
