const RUTA_JSON = 'curiosidades.json';

async function cargarDatos() {
  try {
    const res = await fetch(RUTA_JSON);
    const datos = await res.json();
    return Array.isArray(datos) ? datos : [];
  } catch (err) {
    console.error("Error al cargar datos:", err);
    return [];
  }
}

async function mostrarCuriosidades() {
  const datos = await cargarDatos();
  const lista = document.getElementById('curiosidades-list');
  if (lista) lista.innerHTML = '';

  datos.forEach(dato => {
    const titulo = dato.titulo || 'Sin título';
    const descripcion = dato.descripcion || 'Sin descripción';
    const imagen = dato.imagen || 'https://via.placeholder.com/300x200?text=Sin+Imagen';

    const div = document.createElement('div');
    div.classList.add('curiosidad-item');
    div.innerHTML = `
      <img src="${imagen}" alt="${titulo}">
      <div>
        <h2>${titulo}</h2>
        <p>${descripcion}</p>
      </div>
    `;
    lista.appendChild(div);
  });
}

document.addEventListener('DOMContentLoaded', mostrarCuriosidades);
