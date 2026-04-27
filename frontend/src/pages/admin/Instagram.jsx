import { useState, useEffect } from 'react'
import { getAllPosts, deletePost, updatePostSubcategory, createManualPost } from '../../services/instagram'
import { getSubcategories } from '../../services/decoratedCakes'
import { adminInstagramStyles as s } from '../../styles/adminInstagram.styles'
import toast from 'react-hot-toast'

export default function AdminInstagram() {
  const [posts, setPosts] = useState([])
  const [subcategories, setSubcategories] = useState([])
  const [filterSubcategory, setFilterSubcategory] = useState('')
  const [loading, setLoading] = useState(true)

  // Modal de upload manual
  const [uploadModalOpen, setUploadModalOpen] = useState(false)
  const [uploadForm, setUploadForm] = useState({ image: null, previewUrl: '', subcategory_id: '' })
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState('')

  // Modal de classificar
  const [classifyModalOpen, setClassifyModalOpen] = useState(false)
  const [classifyPost, setClassifyPost] = useState(null)
  const [classifySubcategoryId, setClassifySubcategoryId] = useState('')
  const [classifying, setClassifying] = useState(false)
  const [classifyError, setClassifyError] = useState('')

  const fetchAll = async () => {
    try {
      const [postsRes, subsRes] = await Promise.all([getAllPosts(), getSubcategories()])
      setPosts(postsRes.data)
      setSubcategories(subsRes.data)
    } catch {
      setPosts([])
      setSubcategories([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchAll() }, [])

  // Upload manual
  const openUploadModal = () => {
    setUploadForm({ image: null, previewUrl: '', subcategory_id: '' })
    setUploadError('')
    setUploadModalOpen(true)
  }

  const handleImageChange = (e) => {
    const file = e.target.files[0]
    if (!file) return
    setUploadForm(prev => ({ ...prev, image: file, previewUrl: URL.createObjectURL(file) }))
  }

  const handleUploadSubmit = async () => {
  if (!uploadForm.image) return setUploadError('Selecione uma imagem.')
  setUploading(true)
  setUploadError('')
  try {
    const formData = new FormData()
    formData.append('file', uploadForm.image)
    if (uploadForm.subcategory_id) {
      formData.append('subcategory_id', uploadForm.subcategory_id)
    }
    await createManualPost(formData)
    toast.success('Foto enviada com sucesso!')
    await fetchAll()
    setUploadModalOpen(false)
  } catch {
    toast.error('Erro ao enviar foto.')
    setUploadError('Erro ao fazer upload. Tente novamente.')
  } finally {
    setUploading(false)
  }
  }

  // Classificar post
  const openClassifyModal = (post) => {
    setClassifyPost(post)
    setClassifySubcategoryId(post.subcategory_id || '')
    setClassifyError('')
    setClassifyModalOpen(true)
  }

  const handleClassifySubmit = async () => {
  if (!classifySubcategoryId) return setClassifyError('Selecione uma subcategoria.')
  setClassifying(true)
  setClassifyError('')
  try {
    await updatePostSubcategory(classifyPost.id, classifySubcategoryId)
    toast.success('Post classificado com sucesso!')
    await fetchAll()
    setClassifyModalOpen(false)
  } catch {
    toast.error('Erro ao classificar post.')
    setClassifyError('Erro ao classificar. Tente novamente.')
  } finally {
    setClassifying(false)
  }
  }

  // Deletar
  const handleDelete = async (id) => {
  if (!confirm('Tem certeza que deseja excluir este post?')) return
  try {
    await deletePost(id)
    toast.success('Post excluído com sucesso!')
    await fetchAll()
  } catch {
    toast.error('Erro ao excluir post.')
  }
  }

  const getSubcategoryName = (id) => subcategories.find(s => s.id === id)?.name || null

  const filtered = filterSubcategory
    ? posts.filter(p => p.subcategory_id === filterSubcategory)
    : posts

  return (
    <div className={s.wrapper}>

      <div className={s.header}>
        <h1 className={s.heading}>Instagram</h1>
        <button className={s.addBtn} onClick={openUploadModal}>+ Nova foto</button>
      </div>

      <div className={s.filterWrapper}>
        <select
          className={s.select}
          value={filterSubcategory}
          onChange={e => setFilterSubcategory(e.target.value)}
        >
          <option value="">Todos os posts</option>
          <option value="unclassified">Sem subcategoria</option>
          {subcategories.map(sub => (
            <option key={sub.id} value={sub.id}>{sub.name}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <p className={s.empty}>Carregando...</p>
      ) : filtered.length === 0 ? (
        <p className={s.empty}>Nenhum post encontrado.</p>
      ) : (
        <div className={s.grid}>
          {filtered.map(post => (
            <div key={post.id} className={s.card}>
              <img src={post.media_url} alt={post.caption || 'Post'} className={s.cardImg} />
              <div className={s.cardOverlay}>
                {post.subcategory_id && (
                  <span className={s.cardSubcategory}>{getSubcategoryName(post.subcategory_id)}</span>
                )}
                <button className={s.cardClassifyBtn} onClick={() => openClassifyModal(post)}>
                  Classificar
                </button>
                <button className={s.cardDeleteBtn} onClick={() => handleDelete(post.id)}>
                  Excluir
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal upload manual */}
      {uploadModalOpen && (
        <div className={s.modalOverlay} onClick={() => setUploadModalOpen(false)}>
          <div className={s.modal} onClick={e => e.stopPropagation()}>
            <div className={s.modalHeader}>
              <h2 className={s.modalTitle}>Nova foto</h2>
              <button className={s.modalClose} onClick={() => setUploadModalOpen(false)}>✕</button>
            </div>
            <div className={s.modalBody}>
              <div className={s.fieldWrapper}>
                <label className={s.label}>Imagem</label>
                <input type="file" accept="image/*" onChange={handleImageChange} className={s.fileInput} />
                {uploadForm.previewUrl && (
                  <div className={s.previewWrapper}>
                    <img src={uploadForm.previewUrl} alt="Preview" className={s.preview} />
                  </div>
                )}
              </div>
              <div className={s.fieldWrapper}>
                <label className={s.label}>Subcategoria (opcional)</label>
                <select
                  value={uploadForm.subcategory_id}
                  onChange={e => setUploadForm(prev => ({ ...prev, subcategory_id: e.target.value }))}
                  className={s.input}
                >
                  <option value="">Sem subcategoria</option>
                  {subcategories.map(sub => (
                    <option key={sub.id} value={sub.id}>{sub.name}</option>
                  ))}
                </select>
              </div>
              {uploadError && <p className="text-red-500 text-sm">{uploadError}</p>}
            </div>
            <div className={s.modalFooter}>
              <button className={s.cancelBtn} onClick={() => setUploadModalOpen(false)}>Cancelar</button>
              <button className={s.saveBtn} onClick={handleUploadSubmit} disabled={uploading}>
                {uploading ? 'Enviando...' : 'Enviar'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal classificar */}
      {classifyModalOpen && (
        <div className={s.modalOverlay} onClick={() => setClassifyModalOpen(false)}>
          <div className={s.modal} onClick={e => e.stopPropagation()}>
            <div className={s.modalHeader}>
              <h2 className={s.modalTitle}>Classificar post</h2>
              <button className={s.modalClose} onClick={() => setClassifyModalOpen(false)}>✕</button>
            </div>
            <div className={s.modalBody}>
              <div className={s.fieldWrapper}>
                <label className={s.label}>Subcategoria</label>
                <select
                  value={classifySubcategoryId}
                  onChange={e => setClassifySubcategoryId(e.target.value)}
                  className={s.input}
                >
                  <option value="">Selecione uma subcategoria</option>
                  {subcategories.map(sub => (
                    <option key={sub.id} value={sub.id}>{sub.name}</option>
                  ))}
                </select>
              </div>
              {classifyError && <p className="text-red-500 text-sm">{classifyError}</p>}
            </div>
            <div className={s.modalFooter}>
              <button className={s.cancelBtn} onClick={() => setClassifyModalOpen(false)}>Cancelar</button>
              <button className={s.saveBtn} onClick={handleClassifySubmit} disabled={classifying}>
                {classifying ? 'Salvando...' : 'Salvar'}
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  )
}
