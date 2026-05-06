export default function ChatbotMascot({ isThinking = false, size = 48 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 200 200"
      xmlns="http://www.w3.org/2000/svg"
      aria-label="DoceBOT"
    >
      <defs>
        <linearGradient id="cm-visor" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%"   stop-color="#fff3e0"/>
          <stop offset="100%" stop-color="#ffb74d"/>
        </linearGradient>
        <linearGradient id="cm-body" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%"   stop-color="#f8e1e7"/>
          <stop offset="100%" stop-color="#e7c6cf"/>
        </linearGradient>
        <linearGradient id="cm-icing" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%"   stop-color="#f4acb7"/>
          <stop offset="100%" stop-color="#e5989b"/>
        </linearGradient>
        <linearGradient id="cm-handle" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%"   stop-color="#a0785a"/>
          <stop offset="100%" stop-color="#c9956a"/>
        </linearGradient>
        <filter id="cm-shadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="4" stdDeviation="3"
                        flood-color="#000" flood-opacity="0.15"/>
        </filter>

        <style>{`
          @keyframes cm-thinking {
            0%   { transform: translateX(0px);  }
            20%  { transform: translateX(-3px); }
            50%  { transform: translateX(0px);  }
            80%  { transform: translateX(3px);  }
            100% { transform: translateX(0px);  }
          }
          @keyframes cm-blink {
            0%, 90%, 100% { transform: scaleY(1);   }
            95%            { transform: scaleY(0.1); }
          }
          .cm-pupils-thinking {
            animation: cm-thinking 1.1s ease-in-out infinite;
          }
          .cm-pupils-idle {
            animation: cm-blink 4s ease-in-out infinite;
          }
        `}</style>
      </defs>

      {/* fundo */}
      <circle cx="100" cy="100" r="95" fill="#fff5f7"/>

      {/* chapéu */}
      <g filter="url(#cm-shadow)">
        <ellipse cx="100" cy="50" rx="34" ry="16" fill="#ffffff"/>
        <rect x="70" y="50" width="60" height="18" rx="8" fill="#ffffff"/>
        <rect x="79" y="51" width="42" height="14" rx="5" fill="#f4acb7"/>
        <text
          x="100" y="59"
          textAnchor="middle"
          dominantBaseline="middle"
          fontFamily="Arial, Helvetica, sans-serif"
          fontSize="7"
          fontWeight="bold"
          fill="#ffffff"
          letterSpacing="0.3"
        >DoceBOT</text>
      </g>

      {/* cabeça */}
      <g filter="url(#cm-shadow)">
        <rect x="55" y="65" width="90" height="60" rx="20" fill="url(#cm-visor)"/>
      </g>

      {/* olhos — esclerótica */}
      <circle cx="80"  cy="95" r="7" fill="#ffffff"/>
      <circle cx="120" cy="95" r="7" fill="#ffffff"/>

      {/* pupilas animadas */}
      <g
        className={isThinking ? 'cm-pupils-thinking' : 'cm-pupils-idle'}
        style={{ transformOrigin: '100px 95px' }}
      >
        <circle cx="81"  cy="95" r="3" fill="#5d4037"/>
        <circle cx="121" cy="95" r="3" fill="#5d4037"/>
        {/* brilho */}
        <circle cx="83"  cy="93" r="1" fill="#ffffff"/>
        <circle cx="123" cy="93" r="1" fill="#ffffff"/>
      </g>

      {/* sorriso */}
      <path
        d="M82 110 Q100 122 118 110"
        stroke="#5d4037" strokeWidth="2.5"
        fill="none" strokeLinecap="round"
      />

      {/* corpo */}
      <g filter="url(#cm-shadow)">
        <rect x="60" y="125" width="80" height="50" rx="18" fill="url(#cm-body)"/>
      </g>

      {/* cobertura */}
      <path
        d="M60 135 Q70 122 80 135 Q90 122 100 135 Q110 122 120 135 Q130 122 140 135 L140 150 L60 150 Z"
        fill="url(#cm-icing)"
      />

      {/* granulado */}
      <circle cx="82"  cy="148" r="2"   fill="#d98c9a"/>
      <circle cx="93"  cy="156" r="1.5" fill="#cdb4db"/>
      <circle cx="100" cy="148" r="2"   fill="#cdb4db"/>
      <circle cx="110" cy="155" r="1.5" fill="#f4acb7"/>
      <circle cx="119" cy="148" r="2"   fill="#d98c9a"/>

      {/* braço esquerdo */}
      <line x1="62" y1="140" x2="40" y2="158"
            stroke="#cdb4db" strokeWidth="9" strokeLinecap="round"/>

      {/* braço direito */}
      <line x1="138" y1="140" x2="158" y2="156"
            stroke="#cdb4db" strokeWidth="9" strokeLinecap="round"/>

      {/* fouet */}
      <g transform="translate(160,150) rotate(25)">
        <rect x="-3" y="4" width="6" height="22" rx="3" fill="url(#cm-handle)"/>
        <rect x="-4" y="2" width="8" height="5" rx="2" fill="#a0a0a0"/>
        <path d="M 0 2 C -13 -4 -12 -16 0 -20"
              fill="none" stroke="#c8c8c8" strokeWidth="1.3" strokeLinecap="round"/>
        <path d="M 0 2 C  13 -4  12 -16 0 -20"
              fill="none" stroke="#c8c8c8" strokeWidth="1.3" strokeLinecap="round"/>
        <path d="M 0 2 C -9 -3  -9 -15 0 -20"
              fill="none" stroke="#d0d0d0" strokeWidth="1.3" strokeLinecap="round"/>
        <path d="M 0 2 C  9 -3   9 -15 0 -20"
              fill="none" stroke="#d0d0d0" strokeWidth="1.3" strokeLinecap="round"/>
        <path d="M 0 2 C -4 -2  -4 -14 0 -20"
              fill="none" stroke="#d8d8d8" strokeWidth="1.3" strokeLinecap="round"/>
        <path d="M 0 2 C  4 -2   4 -14 0 -20"
              fill="none" stroke="#d8d8d8" strokeWidth="1.3" strokeLinecap="round"/>
        <circle cx="0" cy="-20" r="1.8" fill="#a0a0a0"/>
      </g>
    </svg>
  )
}
