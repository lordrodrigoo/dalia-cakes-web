import { Link, NavLink } from "react-router-dom"
import { useState } from "react"
import { headerStyles as s } from "../styles/header.styles"
import WhatsAppButton from "./home/WhatsAppButton"
import IfoodButton from "./home/IfoodButton"   
import InstagramButton from "./home/InstagramButton"
import FacebookButton from "./home/FacebookButton"


const links = [
  { to: "/", label: "Início" },
  { to: "/cardapio", label: "Cardápio" },
  { to: "/bolos-decorados", label: "Bolos Decorados" },
  { to: "/sobre", label: "Sobre" },
  { to: "/contato", label: "Contato" },
]

export default function Header() {
  const [open, setOpen] = useState(false)

  const whatsappNumber = import.meta.env.VITE_WHATSAPP_NUMBER
  const whatsappLink = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent('Olá! Vim pelo site e gostaria de fazer um pedido 🎂')}`

  return (
    <header className={s.header}>

      <div className={s.inner}>
        <div className={s.navWrapper}>
          <nav className={s.nav}>
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                end={link.to === "/"}
                className={({ isActive }) => isActive ? s.linkActive : s.link}
              >
                {link.label}
              </NavLink>
            ))}
          </nav>
        </div>
        {/* Botão Hamburger Mobile */}
        <button
          className={s.hamburger}
          onClick={() => setOpen((prev) => !prev)}
          aria-label={open ? "Fechar menu" : "Abrir menu"}
          aria-expanded={open}
        >
          <span className={s.hamburgerBar} />
          <span className={s.hamburgerBar} />
          <span className={s.hamburgerBar} />
        </button>
        {/* Navegação Mobile */}
        <nav
          className={
            `${s.navOpen.replace('pointer-events-none', open ? 'pointer-events-auto' : 'pointer-events-none')} ${open ? s.navOpenActive : ''}`
          }
          style={{ display: open ? 'flex' : 'none' }}
        >
          {links.map((link) => (
            <div key={link.to}>
              <NavLink
                to={link.to}
                end={link.to === "/"}
                className={({ isActive }) => isActive ? s.linkActive : s.link}
                onClick={() => setOpen(false)}
              >
                {link.label}
              </NavLink>
            </div>
          ))}
          <div className={s.btnGroupMobile}>
            <WhatsAppButton/>
            <IfoodButton/>
            <InstagramButton/>
            <FacebookButton/>
          </div>
        </nav>
      </div>
    </header>
  )
}