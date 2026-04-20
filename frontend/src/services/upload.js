import api from "./api"

export const uploadImage = async (file, folder = "products") => {
  const formData = new FormData()
  formData.append("file", file)
  const res = await api.post(`/upload/image?folder=${folder}`, formData, {
    headers: { "Content-Type": "multipart/form-data" }
  })
  return res.data.url
}
