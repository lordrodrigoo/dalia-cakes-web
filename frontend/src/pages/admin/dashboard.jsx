import { useNavigate } from 'react-router-dom'
import { adminDashboardStyles as s } from '../../styles/adminDashboard.styles'

const shortcuts = [
  { to: "/admin/categorias", icon: "🗂️", title: "Categorias", desc: "Gerenciar categorias de produtos" },
  { to: "/admin/produtos", icon: "🎂", title: "Produtos", desc: "Gerenciar produtos do cardápio" },
  { to: "/admin/bolos-decorados", icon: "✨", title: "Bolos Decorados", desc: "Gerenciar bolos decorados" },
  { to: "/admin/instagram", icon: "📸", title: "Instagram", desc: "Gerenciar posts do Instagram" },
]

export default function AdminDashboard() {
  const navigate = useNavigate()

  return (
    <div className={s.wrapper}>
      <div>
        <h1 className={s.heading}>Bem-vindo ao painel administrativo 👋</h1>
        <p className={s.subheading}>O que você deseja gerenciar hoje?</p>
      </div>

      <div className={s.grid}>
        {shortcuts.map((item) => (
          <div key={item.to} className={s.card} onClick={() => navigate(item.to)}>
            <span className={s.cardIcon}>{item.icon}</span>
            <span className={s.cardTitle}>{item.title}</span>
            <span className={s.cardDesc}>{item.desc}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
