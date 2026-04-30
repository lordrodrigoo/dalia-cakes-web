import { getFeaturedPosts } from "../../services/instagram"
import { useKeenSlider } from "keen-slider/react"
import { useEffect, useState } from "react"
import "keen-slider/keen-slider.min.css"
import { instagramFeedStyles as s } from "../../styles/instagramFeed.styles"

const isInstagramUrl = (url) => url && url.includes("instagram.com")

export default function InstagramFeed() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState(null)
  const [shareMenuOpen, setShareMenuOpen] = useState(false)
  const [copied, setCopied] = useState(false)

  const [sliderRef, instanceRef] = useKeenSlider({
    slides: { perView: 1, spacing: 8 },
    breakpoints: {
      "(min-width: 640px)": { slides: { perView: 2, spacing: 12 } },
      "(min-width: 1024px)": { slides: { perView: 3, spacing: 16 } },
    },
    loop: true,
  })

  useEffect(() => {
    getFeaturedPosts()
      .then(res => setPosts(res.data))
      .catch(() => setPosts([]))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    if (posts.length > 1 && instanceRef.current) {
      const interval = setInterval(() => instanceRef.current.next(), 8000)
      return () => clearInterval(interval)
    }
  }, [instanceRef, posts.length])

  useEffect(() => {
    const onKey = (e) => { if (e.key === "Escape") setSelected(null) }
    window.addEventListener("keydown", onKey)
    return () => window.removeEventListener("keydown", onKey)
  }, [])

  const handleShareWhatsApp = (url) => {
    const text = encodeURIComponent(`Olha este bolo que vi no site da Confeitaria da Dalia!\n${url}`)
    window.open(`https://wa.me/?text=${text}`, '_blank')
    setShareMenuOpen(false)
  }

  const handleCopyLink = async (url) => {
    await navigator.clipboard.writeText(url)
    setCopied(true)
    setShareMenuOpen(false)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleNativeShare = async (post) => {
    if (navigator.share) {
      try {
        await navigator.share({ title: "Confeitaria da Dalia", url: post.permalink })
      } catch { /* share cancelled */ }
    } else {
      setShareMenuOpen(prev => !prev)
    }
  }

if (loading) return <div>Carregando...</div>
  if (posts.length === 0) return null

  return (
    <section className={s.section}>
      <h2 className={s.title}>Nossos últimos posts no Instagram</h2>

      {posts.length === 1 ? (
        <div className={s.single}>
          <div className={`${s.item} ${s.singleItem}`} onClick={() => setSelected(posts[0])}>
            <div className={s.imgWrapper}>
              <img src={posts[0].media_url} alt="" className={s.img} />
              <div className={s.overlay}>
                <span className={s.overlayHint}>Ver foto</span>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className={s.sliderWrapper}>
          <button className={s.arrow} onClick={() => instanceRef.current?.prev()} aria-label="Anterior">‹</button>
          <div ref={sliderRef} className={`keen-slider ${s.carousel}`}>
            {posts.map(post => (
              <div key={post.id} className={`keen-slider__slide ${s.item}`} onClick={() => setSelected(post)}>
                <div className={s.imgWrapper}>
                  <img src={post.media_url} alt="" className={s.img} />
                  <div className={s.overlay}>
                    <span className={s.overlayHint}>Ver foto</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <button className={s.arrow} onClick={() => instanceRef.current?.next()} aria-label="Próximo">›</button>
        </div>
      )}

      {selected && (
        <div className={s.lightboxOverlay} onClick={() => { setSelected(null); setShareMenuOpen(false) }}>
          <div className={s.lightboxBox} onClick={e => e.stopPropagation()}>
            <button className={s.lightboxClose} onClick={() => { setSelected(null); setShareMenuOpen(false) }}>✕</button>
            <img src={selected.media_url} alt="" className={s.lightboxImg} />
            <div className={s.lightboxFooter}>
              {isInstagramUrl(selected.permalink) && (
                <a href={selected.permalink} target="_blank" rel="noopener noreferrer" className={s.lightboxInstagramBtn}>
                  Ver no Instagram
                </a>
              )}
              <div className={s.shareWrapper}>
                <button className={s.lightboxShareBtn} onClick={() => handleNativeShare(selected)}>
                  {copied ? 'Link copiado!' : 'Compartilhar'}
                </button>
                {shareMenuOpen && (
                  <div className={s.shareMenu}>
                    <button className={s.shareMenuItem} onClick={() => handleShareWhatsApp(selected.permalink)}>
                      <svg className={`${s.shareMenuIcon} text-green-500`} viewBox="0 0 24 24" fill="currentColor">
                        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                      </svg>
                      WhatsApp
                    </button>
                    <button className={s.shareMenuItem} onClick={() => handleCopyLink(selected.permalink)}>
                      <svg className={s.shareMenuIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/>
                        <path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/>
                      </svg>
                      Copiar link
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}


    </section>
  )
}
