import { Link } from 'react-router-dom'
import logo from '../../assets/images/logo_home.png'
import { heroBannerStyles as s } from '../../styles/heroBanner.styles'

export default function HeroBanner() {
  return (
    <section className={s.section}>
      <div className={s.content}>
        <img src={logo} alt="Dália Moreira Bolos e Doces" className={s.logo} />
        <p className={s.eyebrow}>Confeitaria Artesanal</p>
        <h1 className={s.title}>Bolos, Doces e Sobremesas</h1>
        <p className={s.subtitle}>Encomende seu bolo personalizado para qualquer ocasião</p>
        <Link to="/cardapio" className={s.cta}>Ver Cardápio</Link>
      </div>
    </section>
  )
}
