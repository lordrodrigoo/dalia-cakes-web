import api from './api'


// Buscar posts em destaque
export const getFeaturedPosts = (params) => api.get("/instagram/featured", { params });

// Buscar posts por subcategoria
export const getPostsBySubcategory = (slug, params) => api.get(`/instagram/subcategory/${slug}`, { params });

// Buscar todos os posts (admin)
export const getAllPosts = (params) => api.get("/instagram", { params });
