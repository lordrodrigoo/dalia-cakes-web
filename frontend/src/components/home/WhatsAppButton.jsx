
import whatsappIcon from '../../assets/icons/whatsapp.png'
import { whatsAppButtonStyles as s } from '../../styles/socialButtons.styles'

export default function WhatsAppButton({
  text = '',
  number = import.meta.env.VITE_WHATSAPP_NUMBER,
  className = '',
  ...props
}) {
  const link = `https://wa.me/${number}?text=${encodeURIComponent('Olá! Gostaria de fazer um pedido 🎂')}`
  return (
    <a
      href={link}
      target="_blank"
      rel="noopener noreferrer"
      className={`${s.btn} ${className}`}
      {...props}
    >
      <img src={whatsappIcon} alt="WhatsApp" className={s.icon} />
    </a>
  )
}
