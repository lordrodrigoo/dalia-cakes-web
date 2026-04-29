export const instagramFeedStyles = {
  section: "py-10 px-0 w-full",
  title: "text-2xl font-bold text-gray-800 mb-6 text-center",
  sliderWrapper: "relative flex items-center gap-2 px-2",
  carousel: "flex-1",
  item: "block bg-white rounded-xl shadow overflow-hidden cursor-pointer group",
  imgWrapper: "relative overflow-hidden",
  img: "w-full aspect-square object-cover transition-transform duration-500 ease-in-out group-hover:scale-105",
  overlay: "absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center",
  overlayHint: "text-white text-sm font-semibold tracking-wide",
  single: "flex justify-center",
  singleItem: "max-w-sm w-full",
  arrow: "flex-shrink-0 bg-white border border-pink-200 text-pink-500 rounded-full w-10 h-10 flex items-center justify-center text-2xl font-bold shadow hover:bg-pink-50 hover:border-pink-400 transition-all cursor-pointer select-none z-10",

  // Lightbox
  lightboxOverlay: "fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4",
  lightboxBox: "relative bg-white rounded-2xl overflow-hidden shadow-2xl max-w-lg w-full",
  lightboxImg: "w-full aspect-square object-cover",
  lightboxFooter: "flex items-center justify-center gap-3 px-4 py-4",
  lightboxInstagramBtn: "flex items-center gap-1.5 text-xs font-semibold text-white bg-gradient-to-r from-pink-500 to-purple-600 px-4 py-2 rounded-full hover:opacity-90 transition-opacity no-underline",
  lightboxShareBtn: "flex items-center gap-1.5 text-xs font-semibold text-gray-700 border border-gray-300 px-4 py-2 rounded-full hover:bg-gray-100 transition-colors",
  lightboxClose: "absolute top-3 right-3 bg-black/50 hover:bg-black/70 text-white rounded-full w-8 h-8 flex items-center justify-center text-lg transition-colors cursor-pointer z-10",

  // Share menu
  shareWrapper: "relative",
  shareMenu: "absolute bottom-full mb-2 right-0 bg-white border border-gray-200 rounded-xl shadow-lg py-1 min-w-[160px] z-10",
  shareMenuItem: "flex items-center gap-2 w-full px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 transition-colors text-left",
  shareMenuIcon: "w-4 h-4 flex-shrink-0",
}
