// Tema oscuro
document.querySelectorAll(".theme-toggle").forEach(btn => {
  btn.addEventListener("click", () => document.body.classList.toggle("dark"));
});

// Función común para cargar todos los datos en index
async function cargarCuriosidades() {
  const response = await fetch("curiosidades_moderno.json");
  const datos = await response.json();
  const contenedor = document.getElementById("curiosidades-container");
  if (!contenedor) return;

  contenedor.innerHTML = "";
  datos.forEach(c => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <img src="${c.imagen}" alt="Imagen curiosidad">
      <div class="card-body">
        <h3>${c.titulo}</h3>
        <p>${c.descripcion}</p>
        <span class="categoria">Categoría: ${c.categoria}</span>
        <a href="curiosidad.html?id=${c.id}" class="ver-mas">Ver más</a>
      </div>
    `;
    contenedor.appendChild(card);
  });
}

// Función para cargar un dato en detalle
async function cargarCuriosidadDetalle() {
  const contenedor = document.getElementById("curiosidad-container");
  if (!contenedor) return;

  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");
  if (!id) return;

  const response = await fetch("curiosidades_moderno.json");
  const datos = await response.json();
  const c = datos.find(item => item.id == id);
  if (!c) return;

  contenedor.innerHTML = `
    <div class="card">
      <img src="${c.imagen}" alt="Imagen curiosidad">
      <div class="card-body">
        <h1>${c.titulo}</h1>
        <p>${c.descripcion}</p>
        <span class="categoria">Categoría: ${c.categoria}</span>
        <a href="index.html" class="back-link">← Volver al Inicio</a>
      </div>
    </div>
  `;
}

// Detectar dónde estamos
document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("curiosidades-container")) {
    cargarCuriosidades();
  } else if (document.getElementById("curiosidad-container")) {
    cargarCuriosidadDetalle();
  }
});
