// Dark/Light Mode
const toggle = document.querySelector(".theme-toggle");
toggle.addEventListener("click", () => {
  document.body.classList.toggle("dark");
});

// Cargar curiosidades desde JSON moderno
async function cargarCuriosidades(filtroCategoria = null, filtroTexto = null) {
  const response = await fetch("data/curiosidades_moderno.json");
  const datos = await response.json();

  let curiosidades = datos;

  // Filtrar por categoría
  if (filtroCategoria && filtroCategoria !== "Inicio") {
    curiosidades = curiosidades.filter(c => c.categoria === filtroCategoria);
  }

  // Filtrar por búsqueda
  if (filtroTexto) {
    curiosidades = curiosidades.filter(c =>
      c.titulo.toLowerCase().includes(filtroTexto.toLowerCase()) ||
      c.descripcion.toLowerCase().includes(filtroTexto.toLowerCase())
    );
  }

  const container = document.getElementById("curiosidades-container");
  container.innerHTML = "";

  // Si es inicio, mostrar solo los 5 primeros
  if (!filtroCategoria || filtroCategoria === "Inicio") {
    curiosidades = curiosidades.slice(0, 5);
  }

  curiosidades.forEach(c => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <img src="${c.imagen}" alt="Imagen curiosidad">
      <div class="card-body">
        <h3>${c.titulo}</h3>
        <p>${c.descripcion.substring(0, 100)}...</p>
        <span class="categoria">Categoría: ${c.categoria}</span>
        <a href="curiosidad.html?id=${c.id}" class="ver-mas">Ver más →</a>
      </div>
    `;
    container.appendChild(card);
  });
}

// Navegación por categorías
document.querySelectorAll(".category-link").forEach(link => {
  link.addEventListener("click", e => {
    e.preventDefault();
    document.querySelectorAll(".category-link").forEach(l => l.classList.remove("active"));
    link.classList.add("active");
    cargarCuriosidades(link.dataset.category);
  });
});

// Inicializar
document.addEventListener("DOMContentLoaded", () => {
  cargarCuriosidades();
});
