import { useState } from 'react'
import { login, saveToken } from '../services/auth'
import { loginPageStyles as s } from '../styles/loginPage.styles'
import logo from '../assets/images/logo_home.png'
import toast from 'react-hot-toast'

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [remember, setRemember] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const data = await login(username, password)
      saveToken(data.access_token, data.refresh_token)
      toast.success('Logado com sucesso!')
      if (onLogin) onLogin()
    } catch {
      toast.error('Acesso restrito. Verifique suas credenciais.')
      setError('Acesso restrito. Verifique suas credenciais.')
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
            autoCapitalize="none"
            autoCorrect="off"
            autoComplete="username"
            required
          />
        </div>
        <div className={s.fieldWrapper}>
          <label className={s.label}>Senha</label>
          <div className={s.passwordWrapper}>
            <input
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={e => setPassword(e.target.value)}
              className={s.passwordInput}
              required
            />
            <button type="button" onClick={() => setShowPassword(p => !p)} className={s.eyeBtn} aria-label={showPassword ? 'Ocultar senha' : 'Mostrar senha'}>
              {showPassword ? (
                <svg xmlns="http://www.w3.org/2000/svg" className={s.eyeIcon} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-5 0-9-4-9-7s4-7 9-7a9.96 9.96 0 015.657 1.757M15 12a3 3 0 01-3 3m0 0a3 3 0 01-3-3m3 3v.01M3 3l18 18" />
                </svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className={s.eyeIcon} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              )}
            </button>
          </div>
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
