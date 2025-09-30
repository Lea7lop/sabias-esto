async function cargarCuriosidades(filtroCategoria = null, filtroTexto = null) {
  const response = await fetch("data/curiosidades_moderno.json");
  const datos = await response.json();

  let curiosidades = datos;

  // IDs de los primeros 5 datos fijos (incluye la pirata mujer)
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

  const contenedor = document.getElementById("curiosidadesContainer");
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
    card.className = "curiosidad-card";
    card.innerHTML = `
      ${c.imagen ? `<img src="${c.imagen}" alt="${c.titulo}">` : ""}
      <div class="categoria">${c.categoria}</div>
      <h3>${c.titulo}</h3>
      <p>${c.descripcion.length > 200 ? c.descripcion.substring(0,200) + "..." : c.descripcion}</p>
      <a href="curiosidad.html?id=${c.id}" class="ver-mas">Ver más →</a>
    `;
    contenedor.appendChild(card);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".theme-toggle");
  if(toggle) toggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
  });

  cargarCuriosidades(); // al cargar la página

  // Filtrar por categorías
  document.querySelectorAll(".filtro").forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      const cat = link.dataset.categoria;
      cargarCuriosidades(cat === "Todos" ? null : cat);
    });
  });

  // Buscar por texto
  const busquedaInput = document.getElementById("busqueda");
  if(busquedaInput) {
    busquedaInput.addEventListener("input", () => {
      const termino = busquedaInput.value.toLowerCase();
      cargarCuriosidades(null, termino);
    });
  }
});
