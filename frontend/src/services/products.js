import api from "./api"

export const getProducts = () => api.get('/products')
export const getProductById = (id) => api.get(`/products/${id}`)
export const getProductsByCategory = (categoryId) => api.get(`/products/category/${categoryId}`)

export const createProduct = (data) => api.post('/products', data)
export const updateProduct = (id, data) => api.put(`/products/${id}`, data)
export const deleteProduct = (id) => api.delete(`/products/${id}`)
