// main.js

async function cargarCuriosidades(filtroCategoria = null, filtroTexto = null) {
  const response = await fetch("curiosidades_moderno.json");
  const datos = await response.json();

  let curiosidades = datos;

  // Filtrar por categoría si existe
  if (filtroCategoria) {
    curiosidades = curiosidades.filter(c => c.categoria === filtroCategoria);
  }

  // Filtrar por texto si existe
  if (filtroTexto) {
    curiosidades = curiosidades.filter(c =>
      c.titulo.toLowerCase().includes(filtroTexto.toLowerCase()) ||
      c.descripcion.toLowerCase().includes(filtroTexto.toLowerCase())
    );
  }

  // Ordenar por fecha descendente si existe campo date, sino por id
  curiosidades.sort((a,b) => (b.date ? new Date(b.date) - new Date(a.date) : b.id - a.id));

  // Tomar solo los 5 primeros si no hay filtro de texto ni categoría
  if (!filtroCategoria && !filtroTexto) {
    curiosidades = curiosidades.slice(0, 5);
  }

  const contenedor = document.getElementById("curiosidades-container");
  if (!contenedor) return;
  contenedor.innerHTML = "";

  curiosidades.forEach(c => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <img src="${c.imagen}" alt="Imagen curiosidad">
      <div class="card-body">
        <h3>${c.titulo}</h3>
        <p>${c.descripcion.length > 100 ? c.descripcion.substring(0, 100) + "..." : c.descripcion}</p>
        <span class="categoria">Categoría: ${c.categoria}</span>
        <a href="curiosidad.html?id=${c.id}" class="ver-mas">Ver más</a>
      </div>
    `;
    contenedor.appendChild(card);
  });
}

// Detectar categoría en URL
function detectarCategoriaDeURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("cat");
}

// Búsqueda
function buscarCuriosidad() {
  const input = document.getElementById("searchInput").value;
  cargarCuriosidades(null, input);
}

// Inicializar
document.addEventListener("DOMContentLoaded", () => {
  const categoria = detectarCategoriaDeURL();
  if (categoria) {
    const title = document.getElementById("categoria-title");
    if (title) title.textContent = "Categoría: " + categoria;
    cargarCuriosidades(categoria);
  } else {
    cargarCuriosidades(); // Esto carga los 5 datos principales
  }
});
