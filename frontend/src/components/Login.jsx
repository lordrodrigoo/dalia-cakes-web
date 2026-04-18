import { useState } from 'react'
import { login, saveToken } from '../services/auth'
import { loginPageStyles as s } from '../styles/loginPage.styles'
import logo from '../assets/images/logo_home.png'

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [remember, setRemember] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const data = await login(username, password)
      saveToken(data.access_token)
      if (onLogin) onLogin()
    } catch {
      setError('Usuário ou senha inválidos.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={s.layout}>
      <form onSubmit={handleSubmit} className={s.form}>

        <div className={s.logoWrapper}>
          <img src={logo} alt="Dalia Bolos e Doces" className={s.logo} />
        </div>

        <h1 className={s.heading}>Login</h1>

        <div className={s.fieldWrapper}>
          <label className={s.label}>Usuário</label>
          <input
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            className={s.input}
            required
          />
        </div>

        <div className={s.fieldWrapper}>
          <label className={s.label}>Senha</label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            className={s.input}
            required
          />
        </div>

        <div className={s.row}>
          <div className={s.checkboxWrapper}>
            <input
              type="checkbox"
              id="remember"
              checked={remember}
              onChange={e => setRemember(e.target.checked)}
              className={s.checkbox}
            />
            <label htmlFor="remember" className={s.checkboxLabel}>Lembrar de mim</label>
          </div>
          <a href="#" className={s.forgotLink}>Esqueceu a senha?</a>
        </div>

        {error && <p className={s.error}>{error}</p>}

        <button type="submit" className={s.button} disabled={loading}>
          {loading ? 'Entrando...' : 'Entrar'}
        </button>


      </form>
      <p className={s.bottomText}>
        <a href="/" className={s.signupLink}>← Voltar para o site</a>
      </p>
    </div>
  )
}