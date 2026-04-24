import ifoodIcon from '../../assets/icons/Logo_pede_ifood.png'
import { ifoodButtonStyles as s } from '../../styles/socialButtons.styles'

export default function IfoodButton({
  url = import.meta.env.VITE_IFOOD_URL,
  className = '',
  ...props
}) {
  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className={`${s.btn} ${className}`}
      {...props}
    >
      <img src={ifoodIcon} alt="iFood" className={s.icon} />
    </a>
  )
}
