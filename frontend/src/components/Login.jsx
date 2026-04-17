import { useState } from 'react'
import { login, saveToken } from '../services/auth'
import { loginStyles as s } from '../styles/login.styles'

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
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
    <form onSubmit={handleSubmit} className={s.form}>
      <h2 className={s.title}>Login</h2>

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

      {error && <p className={s.error}>{error}</p>}

      <button type="submit" className={s.button} disabled={loading}>
        {loading ? 'Entrando...' : 'Entrar'}
      </button>
    </form>
  )
}