const BASE = 'http://127.0.0.1:8000'

const el = id => document.getElementById(id)
const results = el('results')
const recs = el('recommendations')

async function search() {
  console.debug('search() called')
  const q = el('q').value
  const category = el('category').value
  const min_price = el('min_price').value
  const max_price = el('max_price').value
  const sort_by = el('sort_by').value
  const sort_order = el('sort_order').value

  const params = new URLSearchParams()
  if (q) params.append('q', q)
  if (category) params.append('category', category)
  if (min_price) params.append('min_price', min_price)
  if (max_price) params.append('max_price', max_price)
  if (sort_by) params.append('sort_by', sort_by)
  params.append('sort_order', sort_order)
  params.append('page', 1)
  params.append('size', 20)

  try {
    const res = await fetch(`${BASE}/products/search?${params.toString()}`)
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    const data = await res.json()
    showResults(data)
  } catch (err) {
    console.error('Search error:', err)
    results.innerHTML = `<p class="small" style="color:red;">Error: ${err.message} - Backend at ${BASE}</p>`
  }
}

function showResults(list){
  results.innerHTML = ''
  if (!list || list.length === 0) {
    results.innerHTML = '<p class="small">No results</p>'
    return
  }
  for (const p of list){
    const d = document.createElement('div')
    d.className = 'card'
    d.innerHTML = `
      <strong>${p.name}</strong> <span class="small">(#${p.id})</span>
      <div class="small">${p.category} • $${p.price} • rating: ${p.rating} • stock: ${p.stock}</div>
      <div class="small">views: ${p.views} clicks: ${p.clicks}</div>
      <div style="margin-top:8px">
        <button type="button" onclick="view(${p.id})">View</button>
        <button type="button" class="secondary" onclick="clickProduct(${p.id})">Click</button>
        <button type="button" class="secondary" onclick="recommend(${p.id})">Recommend</button>
      </div>
    `
    results.appendChild(d)
  }
}

async function view(id){
  console.debug('view()', id)
  try {
    const res = await fetch(`${BASE}/products/${id}/view`)
    if (!res.ok) throw new Error(`View failed: ${res.status}`)
    await search()
  } catch (err) {
    console.error('View error:', err)
    results.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`
  }
}

async function clickProduct(id){
  console.debug('click()', id)
  try {
    const res = await fetch(`${BASE}/products/${id}/click`)
    if (!res.ok) throw new Error(`Click failed: ${res.status}`)
    await search()
  } catch (err) {
    console.error('Click error:', err)
    results.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`
  }
}

async function recommend(product_id){
  console.debug('recommend()', product_id)
  try {
    const res = await fetch(`${BASE}/recommend/${product_id}`)
    if (!res.ok) throw new Error(`Recommend failed: ${res.status}`)
    const data = await res.json()
    showRecommendations(data)
  } catch (err) {
    console.error('Recommend error:', err)
    recs.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`
  }
}

function showRecommendations(data){
  recs.innerHTML = ''
  const related = data.related || []
  const popular = data.popular || []
  const rDiv = document.createElement('div')
  rDiv.innerHTML = '<h3>Related</h3>'
  if (related.length === 0) rDiv.innerHTML += '<p class="small">No related products</p>'
  for (const p of related) {
    const elP = document.createElement('div')
    elP.className = 'card'
    elP.innerHTML = `<strong>${p.name}</strong> <div class="small">$${p.price} • ${p.category}</div>`
    rDiv.appendChild(elP)
  }
  const pDiv = document.createElement('div')
  pDiv.innerHTML = '<h3>Popular</h3>'
  for (const p of popular) {
    const elP = document.createElement('div')
    elP.className = 'card'
    elP.innerHTML = `<strong>${p.name}</strong> <div class="small">rating: ${p.rating} • views: ${p.views} • clicks: ${p.clicks}</div>`
    pDiv.appendChild(elP)
  }
  recs.appendChild(rDiv)
  recs.appendChild(pDiv)
}

async function popular(){
  try {
    const res = await fetch(`${BASE}/popular`)
    if (!res.ok) throw new Error(`Popular failed: ${res.status}`)
    const data = await res.json()
    showResults(data)
  } catch (err) {
    console.error('Popular error:', err)
    results.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`
  }
}

el('searchBtn').addEventListener('click', search)
el('popularBtn').addEventListener('click', popular)

// initial load
search()
