import { useState, useEffect, useRef } from 'react'
import { sendMessage } from '../services/chatbot'
import ChatbotMascot from './ChatbotMascot'
import { chatbotStyles as s } from '../styles/chatbotWidget.styles'

const SESSION_KEY = 'docebot_session_id'

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

export default function ChatbotWidget() {
  const [open, setOpen]           = useState(false)
  const [messages, setMessages]   = useState([
    { from: 'bot', text: 'Olá! Sou o DoceBOT 🎂 Como posso te ajudar hoje?' }
  ])
  const [input, setInput]         = useState('')
  const [isThinking, setIsThinking] = useState(false)
  const [hasUnread, setHasUnread] = useState(false)
  const messagesEndRef            = useRef(null)
  const inputRef                  = useRef(null)

  // Scroll automático para última mensagem
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isThinking])

  // Foca no input quando abre
  useEffect(() => {
    if (open) {
      setHasUnread(false)
      setTimeout(() => inputRef.current?.focus(), 100)
    }
  }, [open])

  const getSessionId = () => {
    let id = sessionStorage.getItem(SESSION_KEY)
    if (!id) {
      id = crypto.randomUUID()
      sessionStorage.setItem(SESSION_KEY, id)
    }
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
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <>
      {/* Janela de chat */}
      {open && (
        <div className={`${s.window} ${s.windowEnter}`}>

          {/* Header */}
          <div className={s.header}>
            <div className={s.headerMascot}>
              <ChatbotMascot size={52} isThinking={isThinking} />
            </div>
            <div className={s.headerInfo}>
              <p className={s.headerName}>DoceBOT</p>
              <p className={s.headerStatus}>
                {isThinking ? 'Pensando...' : 'Online ✦'}
              </p>
            </div>
            <button
              className={s.headerClose}
              onClick={() => setOpen(false)}
              aria-label="Fechar chat"
            >✕</button>
          </div>

          {/* Mensagens */}
          <div className={s.messages}>
            {messages.map((msg, i) =>
              msg.from === 'bot' ? (
                <div key={i} className={s.bubbleBot}>
                  <div className={s.bubbleBotAvatar}>
                    <ChatbotMascot size={38} isThinking={false} />
                  </div>
                  <p className={s.bubbleBotText}>{msg.text}</p>
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

          {/* Input */}
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

      {/* Botão flutuante */}
      <button
        className={s.fab}
        onClick={() => setOpen(prev => !prev)}
        aria-label={open ? 'Fechar chat' : 'Abrir chat com DoceBOT'}
      >
        <ChatbotMascot size={68} isThinking={false} />
        {hasUnread && !open && <span className={s.fabUnread} />}
      </button>
    </>
  )
}
