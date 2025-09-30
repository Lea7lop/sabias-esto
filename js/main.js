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

  // Evitar títulos repetidos
  const unicos = [];
  const vistos = new Set();
  curiosidades.forEach(c => {
    if (!vistos.has(c.titulo)) {
      vistos.add(c.titulo);
      unicos.push(c);
    }
  });

  // Mostrar solo 5 en inicio (con Ching Shih primero), máximo 50 en categorías
  let mostrar;
  if (!filtroCategoria || filtroCategoria === "Inicio") {
    const chingShih = unicos.find(c => c.titulo.includes("Ching Shih"));
    mostrar = [chingShih, ...unicos.filter(c => c.titulo !== chingShih.titulo)].slice(0,5);
  } else {
    mostrar = unicos.slice(0,50);
  }

  const contenedor = document.getElementById("curiosidades-container");
  if (!contenedor) return;
  contenedor.innerHTML = "";

  mostrar.forEach(c => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      ${c.imagen ? `<img src="${c.imagen}" alt="${c.titulo}" class="card-img">` : ""}
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

// Detectar categoría en la URL
function detectarCategoriaDeURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("cat");
}

// Búsqueda por texto
function buscarCuriosidad() {
  const input = document.getElementById("searchInput")?.value;
  cargarCuriosidades(null, input);
}

document.addEventListener("DOMContentLoaded", () => {
  // Toggle tema oscuro
  const toggle = document.querySelector(".theme-toggle");
  if(toggle) toggle.addEventListener("click", () => document.body.classList.toggle("dark"));

  const categoria = detectarCategoriaDeURL();
  if (categoria) {
    cargarCuriosidades(categoria);
  } else {
    cargarCuriosidades();
  }

  // Filtros de categorías
  document.querySelectorAll(".category-link").forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      document.querySelectorAll(".category-link").forEach(l => l.classList.remove("active"));
      link.classList.add("active");
      cargarCuriosidades(link.dataset.category);
    });
  });

  // Input de búsqueda
  const searchInput = document.getElementById("searchInput");
  if(searchInput) {
    searchInput.addEventListener("input", () => {
      buscarCuriosidad();
    });
  }
});
