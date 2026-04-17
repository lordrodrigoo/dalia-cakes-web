import HeroBanner from '../components/home/HeroBanner'
import CategoryCards from '../components/home/CategoryCards'
import InstagramFeed from '../components/home/InstagramFeed'
import WhatsAppCTA from '../components/home/WhatsAppCTA'

export default function Home() {
  return (
    <>
      <HeroBanner />
      <InstagramFeed />
      <CategoryCards />
      <WhatsAppCTA />
    </>
  )
}