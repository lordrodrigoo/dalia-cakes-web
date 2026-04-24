export const headerStyles = {
  header: "w-screen bg-white shadow-sm sticky top-0 z-50",
  inner: "w-full flex items-center justify-between px-4 md:px-8 py-3",
  navWrapper: "flex-1 flex justify-center items-center",
  nav: "text-sm hidden md:flex items-center gap-12",
  navOpen: "flex flex-col items-center text-center gap-4 absolute top-full left-0 w-full bg-white px-4 py-4 shadow-md md:hidden transition-all duration-500 transform scale-95 opacity-0 pointer-events-none z-50",
  navOpenActive: "scale-100 opacity-100 pointer-events-auto",
  link: "relative text-gray-600 font-medium transition-colors duration-200 after:content-[''] after:absolute after:left-0 after:-bottom-1 after:w-0 after:h-0.5 after:bg-pink-500 after:transition-all after:duration-300 hover:after:w-full hover:text-pink-500",
  linkActive: "relative text-pink-600 font-bold  border-pink-600 after:content-[''] after:absolute after:left-0 after:-bottom-1 after:w-full after:h-0.5 after:bg-pink-600",
  btnGroupDesktop: "justify-end gap-4 ml-2",
  btnGroupMobile: "flex md:hidden items-center justify-center gap-7",
  hamburger: "flex flex-col gap-1 md:hidden cursor-pointer mr-4",
  hamburgerBar: "w-6 h-0.5 bg-gray-900 transition-all duration-500",
}
