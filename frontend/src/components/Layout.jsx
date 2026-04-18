import { Outlet } from 'react-router-dom'
import Header from './Header'
import { layoutStyles as s } from '../styles/layout.styles'

export default function Layout() {
  return (
    <div className={s.layout}>
      <Header />
      <main className={s.main}>
        <Outlet />
      </main>
    </div>
  )
}
