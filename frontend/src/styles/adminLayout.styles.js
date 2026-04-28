export const adminLayoutStyles = {
  wrapper: "min-h-screen flex bg-gray-50",
  
  // Sidebar
  sidebar: "fixed inset-y-0 left-0 z-50 w-64 bg-zinc-950 text-white flex flex-col transition-transform duration-300",
  sidebarOpen: "translate-x-0",
  sidebarClosed: "-translate-x-full",
  sidebarDesktop: "md:translate-x-0",
  overlay: "fixed inset-0 z-40 bg-black/50 md:hidden",
  
  // Sidebar header
  sidebarHeader: "relative flex items-center justify-center px-6 py-4 border-b border-zinc-800",
  sidebarLogo: "h-20 md:h-32 w-auto object-contain",
  sidebarClose: "md:hidden absolute right-4 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-white transition-colors text-lg",

  // Nav
  nav: "flex-1 px-4 py-6 flex flex-col gap-1",
  navLink: "flex items-center gap-3 px-4 py-3 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition-all text-sm font-medium",
  navLinkActive: "flex items-center gap-3 px-4 py-3 rounded-lg text-white bg-zinc-800 text-sm font-medium",
  navIcon: "w-5 h-5",

  // Sidebar footer
  sidebarFooter: "px-4 py-4 border-t border-zinc-800",
  logoutBtn: "flex items-center gap-3 px-4 py-3 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition-all text-sm font-medium w-full",

  // Main content
  main: "flex-1 md:ml-64 flex flex-col min-h-screen",
  
  // Top bar mobile
  topbar: "sticky top-0 z-30 bg-white border-b border-gray-200 px-4 py-3 flex items-center gap-4 md:hidden",
  topbarTitle: "text-sm font-semibold text-gray-800 flex-1",
  hamburger: "text-gray-700",

  // Content area
  content: "flex-1 p-4 md:p-6",

  // back to site
  siteLink: "flex items-center gap-3 px-4 py-3 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition-all text-sm font-medium w-full",
  topbarSiteLink: "text-sm text-gray-500 hover:text-gray-800 transition-colors font-medium",
}
