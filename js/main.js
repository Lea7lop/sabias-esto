async function cargarCuriosidades(filtroCategoria = null, filtroTexto = null) {
  const response = await fetch("curiosidades_moderno.json");
  const datos = await response.json();
  let curiosidades = datos;

  if (filtroCategoria && filtroCategoria !== "Inicio") {
    curiosidades = curiosidades.filter(c => c.categoria.toLowerCase() === filtroCategoria.toLowerCase());
  }

  if (filtroTexto) {
    curiosidades = curiosidades.filter(c =>
      c.titulo.toLowerCase().includes(filtroTexto.toLowerCase()) ||
      c.descripcion.toLowerCase().includes(filtroTexto.toLowerCase())
    );
  }

  if (filtroCategoria === "Inicio") {
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
        <p>${c.descripcion.substring(0, 80)}...</p>
        <span class="categoria">Categoría: ${c.categoria}</span>
        <a href="curiosidad.html?id=${c.id}" class="ver-mas">Ver más →</a>
      </div>
    `;
    contenedor.appendChild(card);
  });
}

// Navegación de categorías
document.querySelectorAll(".category-link").forEach(link => {
  link.addEventListener("click", e => {
    e.preventDefault();
    document.querySelectorAll(".category-link").forEach(l => l.classList.remove("active"));
    link.classList.add("active");
    cargarCuriosidades(link.dataset.category);
  });
});

// Buscador
document.getElementById("searchInput")?.addEventListener("input", () => {
  cargarCuriosidades(null, document.getElementById("searchInput").value);
});

// Modo nocturno
document.querySelector(".theme-toggle").addEventListener("click", () => {
  document.body.classList.toggle("dark");
});

// Inicializar
document.addEventListener("DOMContentLoaded", () => cargarCuriosidades("Inicio"));
