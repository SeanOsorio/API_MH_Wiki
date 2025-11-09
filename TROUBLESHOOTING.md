# 🔍 GUÍA DE SOLUCIÓN - Sistema de Autenticación

## ✅ Estado Actual del Sistema

### Backend (100% Funcional)
- ✅ API de autenticación funcionando correctamente
- ✅ Login endpoint: `POST /api/auth/login`
- ✅ Register endpoint: `POST /api/auth/register`
- ✅ Tokens JWT generándose correctamente
- ✅ Base de datos PostgreSQL conectada
- ✅ Usuario admin creado y verificado

### Frontend (Implementado)
- ✅ Modal de autenticación creado (`auth_modal.html`)
- ✅ JavaScript de autenticación implementado (`auth.js`)
- ✅ Estilos CSS aplicados (`auth.css`)
- ✅ Integrado en `base.html`

## 🎯 Cómo Probarlo

### Opción 1: Página de Pruebas (RECOMENDADO)
1. **Abre en tu navegador:** http://127.0.0.1:5000/test-auth
2. **Haz clic en "Probar Login de Admin"**
3. **Verás el resultado del test del backend**
4. **Luego haz clic en "Ir a la Página Principal"**
5. **En la página principal, busca el enlace "acceder/crear cuenta"** (esquina superior derecha)
6. **Haz clic y debería abrirse el modal**

### Opción 2: Directo en la Página Principal
1. **Abre:** http://127.0.0.1:5000
2. **Espera a que cargue completamente la página**
3. **Busca en la esquina superior derecha el enlace "acceder/crear cuenta"**
4. **Haz clic en el enlace**
5. **El modal debe aparecer con las pestañas Login/Registro**

### Opción 3: Consola del Navegador (Para Debugging)
1. **Abre:** http://127.0.0.1:5000
2. **Presiona F12 para abrir DevTools**
3. **Ve a la pestaña "Console"**
4. **Busca mensajes como:**
   - "Sistema de autenticación inicializado correctamente"
   - O algún error en rojo
5. **Si ves errores, copia el mensaje para revisarlo**

## 🔧 Troubleshooting

### Si el modal no se abre:

1. **Verifica en la consola del navegador (F12)** si hay errores
2. **Limpia la caché del navegador:** Ctrl + Shift + R
3. **Verifica que los archivos se estén cargando:**
   - En DevTools → Network → busca `auth.js` y `auth.css`
   - Deben aparecer con status 200

### Si el login no funciona:

1. **Verifica que el backend esté corriendo**
2. **Prueba el endpoint directo en la página de test**
3. **Revisa la consola del navegador para errores de red**

### Credenciales de Prueba:

**Usuario Admin:**
```
Username: admin
Password: qwertyuiop+
```

**O crea un usuario nuevo:**
- Username: cualquier_nombre (min 3 caracteres)
- Email: tu@email.com
- Password: cualquier_pass (min 6 caracteres)

## 📱 Lo que deberías ver:

### Cuando funcione correctamente:

1. **Al hacer clic en "acceder/crear cuenta":**
   - Aparece un modal centrado
   - Fondo oscuro semi-transparente
   - Dos pestañas: "Iniciar Sesión" y "Crear Cuenta"

2. **En el formulario de Login:**
   - Campo para usuario o email
   - Campo para contraseña
   - Botón "Iniciar Sesión"

3. **Al iniciar sesión correctamente:**
   - Mensaje de éxito
   - El modal se cierra
   - Aparece un panel de usuario en la esquina superior derecha
   - El enlace "no has accedido" cambia a tu username

4. **Si eres admin:**
   - Badge dorado "👑 ADMIN"
   - Botón "Panel Admin" visible
   - Acceso a funciones especiales

## 🚨 Errores Comunes

### Error: "No se puede conectar al servidor"
- **Solución:** Verifica que `python app.py` esté corriendo
- **Comando:** `python app.py` en una terminal

### Error: "auth.js no se encuentra"
- **Solución:** Verifica la estructura de carpetas
- **Ubicación correcta:** `static/js/auth.js`

### Error: "El modal no aparece"
- **Solución 1:** Limpia caché (Ctrl + Shift + R)
- **Solución 2:** Verifica la consola del navegador (F12)
- **Solución 3:** Abre http://127.0.0.1:5000/test-auth primero

### Error: "401 Unauthorized"
- **Causa:** Token inválido o expirado
- **Solución:** Cierra sesión y vuelve a iniciar sesión

## 📞 Verificación Rápida

Ejecuta en PowerShell:
```powershell
# Test 1: Verificar que el servidor responde
curl http://127.0.0.1:5000/health

# Test 2: Probar login
curl http://127.0.0.1:5000/api/auth/login -Method POST -Headers @{'Content-Type'='application/json'} -Body '{"username":"admin","password":"qwertyuiop+"}'

# Test 3: Abrir navegador en página de test
Start-Process http://127.0.0.1:5000/test-auth
```

## ✅ Checklist de Verificación

- [ ] Servidor corriendo en http://127.0.0.1:5000
- [ ] Página principal carga sin errores
- [ ] Archivo auth.js se carga (verificar en Network tab)
- [ ] Archivo auth.css se carga (verificar en Network tab)
- [ ] Modal aparece al hacer clic en "acceder/crear cuenta"
- [ ] Login funciona con las credenciales de admin
- [ ] Registro crea nuevos usuarios
- [ ] Panel de usuario aparece después del login
- [ ] Botón de logout funciona

---

**Si sigues teniendo problemas:**
1. Abre http://127.0.0.1:5000/test-auth
2. Haz clic en "Probar Login de Admin"
3. Captura el resultado y compártelo
4. Abre F12 en la página principal
5. Captura cualquier error en rojo de la consola
