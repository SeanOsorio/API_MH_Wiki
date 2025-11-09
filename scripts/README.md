# 📁 Scripts de Utilidad

Esta carpeta contiene scripts auxiliares que no son parte del core de la aplicación.

## 🛠️ Setup Scripts (`setup/`)

Scripts para configuración inicial y mantenimiento de la base de datos:

### `create_admin.py`
Crea un usuario administrador en la base de datos.
```bash
python scripts/setup/create_admin.py
```
- **Cuándo usar**: Primera vez que configuras el proyecto o necesitas crear otro admin
- **Credenciales default**: admin / qwertyuiop+

### `migrate_users_table.py`
Crea la tabla de usuarios en PostgreSQL.
```bash
python scripts/setup/migrate_users_table.py
```
- **Cuándo usar**: Si la tabla `users` no existe en la BD
- **Nota**: Ya ejecutado en producción

### `seed_database.py`
Puebla la base de datos con armas de Monster Hunter.
```bash
python scripts/setup/seed_database.py
```
- **Cuándo usar**: Para cargar datos de ejemplo de categorías y armas
- **Nota**: Ya ejecutado en producción

### `create_sequences.py`
Crea secuencias de PostgreSQL para IDs autoincrementales.
```bash
python scripts/setup/create_sequences.py
```
- **Cuándo usar**: Si hay problemas con IDs autoincrementales

### `upload_real_images.py`
Sube imágenes de armas a la base de datos.
```bash
python scripts/setup/upload_real_images.py
```
- **Cuándo usar**: Para cargar imágenes de armas desde archivos locales

### `clear_database.py`
Limpia todas las tablas de la base de datos.
```bash
python scripts/setup/clear_database.py
```
- **⚠️ PELIGRO**: Elimina todos los datos
- **Cuándo usar**: Para resetear la BD completamente

---

## 🧪 Testing Scripts (`testing/`)

Scripts para pruebas y debugging:

### `test_auth.py`
Suite completa de pruebas de autenticación.
```bash
python scripts/testing/test_auth.py
```
- **Qué prueba**: Login, registro, permisos, CAPTCHA, JWT tokens
- **Requiere**: Servidor corriendo en http://127.0.0.1:5000

### `test_connection.py`
Verifica conexión a PostgreSQL y tablas.
```bash
python scripts/testing/test_connection.py
```
- **Qué prueba**: Conexión a Railway, versión de PostgreSQL, tablas creadas
- **Útil para**: Debugging de problemas de conexión

---

## 📝 Notas Importantes

1. **Todos los scripts deben ejecutarse desde la raíz del proyecto**
2. **Requieren archivo `.env` configurado** con credenciales de Railway
3. **Los scripts de setup son idempotentes** (se pueden ejecutar múltiples veces)
4. **Backup antes de usar `clear_database.py`** ⚠️

---

## 🚀 Orden Recomendado para Setup Inicial

```bash
# 1. Probar conexión
python scripts/testing/test_connection.py

# 2. Crear tabla de usuarios (si no existe)
python scripts/setup/migrate_users_table.py

# 3. Crear secuencias (si es necesario)
python scripts/setup/create_sequences.py

# 4. Crear admin
python scripts/setup/create_admin.py

# 5. Poblar con datos de Monster Hunter
python scripts/setup/seed_database.py

# 6. Subir imágenes (opcional)
python scripts/setup/upload_real_images.py

# 7. Probar autenticación
python scripts/testing/test_auth.py
```
