import instagramIcon from '../../assets/icons/instagram.png'
import { instagramButtonStyles as s } from '../../styles/socialButtons.styles'

export default function InstagramButton({ className = '', ...props }) {
  return (
    <a
      href="https://instagram.com/seuPerfil"
      target="_blank"
      rel="noopener noreferrer"
      className={`${s.btn} ${className}`}
      {...props}
    >
      <img src={instagramIcon} alt="Instagram" className={s.icon} />
    </a>
  )
}
