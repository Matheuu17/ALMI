# ALMI CRM 🚀

Un sistema de gestión de relaciones con clientes (CRM) y tablero Kanban de actividades desarrollado en Django.

## 🛠️ Tecnologías
* **Backend:** Django (Python)
* **Base de Datos:** PostgreSQL (Neon)
* **Almacenamiento de Archivos:** Cloudinary
* **Frontend:** HTML5, CSS3 (CSS Variables y Flexbox/Grid) y Vanilla JS
* **Despliegue:** Render

## ✨ Características Principales
* **Gestión de Contactos:** Registro de Empresas y Miembros con soporte para subida de documentos y *Soft Delete* (desactivación sin borrado físico).
* **Tablero Kanban Kanban:** Seguimiento visual de actividades (Pendiente, En Proceso, Completada).
* **Asignación Múltiple:** Capacidad de asignar varios contactos a una misma actividad.
* **Panel Administrativo:** Interfaz exclusiva para administrar usuarios del sistema, resetear contraseñas (DNI por defecto) y gestionar roles.
* **Diseño Responsivo:** Interfaz adaptada para dispositivos móviles y escritorio.

## 🚀 Instalación Local (Desarrollo)
1. Clona este repositorio.
2. Crea un entorno virtual: `python -m venv .venv`
3. Activa el entorno virtual y ejecuta: `pip install -r requirements.txt`
4. Realiza las migraciones: `python manage.py migrate`
5. Levanta el servidor: `python manage.py runserver`
