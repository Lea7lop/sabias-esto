// Cargar JSON
async function cargarDatos() {
  const response = await fetch("curiosidades.json");
  const datos = await response.json();
  return datos;
}

// Renderizar tarjetas
function crearCard(dato) {
  return `
    <div class="card">
      <img src="${dato.imagen || 'https://via.placeholder.com/400x200?text=Curiosidad'}" alt="Imagen curiosidad">
      <div class="card-content">
        <h3>${dato.titulo}</h3>
        <p>${dato.descripcion}</p>
        <small><strong>Categoría:</strong> ${dato.categoria}</small>
      </div>
    </div>
  `;
}

// Mostrar últimos 5 en index.html
async function mostrarUltimos() {
  const datos = await cargarDatos();
  const ultimos = datos.slice(-5).reverse();
  const contenedor = document.getElementById("ultimos-datos");

  if (contenedor) {
    contenedor.innerHTML = ultimos.map(d => crearCard(d)).join("");
  }
}

// Mostrar por categoría en categorias.html
async function mostrarCategoria() {
  const params = new URLSearchParams(window.location.search);
  const categoria = params.get("categoria");

  if (!categoria) return;

  const datos = await cargarDatos();
  const filtrados = datos.filter(d => d.categoria.toLowerCase() === categoria.toLowerCase());

  const titulo = document.getElementById("categoria-title");
  const contenedor = document.getElementById("lista-categoria");

  if (titulo) titulo.textContent = `Datos curiosos de ${categoria.charAt(0).toUpperCase() + categoria.slice(1)}`;
  if (contenedor) contenedor.innerHTML = filtrados.map(d => crearCard(d)).join("");
}

// Buscar en todas las curiosidades
async function buscarDato() {
  const input = document.getElementById("searchInput").value.toLowerCase();
  if (!input) return;

  const datos = await cargarDatos();
  const resultados = datos.filter(d =>
    d.titulo.toLowerCase().includes(input) ||
    d.descripcion.toLowerCase().includes(input)
  );

  // Redirigir a una página de búsqueda
  const contenedor = document.getElementById("lista-categoria");
  const titulo = document.getElementById("categoria-title");

  if (contenedor && titulo) {
    titulo.textContent = `Resultados de búsqueda: "${input}"`;
    contenedor.innerHTML = resultados.length
      ? resultados.map(d => crearCard(d)).join("")
      : `<p>No se encontraron resultados para "${input}".</p>`;
  } else {
    window.location.href = `categorias.html?categoria=buscar&query=${input}`;
  }
}

// Mostrar resultados si es búsqueda desde URL
async function mostrarBusqueda() {
  const params = new URLSearchParams(window.location.search);
  const query = params.get("query");

  if (!query) return;

  const datos = await cargarDatos();
  const resultados = datos.filter(d =>
    d.titulo.toLowerCase().includes(query.toLowerCase()) ||
    d.descripcion.toLowerCase().includes(query.toLowerCase())
  );

  const titulo = document.getElementById("categoria-title");
  const contenedor = document.getElementById("lista-categoria");

  if (titulo) titulo.textContent = `Resultados de búsqueda: "${query}"`;
  if (contenedor) {
    contenedor.innerHTML = resultados.length
      ? resultados.map(d => crearCard(d)).join("")
      : `<p>No se encontraron resultados para "${query}".</p>`;
  }
}

// Ejecutar funciones dependiendo de la página
document.addEventListener("DOMContentLoaded", () => {
  mostrarUltimos();
  mostrarCategoria();
  mostrarBusqueda();
});
