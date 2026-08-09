document.addEventListener("DOMContentLoaded", () => {
  const modalView = document.getElementById("modal-view-actividad");
  const modalEdit = document.getElementById("modal-edit-actividad");
  const closeBtns = document.querySelectorAll(".btn-close-modal");
  const formEdit = document.getElementById("form-edit-actividad");

  // 1. ABRIR MODAL VISTA DETALLE
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

  // 2. ABRIR MODAL EDITAR (LÁPIZ)
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

      // Selección múltiple de contactos asignados
      const asignadoSelect = document.getElementById("edit-asignado");
      if (asignadoSelect) {
        const selectedIds = data.asignadoIds ? data.asignadoIds.split(",") : [];
        Array.from(asignadoSelect.options).forEach((opt) => {
          opt.selected = selectedIds.includes(opt.value);
        });
      }

      modalEdit?.classList.add("is-open");
    });
  });

  // 3. CIERRE DE MODALES
  closeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      modalView?.classList.remove("is-open");
      modalEdit?.classList.remove("is-open");
    });
  });

  // 4. CIERRE AL HACER CLIC EN EL BLUR (FONDO)
  document.querySelectorAll(".modal-overlay").forEach((overlay) => {
    overlay.addEventListener("click", (e) => {
      if (e.target === e.currentTarget) {
        overlay.classList.remove("is-open");
      }
    });
  });
});