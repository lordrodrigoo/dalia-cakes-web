import { footerStyles as s } from '../styles/footer.styles'
import dividerHeart from '../assets/icons/devider_heart.png'
import whatsappIcon from '../assets/icons/whatsapp.png'
import instagramIcon from '../assets/icons/instagram.png'
import facebookIcon from '../assets/icons/facebook.png'
import ifoodIcon from '../assets/icons/Ifood_logo_sem_fundo.png'

const WHATSAPP_NUMBER = import.meta.env.VITE_WHATSAPP_NUMBER
const WHATSAPP_LINK = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent('Ola! Gostaria de fazer um pedido!')}`
const IFOOD_URL = import.meta.env.VITE_IFOOD_URL
const INSTAGRAM_URL = import.meta.env.VITE_INSTAGRAM_URL
const FACEBOOK_URL = import.meta.env.VITE_FACEBOOK_URL

export default function Footer() {
  return (
    <footer className={s.footer}>

      <img src={dividerHeart} alt="" className={s.divider} />

      <div className={s.body}>
        <span className={s.brandName}>Dalia Bolos e Doces</span>
        <p className={s.brandTagline}>Confeitaria artesanal desde 2015 — feita com amor em cada detalhe.</p>

        <div className={s.socialRow}>
          <a href={WHATSAPP_LINK} target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">
            <img src={whatsappIcon} alt="WhatsApp" className={s.socialIconWhatsapp} style={{ filter: 'brightness(0) saturate(100%) invert(58%) sepia(93%) saturate(401%) hue-rotate(103deg) brightness(97%) contrast(91%)' }} />
          </a>
          {IFOOD_URL && (
            <a href={IFOOD_URL} target="_blank" rel="noopener noreferrer" aria-label="iFood">
              <img src={ifoodIcon} alt="iFood" className={s.socialIconIfood} style={{ filter: 'brightness(0) saturate(100%) invert(11%) sepia(90%) saturate(6000%) hue-rotate(355deg) brightness(100%) contrast(100%)' }} />
            </a>
          )}
          <a href={INSTAGRAM_URL} target="_blank" rel="noopener noreferrer" aria-label="Instagram">
            <img src={instagramIcon} alt="Instagram" className={s.socialIcon} />
          </a>
          <a href={FACEBOOK_URL} target="_blank" rel="noopener noreferrer" aria-label="Facebook">
            <img src={facebookIcon} alt="Facebook" className={s.socialIcon} />
          </a>
        </div>
      </div>

      <div className={s.bottomBar}>
        <span className={s.copyright}>© {new Date().getFullYear()} Dalia Bolos e Doces. Todos os direitos reservados.</span>
      </div>

    </footer>
  )
}
