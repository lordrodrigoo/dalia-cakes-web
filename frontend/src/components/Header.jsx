import { Link, NavLink } from "react-router-dom"
import { useState } from "react"
import { headerStyles as s } from "../styles/header.styles"

const links = [
  { to: "/", label: "Início" },
  { to: "/cardapio", label: "Cardápio" },
  { to: "/bolos-decorados", label: "Bolos Decorados" },
  { to: "/sobre", label: "Sobre" },
  { to: "/contato", label: "Contato" },
]

export default function Header() {
  const [open, setOpen] = useState(false)

  return (
    <header className={s.header}>
      <div className={s.inner}>
        <Link to="/" className={s.logo}>
          Dalia Bolos e Doces
        </Link>

        <nav className={open ? s.navOpen : s.nav}>
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.to === "/"}
              className={({ isActive }) => isActive ? s.linkActive : s.link}
              onClick={() => setOpen(false)}
            >
              {link.label}
            </NavLink>
          ))}
        </nav>

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
      </div>
    </header>
  )
}