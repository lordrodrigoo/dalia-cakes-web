export const bolosDecoradosStyles = {
  wrapper: "flex flex-col gap-8 px-4 py-10 max-w-6xl mx-auto",

  // Header
  heading: "text-3xl font-bold text-gray-900 text-center",
  subheading: "text-gray-500 text-base text-center",

  // Tabs de subcategorias
  tabs: "flex gap-2 flex-wrap justify-center",
  tab: "px-4 py-2 rounded-full text-sm font-medium border border-gray-300 text-gray-600 hover:border-gray-900 hover:text-gray-900 transition-colors cursor-pointer",
  tabActive: "px-4 py-2 rounded-full text-sm font-medium border border-gray-900 bg-gray-900 text-white cursor-pointer",

  // Grid de fotos
  grid: "grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3",
  imgWrapper: "overflow-hidden rounded-xl aspect-square cursor-pointer group",
  img: "w-full h-full object-cover group-hover:scale-105 transition-transform duration-300",
  imgFallback: "w-full h-full items-center justify-center bg-gray-100 text-4xl",

  // Empty / loading
  empty: "text-center py-20 text-gray-400",

  // Modal
  modalOverlay: "fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4",
  modal: "relative max-w-2xl w-full",
  modalImg: "w-full rounded-xl object-contain max-h-[80vh]",
  modalClose: "absolute top-3 right-3 bg-black/50 hover:bg-black/70 text-white rounded-full w-8 h-8 flex items-center justify-center text-lg transition-colors cursor-pointer z-10",
  modalNav: "absolute inset-y-0 flex items-center justify-between w-full px-2 pointer-events-none",
  modalPrev: "pointer-events-auto bg-white/20 hover:bg-white/40 text-white rounded-full w-10 h-10 flex items-center justify-center text-xl transition-colors",
  modalNext: "pointer-events-auto bg-white/20 hover:bg-white/40 text-white rounded-full w-10 h-10 flex items-center justify-center text-xl transition-colors",

  // WhatsApp
  modalFooter: "flex justify-center mt-4",
  whatsappBtn: "flex items-center gap-2 bg-green-500 hover:bg-green-600 text-white font-semibold px-6 py-2.5 rounded-full transition-colors no-underline text-sm",
  whatsappIcon: "w-5 h-5 object-contain",
}
