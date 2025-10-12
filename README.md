# �️ Parcial1Web - Sistema Completo de Autenticación con Roles

**🎯 Sistema empresarial de autenticación JWT con control granular de roles y permisos**

**¡Solo ejecuta `python app.py` y todo funciona automáticamente!**

API REST desarrollada en Flask que implementa un sistema completo de autenticación con JWT y **sistema avanzado de roles y permisos**, con configuración automática y lista para usar en segundos.

## ⚡ Inicio Ultra-Rápido (30 segundos)

### 🎯 Un solo comando para ejecutar todo:

```bash
python app.py
```

**¡Eso es todo!** El sistema se auto-configura completamente:

- ✅ **Crea automáticamente** el archivo `.env` si no existe
- ✅ **Detecta y configura** la base de datos (PostgreSQL o SQLite local)
- ✅ **Crea todas las tablas** automáticamente (usuarios, roles, tokens, armas, categorías)
- ✅ **Inicializa roles por defecto** (admin, moderator, user)
- ✅ **Crea usuario administrador** (admin/admin123)
- ✅ **Inicia el servidor** Flask en http://localhost:5000
- ✅ **Muestra información completa** de todos los endpoints disponibles

### 📋 Requisitos mínimos:
- Python 3.11+
- Las dependencias se instalan automáticamente con: `pip install -r requirements.txt`

## 🔧 Características Principales

### 🔐 **Sistema de Autenticación Completo**
- **🚀 Auto-configuración completa** - Sin configuración manual necesaria
- **🔐 Registro de usuarios** con validación de email único y contraseñas seguras  
- **🎫 Autenticación JWT** con access tokens (1h) y refresh tokens (30 días)

### 🛡️ **Sistema Avanzado de Roles y Permisos** 
- **👑 Control granular de acceso** basado en roles (RBAC)
- **🎯 Permisos específicos** por endpoint y operación
- **⚙️ Gestión administrativa** completa de usuarios y roles
- **🔒 Decoradores de seguridad** automáticos para endpoints
- **🔒 Hash de contraseñas** con bcrypt para máxima seguridad
- **🗄️ Base de datos inteligente** - PostgreSQL en producción, SQLite en desarrollo
- **🛡️ Gestión de armas y categorías** con endpoints CRUD completos
- **📚 Documentación profesional** - Postman Collection + OpenAPI/Swagger

## 💡 Lo que hace el sistema automáticamente

### 🏗️ **Configuración de entorno:**
- Crea archivo `.env` con valores por defecto seguros
- Carga variables de entorno automáticamente
- Configura JWT con claves seguras

### 🗄️ **Base de datos inteligente:**
1. **Intenta PostgreSQL** primero (si está configurado)
2. **Usa SQLite local** como respaldo automático
3. **Crea todas las tablas** necesarias
4. **Valida conexión** antes de continuar

### 🌐 **Servidor Flask:**
- Inicia automáticamente en puerto 5000
- Modo debug habilitado para desarrollo
- Endpoints listos para usar inmediatamente

## 📖 Endpoints Disponibles

### 🔐 **Autenticación (JWT)**

| Endpoint | Método | Auth | Descripción |
|----------|--------|------|-------------|
| `/auth/register` | POST | ❌ | Registro de nuevo usuario |
| `/auth/login` | POST | ❌ | Login y obtención de tokens |
| `/auth/me` | GET | ✅ | Información del usuario actual |
| `/auth/refresh` | POST | ❌ | Renovar access token |
| `/auth/logout` | POST | ✅ | Cerrar sesión (específico/total) |
| `/auth/revoke-all` | POST | ✅ | Revocar todos los tokens |

### 🛡️ **Gestión de Armas**

| Endpoint | Método | Permisos Requeridos | Descripción |
|----------|--------|--------------------|-------------|
| `/categories` | GET | `category_read` | Listar categorías |
| `/categories` | POST | `category_create` | Crear nueva categoría |
| `/categories/{id}` | PUT | `category_update` | Actualizar categoría |
| `/categories/{id}` | DELETE | `category_delete` | Eliminar categoría |
| `/weapons` | GET | `weapon_read` | Listar armas |
| `/weapons` | POST | `weapon_create` | Crear nueva arma |
| `/weapons/{id}` | PUT | `weapon_update` | Actualizar arma |
| `/weapons/{id}` | DELETE | `weapon_delete` | Eliminar arma |

### 👥 **Gestión de Usuarios y Roles**

| Endpoint | Método | Permisos Requeridos | Descripción |
|----------|--------|--------------------|-------------|
| `/auth/users` | GET | `admin` o `user_management` | Listar todos los usuarios |
| `/auth/users/{id}` | GET | `admin` o propio recurso | Ver perfil específico |
| `/auth/users/{id}/role` | PUT | `admin` | Cambiar rol de usuario |
| `/auth/roles` | GET | `admin` o `role_management` | Listar todos los roles |
| `/auth/roles` | POST | `admin` | Crear nuevo rol |

### 📊 **Sistema**

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Health check de la API |
| `/info` | GET | Información del sistema |

## 🛡️ Roles y Permisos

### **👑 ADMIN (Administrador)**
- **Permisos:** TODOS (incluyendo `admin`)
- **Puede hacer:** Gestionar usuarios, roles, crear/editar/eliminar todo
- **Credenciales por defecto:** admin/admin123

### **👨‍💼 MODERATOR (Moderador)**  
- **Permisos:** `weapon_*`, `category_*` (excepto delete)
- **Puede hacer:** Crear y editar contenido, NO eliminar ni gestionar usuarios
- **Ideal para:** Editores de contenido

### **👤 USER (Usuario)**
- **Permisos:** Solo `*_read`
- **Puede hacer:** Solo leer armas y categorías, ver su propio perfil
- **Ideal para:** Usuarios finales/consumidores

## 🧪 Probar la API Inmediatamente

### **Opción 1: Colección Completa de Postman (Recomendado)**
1. **Importar en Postman:**
   - **Colección de Roles:** `postman/Parcial1Web_Roles_Complete_Collection.json`
   - **Environment:** `postman/Parcial1Web_Roles_Environment.json`
2. **¡Ejecutar flujo completo!** (Login Admin → Crear Usuarios → Test Permisos)

### **Opción 2: Validador Automático de Roles**
```bash
python test_roles_system.py
```
Ejecuta pruebas automáticas completas del sistema de roles y permisos.

### **Opción 3: Validador Original**
```bash
python validate_system.py
```
Validación rápida de funcionamiento básico.

### **Opción 4: Manual con curl**
```bash
# Health check
curl http://localhost:5000/

# Login como admin
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Registrar usuario con rol
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"Password123","role":"user"}'
```

## 📚 Documentación Completa

- **🔧 Guía de Postman**: [`POSTMAN_GUIDE.md`](POSTMAN_GUIDE.md) - Inicio en 2 minutos
- **📖 OpenAPI/Swagger**: [`docs/openapi.yaml`](docs/openapi.yaml) - Documentación interactiva
- **📬 Postman Collection**: [`postman/`](postman/) - Tests listos para usar

## 🔒 Seguridad Implementada

- **🔐 Contraseñas hasheadas** con bcrypt (12 rounds)
- **🎫 Tokens JWT seguros** con expiración automática
- **♻️ Refresh tokens** almacenados en base de datos
- **🛡️ Validación de entrada** en todos los endpoints
- **⚠️ Manejo de errores** completo y seguro
- **🚫 Revocación de tokens** para logout seguro

## 🔧 Configuración Avanzada (Opcional)

### **Para usar PostgreSQL:**
Edita `.env` y descomenta las líneas de PostgreSQL:
```env
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### **Para cambiar configuraciones:**
```env
JWT_SECRET_KEY=tu-clave-super-segura
FLASK_ENV=production  # Para producción
FLASK_DEBUG=False     # Desactivar debug
```

## 📦 Tecnologías Utilizadas

- **Flask** 3.1.2 - Framework web minimalista
- **Flask-JWT-Extended** 4.5.2 - Manejo avanzado de JWT
- **Flask-Bcrypt** 1.0.1 - Hash seguro de contraseñas
- **SQLAlchemy** 2.0.43 - ORM moderno para bases de datos
- **PostgreSQL/SQLite** - Base de datos flexible
- **Python** 3.11+ - Lenguaje de programación

## 🎯 Flujo de Uso Típico

1. **Ejecutar:** `python app.py`
2. **Registrar usuario:** POST `/auth/register`
3. **Hacer login:** POST `/auth/login` (obtiene tokens)
4. **Usar API:** Incluir `Authorization: Bearer {token}` en headers
5. **Refresh token:** POST `/auth/refresh` cuando expire
6. **Logout:** POST `/auth/logout`

## 🛠️ Para Desarrolladores

### **Estructura del proyecto:**
```
📁 Parcial1Web/
├── 🚀 app.py                 # ← EJECUTAR ESTE ARCHIVO
├── 📋 requirements.txt       # Dependencias
├── 🔧 config/               # Configuración DB
├── 🏛️ models/               # Modelos SQLAlchemy  
├── 🎮 controllers/          # Endpoints/rutas
├── ⚙️ services/             # Lógica de negocio
├── 📬 postman/              # Colección Postman
├── 📖 docs/                 # Documentación OpenAPI
└── 🗄️ data/                # Base de datos SQLite local
```

### **Agregar nuevos endpoints:**
1. Crear controller en `controllers/`
2. Registrar blueprint en `app.py`
3. ¡Listo! El sistema los detecta automáticamente

## 🎉 ¡Y eso es todo!

**Con un solo `python app.py` tienes:**
- ✅ Sistema completo de autenticación JWT
- ✅ Base de datos auto-configurada  
- ✅ API REST lista para usar
- ✅ Documentación profesional
- ✅ Tests automáticos incluidos

**¡Sin configuración, sin complicaciones, solo ejecutar y usar!** 🚀