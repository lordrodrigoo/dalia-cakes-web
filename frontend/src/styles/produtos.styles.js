import { productCardStyles } from './productCard.styles'

export const produtosStyles = {
  wrapper: "flex flex-col gap-8 px-4 py-10 max-w-6xl mx-auto",
  header: "flex flex-col gap-1",
  heading: "text-3xl font-bold text-gray-900",
  subheading: "text-gray-500 text-base",
  empty: "text-center py-20 text-gray-400",
  ...productCardStyles,
}
