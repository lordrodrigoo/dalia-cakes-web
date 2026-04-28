import ifoodIcon from '../../assets/icons/Ifood_logo_sem_fundo.png'
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
      <img src={ifoodIcon} alt="iFood" className={s.icon} style={{ filter: 'brightness(0) saturate(100%) invert(11%) sepia(90%) saturate(6000%) hue-rotate(355deg) brightness(100%) contrast(100%)' }} />
    </a>
  )
}
