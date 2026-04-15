import api from "./api";

export const getCategories = () => api.get('/categories')
export const getCategoryBySlug = (slug) => api.get(`/categories/${slug}`)
