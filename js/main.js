async function cargarCuriosidades(filtroCategoria = null, filtroTexto = null) {
  const response = await fetch("data/curiosidades_moderno.json");
  const datos = await response.json();

  let curiosidades = datos;

  // IDs de los primeros 5 datos fijos
  const primeros5Ids = [1,2,3,4,5];
  const primeros5 = curiosidades.filter(c => primeros5Ids.includes(c.id));

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

  let mostrar = [];

  if (!filtroCategoria || filtroCategoria === "Inicio") {
    // Al inicio siempre mostrar los 5 fijos
    mostrar = primeros5;
  } else {
    // En categorías, mostrar máximo 50 curiosidades sin duplicados
    const idsMostrados = new Set();
    mostrar = curiosidades.filter(c => {
      if(idsMostrados.has(c.id)) return false;
      idsMostrados.add(c.id);
      return true;
    }).slice(0, 50);
  }

  mostrar.forEach(c => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      ${c.imagen ? `<img src="${c.imagen}" alt="${c.titulo}" class="card-img">` : ""}
      <div class="card-body">
        <span class="categoria">${c.categoria}</span>
        <h3>${c.titulo}</h3>
        <p>${c.descripcion.length > 200 ? c.descripcion.substring(0,200) + "..." : c.descripcion}</p>
        <a href="curiosidad.html?id=${c.id}" class="ver-mas">Ver más →</a>
      </div>
    `;
    contenedor.appendChild(card);
  });
}

function detectarCategoriaDeURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("cat");
}

function buscarCuriosidad() {
  const input = document.getElementById("searchInput").value;
  cargarCuriosidades(null, input);
}

document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".theme-toggle");
  if(toggle) toggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
  });

  const categoria = detectarCategoriaDeURL();
  if (categoria) {
    cargarCuriosidades(categoria);
  } else {
    cargarCuriosidades();
  }

  document.querySelectorAll(".category-link").forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      document.querySelectorAll(".category-link").forEach(l => l.classList.remove("active"));
      link.classList.add("active");
      cargarCuriosidades(link.dataset.category);
    });
  });
});
