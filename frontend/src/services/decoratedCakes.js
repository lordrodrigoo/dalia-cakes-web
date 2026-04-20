import api from "./api"

export const getSubcategories = () => api.get('/decorated-cakes')
export const getPostsBySubcategory = (id) => api.get(`/decorated-cakes/${id}/posts`)

export const createSubcategory = (data) => api.post('/decorated-cakes/subcategories', data)
export const updateSubcategory = (id, data) => api.put(`/decorated-cakes/subcategories/${id}`, data)
export const deleteSubcategory = (id) => api.delete(`/decorated-cakes/subcategories/${id}`)
