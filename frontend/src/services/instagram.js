import api from './api'

export const getFeaturedPosts = () => api.get('/instagram-posts/featured')
export const getPostsBySubcategory = (slug) => api.get(`/instagram-posts/subcategory/${slug}`)
