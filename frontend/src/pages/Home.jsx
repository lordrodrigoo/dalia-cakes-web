import HeroBanner from '../components/home/HeroBanner'
import CategoryCards from '../components/home/CategoryCards'
import FeaturedProducts from '../components/home/FeaturedProducts'
import InstagramFeed from '../components/home/InstagramFeed'
import WhatsAppCTA from '../components/home/WhatsAppCTA'

export default function Home() {
    return (
        <main>
            <HeroBanner />
            <InstagramFeed />
            <CategoryCards />
            <FeaturedProducts />
            <WhatsAppCTA />
        </main>
    )
}
