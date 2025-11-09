# 🎮 MonsterHunterWiki

<div align="center">

![Version](https://img.shields.io/badge/Version-2.0.0-orange?style=for-the-badge)
![Monster Hunter](https://img.shields.io/badge/Monster%20Hunter-Wilds%20Edition-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1.2-black?style=for-the-badge&logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.6-blue?style=for-the-badge&logo=postgresql)
![Railway](https://img.shields.io/badge/Railway-Deployed-purple?style=for-the-badge&logo=railway)

**La enciclopedia Monster Hunter en español - WikiDex Style con Monster Hunter Wilds Theme**

[Ver Demo](#) • [Reportar Bug](https://github.com/SeanOsorio/ClassApi/issues) • [Solicitar Feature](https://github.com/SeanOsorio/ClassApi/issues)

</div>

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [🆕 Novedades v2.0.0](#-novedades-v200)
- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [API Endpoints](#-api-endpoints)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Despliegue](#-despliegue)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)
- [Autor](#-autor)

---

## 🎯 Descripción

**MonsterHunterWiki** es una enciclopedia web completa sobre Monster Hunter, inspirada en WikiDex pero enfocada en el universo de Monster Hunter. El proyecto incluye:

- 🌐 **Frontend** estilo WikiDex con diseño moderno y responsive
- 🎨 **Sistema de Temas** Monster Hunter Wilds con modo día/noche
- 🔌 **API REST** completa para gestionar contenido
- 🗄️ **Base de datos PostgreSQL** en Railway
- ⚔️ **Navegación jerárquica** de tres niveles para explorar armas

---

## � Novedades v2.0.0

### �🎨 Monster Hunter Wilds Theme System
- **Modo Diurno/Nocturno**: Toggle dinámico con paleta oficial de MH Wilds
  - Colores naranja difuminado: `#c0821a` → `#e0b054`
  - Colores verde tierra: `#b08e36` → `#97b78d`
  - Fondos oscuros atmosféricos en modo nocturno
  - Persistencia de preferencia con localStorage
- **CSS Variables System**: Sistema completo de variables CSS para theming
- **Smooth Transitions**: Animaciones fluidas entre temas

### 🎮 WikiDex-Style Navigation
- **Tres Niveles de Navegación**:
  1. `/weapons` - Grid de categorías con conteo de armas
  2. `/weapons/category/{id}` - Tabla estilo WikiDex con lista de armas
  3. `/weapons/{id}` - Vista detallada de arma con stats
- **Breadcrumbs**: Navegación clara de jerarquía
- **Responsive Design**: Optimizado para todos los dispositivos

### 🗃️ PostgreSQL Migration Complete
- ✅ Migración completa de MongoDB a PostgreSQL
- ✅ 14 categorías de armas + 32 armas pobladas
- ✅ Relaciones de claves foráneas correctamente implementadas
- ✅ SQLAlchemy ORM con auto-incremento nativo

---

## ✨ Características

### Frontend (Wiki)
- ✅ Página de inicio estilo WikiDex
- ✅ Navegación lateral con menús interactivos
- ✅ Sección de armas con filtros y búsqueda
- ✅ Diseño responsive para móviles y tablets
- ✅ Animaciones y transiciones suaves
- ✅ Estadísticas en tiempo real

### Backend (API REST)
- ✅ CRUD completo para categorías de armas
- ✅ CRUD completo para armas específicas
- ✅ Validaciones de integridad referencial
- ✅ IDs independientes por tabla
- ✅ Manejo robusto de errores HTTP
- ✅ Documentación de endpoints

### Base de Datos
- ✅ PostgreSQL en Railway (producción)
- ✅ Auto-incremento nativo de PostgreSQL
- ✅ Relaciones de claves foráneas
- ✅ Migraciones automáticas
- ✅ Pool de conexiones optimizado

---

## 🛠️ Tecnologías

### Backend
- **Python 3.11** - Lenguaje de programación
- **Flask 3.1.2** - Framework web
- **SQLAlchemy 2.0.23** - ORM para base de datos
- **psycopg2-binary 2.9.9** - Driver de PostgreSQL
- **python-dotenv** - Gestión de variables de entorno

### Frontend
- **HTML5** - Estructura
- **CSS3** - Estilos con gradientes y animaciones
- **JavaScript (Vanilla)** - Interactividad
- **Google Fonts (Roboto)** - Tipografía

### Base de Datos
- **PostgreSQL 17.6** - Base de datos relacional
- **Railway** - Hosting de base de datos

### Infraestructura
- **Railway** - Despliegue y hosting
- **Git/GitHub** - Control de versiones

---

## 📦 Instalación

### Prerrequisitos

```bash
Python 3.11+
pip (gestor de paquetes de Python)
Git
```

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/SeanOsorio/ClassApi.git
cd ClassApi
```

### Paso 2: Crear entorno virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# PostgreSQL Configuration - Railway
DBUSER=postgres
DBPASSWORD=tu_password
DBHOST=tramway.proxy.rlwy.net
DBPORT=42753
DBNAME=railway
```

### Paso 5: Inicializar la base de datos

```bash
python test_connection.py  # Probar conexión
python seed_database.py     # Poblar con datos de ejemplo
```

### Paso 6: Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://127.0.0.1:5000`

---

## 🚀 Uso

### Acceder a la Wiki

1. Abre tu navegador en `http://127.0.0.1:5000`
2. Explora las secciones:
   - **Inicio**: Bienvenida y noticias
   - **Armas**: Categorías y armas específicas
   - **Monstruos**: (Próximamente)
   - **Objetos**: (Próximamente)
   - **Armaduras**: (Próximamente)

### Usar la API

#### Listar todas las categorías
```bash
curl http://127.0.0.1:5000/categories
```

#### Crear una nueva categoría
```bash
curl -X POST http://127.0.0.1:5000/categories \
  -H "Content-Type: application/json" \
  -d '{"name":"Great Sword","description":"Arma pesada"}'
```

#### Listar todas las armas
```bash
curl http://127.0.0.1:5000/weapons
```

#### Crear una nueva arma
```bash
curl -X POST http://127.0.0.1:5000/weapons \
  -H "Content-Type: application/json" \
  -d '{"name":"Rathalos Sword","category_id":1,"description":"Espada de Rathalos"}'
```

---

## 🔌 API Endpoints

### Categorías de Armas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/categories` | Listar todas las categorías |
| POST | `/categories` | Crear nueva categoría |
| GET | `/categories/{id}` | Obtener categoría por ID |
| PUT | `/categories/{id}` | Actualizar categoría |
| DELETE | `/categories/{id}` | Eliminar categoría |
| GET | `/categories/{id}/weapons` | Armas de una categoría |

### Armas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/weapons` | Listar todas las armas |
| POST | `/weapons` | Crear nueva arma |
| GET | `/weapons/{id}` | Obtener arma por ID |
| PUT | `/weapons/{id}` | Actualizar arma |
| DELETE | `/weapons/{id}` | Eliminar arma |

### Otros

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Página de inicio |
| GET | `/weapons` | Página de armas |
| GET | `/api/stats` | Estadísticas de la wiki |
| GET | `/health` | Health check |

---

## 📁 Estructura del Proyecto

```
ClassApi/
├── 📁 config/              # Configuración
│   ├── __init__.py
│   └── database.py         # Conexión a PostgreSQL
├── 📁 controllers/         # Controladores (rutas)
│   ├── __init__.py
│   └── weapons_controller.py
├── 📁 models/              # Modelos de datos
│   ├── __init__.py
│   └── weapons_model.py    # WeaponCategory, Weapon
├── 📁 repositories/        # Capa de acceso a datos
│   ├── __init__.py
│   ├── weapon_category_repository.py
│   └── weapon_repository.py
├── 📁 services/            # Lógica de negocio
│   ├── __init__.py
│   └── weapons_service.py
├── 📁 static/              # Archivos estáticos
│   ├── 📁 css/
│   │   └── style.css       # Estilos principales
│   ├── 📁 js/
│   │   └── main.js         # JavaScript principal
│   └── 📁 images/          # Imágenes y assets
├── 📁 templates/           # Templates HTML
│   ├── base.html           # Template base
│   ├── index.html          # Página de inicio
│   ├── weapons.html        # Página de armas
│   └── coming_soon.html    # Páginas en desarrollo
├── 📁 test/                # Tests
│   └── test_database.py
├── .env                    # Variables de entorno
├── .gitignore             # Archivos ignorados por Git
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias Python
├── seed_database.py       # Script para poblar DB
├── test_connection.py     # Test de conexión
├── LICENSE                # Licencia MIT
└── README.md              # Este archivo
```

---

## 🌐 Despliegue

### Railway (Base de Datos)

La base de datos ya está desplegada en Railway:
- Host: `tramway.proxy.rlwy.net`
- Puerto: `42753`
- Base de datos: `railway`

### Desplegar la Aplicación

#### Opción 1: Railway

1. Crea un nuevo proyecto en [Railway](https://railway.app)
2. Conecta tu repositorio de GitHub
3. Añade las variables de entorno desde el panel
4. Railway desplegará automáticamente

#### Opción 2: Heroku

```bash
heroku create monsterhunterwiki
heroku config:set DBUSER=postgres DBPASSWORD=xxx DBHOST=xxx DBPORT=xxx DBNAME=railway
git push heroku main
```

#### Opción 3: Vercel

```bash
vercel
# Configura las variables de entorno en el dashboard
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Áreas para Contribuir

- 🐲 **Monstruos**: Sistema completo de monstruos
- 🛡️ **Armaduras**: Catálogo de armaduras
- 💎 **Objetos**: Base de datos de objetos
- 🎯 **Misiones**: Sistema de misiones
- 📱 **Responsive**: Mejorar diseño móvil
- 🌍 **i18n**: Soporte multiidioma
- 🔍 **Búsqueda**: Motor de búsqueda avanzado

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

**Sean Osorio**

- GitHub: [@SeanOsorio](https://github.com/SeanOsorio)
- Repositorio: [ClassApi](https://github.com/SeanOsorio/ClassApi)

---

## 🙏 Agradecimientos

- Inspirado en [WikiDex](https://www.wikidex.net)
- Datos de Monster Hunter: Capcom
- Comunidad de Monster Hunter

---

## 📊 Estadísticas del Proyecto

```
📦 14 Categorías de Armas
🗡️ 32+ Armas Específicas
🎮 100% Funcional
💚 PostgreSQL en Railway
```

---

<div align="center">

### ⭐ ¡Si te gusta este proyecto, dale una estrella en GitHub! ⭐

**Hecho con ❤️ y Python**

</div>
