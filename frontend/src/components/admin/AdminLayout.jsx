import { useState } from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { adminLayoutStyles as s } from '../../styles/adminLayout.styles'
import { logout } from '../../services/auth'
import logo from '../../assets/images/logo_home.png'
import toast from 'react-hot-toast'


const handleLogout = () => {
  logout()
  toast.success('Até logo!')
  navigate('/login')
}

const navItems = [
  { to: "/admin", label: "Dashboard", icon: "📊", end: true },
  { to: "/admin/categorias", label: "Categorias", icon: "🗂️" },
  { to: "/admin/produtos", label: "Produtos", icon: "🎂" },
  { to: "/admin/bolos-decorados", label: "Bolos Decorados", icon: "✨" },
  { to: "/admin/instagram", label: "Instagram", icon: "📸" },
]

export default function AdminLayout() {
  const [open, setOpen] = useState(false)
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className={s.wrapper}>

      {/* Overlay mobile */}
      {open && <div className={s.overlay} onClick={() => setOpen(false)} />}

      {/* Sidebar */}
      <aside className={`${s.sidebar} ${s.sidebarDesktop} ${open ? s.sidebarOpen : s.sidebarClosed}`}>
        
        <div className={s.sidebarHeader}>
          <img src={logo} alt="Dalia Bolos e Doces" className={s.sidebarLogo} />
          <button className={s.sidebarClose} onClick={() => setOpen(false)} aria-label="Fechar menu">
            ✕
          </button>
        </div>

        <nav className={s.nav}>
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) => isActive ? s.navLinkActive : s.navLink}
              onClick={() => setOpen(false)}
            >
              <span className={s.navIcon}>{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className={s.sidebarFooter}>
          <a href="/" className={s.siteLink}>
            <span className={s.navIcon}>🌐</span>
            Ver site
          </a>
          <button className={s.logoutBtn} onClick={handleLogout}>
            <span className={s.navIcon}>🚪</span>
            Sair
          </button>
        </div>

      </aside>

      {/* Main */}
      <div className={s.main}>

        <div className={s.topbar}>
          <button className={s.hamburger} onClick={() => setOpen(true)} aria-label="Abrir menu">☰</button>
          <span className={s.topbarTitle}>Painel Admin</span>
          <a href="/" className={s.topbarSiteLink}>Ver site</a>
        </div>

        <div className={s.content}>
          <Outlet />
        </div>

      </div>

    </div>
  )
}
