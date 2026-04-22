import { sobreStyles as s } from '../styles/sobre.styles'
import caricatura from '../assets/images/caricatura_dalia.jpeg'

const diferenciais = [
  {
    icon: "🎂",
    title: "100% Artesanal",
    text: "Tudo feito à mão, com receitas próprias e muito carinho em cada detalhe.",
  },
  {
    icon: "🌿",
    title: "Sem Conservantes",
    text: "Ingredientes frescos e naturais, sem aditivos artificiais ou conservantes.",
  },
  {
    icon: "💝",
    title: "Feito com Amor",
    text: "Cada produto é preparado com dedicação para tornar seu momento especial.",
  },
]

const hours = [
  { days: "Segunda a Sexta", time: "10h30 às 22h" },
  { days: "Sábado", time: "10h às 22h" },
  { days: "Domingo e Feriados", time: "10h às 20h" },
]

export default function Sobre() {
  return (
    <div className={s.wrapper}>

      {/* Hero */}
      <div className={s.hero}>
        <img src={caricatura} alt="Dália Moreira" className={s.heroImg} />
        <div className={s.heroContent}>
          <p className={s.heroSubtitle}>Nossa história</p>
          <h1 className={s.heroTitle}>Dalia Bolos e Doces</h1>
          <p className={s.heroText}>
            Tudo começou com muito esforço, amor e uma bandeja de bolos nas mãos. 
            Dália Moreira iniciou sua jornada fazendo encomendas e vendendo de porta em porta, 
            acreditando que cada fatia poderia adoçar o dia de alguém.
          </p>
          <p className={s.heroText}>
            Com o tempo, o que era paixão virou negócio — e o negócio virou referência. 
            Desde 2015, a confeitaria cresce com o mesmo cuidado artesanal do primeiro dia: 
            tudo feito à mão, sem conservantes, com ingredientes frescos e receitas que carregam 
            a assinatura da Dália em cada detalhe.
          </p>
        </div>
      </div>

      {/* Missão */}
      <div className={s.missionSection}>
        <h2 className={s.missionTitle}>Nossa Missão</h2>
        <p className={s.missionText}>
          Transformar momentos especiais em memórias doces e inesquecíveis. 
          Cada bolo, cada doce, cada sobremesa é criado com a intenção de celebrar 
          — seja um aniversário, um casamento ou simplesmente um dia que merece algo gostoso.
        </p>
      </div>

      {/* Diferenciais */}
      <div className={s.differentialsSection}>
        <h2 className={s.differentialsTitle}>Por que escolher a Dalia?</h2>
        <div className={s.differentialsGrid}>
          {diferenciais.map((item) => (
            <div key={item.title} className={s.differentialCard}>
              <span className={s.differentialIcon}>{item.icon}</span>
              <span className={s.differentialTitle}>{item.title}</span>
              <p className={s.differentialText}>{item.text}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Horários */}
      <div className={s.hoursSection}>
        <h2 className={s.hoursTitle}>Horários de Atendimento</h2>
        <div className={s.hoursGrid}>
          {hours.map((item) => (
            <div key={item.days} className={s.hoursCard}>
              <span className={s.hoursDays}>{item.days}</span>
              <span className={s.hoursTime}>{item.time}</span>
            </div>
          ))}
        </div>
      </div>

    </div>
  )
}
