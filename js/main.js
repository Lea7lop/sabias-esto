// Cargar curiosidades desde el JSON moderno
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
        <p>${c.descripcion}</p>
        <span class="categoria">Categoría: ${c.categoria}</span>
      </div>
    `;
    contenedor.appendChild(card);
  });
}

// Detectar categoría en categorias.html
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
    cargarCuriosidades();
  }
});
