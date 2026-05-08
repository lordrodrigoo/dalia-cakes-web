import { useState, useEffect, useRef } from 'react'
import { sendMessage } from '../services/chatbot'
import ChatbotMascot from './ChatbotMascot'
import { chatbotStyles as s } from '../styles/chatbotWidget.styles'

const SESSION_KEY  = 'docebot_session_id'
const FAB_SIZE     = 96   // w-24 em px
const GAP          = 24   // bottom-6 / right-6 em px
const DRAG_THRESHOLD = 6  // px para distinguir click de drag

function getDefaultPos() {
  return {
    x: window.innerWidth  - FAB_SIZE - GAP,
    y: window.innerHeight - FAB_SIZE - GAP,
  }
}

// ─── Renderizador de markdown simples ──────────────────────────────────────
function renderMarkdown(text) {
  if (!text) return null
  const lines = text.split('\n')

  return lines.map((line, lineIdx) => {
    const tokens = []
    // captura: [texto](url) | URL crua | **texto** | *texto*
    const regex = /(\[([^\]]+)\]\((https?:\/\/[^)]+)\)|https?:\/\/[^\s)]+|\*\*([^*]+)\*\*|\*([^*]+)\*)/g
    let last = 0, match

    while ((match = regex.exec(line)) !== null) {
      if (match.index > last)
        tokens.push({ type: 'text', content: line.slice(last, match.index) })

      if (match[0].startsWith('[')) {
        // link markdown [label](url)
        tokens.push({ type: 'link', label: match[2], url: match[3] })
      } else if (match[0].startsWith('http')) {
        // URL crua
        tokens.push({ type: 'link', label: match[0], url: match[0] })
      } else if (match[0].startsWith('**')) {
        const inner = match[0].slice(2, -2)
        const digits = inner.replace(/\D/g, '')
        if (/^\+?[\d\s\-().]{8,}$/.test(inner.trim()) && digits.length >= 8)
          tokens.push({ type: 'phone', content: inner, digits })
        else
          tokens.push({ type: 'bold', content: inner })
      } else if (match[0].startsWith('*')) {
        tokens.push({ type: 'italic', content: match[0].slice(1, -1) })
      }
      last = match.index + match[0].length
    }

    if (last < line.length)
      tokens.push({ type: 'text', content: line.slice(last) })

    const rendered = tokens.map((t, i) => {
      if (t.type === 'bold')
        return <strong key={i}>{t.content}</strong>
      if (t.type === 'italic')
        return <em key={i}>{t.content}</em>
      if (t.type === 'link')
        return (
          <a key={i} href={t.url} target="_blank" rel="noopener noreferrer"
             className="text-[#ad1457] underline break-all">
            {t.label}
          </a>
        )
      if (t.type === 'phone')
        return (
          <a key={i} href={`https://wa.me/${t.digits}`}
             target="_blank" rel="noopener noreferrer"
             className="font-semibold text-[#ad1457] underline">
            {t.content}
          </a>
        )
      return t.content
    })

    return (
      <span key={lineIdx}>
        {rendered}
        {lineIdx < lines.length - 1 && <br />}
      </span>
    )
  })
}

// ─── Indicador de digitação ────────────────────────────────────────────────
function TypingIndicator() {
  return (
    <div className={s.typing}>
      <div className={s.typingBubble}>
        <span className={`${s.typingDot} animate-bounce [animation-delay:0ms]`}/>
        <span className={`${s.typingDot} animate-bounce [animation-delay:150ms]`}/>
        <span className={`${s.typingDot} animate-bounce [animation-delay:300ms]`}/>
      </div>
    </div>
  )
}

// ─── Widget principal ──────────────────────────────────────────────────────
export default function ChatbotWidget() {
  const [open, setOpen]             = useState(false)
  const [messages, setMessages]     = useState([
    { from: 'bot', text: 'Olá! Sou a assistente virtual da Dalia Bolos 🎂 Como posso te ajudar hoje?' }
  ])
  const [input, setInput]           = useState('')
  const [isThinking, setIsThinking] = useState(false)
  const [hasUnread, setHasUnread]   = useState(false)
  const [pos, setPos]               = useState(null) // null = padrão bottom-right
  const [showGreeting, setShowGreeting] = useState(false)
  const greetingShownRef            = useRef(false)

  const messagesEndRef = useRef(null)
  const inputRef       = useRef(null)

  // Inicializa posição após mount (evita SSR)
  useEffect(() => { setPos(getDefaultPos()) }, [])

  // Exibe bolinha de saudação após 3.5s (uma única vez por sessão)
  useEffect(() => {
    const t = setTimeout(() => {
      if (!greetingShownRef.current) {
        setShowGreeting(true)
        greetingShownRef.current = true
      }
    }, 3500)
    return () => clearTimeout(t)
  }, [])

  // Auto-esconde a saudação após 7s
  useEffect(() => {
    if (!showGreeting) return
    const t = setTimeout(() => setShowGreeting(false), 7000)
    return () => clearTimeout(t)
  }, [showGreeting])

  // Scroll automático
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isThinking])

  // Foca input ao abrir; esconde saudação
  useEffect(() => {
    if (open) {
      setHasUnread(false)
      setShowGreeting(false)
      setTimeout(() => inputRef.current?.focus(), 100)
    }
  }, [open])

  // ── Drag & drop ────────────────────────────────────────────────────────
  const handleMouseDown = (e) => {
    if (e.button !== 0) return
    e.preventDefault()

    const startMX   = e.clientX
    const startMY   = e.clientY
    const startPosX = pos?.x ?? getDefaultPos().x
    const startPosY = pos?.y ?? getDefaultPos().y
    let   dragged   = false

    const onMove = (ev) => {
      const dx = ev.clientX - startMX
      const dy = ev.clientY - startMY
      if (!dragged && (Math.abs(dx) < DRAG_THRESHOLD && Math.abs(dy) < DRAG_THRESHOLD)) return
      dragged = true
      setPos({
        x: Math.max(0, Math.min(window.innerWidth  - FAB_SIZE, startPosX + dx)),
        y: Math.max(0, Math.min(window.innerHeight - FAB_SIZE, startPosY + dy)),
      })
    }

    const onUp = () => {
      document.removeEventListener('mousemove', onMove)
      document.removeEventListener('mouseup',   onUp)
      if (!dragged) setOpen(prev => !prev) // clique simples → abre/fecha
    }

    document.addEventListener('mousemove', onMove)
    document.addEventListener('mouseup',   onUp)
  }

  // ── Envio de mensagem ──────────────────────────────────────────────────
  const getSessionId = () => {
    let id = sessionStorage.getItem(SESSION_KEY)
    if (!id) { id = crypto.randomUUID(); sessionStorage.setItem(SESSION_KEY, id) }
    return id
  }

  const handleSend = async () => {
    const text = input.trim()
    if (!text || isThinking) return
    setInput('')
    setMessages(prev => [...prev, { from: 'user', text }])
    setIsThinking(true)
    try {
      const { data } = await sendMessage(text, getSessionId())
      setMessages(prev => [...prev, { from: 'bot', text: data.reply }])
      if (!open) setHasUnread(true)
    } catch {
      setMessages(prev => [
        ...prev,
        { from: 'bot', text: 'Ops, tive um probleminha aqui 😅 Tente novamente em instantes!' }
      ])
    } finally {
      setIsThinking(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend() }
  }

  // ── Posição da janela de chat — sempre dentro do viewport ────────────
  const chatStyle = pos ? (() => {
    const CHAT_W = 320
    const CHAT_H = 480

    // Horizontal: alinha borda direita da janela com a do FAB, depois clamp
    let left = pos.x + FAB_SIZE - CHAT_W
    left = Math.max(GAP, Math.min(window.innerWidth - CHAT_W - GAP, left))

    // Vertical: tenta abrir acima do FAB; se não couber, abre abaixo
    let top = pos.y - CHAT_H - 8
    if (top < GAP) top = pos.y + FAB_SIZE + 8
    top = Math.max(GAP, Math.min(window.innerHeight - CHAT_H - GAP, top))

    return { position: 'fixed', left, top, zIndex: 50 }
  })() : {}

  // ── Posição do FAB ─────────────────────────────────────────────────────
  const fabStyle = pos ? {
    position: 'fixed',
    left:   pos.x,
    top:    pos.y,
    zIndex: 50,
    cursor: 'grab',
    userSelect: 'none',
  } : {}

  // ── Posição da bolinha de saudação — acima e centralizada no FAB ───────
  const greetingStyle = pos ? {
    position:  'fixed',
    left:      pos.x + FAB_SIZE / 2,
    top:       pos.y - 12,
    transform: 'translate(-50%, -100%)',
    zIndex:    50,
  } : {}

  return (
    <>
      {/* Janela de chat */}
      {open && (
        <div className={`${s.window} ${s.windowEnter}`} style={chatStyle}>

          <div className={s.header}>
            <div className={s.headerMascot}>
              <ChatbotMascot size={52} isThinking={isThinking} />
            </div>
            <div className={s.headerInfo}>
              <p className={s.headerName}>Assistente Virtual</p>
              <p className={s.headerStatus}>{isThinking ? 'Pensando...' : 'Online ✦'}</p>
            </div>
            <button className={s.headerClose} onClick={() => setOpen(false)} aria-label="Fechar">✕</button>
          </div>

          <div className={s.messages}>
            {messages.map((msg, i) =>
              msg.from === 'bot' ? (
                <div key={i} className={s.bubbleBot}>
                  <div className={s.bubbleBotAvatar}>
                    <ChatbotMascot size={38} isThinking={false} />
                  </div>
                  <p className={s.bubbleBotText}>{renderMarkdown(msg.text)}</p>
                </div>
              ) : (
                <div key={i} className={s.bubbleUser}>
                  <p className={s.bubbleUserText}>{msg.text}</p>
                </div>
              )
            )}
            {isThinking && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </div>

          <div className={s.inputArea}>
            <input
              ref={inputRef}
              className={s.input}
              placeholder="Digite sua mensagem..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isThinking}
              maxLength={500}
            />
            <button
              className={s.sendBtn}
              onClick={handleSend}
              disabled={!input.trim() || isThinking}
              aria-label="Enviar"
            >
              <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16">
                <path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/>
              </svg>
            </button>
          </div>

        </div>
      )}

      {/* Bolinha de saudação */}
      {!open && showGreeting && pos && (
        <div style={greetingStyle} className={s.greetingBubble}>
          <button className={s.greetingClose} onClick={() => setShowGreeting(false)} aria-label="Fechar">✕</button>
          <p className={s.greetingText}>Oi! Posso ajudar? 🎂</p>
          <div className={s.greetingTail} />
        </div>
      )}

      {/* Botão flutuante — some quando o chat está aberto */}
      {!open && (
        <button
          className={s.fab}
          style={fabStyle}
          onMouseDown={handleMouseDown}
          aria-label="Abrir chat com a Assistente Virtual"
        >
          <ChatbotMascot size={68} isThinking={false} />
          {hasUnread && <span className={s.fabUnread} />}
        </button>
      )}
    </>
  )
}
