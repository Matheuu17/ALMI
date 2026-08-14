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

// Array global para acumular los IDs de los archivos marcados para borrar en el modal de edición
let archivosAEliminar = [];

// Función expuesta globalmente para eliminar un chip de archivo en el Modal de Edición
window.marcarArchivoEliminar = function(archId) {
  if (!archivosAEliminar.includes(archId)) {
    archivosAEliminar.push(archId);
  }

  // Actualizar el campo oculto con los IDs separados por coma (ej: "1,4,9")
  const hiddenEliminar = document.getElementById("edit-archivos-eliminar");
  if (hiddenEliminar) hiddenEliminar.value = archivosAEliminar.join(",");

  // Remover visualmente el chip de la pantalla
  const chip = document.getElementById(`chip-file-${archId}`);
  if (chip) chip.remove();

  // Si ya no quedan más chips, mostrar el mensaje de advertencia
  const editArchivosList = document.getElementById("edit-archivos-list");
  const editNoFileText = document.getElementById("edit-no-file-text");
  if (editArchivosList && editArchivosList.children.length === 0 && editNoFileText) {
    editNoFileText.textContent = "Archivos marcados para eliminar al guardar.";
    editNoFileText.style.display = "block";
  }
};

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

  // --- 1. BUSCADOR Y FILTROS ---
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

  // --- 2. REFERENCIAS A ELEMENTOS DE MODALES ---
  const modalEdit = document.getElementById("modal-edit-contacto");
  const modalView = document.getElementById("modal-view-contacto");
  const closeBtns = document.querySelectorAll(".btn-close-modal");

  const formEdit = document.getElementById("form-edit-contacto");
  const formDesactivar = document.getElementById("form-desactivar-contacto");
  const btnDesactivar = document.getElementById("btn-desactivar-contacto");
  const editTipoSelect = document.getElementById("edit-tipo");

  // --- 3. SELECTOR DINÁMICO DE CARRERA / RUBRO ---
  function actualizarCamposTipo(tipo, valorSeleccionado = "") {
    const labelNombre = document.getElementById("edit-label-nombre");
    const labelCarreraRubro = document.getElementById("edit-label-carrera-rubro");
    const selectCarreraRubro = document.getElementById("edit-carrera-rubro");

    if (!selectCarreraRubro) return;

    selectCarreraRubro.innerHTML = "";

    const esEmpresa = tipo === "empresa";
    const rawList = esEmpresa ? RUBROS_LIST : CARRERAS_LIST;
    const listaUsar = Array.isArray(rawList) ? rawList : [];

    if (labelNombre) {
      labelNombre.textContent = esEmpresa ? "Nombre de la Empresa" : "Nombre y Apellido";
    }
    if (labelCarreraRubro) {
      labelCarreraRubro.textContent = esEmpresa ? "Rubro" : "Carrera";
    }

    const optDefault = document.createElement("option");
    optDefault.value = "";
    optDefault.textContent = esEmpresa ? "-- Seleccionar rubro --" : "-- Seleccionar carrera --";
    selectCarreraRubro.appendChild(optDefault);

    listaUsar.forEach((item) => {
      if (!item || item.includes("---")) return;

      const opt = document.createElement("option");
      opt.value = item;
      opt.textContent = item;
      selectCarreraRubro.appendChild(opt);
    });

    if (valorSeleccionado) {
      selectCarreraRubro.value = valorSeleccionado;
    }
  }

  editTipoSelect?.addEventListener("change", (e) => {
    actualizarCamposTipo(e.target.value);
  });

  // --- 4. ABRIR MODAL PARA EDITAR ---
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

      // Llenar campos de texto
      const editNombre = document.getElementById("edit-nombre");
      const editArea = document.getElementById("edit-area");
      const editTelefono = document.getElementById("edit-telefono");
      const editEmail = document.getElementById("edit-email");

      if (editNombre) editNombre.value = cleanValue(data.nombre);
      if (editArea) editArea.value = cleanValue(data.area);
      if (editTelefono) editTelefono.value = cleanValue(data.telefono);
      if (editEmail) editEmail.value = cleanValue(data.email);

      // Resetear input de subida nueva y array de eliminados
      const inputFiles = document.getElementById("edit-archivos-input");
      if (inputFiles) inputFiles.value = "";

      archivosAEliminar = [];
      const hiddenEliminar = document.getElementById("edit-archivos-eliminar");
      if (hiddenEliminar) hiddenEliminar.value = "";

      // Parsear y renderizar chips de archivos acumulados
      const editArchivosList = document.getElementById("edit-archivos-list");
      const editNoFileText = document.getElementById("edit-no-file-text");

      let archivos = [];
      try {
        archivos = JSON.parse(data.archivos || "[]");
      } catch (err) {
        archivos = [];
      }

      if (editArchivosList) editArchivosList.innerHTML = "";

      if (archivos.length > 0) {
        if (editNoFileText) editNoFileText.style.display = "none";
        archivos.forEach((arch) => {
          const chip = document.createElement("div");
          chip.className = "file-chip-wrapper";
          chip.id = `chip-file-${arch.id}`;
          chip.innerHTML = `
            <a href="${arch.url}" target="_blank" rel="noopener noreferrer" class="file-chip__link">
              <i class="fa-solid fa-paperclip"></i>
              <span>${arch.nombre}</span>
            </a>
            <button type="button" class="file-chip__btn-delete" title="Eliminar archivo" onclick="marcarArchivoEliminar(${arch.id})">&times;</button>
          `;
          editArchivosList.appendChild(chip);
        });
      } else {
        if (editNoFileText) {
          editNoFileText.textContent = "Sin archivos adjuntos";
          editNoFileText.style.display = "block";
        }
      }

      modalEdit?.classList.add("is-open");
    });
  });

  // --- 5. ABRIR MODAL DE DETALLE (VISTA GENERAL) ---
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
        badge.textContent = data.tipoDisplay || (data.tipo === "empresa" ? "Empresa" : "Miembro");
        badge.className = `badge ${data.tipo === "empresa" ? "badge--empresa" : "badge--miembro"}`;
      }

      // Parsear y renderizar chips de archivos en vista de detalle
      let archivos = [];
      try {
        archivos = JSON.parse(data.archivos || "[]");
      } catch (err) {
        archivos = [];
      }

      if (viewArchivoContainer) {
        viewArchivoContainer.innerHTML = "";
        if (archivos.length > 0) {
          archivos.forEach((arch) => {
            const chip = document.createElement("div");
            chip.className = "file-chip-wrapper";
            chip.innerHTML = `
              <a href="${arch.url}" target="_blank" rel="noopener noreferrer" class="file-chip__link">
                <i class="fa-solid fa-paperclip"></i>
                <span>${arch.nombre}</span>
              </a>
            `;
            viewArchivoContainer.appendChild(chip);
          });
        } else {
          viewArchivoContainer.innerHTML = `<span class="text-muted">Sin archivos adjuntos</span>`;
        }
      }

      modalView?.classList.add("is-open");
    });
  });

  // --- 6. CIERRE DE MODALES ---
  closeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      modalEdit?.classList.remove("is-open");
      modalView?.classList.remove("is-open");
    });
  });

  document.querySelectorAll(".modal-overlay").forEach((overlay) => {
    overlay.addEventListener("click", (e) => {
      if (e.target === e.currentTarget) {
        overlay.classList.remove("is-open");
      }
    });
  });

  // --- 7. BOTÓN DESACTIVAR CONTACTO ---
  btnDesactivar?.addEventListener("click", () => {
    if (confirm("¿Estás seguro de que deseas desactivar este contacto? Ya no se mostrará en la lista activa.")) {
      formDesactivar?.submit();
    }
  });
});