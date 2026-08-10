document.addEventListener("DOMContentLoaded", () => {
  // ==========================================
  // 1. MANEJO DE MODALES (VER / EDITAR)
  // ==========================================
  const modalView = document.getElementById("modal-view-actividad");
  const modalEdit = document.getElementById("modal-edit-actividad");
  const closeBtns = document.querySelectorAll(".btn-close-modal, .js-close-modal");
  const formEdit = document.getElementById("form-edit-actividad");


  // Abrir modal Ver Detalle
  document.querySelectorAll(".activity-card").forEach((card) => {
    card.addEventListener("click", (e) => {
      if (e.target.closest(".activity-card__actions")) return;

      const data = card.dataset;

      const viewResumen = document.getElementById("view-resumen");
      const viewTipoBadge = document.getElementById("view-tipo-badge");
      const viewEstado = document.getElementById("view-estado");
      const viewFecha = document.getElementById("view-fecha");
      const viewAsignado = document.getElementById("view-asignado");
      const viewCreador = document.getElementById("view-creador");
      const viewNotas = document.getElementById("view-notas");

      if (viewResumen) viewResumen.textContent = data.resumen || "Sin asunto";
      if (viewTipoBadge) viewTipoBadge.textContent = data.tipo || "Actividad";
      if (viewEstado) viewEstado.textContent = data.estado || "-";
      if (viewFecha) viewFecha.textContent = data.fecha || "-";
      if (viewAsignado) viewAsignado.textContent = data.asignado || "Sin asignar";
      if (viewCreador) viewCreador.textContent = data.creador || "-";

      if (viewNotas) {
        const notasTexto = (data.notas || "").trim();
        viewNotas.textContent = notasTexto.length > 0 ? notasTexto : "Sin notas adicionales.";
      }

      modalView?.classList.add("is-open");
    });
  });

  // Abrir modal Editar (Lápiz)
  document.querySelectorAll(".btn-edit-actividad").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();

      const card = btn.closest(".activity-card");
      if (!card) return;

      const data = card.dataset;
      const id = data.id;

      if (formEdit) {
        formEdit.action = `/panel_user/actividades/editar/${id}/`;
      }

      const inputResumen = document.getElementById("edit-resumen");
      const selectTipo = document.getElementById("edit-tipo");
      const selectEstado = document.getElementById("edit-estado");
      const inputFecha = document.getElementById("edit-fecha");
      const textareaNotas = document.getElementById("edit-notas");

      if (inputResumen) inputResumen.value = data.resumen || "";
      if (selectTipo) selectTipo.value = data.tipoKey || "";
      if (selectEstado) selectEstado.value = data.estadoKey || "pendiente";
      if (inputFecha) inputFecha.value = data.fechaIso || "";
      if (textareaNotas) textareaNotas.value = data.notas || "";

      // Carga de chips asignados al editar
      if (window.editChipsManager) {
        const rawIds = data.asignadoIds || "";
        const selectedIds = rawIds
          ? rawIds.split(",").map((i) => parseInt(i.trim(), 10)).filter(Boolean)
          : [];
        window.editChipsManager.setSelectedIds(selectedIds);
      }

      modalEdit?.classList.add("is-open");
    });
  });

  // Cierre de modales (tanto botón X como botón Cancelar)
  closeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      modalView?.classList.remove("is-open");
      modalEdit?.classList.remove("is-open");
    });
  });

  // Cierre al hacer clic en el fondo oscuro
  document.querySelectorAll(".modal-overlay").forEach((overlay) => {
    overlay.addEventListener("click", (e) => {
      if (e.target === e.currentTarget) {
        overlay.classList.remove("is-open");
      }
    });
  });

  // ==========================================
  // 2. COMPONENTE BUSCADOR DE CHIPS (REUTILIZABLE)
  // ==========================================
  function initChipsInput(prefix = "") {
    const containerId = prefix ? `${prefix}-chips-container` : "chips-container";
    const searchInputId = prefix ? `${prefix}-contact-search-input` : "contact-search-input";
    const dropdownId = prefix ? `${prefix}-contact-suggestions` : "contact-suggestions";
    const chipsListId = prefix ? `${prefix}-chips-list` : "chips-list";
    const hiddenInputsId = prefix ? `${prefix}-hidden-inputs-container` : "hidden-inputs-container";

    const container = document.getElementById(containerId);
    const searchInput = document.getElementById(searchInputId);
    const suggestionsDropdown = document.getElementById(dropdownId);
    const chipsList = document.getElementById(chipsListId);
    const hiddenInputsContainer = document.getElementById(hiddenInputsId);

    if (!container || !searchInput || !suggestionsDropdown) return null;

    const allContacts = window.CONTACTOS_DATA || [];
    let selectedIds = new Set();

    container.addEventListener("click", () => searchInput.focus());

    function renderChips() {
      chipsList.innerHTML = "";
      hiddenInputsContainer.innerHTML = "";

      selectedIds.forEach((id) => {
        const contact = allContacts.find((c) => c.id == id);
        if (!contact) return;

        const chip = document.createElement("div");
        chip.className = "chip";
        chip.innerHTML = `
          <span>${contact.nombre}</span>
          <button type="button" class="chip__remove" data-id="${contact.id}">&times;</button>
        `;
        chipsList.appendChild(chip);

        const hiddenInput = document.createElement("input");
        hiddenInput.type = "hidden";
        hiddenInput.name = "asignado_a";
        hiddenInput.value = contact.id;
        hiddenInputsContainer.appendChild(hiddenInput);
      });
    }

    function renderSuggestions(filterText = "") {
      suggestionsDropdown.innerHTML = "";
      const filter = (filterText || "").toLowerCase().trim();

      const matches = allContacts.filter((c) => {
        if (selectedIds.has(c.id)) return false;
        const nombreMatch = (c.nombre || "").toLowerCase().includes(filter);
        const emailMatch = (c.email || "").toLowerCase().includes(filter);
        return nombreMatch || emailMatch;
      });

      if (matches.length === 0) {
        suggestionsDropdown.classList.remove("is-active");
        return;
      }

      matches.forEach((c) => {
        const item = document.createElement("div");
        item.className = "suggestion-item";
        const inicial = (c.nombre && c.nombre.length > 0) ? c.nombre.charAt(0).toUpperCase() : "?";

        item.innerHTML = `
          <div class="suggestion-avatar">${inicial}</div>
          <div class="suggestion-info">
            <span class="suggestion-name">${c.nombre || 'Sin nombre'}</span>
            <span class="suggestion-email">${c.email || 'Sin correo'}</span>
          </div>
        `;

        item.addEventListener("mousedown", (e) => {
          e.preventDefault();
          selectedIds.add(c.id);
          renderChips();
          searchInput.value = "";
          suggestionsDropdown.classList.remove("is-active");
          searchInput.focus();
        });

        suggestionsDropdown.appendChild(item);
      });

      suggestionsDropdown.classList.add("is-active");
    }

    searchInput.addEventListener("focus", () => renderSuggestions(searchInput.value));
    searchInput.addEventListener("input", (e) => renderSuggestions(e.target.value));

    chipsList.addEventListener("click", (e) => {
      if (e.target.classList.contains("chip__remove")) {
        e.stopPropagation();
        const id = parseInt(e.target.dataset.id, 10);
        selectedIds.delete(id);
        renderChips();
      }
    });

    document.addEventListener("click", (e) => {
      if (!container.contains(e.target) && !suggestionsDropdown.contains(e.target)) {
        suggestionsDropdown.classList.remove("is-active");
      }
    });

    return {
      setSelectedIds: (idsArray) => {
        selectedIds = new Set(idsArray);
        renderChips();
      }
    };
  }

  // Inicializar buscador en vista de creación
  initChipsInput("");

  // Inicializar buscador en modal de edición
  window.editChipsManager = initChipsInput("edit");
});