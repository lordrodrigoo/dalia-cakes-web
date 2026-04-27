import { useState, useEffect } from 'react'
import { getCategories, createCategory, updateCategory, deleteCategory } from '../../services/categories'
import { adminCategoriasStyles as s } from '../../styles/adminCategorias.styles'
import { uploadImage } from '../../services/upload'
import toast from 'react-hot-toast'

function slugify(text) {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
}

const emptyForm = { name: '', slug: '', image: null, previewUrl: '' }

export default function AdminCategorias() {
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(emptyForm)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const fetchCategories = async () => {
    try {
      const res = await getCategories()
      setCategories(res.data)
    } catch {
      setCategories([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchCategories() }, [])

  const openCreate = () => {
    setEditing(null)
    setForm(emptyForm)
    setError('')
    setModalOpen(true)
  }

  const openEdit = (cat) => {
    setEditing(cat)
    setForm({ name: cat.name, slug: cat.slug, image: null, previewUrl: cat.image_url || '' })
    setError('')
    setModalOpen(true)
  }

  const closeModal = () => {
    setModalOpen(false)
    setEditing(null)
    setForm(emptyForm)
    setError('')
  }

  const handleNameChange = (e) => {
    const name = e.target.value
    setForm(prev => ({ ...prev, name, slug: slugify(name) }))
  }

  const handleImageChange = (e) => {
    const file = e.target.files[0]
    if (!file) return
    setForm(prev => ({ ...prev, image: file, previewUrl: URL.createObjectURL(file) }))
  }

  const handleSubmit = async () => {
  if (!form.name) return setError('Nome é obrigatório.')
  if (!editing && !form.image) return setError('Imagem é obrigatória.')

  setSaving(true)
  setError('')

  try {
    let image_url = form.previewUrl
    if (form.image) {
      image_url = await uploadImage(form.image, 'categories')
    }
    const data = { name: form.name, slug: form.slug, image_url }
    if (editing) {
      await updateCategory(editing.id, data)
      toast.success('Categoria atualizada com sucesso!')
    } else {
      await createCategory(data)
      toast.success('Categoria criada com sucesso!')
    }
    await fetchCategories()
    closeModal()
  } catch {
    toast.error('Erro ao salvar categoria.')
    setError('Erro ao salvar. Tente novamente.')
  } finally {
    setSaving(false)
  }
}

  const handleDelete = async (id) => {
  if (!confirm('Tem certeza que deseja excluir esta categoria?')) return
  try {
    await deleteCategory(id)
    toast.success('Categoria excluída com sucesso!')
    await fetchCategories()
  } catch {
    toast.error('Erro ao excluir categoria.')
  }
}

  return (
    <div className={s.wrapper}>

      <div className={s.header}>
        <h1 className={s.heading}>Categorias</h1>
        <button className={s.addBtn} onClick={openCreate}>
          + Nova categoria
        </button>
      </div>

      <div className={s.tableWrapper}>
        {loading ? (
          <p className={s.empty}>Carregando...</p>
        ) : categories.length === 0 ? (
          <p className={s.empty}>Nenhuma categoria cadastrada.</p>
        ) : (
          <table className={s.table}>
            <thead className={s.thead}>
              <tr>
                <th className={s.th}>Imagem</th>
                <th className={s.th}>Nome</th>
                <th className={s.th}>Slug</th>
                <th className={s.th}>Ações</th>
              </tr>
            </thead>
            <tbody>
              {categories.map((cat) => (
                <tr key={cat.id} className={s.tr}>
                  <td className={s.tdImg}>
                    {cat.image_url && <img src={cat.image_url} alt={cat.name} className={s.img} />}
                  </td>
                  <td className={s.td}>{cat.name}</td>
                  <td className={s.td}>{cat.slug}</td>
                  <td className={s.td}>
                    <div className={s.actions}>
                      <button className={s.editBtn} onClick={() => openEdit(cat)}>Editar</button>
                      <button className={s.deleteBtn} onClick={() => handleDelete(cat.id)}>Excluir</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Modal */}
      {modalOpen && (
        <div className={s.modalOverlay} onClick={closeModal}>
          <div className={s.modal} onClick={e => e.stopPropagation()}>

            <div className={s.modalHeader}>
              <h2 className={s.modalTitle}>{editing ? 'Editar categoria' : 'Nova categoria'}</h2>
              <button className={s.modalClose} onClick={closeModal}>✕</button>
            </div>

            <div className={s.modalBody}>
              <div className={s.fieldWrapper}>
                <label className={s.label}>Nome</label>
                <input
                  type="text"
                  value={form.name}
                  onChange={handleNameChange}
                  className={s.input}
                  placeholder="Ex: Bolos de Pote"
                />
              </div>

              <div className={s.fieldWrapper}>
                <label className={s.label}>Slug (gerado automaticamente)</label>
                <input
                  type="text"
                  value={form.slug}
                  readOnly
                  className={s.inputReadonly}
                />
              </div>

              <div className={s.fieldWrapper}>
                <label className={s.label}>Imagem</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className={s.fileInput}
                />
                {form.previewUrl && (
                  <div className={s.previewWrapper}>
                    <img src={form.previewUrl} alt="Preview" className={s.preview} />
                  </div>
                )}
              </div>

              {error && <p className="text-red-500 text-sm">{error}</p>}
            </div>

            <div className={s.modalFooter}>
              <button className={s.cancelBtn} onClick={closeModal}>Cancelar</button>
              <button className={s.saveBtn} onClick={handleSubmit} disabled={saving}>
                {saving ? 'Salvando...' : 'Salvar'}
              </button>
            </div>

          </div>
        </div>
      )}

    </div>
  )
}
