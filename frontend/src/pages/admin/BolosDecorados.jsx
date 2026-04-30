import { useState, useEffect } from 'react'
import { getSubcategories, createSubcategory, updateSubcategory, deleteSubcategory } from '../../services/decoratedCakes'
import { adminBolosDecoradosStyles as s } from '../../styles/adminBolosDecorados.styles'
import toast from 'react-hot-toast'

function slugify(text) {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
}

function hashtagify(text) {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s_]/g, '')
    .trim()
    .replace(/\s+/g, '_')
    .replace(/_+/g, '_')
}

const emptyForm = { name: '', slug: '', hashtag: '' }

export default function AdminBolosDecorados() {
  const [subcategories, setSubcategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(emptyForm)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const fetchSubcategories = async () => {
    try {
      const res = await getSubcategories()
      setSubcategories(res.data)
    } catch {
      setSubcategories([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchSubcategories() }, [])

  const openCreate = () => {
    setEditing(null)
    setForm(emptyForm)
    setError('')
    setModalOpen(true)
  }

  const openEdit = (sub) => {
    setEditing(sub)
    setForm({ name: sub.name, slug: sub.slug, hashtag: sub.hashtag })
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
    setForm(prev => ({
      ...prev,
      name,
      slug: slugify(name),
      hashtag: hashtagify(name),
    }))
  }

  const handleSubmit = async () => {
  if (!form.name) return setError('Nome é obrigatório.')
  if (!form.hashtag) return setError('Hashtag é obrigatória.')

  setSaving(true)
  setError('')

  const data = { name: form.name, slug: form.slug, hashtag: form.hashtag }

  try {
    if (editing) {
      await updateSubcategory(editing.id, data)
      toast.success('Subcategoria atualizada com sucesso!')
    } else {
      await createSubcategory(data)
      toast.success('Subcategoria criada com sucesso!')
    }
    await fetchSubcategories()
    closeModal()
  } catch (err) {
    const msg = err.response?.data?.detail || err.response?.data?.message || 'Erro ao salvar. Tente novamente.'
    const detail = Array.isArray(msg) ? msg.map(e => e.msg).join(', ') : msg
    toast.error(detail)
    setError(detail)
  } finally {
    setSaving(false)
  }
}

  const handleDelete = async (id) => {
  if (!confirm('Tem certeza que deseja excluir esta subcategoria?')) return
  try {
    await deleteSubcategory(id)
    toast.success('Subcategoria excluída com sucesso!')
    await fetchSubcategories()
  } catch (err) {
    const msg = err.response?.data?.detail || 'Erro ao excluir subcategoria.'
    toast.error(Array.isArray(msg) ? msg.map(e => e.msg).join(', ') : msg)
  }
}

  return (
    <div className={s.wrapper}>

      <div className={s.header}>
        <h1 className={s.heading}>Bolos Decorados</h1>
        <button className={s.addBtn} onClick={openCreate}>+ Nova subcategoria</button>
      </div>

      <div className={s.tableWrapper}>
        {loading ? (
          <p className={s.empty}>Carregando...</p>
        ) : subcategories.length === 0 ? (
          <p className={s.empty}>Nenhuma subcategoria cadastrada.</p>
        ) : (
          <table className={s.table}>
            <thead className={s.thead}>
              <tr>
                <th className={s.th}>Nome</th>
                <th className={`${s.th} hidden sm:table-cell`}>Slug</th>
                <th className={`${s.th} hidden sm:table-cell`}>Hashtag</th>
                <th className={s.th}>Ações</th>
              </tr>
            </thead>
            <tbody>
              {subcategories.map((sub) => (
                <tr key={sub.id} className={s.tr}>
                  <td className={s.td}>{sub.name}</td>
                  <td className={`${s.td} hidden sm:table-cell`}>{sub.slug}</td>
                  <td className={`${s.td} hidden sm:table-cell`}>#{sub.hashtag}</td>
                  <td className={s.td}>
                    <div className={s.actions}>
                      <button className={s.editBtn} onClick={() => openEdit(sub)}>Editar</button>
                      <button className={s.deleteBtn} onClick={() => handleDelete(sub.id)}>Excluir</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {modalOpen && (
        <div className={s.modalOverlay} onClick={closeModal}>
          <div className={s.modal} onClick={e => e.stopPropagation()}>

            <div className={s.modalHeader}>
              <h2 className={s.modalTitle}>{editing ? 'Editar subcategoria' : 'Nova subcategoria'}</h2>
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
                  placeholder="Ex: Bolo Feminino"
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
                <label className={s.label}>Hashtag (gerada automaticamente)</label>
                <input
                  type="text"
                  value={form.hashtag}
                  onChange={e => setForm(prev => ({ ...prev, hashtag: e.target.value }))}
                  className={s.input}
                  placeholder="Ex: bolo_feminino"
                />
                <span className={s.hint}>Usada para classificar posts do Instagram automaticamente.</span>
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
