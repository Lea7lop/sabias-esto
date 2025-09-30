async function cargarCuriosidades(filtroCategoria = null, filtroTexto = null) {
  const response = await fetch("data/curiosidades_moderno.json");
  const datos = await response.json();

  let curiosidades = datos;

  // Filtrar por categoría
  if (filtroCategoria && filtroCategoria !== "Todos") {
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

  // Mostrar solo 5 en Inicio
  const mostrar = filtroCategoria === null || filtroCategoria === "Todos" ? 
                  curiosidades.slice(0,5) : 
                  curiosidades.slice(0,50);

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

const filtros = document.querySelectorAll('.filtro');
const busquedaInput = document.getElementById('busqueda');

// Mostrar al inicio
document.addEventListener("DOMContentLoaded", () => {
  cargarCuriosidades();

  // Filtrar por categoría
  filtros.forEach(filtro => {
    filtro.addEventListener('click', e => {
      e.preventDefault();
      const cat = filtro.dataset.categoria;
      cargarCuriosidades(cat);
    });
  });

  // Buscar por texto
  busquedaInput.addEventListener('input', () => {
    const termino = busquedaInput.value.toLowerCase();
    cargarCuriosidades(null, termino);
  });
});
