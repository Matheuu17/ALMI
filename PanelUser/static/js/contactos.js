/*
Filtro + buscador de la grilla de Contactos.
Funciona 100% en el cliente sobre las cards ya renderizadas
(data-tipo y data-nombre). Cuando haya backend, esto se puede
reemplazar por un fetch/submit real si se prefiere filtrar server-side.
*/

// Limpia valores "None", "undefined" o marcadores por defecto "---"
function cleanValue(val) {
  return (!val || val === "None" || val === "undefined" || val.includes("---")) ? "" : val;
}

document.addEventListener("DOMContentLoaded", () => {
  let CARRERAS_LIST = [];
  let RUBROS_LIST = [];

  try {
    const carrerasElem = document.getElementById("carreras-data");
    const rubrosElem = document.getElementById("rubros-data");

    if (carrerasElem && carrerasElem.textContent) {
      CARRERAS_LIST = JSON.parse(carrerasElem.textContent);
    }
    if (rubrosElem && rubrosElem.textContent) {
      RUBROS_LIST = JSON.parse(rubrosElem.textContent);
    }
  } catch (err) {
    console.warn("No se pudieron cargar las listas JSON de Django:", err);
  }

  // FIltro y buscar
  const searchInput = document.getElementById("contact-search");
  const filterSelect = document.getElementById("contact-filter");
  const cards = document.querySelectorAll("#contacts-grid .contact-card");

  function applyFilters() {
    const query = (searchInput?.value || "").trim().toLowerCase();
    const tipo = filterSelect?.value || "todos";

    cards.forEach((card) => {
      const matchesTipo = tipo === "todos" || card.dataset.tipo === tipo;
      const matchesQuery = (card.dataset.nombre || "").toLowerCase().includes(query);
      card.style.display = matchesTipo && matchesQuery ? "" : "none";
    });
  }

  searchInput?.addEventListener("input", applyFilters);
  filterSelect?.addEventListener("change", applyFilters);

  // Elementos de Modales
  const modalEdit = document.getElementById("modal-edit-contacto");
  const modalView = document.getElementById("modal-view-contacto");
  const closeBtns = document.querySelectorAll(".btn-close-modal");

  const formEdit = document.getElementById("form-edit-contacto");
  const formDesactivar = document.getElementById("form-desactivar-contacto");
  const btnDesactivar = document.getElementById("btn-desactivar-contacto");
  const archivoContainer = document.getElementById("archivo-actual-container");
  const editTipoSelect = document.getElementById("edit-tipo");

  // Función blindada para actualizar el selector de Carrera / Rubro
    function actualizarCamposTipo(tipo, valorSeleccionado = "") {
      const labelNombre = document.getElementById("edit-label-nombre");
      const labelCarreraRubro = document.getElementById("edit-label-carrera-rubro");
      const selectCarreraRubro = document.getElementById("edit-carrera-rubro");

      if (!selectCarreraRubro) return;

      selectCarreraRubro.innerHTML = ""; // Limpiar opciones anteriores

      const esEmpresa = tipo === "empresa";
      const rawList = esEmpresa ? RUBROS_LIST : CARRERAS_LIST;
      const listaUsar = Array.isArray(rawList) ? rawList : [];

      if (labelNombre) {
        labelNombre.textContent = esEmpresa ? "Nombre de la Empresa" : "Nombre y Apellido";
      }
      if (labelCarreraRubro) {
        labelCarreraRubro.textContent = esEmpresa ? "Rubro" : "Carrera";
      }

      // Opción inicial vacía
      const optDefault = document.createElement("option");
      optDefault.value = "";
      optDefault.textContent = esEmpresa ? "-- Seleccionar rubro --" : "-- Seleccionar carrera --";
      selectCarreraRubro.appendChild(optDefault);

      // Recorrer la lista sin riesgo de error
      listaUsar.forEach((item) => {
        if (!item || item.includes("---")) return; // Omite separadores o nulos

        const opt = document.createElement("option");
        opt.value = item;
        opt.textContent = item;
        selectCarreraRubro.appendChild(opt);
      });

      // Asignar el valor que venía guardado
      if (valorSeleccionado) {
        selectCarreraRubro.value = valorSeleccionado;
      }
    }

      editTipoSelect?.addEventListener("change", (e) => {
        actualizarCamposTipo(e.target.value);
      });

  // Modal para editar
  document.querySelectorAll(".btn-edit-contacto").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();

      const card = btn.closest(".contact-card");
      if (!card) return;

      const data = card.dataset;
      const id = data.id;

      if (formEdit) formEdit.action = `/panel_user/contactos/editar/${id}/`;
      if (formDesactivar) formDesactivar.action = `/panel_user/contactos/desactivar/${id}/`;

      const tipo = data.tipo || "miembro";
      if (editTipoSelect) editTipoSelect.value = tipo;

      actualizarCamposTipo(tipo, cleanValue(data.carrera));

      const editNombre = document.getElementById("edit-nombre");
      const editArea = document.getElementById("edit-area");
      const editTelefono = document.getElementById("edit-telefono");
      const editEmail = document.getElementById("edit-email");

      if (editNombre) editNombre.value = cleanValue(data.nombre);
      if (editArea) editArea.value = cleanValue(data.area); // 👈 Asigna el área guardada
      if (editTelefono) editTelefono.value = cleanValue(data.telefono);
      if (editEmail) editEmail.value = cleanValue(data.email);

      if (archivoContainer) {
        if (data.archivo) {
          let fullPath = data.archivoNombre || data.archivo;
          let fileName = fullPath.split('/').pop();

          archivoContainer.innerHTML = `
            <a href="${data.archivo}" target="_blank" rel="noopener noreferrer" class="file-link">
              <i class="fa-solid fa-paperclip"></i>
              <span>${fileName}</span>
            </a>
          `;
        } else {
          archivoContainer.innerHTML = `<span class="text-muted">Sin archivo adjunto</span>`;
        }
      }

      modalEdit?.classList.add("is-open");
    });
  });

  //Modal para vista general
  cards.forEach((card) => {
    card.addEventListener("click", (e) => {
      if (e.target.closest(".btn-edit-contacto")) return;

      const data = card.dataset;

      const viewNombre = document.getElementById("view-nombre");
      const viewEmail = document.getElementById("view-email");
      const viewTelefono = document.getElementById("view-telefono");
      const viewCarrera = document.getElementById("view-carrera");
      const viewArea = document.getElementById("view-area");
      const viewCreado = document.getElementById("view-creado");
      const labelCarrera = document.getElementById("label-carrera-rubro");
      const badge = document.getElementById("view-tipo-badge");
      const viewArchivoContainer = document.getElementById("view-archivo-container");

      if (viewNombre) viewNombre.textContent = cleanValue(data.nombre);
      if (viewEmail) viewEmail.textContent = cleanValue(data.email) || "-";
      if (viewTelefono) viewTelefono.textContent = cleanValue(data.telefono) || "-";
      if (viewCarrera) viewCarrera.textContent = cleanValue(data.carrera) || "-";
      if (viewArea) viewArea.textContent = cleanValue(data.area) || "-";
      if (viewCreado) viewCreado.textContent = cleanValue(data.creado) || "-";

      if (labelCarrera) {
        labelCarrera.textContent = data.tipo === "empresa" ? "Rubro" : "Carrera";
      }

      if (badge) {
        badge.textContent = data.tipoDisplay || (data.tipo === 'empresa' ? 'Empresa' : 'Miembro');
        badge.className = `badge ${data.tipo === 'empresa' ? 'badge--empresa' : 'badge--miembro'}`;
      }

      if (viewArchivoContainer) {
        if (data.archivo) {
          let fullPath = data.archivoNombre || data.archivo;
          let fileName = fullPath.split('/').pop();

          viewArchivoContainer.innerHTML = `
            <a href="${data.archivo}" target="_blank" rel="noopener noreferrer" class="file-link">
              <i class="fa-solid fa-paperclip"></i>
              <span>${fileName}</span>
            </a>
          `;
        } else {
          viewArchivoContainer.innerHTML = `<span class="text-muted">Sin archivo adjunto</span>`;
        }
      }

      modalView?.classList.add("is-open");
    });
  });

  // Cierres
  closeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      modalEdit?.classList.remove("is-open");
      modalView?.classList.remove("is-open");
    });
  });

  // Cerrar al hacer clic en el fondo borroso (fuera del cuadro)
  document.querySelectorAll(".modal-overlay").forEach((overlay) => {
    overlay.addEventListener("click", (e) => {
      if (e.target === e.currentTarget) {
        overlay.classList.remove("is-open");
      }
    });
  });

  btnDesactivar?.addEventListener("click", () => {
    if (confirm("¿Estás seguro de que deseas desactivar este contacto? Ya no se mostrará en la lista activa.")) {
      formDesactivar?.submit();
    }
  });
});