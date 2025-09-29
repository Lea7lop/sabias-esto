document.querySelector(".theme-toggle").addEventListener("click", () => {
  document.body.classList.toggle("dark");
});

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

  if (!filtroCategoria && !filtroTexto) curiosidades = curiosidades.slice(0, 5);

  const contenedor = document.getElementById("curiosidades-container");
  contenedor.innerHTML = "";

  // Animación en cascada
  curiosidades.forEach((c, i) => {
    const card = document.createElement("div");
    card.className = "card";
    card.style.animation = `fadeUp 0.6s forwards ${i * 0.15}s`;
    card.innerHTML = `
      <img src="${c.imagen}" alt="Imagen curiosidad">
      <div class="card-body">
        <h3>${c.titulo}</h3>
        <p>${c.descripcion.substring(0, 150)}...</p>
        <span class="categoria">Categoría: ${c.categoria}</span>
        <a href="curiosidad.html?id=${c.id}" class="ver-mas">Ver más →</a>
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

// Búsqueda
document.getElementById("searchBtn").addEventListener("click", () => {
  const input = document.getElementById("searchInput").value;
  cargarCuriosidades(null, input);
});

document.addEventListener("DOMContentLoaded", () => {
  cargarCuriosidades();
});
