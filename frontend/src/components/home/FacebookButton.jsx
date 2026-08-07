import facebookIcon from '../../assets/icons/facebook.png'
import { facebookButtonStyles as s } from '../../styles/socialButtons.styles'

const FACEBOOK_URL = import.meta.env.VITE_FACEBOOK_URL

export default function FacebookButton({ className = '', ...props }) {
  return (
    <a
      href={FACEBOOK_URL}
      target="_blank"
      rel="noopener noreferrer"
      className={`${s.btn} ${className}`}
      {...props}
    >
      <img src={facebookIcon} alt="Facebook" className={s.icon} />
    </a>
  )
}
