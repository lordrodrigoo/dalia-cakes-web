import api from './api'

export const getFeaturedPosts = () => api.get("/instagram-posts/featured")
export const getAllPosts = () => api.get("/instagram-posts")
export const getUnclassifiedPosts = () => api.get("/instagram-posts/unclassified")
export const getPostsBySubcategory = (id) => api.get(`/decorated-cakes/${id}/posts`)
export const updatePostSubcategory = (postId, subcategoryId) => api.patch(`/instagram-posts/${postId}/subcategory`, { subcategory_id: subcategoryId })
export const deletePost = (postId) => api.delete(`/instagram-posts/${postId}`)
export const createManualPost = (formData) => api.post('/instagram-posts/manual', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
