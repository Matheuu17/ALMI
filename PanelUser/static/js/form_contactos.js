/*toggle del formulario de Agregar Contacto según tipo de contacto*/
document.addEventListener("DOMContentLoaded", () => {
  const tipoSelect = document.getElementById("tipo_contacto");
  const labelNombre = document.getElementById("label-nombre");
  const labelCarreraRubro = document.getElementById("label-carrera-rubro");
  const carreraRubroSelect = document.getElementById("carrera_rubro");

  const carreras = JSON.parse(document.getElementById("carreras-data")?.textContent || "[]");
  const rubros = JSON.parse(document.getElementById("rubros-data")?.textContent || "[]");

  function fillOptions(select, options) {
    select.innerHTML = "";
    options.forEach((opt) => {
      const option = document.createElement("option");
      option.value = opt;
      option.textContent = opt;
      select.appendChild(option);
    });
  }

  function updateForm() {
    const esEmpresa = tipoSelect.value === "empresa";

    labelNombre.textContent = esEmpresa ? "Nombre de empresa" : "Nombre y Apellido";
    labelCarreraRubro.textContent = esEmpresa ? "Rubro" : "Carrera";

    fillOptions(carreraRubroSelect, esEmpresa ? rubros : carreras);
  }

  tipoSelect?.addEventListener("change", updateForm);
  updateForm();
});