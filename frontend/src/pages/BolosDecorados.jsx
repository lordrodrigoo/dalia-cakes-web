import { useState, useEffect } from 'react'
import { getSubcategories, getPostsBySubcategory } from '../services/decoratedCakes'
import { bolosDecoradosStyles as s } from '../styles/bolosDecorados.styles'

export default function BolosDecorados() {
  const [subcategories, setSubcategories] = useState([])
  const [activeTab, setActiveTab] = useState(null)
  const [posts, setPosts] = useState([])
  const [loadingPosts, setLoadingPosts] = useState(false)
  const [loading, setLoading] = useState(true)
  const [selectedIndex, setSelectedIndex] = useState(null)

  useEffect(() => {
    const fetchSubcategories = async () => {
      try {
        const res = await getSubcategories()
        setSubcategories(res.data)
        if (res.data.length > 0) {
          setActiveTab(res.data[0].id)
        }
      } catch {
        setSubcategories([])
      } finally {
        setLoading(false)
      }
    }
    fetchSubcategories()
  }, [])

  useEffect(() => {
    if (!activeTab) return
    const fetchPosts = async () => {
      setLoadingPosts(true)
      try {
        const res = await getPostsBySubcategory(activeTab)
        setPosts(res.data)
      } catch {
        setPosts([])
      } finally {
        setLoadingPosts(false)
      }
    }
    fetchPosts()
  }, [activeTab])

  const handlePrev = () => {
    setSelectedIndex(prev => (prev > 0 ? prev - 1 : posts.length - 1))
  }

  const handleNext = () => {
    setSelectedIndex(prev => (prev < posts.length - 1 ? prev + 1 : 0))
  }

  if (loading) return <p className={s.empty}>Carregando...</p>

  return (
    <div className={s.wrapper}>
      <div>
        <h1 className={s.heading}>Bolos Decorados</h1>
        <p className={s.subheading}>Personalizados para qualquer ocasião</p>
      </div>

      {/* Tabs */}
      <div className={s.tabs}>
        {subcategories.map(sub => (
          <button
            key={sub.id}
            className={activeTab === sub.id ? s.tabActive : s.tab}
            onClick={() => setActiveTab(sub.id)}
          >
            {sub.name}
          </button>
        ))}
      </div>

      {/* Grid */}
      {loadingPosts ? (
        <p className={s.empty}>Carregando fotos...</p>
      ) : posts.length === 0 ? (
        <p className={s.empty}>Nenhuma foto nesta categoria ainda.</p>
      ) : (
        <div className={s.grid}>
          {posts.map((post, index) => (
            <div
              key={post.id}
              className={s.imgWrapper}
              onClick={() => setSelectedIndex(index)}
            >
              <img src={post.media_url} alt={post.caption || 'Bolo decorado'} className={s.img} />
            </div>
          ))}
        </div>
      )}

      {/* Modal lightbox */}
      {selectedIndex !== null && (
        <div className={s.modalOverlay} onClick={() => setSelectedIndex(null)}>
          <div className={s.modal} onClick={e => e.stopPropagation()}>
            <button className={s.modalClose} onClick={() => setSelectedIndex(null)}>✕</button>
            <img
              src={posts[selectedIndex].media_url}
              alt={posts[selectedIndex].caption || 'Bolo decorado'}
              className={s.modalImg}
            />
            <div className={s.modalNav}>
              <button className={s.modalPrev} onClick={handlePrev}>‹</button>
              <button className={s.modalNext} onClick={handleNext}>›</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
