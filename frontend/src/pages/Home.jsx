import HeroBanner from '../components/home/HeroBanner'
import CategoryCards from '../components/home/CategoryCards'
import InstagramFeed from '../components/home/InstagramFeed'
import { useSEO } from '../hooks/useSEO'

export default function Home() {
  useSEO({
    description: 'Confeitaria artesanal especializada em bolos decorados, doces finos e muito mais. Encomende pelo WhatsApp ou iFood.',
  })

  return (
    <>
      <HeroBanner />
      <InstagramFeed />
      <CategoryCards />
     

    </>
  )
}