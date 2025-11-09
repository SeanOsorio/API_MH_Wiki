# 🔐 Sistema de Autenticación - MonsterHunterWiki v2.1.0

## ✨ Características Implementadas

### 🎯 Funcionalidades del Usuario

1. **Registro de Cuenta**
   - Username mínimo 3 caracteres
   - Email válido requerido
   - Contraseña mínimo 6 caracteres
   - Confirmación de contraseña
   - Validación en tiempo real

2. **Inicio de Sesión**
   - Login con username o email
   - Tokens JWT con 24 horas de expiración
   - Sesión persistente (localStorage)
   - Auto-login al recargar página

3. **Gestión de Sesión**
   - Panel de usuario en esquina superior derecha
   - Indicador de rol (Usuario/Admin)
   - Botón de cerrar sesión
   - Estado actualizado en toda la aplicación

### 👑 Funcionalidades de Administrador

- Badge especial "👑 ADMIN" en panel de usuario
- Acceso a panel de administración
- Visualización de código fuente (próximamente con CAPTCHA)
- Gestión de usuarios (próximamente)

## 🎮 Cómo Usar

### Para Usuarios Nuevos:

1. **Abrir la Aplicación**
   - Visita: http://127.0.0.1:5000
   - Busca el enlace "acceder/crear cuenta" en la parte superior

2. **Crear Cuenta**
   - Haz clic en "acceder/crear cuenta"
   - Selecciona la pestaña "Crear Cuenta"
   - Completa el formulario:
     - Username (mínimo 3 caracteres)
     - Email
     - Contraseña (mínimo 6 caracteres)
     - Confirmar contraseña
   - Haz clic en "Crear Cuenta"
   - ¡Listo! Serás redirigido al login

3. **Iniciar Sesión**
   - Ingresa tu username o email
   - Ingresa tu contraseña
   - Haz clic en "Iniciar Sesión"
   - Verás tu panel de usuario en la esquina superior derecha

4. **Cerrar Sesión**
   - Haz clic en tu panel de usuario
   - Presiona "🚪 Cerrar Sesión"
   - Confirma la acción

### Para Administradores:

**Usuario Admin Pre-creado:**
- **Username:** admin
- **Email:** seanosoriorojas@gmail.com
- **Password:** qwertyuiop+

**Acceso Especial:**
- Panel de administración (botón ⚙️)
- Ver código fuente (requiere CAPTCHA)
- Gestión de usuarios
- Cambio de roles

## 🛠️ Tecnologías Utilizadas

### Backend:
- **Flask 3.1.2** - Framework web
- **PyJWT 2.8.0** - Tokens JWT para autenticación
- **Flask-Bcrypt 1.0.1** - Hash de contraseñas
- **SQLAlchemy 2.0.23** - ORM para base de datos
- **PostgreSQL** - Base de datos en Railway

### Frontend:
- **Vanilla JavaScript** - Sistema de autenticación
- **CSS3** - Estilos responsive con tema Monster Hunter
- **LocalStorage API** - Persistencia de tokens

## 📁 Estructura de Archivos

```
Parcial1Web/
├── models/
│   └── user_model.py              # Modelo de Usuario con roles
├── repositories/
│   └── user_repository.py         # CRUD de usuarios
├── services/
│   ├── auth_service.py            # Lógica de autenticación JWT
│   └── captcha_service.py         # Sistema CAPTCHA
├── controllers/
│   └── auth_controller.py         # Endpoints REST de autenticación
├── templates/
│   ├── base.html                  # Template base (actualizado)
│   └── auth_modal.html            # Modal de login/registro
├── static/
│   ├── css/
│   │   └── auth.css               # Estilos de autenticación
│   └── js/
│       └── auth.js                # Sistema de autenticación frontend
├── create_admin.py                # Script para crear admins
└── migrate_users_table.py         # Migración de base de datos
```

## 🔒 Seguridad

### Implementado:
- ✅ Contraseñas hasheadas con bcrypt (cost factor 12)
- ✅ Tokens JWT con firma HMAC-SHA256
- ✅ Expiración de tokens (24 horas)
- ✅ Validación de roles en backend
- ✅ Protección contra SQL injection (SQLAlchemy ORM)
- ✅ Validación de entrada en frontend y backend
- ✅ Headers HTTP seguros

### Recomendaciones para Producción:
- 🔄 Implementar refresh tokens
- 🔄 Agregar rate limiting
- 🔄 Usar HTTPS obligatorio
- 🔄 Implementar logout (blacklist de tokens)
- 🔄 Agregar verificación de email
- 🔄 Sistema de recuperación de contraseña
- 🔄 Protección CSRF
- 🔄 Mover CAPTCHA storage a Redis

## 🎨 Temas Compatibles

El sistema de autenticación es totalmente compatible con los temas Monster Hunter:

- **🌞 Light Theme** - Tema claro estilo Wilds
- **🌙 Dark Theme** - Tema oscuro estilo Wilds

Los modales y formularios se adaptan automáticamente al tema seleccionado.

## 📝 API Endpoints

### Públicos:
- `POST /api/auth/register` - Registrar nuevo usuario
- `POST /api/auth/login` - Iniciar sesión (retorna JWT)

### Protegidos (requieren token):
- `GET /api/auth/me` - Obtener perfil del usuario actual
- `POST /api/auth/captcha` - Generar CAPTCHA
- `POST /api/auth/captcha/verify` - Verificar CAPTCHA

### Solo Administradores:
- `GET /api/auth/users` - Listar todos los usuarios
- `PUT /api/auth/users/{id}/role` - Cambiar rol de usuario
- `POST /api/auth/source` - Ver código fuente (requiere CAPTCHA)
- `GET /api/auth/source/files` - Listar archivos disponibles

## 🐛 Solución de Problemas

### El botón no abre el modal:
- Verifica que `auth.js` esté cargando correctamente
- Abre la consola del navegador (F12) y busca errores
- Asegúrate de que el servidor esté corriendo

### No puedo iniciar sesión:
- Verifica las credenciales
- Revisa la consola del navegador para errores de red
- Asegúrate de que el servidor backend esté respondiendo

### El token expiró:
- Los tokens duran 24 horas
- Cierra sesión y vuelve a iniciar sesión
- Tu sesión se limpiará automáticamente si el token es inválido

### No veo el panel de usuario:
- Asegúrate de haber iniciado sesión correctamente
- Revisa que `auth.css` esté cargando
- Recarga la página (Ctrl + F5)

## 🚀 Próximas Mejoras

- [ ] Panel de administración completo
- [ ] Visualización de código con CAPTCHA
- [ ] Sistema de permisos granulares
- [ ] Historial de actividad de usuarios
- [ ] Recuperación de contraseña por email
- [ ] Verificación de email al registrarse
- [ ] OAuth2 (Google, Discord)
- [ ] Two-Factor Authentication (2FA)
- [ ] Notificaciones en tiempo real

## 📞 Contacto

**Desarrollador:** Sean Osorio Rojas  
**Email:** seanosoriorojas@gmail.com  
**Versión:** 2.1.0  
**Última Actualización:** Noviembre 8, 2025

---

¡Feliz caza, Hunter! 🎮⚔️
