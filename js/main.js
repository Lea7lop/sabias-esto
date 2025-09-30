async function cargarCuriosidades(filtroCategoria = null, filtroTexto = null) {
  const response = await fetch("data/curiosidades_moderno.json");
  const datos = await response.json();

  let curiosidades = datos;

  // Filtrar por categoría
  if (filtroCategoria && filtroCategoria !== "Inicio") {
    curiosidades = curiosidades.filter(c => c.categoria === filtroCategoria);
  }

  // Filtrar por texto
  if (filtroTexto) {
    curiosidades = curiosidades.filter(c =>
      c.titulo.toLowerCase().includes(filtroTexto.toLowerCase()) ||
      c.descripcion.toLowerCase().includes(filtroTexto.toLowerCase())
    );
  }

  const contenedor = document.getElementById("curiosidades-container");
  if (!contenedor) return;

  contenedor.innerHTML = "";

  // Mostrar solo 5 en Inicio, máximo 50 en categorías
  const mostrar = (filtroCategoria === null || filtroCategoria === "Inicio") ? curiosidades.slice(0,5) : curiosidades.slice(0,50);

  mostrar.forEach(c => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      ${c.imagen ? `<img src="${c.imagen}" alt="${c.titulo}" class="card-img">` : ''}
      <div class="card-body">
        <h3>${c.titulo}</h3>
        <p>${c.descripcion.length > 200 ? c.descripcion.substring(0,200) + "..." : c.descripcion}</p>
        <span class="categoria">Categoría: ${c.categoria}</span>
        <a href="curiosidad.html?id=${c.id}" class="ver-mas">Ver más →</a>
      </div>
    `;
    contenedor.appendChild(card);
  });
}

function buscarCuriosidad() {
  const input = document.getElementById("searchInput").value;
  cargarCuriosidades(null, input);
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelector(".theme-toggle").addEventListener("click", () => {
    document.body.classList.toggle("dark");
  });

  // Detectar categoría de URL
  const params = new URLSearchParams(window.location.search);
  const categoria = params.get("cat");
  if (categoria) {
    cargarCuriosidades(categoria);
  } else {
    cargarCuriosidades();
  }

  // Manejar clics en categorías
  document.querySelectorAll(".category-link").forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      document.querySelectorAll(".category-link").forEach(l => l.classList.remove("active"));
      link.classList.add("active");
      cargarCuriosidades(link.dataset.category);
    });
  });

  // Buscar al presionar Enter
  const input = document.getElementById("searchInput");
  input.addEventListener("keyup", e => {
    if (e.key === "Enter") buscarCuriosidad();
  });
});
