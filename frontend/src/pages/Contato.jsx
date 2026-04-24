import { contatoStyles as s } from '../styles/contato.styles'


const WHATSAPP_NUMBER = import.meta.env.VITE_WHATSAPP_NUMBER
const WHATSAPP_LINK = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent('Olá! Gostaria de fazer um pedido 🎂')}`
const IFOOD_URL = import.meta.env.VITE_IFOOD_URL
const ADDRESS = import.meta.env.VITE_ADDRESS
const MAPS_LINK = import.meta.env.VITE_MAPS_LINK
const MAPS_EMBED = import.meta.env.VITE_MAPS_EMBED

const hours = [
  { days: "Segunda a Sexta", time: "10h30 às 22h" },
  { days: "Sábado", time: "10h às 22h" },
  { days: "Domingo", time: "10h às 21h" },
  { days: "Feriados", time: "10h30 às 20h" },
]

export default function Contato() {
  return (
    <div className={s.wrapper}>
      <div>
        <h1 className={s.heading}>Fale Conosco</h1>
        <p className={s.subheading}>Estamos sempre prontos para atender você!</p>
      </div>

      <div className={s.grid}>

        {/* Informações */}
        <div className={s.infoSection}>

          <div className={s.infoCard}>
            <span className={s.infoLabel}>Endereço</span>
            <a
              href={MAPS_LINK}
              target="_blank"
              rel="noopener noreferrer"
              className={s.infoLink}
            >
              📍 {ADDRESS}
            </a>
          </div>

          <div className={s.infoCard}>
            <span className={s.infoLabel}>WhatsApp</span>
            <span className={s.infoValue}>📱 (11) 99546-9412</span>
          </div>

          <div className={s.infoCard}>
            <span className={s.infoLabel}>Horários de Atendimento</span>
            <div className={s.hoursGrid}>
              {hours.map(item => (
                <div key={item.days} className={s.hoursRow}>
                  <span className={s.hoursDays}>{item.days}</span>
                  <span className={s.hoursTime}>{item.time}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Botões removidos conforme solicitado */}

        </div>

        {/* Mapa */}
        <div className={s.mapWrapper}>
          <iframe
            src={MAPS_EMBED}
            className={s.map}
            allowFullScreen
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
            title="Localização Dalia Bolos e Doces"
          />
        </div>

      </div>
    </div>
  )
}
