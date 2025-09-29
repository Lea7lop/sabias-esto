async function cargarCuriosidades(filtroCategoria = null) {
  const response = await fetch("curiosidades_moderno.json");
  const datos = await response.json();

  let curiosidades = datos.sort((a,b) => new Date(b.date) - new Date(a.date));

  if (filtroCategoria && filtroCategoria !== "Inicio") {
    curiosidades = curiosidades.filter(c => c.categoria === filtroCategoria);
  }

  const contenedor = document.getElementById("curiosidades-container");
  if (!contenedor) return;
  contenedor.innerHTML = "";

  // Mostrar solo 5 últimos en inicio
  if (!filtroCategoria || filtroCategoria === "Inicio") {
    curiosidades = curiosidades.slice(0,5);
  }

  curiosidades.forEach((c, i) => {
    const card = document.createElement("div");
    card.className = "card";
    card.style.animationDelay = `${i*0.1}s`;
    card.innerHTML = `
      <img src="${c.imagen}" alt="Imagen curiosidad">
      <div class="card-body">
        <h3>${c.titulo}</h3>
        <p>${c.descripcion.substring(0,100)}...</p>
        <span class="categoria">Categoría: ${c.categoria}</span>
        <a class="ver-mas" href="curiosidad.html?id=${c.id}">Ver más →</a>
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

// Dark/Light Mode
document.querySelector(".theme-toggle").addEventListener("click", () => {
  document.body.classList.toggle("dark");
});

// Inicializar
document.addEventListener("DOMContentLoaded", () => cargarCuriosidades());
