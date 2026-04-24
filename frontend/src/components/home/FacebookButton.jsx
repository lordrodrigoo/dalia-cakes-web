import facebookIcon from '../../assets/icons/facebook.png'
import { facebookButtonStyles as s } from '../../styles/socialButtons.styles'

export default function FacebookButton({ className = '', ...props }) {
  return (
    <a
      href="https://facebook.com/seuPerfil"
      target="_blank"
      rel="noopener noreferrer"
      className={`${s.btn} ${className}`}
      {...props}
    >
      <img src={facebookIcon} alt="Facebook" className={s.icon} />
    </a>
  )
}
