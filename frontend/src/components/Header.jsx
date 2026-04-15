import { Link, NavLink } from "react-router-dom";
import { useState } from "react";
import "../styles/header.css";

const links = [
    { to: "/", label: "Início" },
    { to: "/cardapio", label: "Cardápio" },
    { to: "/sobre", label: "Sobre" },
    { to: "/contato", label: "Contato" },
];

export default function Header() {
    const [open, setOpen] = useState(false);

    return (
        <header className="header">
            <div className="header__inner">
                <Link to="/" className="header__logo">
                    Dalia Bolos e Doces
                </Link>

                <nav className={`header__nav${open ? " header__nav--open" : ""}`}>
                    {links.map((link) => (
                        <NavLink
                            key={link.to}
                            to={link.to}
                            end={link.to === "/"}
                            className={({ isActive }) =>
                                `header__link${isActive ? " header__link--active" : ""}`
                            }
                            onClick={() => setOpen(false)}
                        >
                            {link.label}
                        </NavLink>
                    ))}
                </nav>

                <button
                    className="header__hamburger"
                    onClick={() => setOpen((prev) => !prev)}
                    aria-label={open ? "Fechar menu" : "Abrir menu"}
                    aria-expanded={open}
                >
                    <span className="header__hamburger-bar" />
                    <span className="header__hamburger-bar" />
                    <span className="header__hamburger-bar" />
                </button>
            </div>
        </header>
    );
}
