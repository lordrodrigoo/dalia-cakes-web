import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'

// Páginas públicas
import Home from './pages/Home'
import Cardapio from './pages/Cardapio'
import BolosDecorados from './pages/BolosDecorados'
import Produtos from './pages/Produtos'
import Sobre from './pages/Sobre'
import Contato from './pages/Contato'
import LoginPage from './pages/LoginPage'

// Admin
import AdminLayout from './components/admin/AdminLayout'
import AdminDashboard from './pages/admin/dashboard'
import AdminCategorias from './pages/admin/Categorias'
import AdminProdutos from './pages/admin/Produtos'
import AdminBolosDecorados from './pages/admin/BolosDecorados'
import AdminInstagram from './pages/admin/Instagram'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Rotas públicas COM layout */}
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/cardapio" element={<Cardapio />} />
          <Route path="/cardapio/:categoriaSlug" element={<Produtos />} />
          <Route path="/bolos-decorados" element={<BolosDecorados />} />
          <Route path="/sobre" element={<Sobre />} />
          <Route path="/contato" element={<Contato />} />
        </Route>

        {/* Login SEM layout */}
        <Route path="/login" element={<LoginPage />} />

        {/* Rotas admin protegidas */}
        <Route path="/admin" element={
          <ProtectedRoute>
            <AdminLayout />
          </ProtectedRoute>
        }>
          <Route index element={<AdminDashboard />} />
          <Route path="categorias" element={<AdminCategorias />} />
          <Route path="produtos" element={<AdminProdutos />} />
          <Route path="bolos-decorados" element={<AdminBolosDecorados />} />
          <Route path="instagram" element={<AdminInstagram />} />
        </Route>

      </Routes>
    </BrowserRouter>
  )
}
