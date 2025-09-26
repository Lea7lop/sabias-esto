// Cambia la ruta según dónde esté tu JSON
const RUTA_JSON = 'curiosidades.json'; // si está en _publicaciones, pon '_publicaciones/curiosidades.json'

// Función para cargar los datos
async function cargarDatos() {
  try {
    const res = await fetch(RUTA_JSON);
    const datos = await res.json();
    return Array.isArray(datos) ? datos : [];
  } catch (err) {
    console.error("Error al cargar datos:", err);
    return [];
  }
}

// Mostrar datos por categoría
async function mostrarPorCategoria() {
  const params = new URLSearchParams(window.location.search);
  const categoria = params.get('categoria') || 'Todas';
  document.getElementById('categoria-title')?.textContent = `Datos curiosos de ${categoria}`;

  const datos = await cargarDatos();

  // Lista principal
  const lista = document.getElementById('curiosidades-list');
  if (lista) lista.innerHTML = '';

  const filtrados = categoria === 'Todas' ? datos : datos.filter(d => d.categoria === categoria);

  filtrados.forEach(dato => {
    const titulo = dato.titulo || 'Sin título';
    const descripcion = dato.descripcion || 'Sin descripción';
    const imagen = dato.imagen || 'https://via.placeholder.com/200x150?text=Sin+Imagen';

    if (lista) {
      const div = document.createElement('div');
      div.classList.add('curiosidad-item');
      div.innerHTML = `
        <img src="${imagen}" alt="${titulo}">
        <div>
          <h2>${titulo}</h2>
          <p>${descripcion}</p>
        </div>
      `;
      lista.appendChild(div);
    }
  });

  // Últimos 5 datos
  const recientesDiv = document.getElementById('recientes');
  if (recientesDiv) {
    recientesDiv.innerHTML = '<h3>Últimos datos curiosos</h3>';
    const recientes = datos.slice(-5).reverse();
    recientes.forEach(dato => {
      const titulo = dato.titulo || 'Sin título';
      const imagen = dato.imagen || 'https://via.placeholder.com/50x50?text=Sin+Imagen';
      const div = document.createElement('div');
      div.classList.add('reciente-item');
      div.innerHTML = `<img src="${imagen}" width="50" alt="${titulo}"> <p>${titulo}</p>`;
      recientesDiv.appendChild(div);
    });
  }
}

// Buscador
document.getElementById('search-form')?.addEventListener('submit', async function(e) {
  e.preventDefault();
  const query = document.getElementById('search-input').value.toLowerCase();
  const datos = await cargarDatos();
  const resultados = datos.filter(d => 
    (d.titulo?.toLowerCase().includes(query) || d.descripcion?.toLowerCase().includes(query))
  );

  localStorage.setItem('resultados', JSON.stringify(resultados));
  window.location.href = 'buscar.html';
});

// Mostrar resultados de búsqueda
async function mostrarResultadosBusqueda() {
  const resultados = JSON.parse(localStorage.getItem('resultados') || '[]');
  const lista = document.getElementById('resultados-list');
  if (!lista) return;
  lista.innerHTML = '';

  resultados.forEach(dato => {
    const titulo = dato.titulo || 'Sin título';
    const descripcion = dato.descripcion || 'Sin descripción';
    const imagen = dato.imagen || 'https://via.placeholder.com/200x150?text=Sin+Imagen';
    const div = document.createElement('div');
    div.classList.add('curiosidad-item');
    div.innerHTML = `
      <img src="${imagen}" alt="${titulo}">
      <div>
        <h2>${titulo}</h2>
        <p>${descripcion}</p>
      </div>
    `;
    lista.appendChild(div);
  });
}

// Ejecutar automáticamente
document.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('categoria-title')) {
    mostrarPorCategoria();
  }
  if (document.getElementById('resultados-list')) {
    mostrarResultadosBusqueda();
  }
});
