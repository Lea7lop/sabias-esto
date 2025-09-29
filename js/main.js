// main.js adaptado para tu HTML actual

// Cargar curiosidades desde el JSON moderno
async function cargarCuriosidades(filtroCategoria = null, filtroTexto = null) {
  const response = await fetch("curiosidades_moderno.json");
  const datos = await response.json();

  let curiosidades = datos;

  // Filtrar por categoría si existe
  if (filtroCategoria && filtroCategoria !== "Inicio") {
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

  curiosidades.forEach((c, i) => {
    const card = document.createElement("div");
    card.className = "card";
    card.style.animationDelay = `${i * 0.1}s`; // efecto cascada igual que antes
    card.innerHTML = `
      <img src="${c.imagen || `https://picsum.photos/600/400?random=${i}`}" alt="Imagen curiosidad">
      <div class="content">
        <h2>${c.titulo}</h2>
        <p>${c.descripcion}</p>
        <span class="categoria">Categoría: ${c.categoria}</span>
      </div>
    `;
    contenedor.appendChild(card);
  });
}

// Detectar categoría desde los links del header
document.querySelectorAll(".category-link").forEach(link => {
  link.addEventListener("click", e => {
    e.preventDefault();
    document.querySelectorAll(".category-link").forEach(l => l.classList.remove("active"));
    link.classList.add("active");
    cargarCuriosidades(link.dataset.category);
  });
});

// Función de búsqueda
function buscarCuriosidad() {
  const input = document.getElementById("searchInput");
  if (!input) return;
  cargarCuriosidades(null, input.value);
}

// Inicializar al cargar la página
document.addEventListener("DOMContentLoaded", () => {
  cargarCuriosidades();

  // Buscar en tiempo real si hay input
  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", buscarCuriosidad);
  }
});
