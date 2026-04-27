import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { getCategoryBySlug } from '../services/categories'
import { getProductsByCategory } from '../services/products'
import { produtosStyles as s } from '../styles/produtos.styles'
import whatsappIcon from '../assets/icons/whatsapp.png'
import ifoodIcon from '../assets/icons/Ifood_logo_sem_fundo.png'

const WHATSAPP_NUMBER = import.meta.env.VITE_BUSINESS_PHONE.replace(/\D/g, '')
const IFOOD_URL = import.meta.env.VITE_IFOOD_URL

function buildWhatsAppLink(productName) {
  const message = encodeURIComponent(`Olá! Tenho interesse no produto: ${productName} 🎂`)
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${message}`
}

export default function Produtos() {
  const { categoriaSlug } = useParams()
  const [category, setCategory] = useState(null)
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedProduct, setSelectedProduct] = useState(null)

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const catRes = await getCategoryBySlug(categoriaSlug)
        const cat = catRes.data
        setCategory(cat)
        const prodRes = await getProductsByCategory(cat.id)
        setProducts(prodRes.data)
      } catch {
        setProducts([])
      } finally {
        setLoading(false)
      }
    }
    fetchAll()
  }, [categoriaSlug])

  if (loading) return <p className={s.empty}>Carregando...</p>

  return (
    <div className={s.wrapper}>
      <div className={s.header}>
        <h1 className={s.heading}>{category?.name || 'Produtos'}</h1>
      </div>

      {products.length === 0 ? (
        <p className={s.empty}>Nenhum produto nesta categoria.</p>
      ) : (
        <div className={s.grid}>
          {products.map(product => (
            <div
              key={product.id}
              className={s.card}
              onClick={() => setSelectedProduct(product)}
            >
              <div className={s.cardImgWrapper}>
                <img src={product.image_url} alt={product.name} className={s.cardImg} />
              </div>
              <div className={s.cardBody}>
                <span className={s.cardName}>{product.name}</span>
                <span className={s.cardPrice}>R$ {Number(product.price).toFixed(2)}</span>
              </div>
            </div>
          ))}
        </div>
      )}

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
                  <img src={whatsappIcon} alt="WhatsApp" className={s.iconBtn} />
                  Encomendar pelo WhatsApp
                </a>
                <a
                  href={IFOOD_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={s.ifoodBtn}
                >
                  <img src={ifoodIcon} alt="iFood" className={s.iconBtn} />
                  Ver no iFood
                </a>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
