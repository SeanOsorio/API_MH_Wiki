# 🚀 INSTRUCCIONES PARA EL PROFESOR

## ¡Solo necesitas 1 comando!

```bash
python app.py
```

**ESO ES TODO** ✅

---

## ¿Qué va a pasar?

1. 🔍 El sistema verificará las dependencias
2. 📦 Instalará automáticamente lo que falte (Flask, JWT, etc.)
3. 🗄️ Configurará la base de datos SQLite
4. 🏗️ Creará todas las tablas necesarias
5. 🚀 Iniciará el servidor en http://localhost:5000

---

## Probar el sistema

**Opción 1: Navegador**
- Ir a http://localhost:5000 (health check)
- Ir a http://localhost:5000/info (información del sistema)

**Opción 2: Postman (más completo)**
- Importar el archivo: `postman/Parcial1Web_Auth_Collection.json`
- Ejecutar los requests en orden

**Opción 3: Validador automático (en otra terminal)**
- Ejecutar: `python validate_system.py`
- Probará todos los endpoints automáticamente

---

## Lo que incluye este sistema:

✅ **Autenticación JWT completa**
- Registro con validación segura
- Login con tokens de acceso y refresh
- Logout con revocación de tokens
- Protección de endpoints

✅ **Base de datos**
- SQLite configurado automáticamente
- Tablas creadas dinámicamente
- Hash seguro de contraseñas con bcrypt

✅ **API REST**
- 9 endpoints funcionales
- Gestión completa de usuarios
- Sistema de armas/categorías

✅ **Documentación profesional**
- Colección completa de Postman
- Especificación OpenAPI/Swagger
- Tests automáticos incluidos

---

## 🎯 Para la presentación:

1. Ejecutar: `python app.py`
2. Esperar que aparezca: "🎉 ¡SISTEMA INICIADO CORRECTAMENTE!"
3. Mostrar http://localhost:5000 en el navegador
4. Demostrar registro/login en Postman
5. **¡Listo!**

---

**🏆 Proyecto completo funcionando con CERO configuración manual**