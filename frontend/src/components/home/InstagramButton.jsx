import instagramIcon from '../../assets/icons/instagram.png'
import { instagramButtonStyles as s } from '../../styles/socialButtons.styles'

const INSTAGRAM_URL = import.meta.env.VITE_INSTAGRAM_URL

export default function InstagramButton({ className = '', ...props }) {
  return (
    <a
      href={INSTAGRAM_URL}
      target="_blank"
      rel="noopener noreferrer"
      className={`${s.btn} ${className}`}
      {...props}
    >
      <img src={instagramIcon} alt="Instagram" className={s.icon} />
    </a>
  )
}
