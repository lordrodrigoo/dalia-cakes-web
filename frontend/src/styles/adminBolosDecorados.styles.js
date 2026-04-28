export const adminBolosDecoradosStyles = {
  wrapper: "flex flex-col gap-6",

  // Header
  header: "flex flex-wrap items-center justify-between gap-3",
  heading: "text-xl md:text-2xl font-bold text-gray-900",
  addBtn: "flex items-center gap-2 bg-zinc-950 text-white px-4 py-2 rounded-lg hover:bg-zinc-800 transition-colors text-sm font-semibold",

  // Tabela
  tableWrapper: "bg-white rounded-xl border border-gray-200 overflow-x-auto",
  table: "w-full text-sm",
  thead: "bg-gray-50 border-b border-gray-200",
  th: "px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
  tr: "border-b border-gray-100 hover:bg-gray-50 transition-colors",
  td: "px-4 py-3 text-gray-700",

  // Ações
  actions: "flex items-center gap-2",
  editBtn: "text-xs px-3 py-1.5 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 transition-colors font-medium",
  deleteBtn: "text-xs px-3 py-1.5 rounded-lg border border-red-200 text-red-600 hover:bg-red-50 transition-colors font-medium",

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
  inputReadonly: "w-full border border-gray-200 rounded-lg px-3 py-2 text-sm bg-gray-50 text-gray-500 cursor-not-allowed",
  hint: "text-xs text-gray-400 mt-0.5",

  // Buttons
  cancelBtn: "px-4 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 transition-colors text-sm font-medium",
  saveBtn: "px-4 py-2 rounded-lg bg-zinc-950 text-white hover:bg-zinc-800 transition-colors text-sm font-semibold disabled:opacity-50 disabled:cursor-not-allowed",
}
