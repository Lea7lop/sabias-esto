// Cargar datos curiosos
async function cargarDatos() {
  const res = await fetch('curiosidades.json');
  return await res.json();
}

// Mostrar datos por categoría
async function mostrarPorCategoria() {
  const params = new URLSearchParams(window.location.search);
  const categoria = params.get('categoria') || 'Todas';
  document.getElementById('categoria-title').textContent = `Datos curiosos de ${categoria}`;

  const datos = await cargarDatos();

  const lista = document.getElementById('curiosidades-list');
  lista.innerHTML = '';

  const filtrados = categoria === 'Todas' ? datos : datos.filter(d => d.categoria === categoria);

  filtrados.forEach(dato => {
    const div = document.createElement('div');
    div.classList.add('curiosidad-item');
    div.innerHTML = `
      <img src="${dato.imagen}" alt="${dato.titulo}">
      <div>
        <h2>${dato.titulo}</h2>
        <p>${dato.descripcion}</p>
      </div>
    `;
    lista.appendChild(div);
  });

  // Últimos 5
  const recientesDiv = document.getElementById('recientes');
  recientesDiv.innerHTML = '<h3>Últimos datos curiosos</h3>';
  const recientes = datos.slice(-5).reverse();
  recientes.forEach(dato => {
    const div = document.createElement('div');
    div.innerHTML = `<img src="${dato.imagen}" width="50"> <p>${dato.titulo}</p>`;
    recientesDiv.appendChild(div);
  });
}

// Buscador
document.getElementById('search-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  const query = document.getElementById('search-input').value.toLowerCase();
  const datos = await cargarDatos();
  const resultados = datos.filter(d => d.titulo.toLowerCase().includes(query) || d.descripcion.toLowerCase().includes(query));
  
  localStorage.setItem('resultados', JSON.stringify(resultados));
  window.location.href = 'buscar.html';
});

// Ejecutar al cargar la página
mostrarPorCategoria();
