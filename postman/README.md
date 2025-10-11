# 📬 Colección de Postman - Sistema de Autenticación

Esta carpeta contiene los archivos necesarios para probar completamente el sistema de autenticación implementado en la API Parcial1Web.

## 📋 Archivos incluidos

### 🔧 Postman Collection
- **`Parcial1Web_Auth_Collection.json`** - Colección completa con todos los endpoints
- **`Parcial1Web_Auth_Environment.json`** - Variables de entorno preconfiguradas

### 📖 Documentación
- **`../docs/openapi.yaml`** - Especificación OpenAPI/Swagger completa

## 🚀 Configuración rápida

### 1. Importar en Postman

1. **Abrir Postman**
2. **Importar Colección:**
   - Click en "Import" 
   - Seleccionar `Parcial1Web_Auth_Collection.json`
   - Click "Import"

3. **Importar Environment:**
   - Click en el icono de engranaje (⚙️) en la esquina superior derecha
   - Click "Import"
   - Seleccionar `Parcial1Web_Auth_Environment.json`
   - Click "Import"

4. **Activar Environment:**
   - Seleccionar "Parcial1Web - Autenticación (Local)" en el dropdown de environments

### 2. Configurar variables

Asegúrate de que estas variables estén configuradas en tu environment:

| Variable | Valor por defecto | Descripción |
|----------|------------------|-------------|
| `base_url` | `http://localhost:5000` | URL de tu API Flask |
| `test_email` | `test@example.com` | Email para pruebas |
| `test_password` | `TestPassword123` | Contraseña para pruebas |
| `access_token` | *(automático)* | Se establece tras login |
| `refresh_token` | *(automático)* | Se establece tras login |

## 🎯 Flujo de pruebas recomendado

### 1. **Registro de Usuario** 
```http
POST /auth/register
```
- Registra un nuevo usuario
- Valida email único y contraseña fuerte
- ✅ **Status esperado:** 201

### 2. **Login**
```http
POST /auth/login  
```
- Autentica al usuario
- Obtiene access_token y refresh_token
- ⚡ **Los tokens se guardan automáticamente**
- ✅ **Status esperado:** 200

### 3. **Obtener Usuario Actual**
```http
GET /auth/me
```
- Prueba que el access_token funciona
- Muestra información del usuario autenticado
- ✅ **Status esperado:** 200

### 4. **Refresh Token**
```http
POST /auth/refresh
```
- Renueva el access_token
- Prueba el sistema de refresh
- ⚡ **El nuevo token se guarda automáticamente**
- ✅ **Status esperado:** 200

### 5. **Logout Específico**
```http
POST /auth/logout (con refresh_token en body)
```
- Revoca un refresh_token específico
- Simula logout de un dispositivo
- ✅ **Status esperado:** 200

### 6. **Logout Total**
```http
POST /auth/logout (sin refresh_token en body)
```
- Revoca TODOS los tokens del usuario
- Simula logout de todos los dispositivos
- 🧹 **Limpia tokens automáticamente**
- ✅ **Status esperado:** 200

### 7. **Revocar Todos los Tokens**
```http
POST /auth/revoke-all
```
- Endpoint dedicado para revocar todos los tokens
- Útil para casos de seguridad
- ✅ **Status esperado:** 200

## 🔍 Features de la colección

### ✨ Tests automatizados
Cada request incluye tests que verifican:
- Status codes correctos
- Estructura de respuesta esperada  
- Presencia de campos obligatorios
- Guardado automático de tokens

### 🔄 Gestión automática de tokens
- **Login**: Guarda access_token y refresh_token automáticamente
- **Refresh**: Actualiza el access_token automáticamente
- **Logout/Revoke**: Limpia tokens automáticamente

### 📊 Logging detallado
- Log de cada request/response
- Verificación de errores 5xx
- Mensajes informativos en consola

### 🛡️ Validaciones de seguridad
- Verificación de tokens JWT válidos
- Tests de autenticación obligatoria
- Validación de respuestas de error

## 🌐 Documentación Swagger/OpenAPI

Para una documentación interactiva, puedes usar el archivo `../docs/openapi.yaml`:

### Opción 1: Swagger Editor online
1. Ir a [editor.swagger.io](https://editor.swagger.io/)
2. Copiar el contenido de `../docs/openapi.yaml`  
3. Pegar en el editor

### Opción 2: Swagger UI local
```bash
# Instalar swagger-ui-serve
npm install -g swagger-ui-serve

# Servir la documentación
swagger-ui-serve ../docs/openapi.yaml
```

### Opción 3: VS Code con extensión
1. Instalar extensión "Swagger Viewer"
2. Abrir `../docs/openapi.yaml`
3. Usar `Shift+Alt+P` → "Preview Swagger"

## 🔧 Solución de problemas

### ❌ Error de conexión
- **Problema**: `Error: connect ECONNREFUSED`
- **Solución**: Verificar que la API Flask esté ejecutándose en `http://localhost:5000`

### ❌ Token inválido
- **Problema**: `401 Unauthorized` 
- **Solución**: Ejecutar login nuevamente para obtener tokens frescos

### ❌ Refresh token expirado
- **Problema**: `401` en refresh
- **Solución**: Ejecutar login completo (los refresh tokens duran 30 días)

### ❌ Variables no configuradas
- **Problema**: `base_url` undefined
- **Solución**: Verificar que el environment esté seleccionado y variables configuradas

## 📈 Métricas de la colección

- **7 endpoints** completamente probados
- **25+ tests automatizados** incluidos  
- **Variables automáticas** para flujo completo
- **100% cobertura** del sistema de autenticación
- **Documentación completa** OpenAPI 3.0

## 🎉 ¡Listo para probar!

Con esta configuración puedes:
1. ✅ Probar todos los endpoints de autenticación
2. ✅ Validar el flujo completo de usuario
3. ✅ Verificar la seguridad JWT
4. ✅ Documentar la API profesionalmente
5. ✅ Automatizar pruebas de integración

**¡Happy testing!** 🚀