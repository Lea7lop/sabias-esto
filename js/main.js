document.addEventListener("DOMContentLoaded", async () => {
  const toggle = document.querySelector(".theme-toggle");
  toggle.addEventListener("click", () => document.body.classList.toggle("dark"));

  const container = document.getElementById("curiosidades-container");
  const searchBtn = document.getElementById("searchBtn");
  const searchInput = document.getElementById("searchInput");

  const response = await fetch("curiosidades_moderno.json");
  let datos = await response.json();

  function mostrarCuriosidades(categoria = "Inicio", texto = "") {
    container.innerHTML = "";
    let filtrados = datos.filter(c => 
      (categoria === "Inicio" || c.categoria === categoria) &&
      (texto === "" || c.titulo.toLowerCase().includes(texto.toLowerCase()) || c.descripcion.toLowerCase().includes(texto.toLowerCase()))
    );

    filtrados.slice(0,5).forEach(c => {
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
        <img src="${c.imagen}" alt="Imagen curiosidad">
        <div class="card-body">
          <h3>${c.titulo}</h3>
          <p>${c.descripcion.substring(0, 100)}...</p>
          <span class="categoria">Categoría: ${c.categoria}</span>
          <a class="ver-mas" href="curiosidad.html?id=${c.id}">Ver más →</a>
        </div>
      `;
      container.appendChild(card);
    });
  }

  document.querySelectorAll(".category-link").forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      document.querySelectorAll(".category-link").forEach(l => l.classList.remove("active"));
      link.classList.add("active");
      mostrarCuriosidades(link.dataset.category);
    });
  });

  searchBtn.addEventListener("click", () => mostrarCuriosidades("Inicio", searchInput.value));

  mostrarCuriosidades();
});
