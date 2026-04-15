import { Link } from 'react-router-dom'
import logo from '../../assets/images/logo_home.png'

export default function HeroBanner() {
    return (
        <section className="hero">
            <div className="hero__content">
                <img src={logo} alt="Dália Moreira Bolos e Doces" className="hero__logo" />
                <p className="hero__eyebrow">Confeitaria Artesanal</p>
                <h1 className="hero__title">
                    Bolos, Doces e Sobremesas<br />
                </h1>
                <p className="hero__subtitle">
                    Encomende seu bolo personalizado para qualquer ocasião
                </p>
                <Link to="/cardapio" className="hero__cta">
                    Ver Cardápio
                </Link>
            </div>
        </section>
    )
}