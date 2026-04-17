import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'

import Home from './pages/Home'
import Cardapio from './pages/Cardapio'
import BolosDecorados from './pages/BolosDecorados'
import Produtos from './pages/Produtos'
import Sobre from './pages/Sobre'
import Contato from './pages/Contato'
import LoginPage from './pages/LoginPage'
import ProtectedRoute from './components/ProtectedRoute'


export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/cardapio" element={<Cardapio />} />
          <Route path="/cardapio/:categoriaSlug" element={<Produtos />} />
          <Route path="/bolos-decorados" element={
            <ProtectedRoute>
              <BolosDecorados />
            </ProtectedRoute>
          } />
          <Route path="/produtos" element={
            <ProtectedRoute>
              <Produtos />
            </ProtectedRoute>
          } />
          <Route path="/sobre" element={<Sobre />} />
          <Route path="/contato" element={<Contato />} />
          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
