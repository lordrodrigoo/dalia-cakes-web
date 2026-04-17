import Header from "./Header"
import { layoutStyles as s } from "../styles/layout.styles"

export default function Layout({ children }) {
  return (
    <div className={s.layout}>
      <Header />
      <main className={s.main}>{children}</main>
    </div>
  )
}
