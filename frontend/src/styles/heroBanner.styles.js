export const heroBannerStyles = {
  section: "relative flex items-center justify-center min-h-[70vh] bg-gradient-to-b from-[#f8bbd0] to-white overflow-hidden",
  content: "flex flex-col items-center text-center px-6 gap-3 z-10",
  logo: "w-44 drop-shadow-md -mt-10",
  eyebrow: "text-rose-400 text-xs -mt-12 font-semibold tracking-widest uppercase",
  title: "text-2xl md:text-4xl font-bold text-gray-800 leading-tight",
  subtitle: "text-gray-500 text-base md:text-lg max-w-md",
  cta: "mt-2 px-8 py-3 bg-[#ad1457] text-white font-semibold rounded-full shadow-md hover:bg-[#880e4f] transition-colors no-underline",
  btnGroupTopRight: "absolute top-6 right-6 flex gap-2 z-10 hidden md:flex",

  // Círculos decorativos nos cantos usando as cores do logo
  decoTopLeft: "absolute -top-16 -left-16 w-64 h-64 rounded-full bg-teal-100/50 blur-2xl pointer-events-none",
  decoBottomRight: "absolute -bottom-16 -right-16 w-72 h-72 rounded-full bg-pink-100/60 blur-2xl pointer-events-none",
}
