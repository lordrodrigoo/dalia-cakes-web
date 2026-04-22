import { whatsAppCTAStyles as s } from '../../styles/whatsAppCTA.styles'

const WHATSAPP_NUMBER = import.meta.env.VITE_BUSINESS_PHONE.replace(/\D/g, '')
const WHATSAPP_LINK = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent('Olá! Gostaria de fazer um pedido 🎂')}`

export default function WhatsAppCTA() {
  return (
    <section className={s.section}>
      <div className={s.inner}>
        <h2 className={s.heading}>Faça sua encomenda pelo WhatsApp!</h2>
        <p className={s.subheading}>
          Atendemos de segunda a sábado das 10h às 22h e domingo das 10h às 21h.
          Entre em contato e faça seu pedido com pelo menos 3 dias de antecedência.
        </p>
        <a href={WHATSAPP_LINK} target="_blank" rel="noopener noreferrer" className={s.btn}>
          💬 Falar no WhatsApp
        </a>
      </div>
    </section>
  )
}
