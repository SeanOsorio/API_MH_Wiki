# 🌐 Sistema de Internacionalización (i18n)

Sistema de traducción dinámica entre Español e Inglés sin recargar la página.

## 📋 Características

- ✅ Cambio de idioma instantáneo sin reload
- ✅ Persistencia con localStorage
- ✅ Animaciones suaves
- ✅ Notificación toast al cambiar idioma
- ✅ Soporte para HTML dentro de traducciones
- ✅ Compatible con tema claro/oscuro

## 🚀 Cómo Usar

### 1. En Templates HTML

Agrega el atributo `data-i18n` a los elementos que quieres traducir:

```html
<!-- Texto simple -->
<h1 data-i18n="welcome">Bienvenido a MonsterHunterWiki</h1>

<!-- Texto con HTML interno (usa data-i18n-html) -->
<p data-i18n="intro_text_1" data-i18n-html>
    <strong>MonsterHunterWiki</strong> es la mayor enciclopedia...
</p>

<!-- Placeholder de input -->
<input data-i18n-placeholder="search" placeholder="Buscar...">

<!-- Title (tooltip) -->
<button data-i18n-title="close_tooltip" title="Cerrar">X</button>
```

### 2. Agregar Nuevas Traducciones

Edita `static/js/i18n.js` y agrega tus traducciones:

```javascript
const translations = {
    es: {
        'mi_clave': 'Texto en español',
        'otro_texto': 'Otro texto en español'
    },
    en: {
        'mi_clave': 'Text in English',
        'otro_texto': 'Another text in English'
    }
};
```

### 3. Usar en JavaScript

```javascript
// Obtener traducción
const textoTraducido = i18n.t('mi_clave');

// Cambiar idioma programáticamente
changeLanguage('en');

// Escuchar cambios de idioma
window.addEventListener('languageChanged', (e) => {
    console.log('Nuevo idioma:', e.detail.language);
});

// Recargar traducciones después de agregar contenido dinámico
reloadTranslations();
```

## 📁 Archivos del Sistema

- **`static/js/i18n.js`** - Sistema de traducción principal
- **`templates/base.html`** - Selector de idioma en header
- **`static/css/style.css`** - Estilos del selector

## 🎨 Selector de Idioma

El selector aparece en el header superior derecho con:
- 🇪🇸 Español (español - default)
- 🇬🇧 English (inglés)

## 🔧 Configuración

El idioma se guarda en `localStorage` con la clave `'language'`:
- Default: `'es'` (Español)
- Opciones: `'es'` | `'en'`

## 💡 Ejemplos de Uso

### Traducir toda una sección

```html
<div class="section">
    <h2 data-i18n="section_title">Título</h2>
    <p data-i18n="section_text">Descripción...</p>
    <button data-i18n="section_button">Botón</button>
</div>
```

### Contenido dinámico

```javascript
// Después de agregar contenido con AJAX
fetch('/api/data')
    .then(response => response.json())
    .then(data => {
        document.getElementById('content').innerHTML = `
            <h3 data-i18n="dynamic_title">Título</h3>
            <p data-i18n="dynamic_text">Texto</p>
        `;
        
        // Recargar traducciones para el nuevo contenido
        reloadTranslations();
    });
```

## 🎯 Traducciones Disponibles

### Página Principal (index.html)
- `welcome` - Título de bienvenida
- `subtitle` - Subtítulo
- `independent` - Texto independiente
- `intro_text_1-4` - Textos introductorios
- `news` - Noticias
- `weapons`, `monsters`, `armor`, `items` - Enlaces rápidos

### Panel de Administración (test_auth.html)
- `admin_panel` - Título del panel
- `admin_subtitle` - Subtítulo
- `test_login`, `test_register`, etc. - Secciones de prueba
- `btn_test`, `btn_close`, `btn_verify` - Botones
- Mensajes de éxito/error/info

## 🐛 Debugging

Para ver el idioma actual:
```javascript
console.log('Idioma actual:', i18n.currentLang);
console.log('Traducciones ES:', translations.es);
console.log('Traducciones EN:', translations.en);
```

## 📱 Responsive

El selector de idioma se adapta automáticamente a dispositivos móviles y tablets.

## 🎨 Temas

El selector funciona con ambos temas (claro/oscuro) y se adapta automáticamente.

---

**Creado por**: MonsterHunterWiki Team  
**Versión**: 1.0.0  
**Última actualización**: 2025-11-09
