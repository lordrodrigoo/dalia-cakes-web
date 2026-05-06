export const adminInstagramStyles = {
  wrapper: "flex flex-col gap-6",

  // Header
  header: "flex items-center justify-between",
  heading: "text-2xl font-bold text-gray-900",
  addBtn: "flex items-center gap-2 bg-zinc-950 text-white px-4 py-2 rounded-lg hover:bg-zinc-800 transition-colors text-sm font-semibold",
  syncBtn: "flex items-center gap-2 border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors text-sm font-semibold disabled:opacity-50 disabled:cursor-not-allowed",

  // Filtros
  filterWrapper: "flex items-center gap-3 flex-wrap",
  select: "border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 transition bg-white",

  // Grid de posts
  grid: "grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4",
  card: "relative bg-white rounded-xl overflow-hidden shadow border border-gray-100 group",
  cardImg: "w-full aspect-square object-cover",
  cardImgFallback: "w-full aspect-square items-center justify-center bg-gray-100 text-4xl",
  cardOverlay: "absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center gap-2 p-2",
  cardSubcategory: "text-xs text-white bg-black/40 px-2 py-1 rounded-full text-center w-full truncate",
  cardDeleteBtn: "text-xs px-3 py-1.5 rounded-lg bg-red-500 text-white hover:bg-red-600 transition-colors font-medium w-full text-center",
  cardClassifyBtn: "text-xs px-3 py-1.5 rounded-lg bg-white text-gray-800 hover:bg-gray-100 transition-colors font-medium w-full text-center",
  cardFeaturedBtn: "text-xs px-3 py-1.5 rounded-lg bg-yellow-400 text-yellow-900 hover:bg-yellow-300 transition-colors font-medium w-full text-center",
  cardFeaturedBadge: "absolute top-2 left-2 bg-yellow-400 text-yellow-900 text-xs font-bold px-2 py-0.5 rounded-full",

  // Empty state
  empty: "text-center py-12 text-gray-400 text-sm",

  // Modal
  modalOverlay: "fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4",
  modal: "bg-white rounded-xl shadow-xl w-full max-w-md",
  modalHeader: "flex items-center justify-between px-6 py-4 border-b border-gray-200",
  modalTitle: "text-lg font-semibold text-gray-900",
  modalClose: "text-gray-400 hover:text-gray-700 transition-colors text-xl",
  modalBody: "px-6 py-4 flex flex-col gap-4",
  modalFooter: "px-6 py-4 border-t border-gray-200 flex justify-end gap-3",

  // Form
  fieldWrapper: "flex flex-col gap-1",
  label: "text-sm font-medium text-gray-700",
  input: "w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-gray-400 transition",
  fileInput: "w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-zinc-950 file:text-white hover:file:bg-zinc-800 cursor-pointer",
  previewWrapper: "mt-2",
  preview: "w-24 h-24 object-cover rounded-lg border border-gray-200",

  // Buttons
  cancelBtn: "px-4 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 transition-colors text-sm font-medium",
  saveBtn: "px-4 py-2 rounded-lg bg-zinc-950 text-white hover:bg-zinc-800 transition-colors text-sm font-semibold disabled:opacity-50 disabled:cursor-not-allowed",
}
