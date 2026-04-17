import { getFeaturedPosts } from "../../services/instagram"
import { useKeenSlider } from "keen-slider/react"
import { useEffect, useState } from "react"
import "keen-slider/keen-slider.min.css"
import { instagramFeedStyles as s } from "../../styles/instagramFeed.styles"


export default function InstagramFeed() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
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

  if (loading) return <div>Carregando...</div>
  if (posts.length === 0) return <div>Nenhum post encontrado.</div>

  if (posts.length === 1) {
    return (
      <section className={s.section}>
        <h2 className={s.title}>Nossos últimos posts no Instagram</h2>
        <div className={s.single}>
          <a href={posts[0].link} target="_blank" rel="noopener noreferrer" className={`${s.item} ${s.singleItem}`}>
            <div className={s.imgWrapper}>
              <img src={posts[0].image} alt={posts[0].caption} className={s.img} />
            </div>
          </a>
        </div>
      </section>
    )
  }

  return (
    <section className={s.section}>
      <h2 className={s.title}>Nossos últimos posts no Instagram</h2>
      <div className={s.sliderWrapper}>
        <button className={s.arrow} onClick={() => instanceRef.current?.prev()} aria-label="Anterior">‹</button>
        <div ref={sliderRef} className={`keen-slider ${s.carousel}`}>
          {posts.map(post => (
            <a key={post.id} href={post.link} target="_blank" rel="noopener noreferrer" className={`keen-slider__slide ${s.item}`}>
              <div className={s.imgWrapper}>
                <img src={post.image} alt={post.caption} className={s.img} />
              </div>
              {post.caption && <p className={s.caption}>{post.caption}</p>}
            </a>
          ))}
        </div>
        <button className={s.arrow} onClick={() => instanceRef.current?.next()} aria-label="Próximo">›</button>
      </div>
    </section>
  )
}
