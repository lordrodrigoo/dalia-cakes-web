const WHATSAPP_NUMBER = import.meta.env.VITE_BUSINESS_PHONE.replace(/\D/g, '')

export function buildWhatsAppLink(message) {
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`
}

export function buildProductOrderLink(productName) {
  return buildWhatsAppLink(`Ola! Vi esse ${productName} no site e gostaria de encomendar!`)
}
