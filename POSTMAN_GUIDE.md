# 🚀 Guía de Uso Rápido - Colección Postman & OpenAPI

## 📦 ¿Qué incluye este paquete?

✅ **Colección completa de Postman** con 7 endpoints  
✅ **Variables de entorno** preconfiguradas  
✅ **Tests automáticos** integrados en Postman  
✅ **Documentación OpenAPI/Swagger** completa  
✅ **Validador de colección** programático  

---

## 🏃‍♂️ Inicio rápido (2 minutos)

### 1. 🔥 Iniciar la API
```bash
cd "c:\Users\seano\Documents\ProyectosPython\Parcial1Web - copia"
python app.py
```
*La API debe estar ejecutándose en http://localhost:5000*

### 2. 📬 Importar en Postman
1. **Abrir Postman**
2. **Import** → Seleccionar `postman/Parcial1Web_Auth_Collection.json`
3. **Settings** ⚙️ → **Import** → `postman/Parcial1Web_Auth_Environment.json`
4. **Seleccionar environment**: "Parcial1Web - Autenticación (Local)"

### 3. 🎯 Probar flujo completo
Ejecutar en orden:
1. `01 - Registro de Usuario`
2. `02 - Login de Usuario` *(guarda tokens automáticamente)*
3. `03 - Obtener Usuario Actual`
4. `04 - Refresh Token`
5. `05 - Logout Específico` o `06 - Logout Total`

---

## 📖 Documentación interactiva

### Option A: Swagger Editor Online
1. Ir a [editor.swagger.io](https://editor.swagger.io/)
2. Copiar contenido de `docs/openapi.yaml`
3. Pegar en el editor

### Option B: VS Code (recomendado)
1. Instalar extensión **"Swagger Viewer"**
2. Abrir `docs/openapi.yaml` en VS Code
3. `Ctrl+Shift+P` → "Preview Swagger"

---

## 🧪 Validación automática

```bash
# Probar que todo funciona (requiere API ejecutándose)
python postman/test_collection.py
```

**Output esperado si todo está bien:**
```
🎯 Resultado: 7/7 pruebas pasaron
🎉 ¡Todas las pruebas pasaron!
```

---

## 📋 Lista de endpoints incluidos

| Endpoint | Método | Autenticación | Descripción |
|----------|--------|---------------|-------------|
| `/auth/register` | POST | ❌ | Registro de usuario nuevo |
| `/auth/login` | POST | ❌ | Login con JWT tokens |
| `/auth/me` | GET | ✅ JWT | Info usuario actual |
| `/auth/refresh` | POST | ❌ | Renovar access token |
| `/auth/logout` | POST | ✅ JWT | Logout específico/total |
| `/auth/revoke-all` | POST | ✅ JWT | Revocar todos los tokens |

---

## ⚡ Variables automáticas

Las siguientes variables se gestionan automáticamente:

- **`access_token`**: Se guarda tras login/refresh
- **`refresh_token`**: Se guarda tras login  
- **`base_url`**: Preconfigurada para localhost:5000

---

## 🏆 Puntos adicionales implementados

### ✨ Colección Postman profesional
- 7 endpoints completos con documentación
- Tests automáticos en cada request
- Gestión automática de tokens JWT
- Variables de entorno preconfiguradas
- Scripts pre-request y post-request

### 📚 Documentación OpenAPI 3.0
- Especificación completa con ejemplos
- Esquemas de request/response detallados
- Descripción de seguridad JWT
- Compatible con Swagger UI/Editor

### 🔧 Herramientas adicionales
- Validador programático de la colección
- README completo con instrucciones
- Guía de solución de problemas
- Scripts de prueba automatizados

---

## 🆘 Solución de problemas comunes

### ❌ "API no responde"
```bash
# Verificar que la API esté ejecutándose
python app.py
```

### ❌ "Token inválido"  
- Ejecutar `02 - Login de Usuario` nuevamente
- Los access tokens duran 1 hora

### ❌ "Refresh token expirado"
- Ejecutar login completo
- Los refresh tokens duran 30 días

### ❌ "Variables no encontradas"
- Verificar que el environment esté seleccionado
- Importar `Parcial1Web_Auth_Environment.json`

---

## 🎉 ¡Listo para usar!

Con esta configuración tienes:
- ✅ **Sistema de autenticación completo** probado
- ✅ **Colección Postman profesional** lista para demo
- ✅ **Documentación OpenAPI** para integración  
- ✅ **Tests automáticos** para validación continua

**¡Happy testing!** 🚀