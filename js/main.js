// Dark/Light Mode
document.querySelector(".theme-toggle").addEventListener("click", () => {
  document.body.classList.toggle("dark");
});

// Cargar curiosidades
async function cargarCuriosidades(filtroCategoria = null) {
  const response = await fetch("curiosidades_moderno.json");
  const datos = await response.json();
  let curiosidades = datos;

  if (filtroCategoria && filtroCategoria !== "Inicio") {
    curiosidades = curiosidades.filter(c => c.categoria === filtroCategoria.toLowerCase());
  }

  const contenedor = document.getElementById("curiosidades-container");
  contenedor.innerHTML = "";

  curiosidades.forEach(c => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <img src="${c.imagen}" alt="Imagen curiosidad">
      <div class="card-body">
        <h3>${c.titulo}</h3>
        <p>${c.descripcion.substring(0, 60)}...</p>
        <span class="categoria">Categoría: ${c.categoria}</span>
        <a href="curiosidad.html?id=${c.id}" class="ver-mas">Ver más</a>
      </div>
    `;
    contenedor.appendChild(card);
  });
}

// Categorías
document.querySelectorAll(".category-link").forEach(link => {
  link.addEventListener("click", e => {
    e.preventDefault();
    document.querySelectorAll(".category-link").forEach(l => l.classList.remove("active"));
    link.classList.add("active");
    cargarCuriosidades(link.dataset.category);
  });
});

// Inicializar
document.addEventListener("DOMContentLoaded", () => cargarCuriosidades("Inicio"));
