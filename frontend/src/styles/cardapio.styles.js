import { productCardStyles } from './productCard.styles'

export const cardapioStyles = {
  wrapper: "flex flex-col gap-12 px-4 py-10 max-w-6xl mx-auto",
  section: "flex flex-col gap-6",
  header: "flex flex-col gap-1",
  heading: "text-3xl font-bold text-gray-900",
  empty: "text-center py-20 text-gray-400",
  ...productCardStyles,
}
