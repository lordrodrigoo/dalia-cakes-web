export const chatbotStyles = {
  // Botão flutuante
  fab: "fixed bottom-6 right-6 z-50 w-24 h-24 rounded-full shadow-2xl bg-white border-2 border-pink-200 flex items-center justify-center cursor-pointer hover:scale-110 transition-transform duration-200 hover:border-pink-400",
  fabUnread: "absolute -top-1 -right-1 w-4 h-4 bg-pink-500 rounded-full border-2 border-white",

  // Janela do chat
  window: "fixed bottom-24 right-6 z-50 w-80 sm:w-96 bg-white rounded-2xl shadow-2xl border border-pink-100 flex flex-col overflow-hidden",
  windowEnter: "animate-[fadeSlideUp_0.25s_ease-out]",

  // Header da janela
  header: "bg-gradient-to-r from-[#f8bbd0] to-[#f48fb1] px-4 py-3 flex items-center gap-3",
  headerMascot: "flex-shrink-0",
  headerInfo: "flex-1",
  headerName: "text-[#880e4f] font-bold text-sm leading-tight",
  headerStatus: "text-[#ad1457] text-xs",
  headerClose: "text-[#ad1457] hover:text-[#880e4f] text-xl leading-none cursor-pointer transition-colors",

  // Área de mensagens
  messages: "flex-1 overflow-y-auto px-4 py-3 space-y-3 max-h-80 min-h-40 bg-gray-50",

  // Bolhas
  bubbleBot: "flex items-end gap-2",
  bubbleBotAvatar: "flex-shrink-0 mb-1",
  bubbleBotText: "bg-white border border-pink-100 text-gray-700 text-sm px-3 py-2 rounded-2xl rounded-bl-sm shadow-sm max-w-[75%] leading-relaxed",

  bubbleUser: "flex justify-end",
  bubbleUserText: "bg-[#ad1457] text-white text-sm px-3 py-2 rounded-2xl rounded-br-sm shadow-sm max-w-[75%] leading-relaxed",

  // Indicador de digitação
  typing: "flex items-end gap-2",
  typingBubble: "bg-white border border-pink-100 px-3 py-3 rounded-2xl rounded-bl-sm shadow-sm flex gap-1",
  typingDot: "w-2 h-2 rounded-full bg-pink-300",

  // Input
  inputArea: "px-3 py-3 border-t border-pink-100 bg-white flex gap-2",
  input: "flex-1 bg-gray-50 border border-pink-200 rounded-full px-4 py-2 text-sm outline-none focus:border-pink-400 focus:bg-white transition-colors placeholder:text-gray-400",
  sendBtn: "w-9 h-9 flex-shrink-0 bg-[#ad1457] hover:bg-[#880e4f] text-white rounded-full flex items-center justify-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed",
}
