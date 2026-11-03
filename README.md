# ALMI 🚀 — CRM & Kanban Operativo

> Sistema integral de gestión de relaciones con contactos (CRM) y tablero Kanban de actividades desarrollado en **Django**, diseñado para centralizar la administración de empresas y miembros, la trazabilidad de reuniones y el control riguroso de accesos y roles internos.

## 📖 Sobre el Proyecto

**ALMI** es una plataforma web creada para optimizar el flujo de trabajo organizativo y la gestión de relaciones institucionales. Permite registrar y clasificar de forma dinámica tanto a miembros individuales como a empresas aliadas, coordinar actividades mediante un tablero interactivo tipo Kanban y gestionar de manera segura a los colaboradores del equipo mediante un sistema personalizado de autenticación y auditoría.

---

## ✨ Características Principales

* **Seguridad y Acceso Asignado:** Asignación inicial de contraseñas basada en el DNI del usuario y obligatoriedad de cambio de contraseña en el primer inicio de sesión.
* **Directorio de Contactos con *Soft Delete*:** Clasificación por distintivos de color (*Miembro* vs. *Empresa*), filtros rápidos, búsqueda en tiempo real y desactivación lógica sin pérdida física de datos.
* **Subida y Visualización de Documentos:** Almacenamiento dinámico de archivos adjuntos (DNI escaneado, constancias, PDFs e imágenes) respaldado en Cloudinary con visualizador en modal interactivo.
* **Tablero Kanban de Actividades:** Flujo visual de tareas (*Pendiente*, *En Proceso*, *Completada*), control de enlaces virtuales (Zoom), duración estimada y trazabilidad de notas de acuerdos.
* **Asignación Múltiple:** Capacidad de asignar uno o múltiples colaboradores y contactos a una misma actividad.
* **Panel de Administración Dedicado:** Control exclusivo para dar de alta usuarios con roles operativos (*Usuario del Panel*, *Coordinador de Audiovisual*, etc.), correos institucionales (`@thdh.club` / `@hunters.club`) y reseteo de claves.

---

## 🧩 Módulos del Sistema

### 1. `Base` (Núcleo y Seguridad)
* Modelos transversales, lógica de auditoría (*"Registrado por..."*) y persistencia base.
* Middleware de control de sesiones y restricción de navegación para usuarios que no han completado el cambio de contraseña inicial.

### 2. `PanelAdmin` (Control de Usuarios y Roles)
* Registro y configuración de perfiles internos (DNI, Teléfono, Cargo, Rol y Correo institucional).
* Gestión de permisos y reestablecimiento asistido de credenciales (DNI por defecto).

### 3. `PanelUser` (Operativa, Contactos y Agenda)
* **Cabecera Persistente:** Muestra permanentemente el nombre del colaborador autenticado y su cargo vigente.
* **Directorio:** Gestión de miembros (carrera universitaria, área/TTI) y empresas (rubro comercial), con carga de documentos adjuntos.
* **Kanban & Agenda:** Planificación de reuniones con enlaces directos, actualización de estados de ciclo de vida y edición rápida de notas mediante modales.

---

## 🛠️ Stack Tecnológico

* **Backend:** Python 3.10+, Django Framework
* **Base de Datos:** PostgreSQL en la nube ([Neon](https://neon.tech/)) / SQLite para pruebas rápidas
* **Almacenamiento Multimedia:** [Cloudinary](https://cloudinary.com/) (imágenes, PDFs y documentos)
* **Frontend:** HTML5 semántico, CSS3 nativo (Variables CSS, Flexbox, CSS Grid) y JavaScript modular (Vanilla JS)
* **Plataforma de Despliegue:** [Render](https://render.com/)

---

## 📂 Estructura del Proyecto

```text
ALMI/
├── Base/                    # Núcleo del sistema, middleware y modelos base
│   ├── migrations/
│   ├── static/css/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── middleware.py        # Validación obligatoria de primer login
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── PanelAdmin/              # Gestión de usuarios internos, roles y reseteo de claves
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── PanelUser/               # Contactos (Soft Delete), carga documental y tablero Kanban
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── config/                  # Ajustes centrales de Django
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── main.py                  # Punto de entrada / utilitario
├── manage.py                # Gestor de comandos CLI de Django
└── requirements.txt         # Lista de dependencias del proyecto
```

---

## 🚀 Instalación Local y Configuración

### 1. Clonar el repositorio
```bash
git clone [https://github.com/Matheuu17/ALMI.git](https://github.com/Matheuu17/ALMI.git)
cd ALMI
```

### 2. Crear y activar el entorno virtual
```bash
# En Windows:
python -m venv .venv
.venv\Scripts\activate

# En macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto tomando como plantilla:

```env
SECRET_KEY=tu-clave-secreta-de-desarrollo
DEBUG=True

# Base de datos (Neon / PostgreSQL o local)
DATABASE_URL=postgresql://usuario:password@ep-ejemplo.us-east-2.aws.neon.tech/almi_db?sslmode=require

# Configuración de Cloudinary
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

### 5. Aplicar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear el Administrador Principal
```bash
python manage.py createsuperuser
```

### 7. Iniciar el servidor de desarrollo
```bash
python manage.py runserver
```

Ingresa desde tu navegador a: **`http://127.0.0.1:8000/`**

---

## ☁️ Despliegue y Variables de Entorno

Para el despliegue en **Render** (o servicios similares):
1. Configura el comando de compilación (*Build Command*):
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
   ```
2. Configura el comando de arranque (*Start Command*):
   ```bash
   gunicorn config.wsgi:application
   ```
3. Registra en el panel de control las variables `DATABASE_URL`, `SECRET_KEY`, `DEBUG=False` y las credenciales de `CLOUDINARY_*`.

---

## 👥 Diseño y Créditos

* **@Lucero Cubas & Me.** 
