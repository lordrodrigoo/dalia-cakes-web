import { useEffect } from 'react'

const SITE_NAME = 'Confeitaria da Dalia'
const DEFAULT_DESCRIPTION = 'Confeitaria artesanal especializada em bolos decorados, doces finos e muito mais. Encomende pelo WhatsApp ou iFood.'

export function useSEO({ title, description } = {}) {
  const fullTitle = title ? `${title} | ${SITE_NAME}` : SITE_NAME

  useEffect(() => {
    document.title = fullTitle

    const setMeta = (name, content, property = false) => {
      const attr = property ? 'property' : 'name'
      let el = document.querySelector(`meta[${attr}="${name}"]`)
      if (!el) {
        el = document.createElement('meta')
        el.setAttribute(attr, name)
        document.head.appendChild(el)
      }
      el.setAttribute('content', content)
    }

    const desc = description || DEFAULT_DESCRIPTION
    setMeta('description', desc)
    setMeta('og:title', fullTitle, true)
    setMeta('og:description', desc, true)
    setMeta('og:url', window.location.href, true)
  }, [fullTitle, description])
}
