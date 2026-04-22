export const productCardStyles = {
  // Grid
  grid: "grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4",

  // Card
  card: "bg-white rounded-xl shadow hover:shadow-md transition-shadow cursor-pointer overflow-hidden group",
  cardImgWrapper: "overflow-hidden",
  cardImg: "w-full aspect-square object-cover group-hover:scale-105 transition-transform duration-300",
  cardBody: "p-3 flex flex-col gap-1",
  cardName: "text-sm font-semibold text-gray-800",
  cardPrice: "text-sm text-pink-600 font-bold",

  // Modal
  modalOverlay: "fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4",
  modal: "bg-white rounded-xl shadow-xl w-full max-w-lg max-h-[90vh] overflow-y-auto",
  modalImg: "w-full aspect-square object-cover",
  modalBody: "p-6 flex flex-col gap-4",
  modalName: "text-2xl font-bold text-gray-900",
  modalPrice: "text-xl font-bold text-pink-600",
  modalDesc: "text-sm text-gray-600 leading-relaxed",
  modalActions: "flex flex-col sm:flex-row gap-3 mt-2",
  whatsappBtn: "flex-1 bg-green-500 hover:bg-green-600 text-white font-semibold py-3 px-4 rounded-xl transition-colors text-center text-sm",
  ifoodBtn: "flex-1 bg-red-500 hover:bg-red-600 text-white font-semibold py-3 px-4 rounded-xl transition-colors text-center text-sm",
  modalClose: "absolute top-4 right-4 bg-white rounded-full w-8 h-8 flex items-center justify-center shadow text-gray-600 hover:text-gray-900 transition-colors",
}
