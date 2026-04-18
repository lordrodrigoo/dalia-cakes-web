import { useState, useEffect } from 'react'
import { getProducts, createProduct, updateProduct, deleteProduct } from '../../services/products'
import { getCategories } from '../../services/categories'
import { adminProdutosStyles as s } from '../../styles/adminProdutos.styles'

function slugify(text) {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
}

const emptyForm = {
  name: '',
  slug: '',
  description: '',
  price: '',
  category_id: '',
  image: null,
  previewUrl: '',
}

export default function AdminProdutos() {
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [filterCategory, setFilterCategory] = useState('')
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(emptyForm)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const fetchAll = async () => {
    try {
      const [prodRes, catRes] = await Promise.all([getProducts(), getCategories()])
      setProducts(prodRes.data)
      setCategories(catRes.data)
    } catch {
      setProducts([])
      setCategories([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchAll() }, [])

  const openCreate = () => {
    setEditing(null)
    setForm(emptyForm)
    setError('')
    setModalOpen(true)
  }

  const openEdit = (prod) => {
    setEditing(prod)
    setForm({
      name: prod.name,
      slug: prod.slug,
      description: prod.description || '',
      price: prod.price,
      category_id: prod.category_id,
      image: null,
      previewUrl: prod.image_url || '',
    })
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
    if (!form.price) return setError('Preço é obrigatório.')
    if (!form.category_id) return setError('Categoria é obrigatória.')
    if (!editing && !form.image) return setError('Imagem é obrigatória.')

    setSaving(true)
    setError('')

    const formData = new FormData()
    formData.append('name', form.name)
    formData.append('slug', form.slug)
    formData.append('description', form.description)
    formData.append('price', form.price)
    formData.append('category_id', form.category_id)
    if (form.image) formData.append('image', form.image)

    try {
      if (editing) {
        await updateProduct(editing.id, formData)
      } else {
        await createProduct(formData)
      }
      await fetchAll()
      closeModal()
    } catch {
      setError('Erro ao salvar. Tente novamente.')
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Tem certeza que deseja excluir este produto?')) return
    try {
      await deleteProduct(id)
      await fetchAll()
    } catch {
      alert('Erro ao excluir produto.')
    }
  }

  const filtered = filterCategory
    ? products.filter(p => p.category_id === Number(filterCategory))
    : products

  const getCategoryName = (id) => categories.find(c => c.id === id)?.name || '-'

  return (
    <div className={s.wrapper}>

      <div className={s.header}>
        <h1 className={s.heading}>Produtos</h1>
        <button className={s.addBtn} onClick={openCreate}>+ Novo produto</button>
      </div>

      <div className={s.filterWrapper}>
        <select
          className={s.select}
          value={filterCategory}
          onChange={e => setFilterCategory(e.target.value)}
        >
          <option value="">Todas as categorias</option>
          {categories.map(cat => (
            <option key={cat.id} value={cat.id}>{cat.name}</option>
          ))}
        </select>
      </div>

      <div className={s.tableWrapper}>
        {loading ? (
          <p className={s.empty}>Carregando...</p>
        ) : filtered.length === 0 ? (
          <p className={s.empty}>Nenhum produto encontrado.</p>
        ) : (
          <table className={s.table}>
            <thead className={s.thead}>
              <tr>
                <th className={s.th}>Imagem</th>
                <th className={s.th}>Nome</th>
                <th className={s.th}>Categoria</th>
                <th className={s.th}>Preço</th>
                <th className={s.th}>Ações</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((prod) => (
                <tr key={prod.id} className={s.tr}>
                  <td className={s.tdImg}>
                    {prod.image_url && <img src={prod.image_url} alt={prod.name} className={s.img} />}
                  </td>
                  <td className={s.td}>{prod.name}</td>
                  <td className={s.td}>{getCategoryName(prod.category_id)}</td>
                  <td className={s.td}>R$ {Number(prod.price).toFixed(2)}</td>
                  <td className={s.td}>
                    <div className={s.actions}>
                      <button className={s.editBtn} onClick={() => openEdit(prod)}>Editar</button>
                      <button className={s.deleteBtn} onClick={() => handleDelete(prod.id)}>Excluir</button>
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
              <h2 className={s.modalTitle}>{editing ? 'Editar produto' : 'Novo produto'}</h2>
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
                  placeholder="Ex: Bolo de Chocolate"
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
                <label className={s.label}>Descrição</label>
                <textarea
                  value={form.description}
                  onChange={e => setForm(prev => ({ ...prev, description: e.target.value }))}
                  className={s.textarea}
                  rows={3}
                  placeholder="Descreva o produto..."
                />
              </div>

              <div className={s.fieldWrapper}>
                <label className={s.label}>Preço (R$)</label>
                <input
                  type="number"
                  min="0"
                  step="0.01"
                  value={form.price}
                  onChange={e => setForm(prev => ({ ...prev, price: e.target.value }))}
                  className={s.input}
                  placeholder="Ex: 45.00"
                />
              </div>

              <div className={s.fieldWrapper}>
                <label className={s.label}>Categoria</label>
                <select
                  value={form.category_id}
                  onChange={e => setForm(prev => ({ ...prev, category_id: e.target.value }))}
                  className={s.input}
                >
                  <option value="">Selecione uma categoria</option>
                  {categories.map(cat => (
                    <option key={cat.id} value={cat.id}>{cat.name}</option>
                  ))}
                </select>
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
