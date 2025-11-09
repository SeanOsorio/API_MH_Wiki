/**
 * Sistema de Internacionalización (i18n)
 * Traduce la página dinámicamente entre Español e Inglés
 */

const translations = {
    es: {
        // Header y navegación
        'welcome': 'Bienvenido a MonsterHunterWiki',
        'subtitle': 'La enciclopedia Monster Hunter en español',
        'independent': 'Independiente y sin anuncios',
        
        // Secciones principales
        'weapons': 'Armas',
        'monsters': 'Monstruos',
        'armor': 'Armaduras',
        'items': 'Objetos',
        'news': 'Noticias',
        'wiki': 'MonsterHunterWiki',
        
        // Intro
        'intro_text_1': '<strong>MonsterHunterWiki</strong> es la mayor enciclopedia <strong>Monster Hunter</strong> en español, con <strong id="articleCount">...</strong> artículos, que abarca toda la información oficial de los <a href="#">videojuegos</a>, <a href="#">anime</a>, <a href="#">manga</a> y <a href="#">Juego de Cartas Coleccionables</a>.',
        'intro_text_2': 'Tú también puedes <a href="#">colaborar con nosotros</a> corrigiendo o ampliando el contenido. Para información básica sobre cómo editar un wiki, puedes consultar nuestras páginas de <a href="#">ayuda</a>. Si tienes cualquier duda o alguna propuesta interesante que quieras anunciar a los demás usuarios utiliza el <a href="#">foro</a>.',
        'intro_text_3': 'Puedes comunicarte con otros usuarios en tiempo real a través de nuestro servidor de Discord pulsando en este logo:',
        'intro_text_4': 'Síguenos en nuestras cuentas de <a href="#">Mastodon</a>, <a href="#">X</a>, <a href="#">Instagram</a> y <a href="#">MeWe</a>. También puedes usar nuestra <a href="#">aplicación para Android</a>.',
        
        // Panel de administración
        'admin_panel': 'Panel de Administración',
        'admin_subtitle': 'Centro de pruebas de autenticación y gestión de sistema',
        'back_home': '← Volver al Inicio',
        
        // Secciones de prueba
        'test_login': 'Iniciar Sesión',
        'test_login_desc': 'Prueba el inicio de sesión con credenciales de administrador o usuario normal.',
        'test_register': 'Registrar Usuario',
        'test_register_desc': 'Crea un nuevo usuario en el sistema con validación de datos.',
        'test_profile': 'Ver Perfil',
        'test_profile_desc': 'Obtén información del usuario autenticado actual.',
        'test_users': 'Listar Usuarios',
        'test_users_desc': 'Ver todos los usuarios registrados en el sistema (requiere admin).',
        'test_source': 'Ver Código Fuente',
        'test_source_desc': 'Examina el código fuente de archivos del proyecto.',
        'test_files': 'Listar Archivos',
        'test_files_desc': 'Ver todos los archivos disponibles en el proyecto.',
        
        // Botones
        'btn_test': 'Probar',
        'btn_close': 'Cerrar',
        'btn_verify': 'Verificar',
        
        // Logs y resultados
        'activity_log': 'Registro de Actividad',
        'clear_log': 'Limpiar Registro',
        'results': 'Resultados',
        'loading': 'Cargando...',
        'success': '[OK]',
        'error': '[ERROR]',
        'info': '[INFO]',
        
        // CAPTCHA
        'captcha_title': 'Verificación reCAPTCHA',
        'captcha_desc': 'Por favor completa la verificación de seguridad para continuar',
        'captcha_verify': 'Verificar y Continuar',
        
        // Mensajes
        'select_file': 'Selecciona un archivo',
        'no_token': 'No hay token disponible. Por favor, inicia sesión primero.',
        'admin_required': 'Se requieren permisos de administrador',
    },
    
    en: {
        // Header y navegación
        'welcome': 'Welcome to MonsterHunterWiki',
        'subtitle': 'The Monster Hunter encyclopedia in Spanish',
        'independent': 'Independent and ad-free',
        
        // Secciones principales
        'weapons': 'Weapons',
        'monsters': 'Monsters',
        'armor': 'Armor',
        'items': 'Items',
        'news': 'News',
        'wiki': 'MonsterHunterWiki',
        
        // Intro
        'intro_text_1': '<strong>MonsterHunterWiki</strong> is the largest <strong>Monster Hunter</strong> encyclopedia in Spanish, with <strong id="articleCount">...</strong> articles, covering all official information from <a href="#">video games</a>, <a href="#">anime</a>, <a href="#">manga</a> and <a href="#">Trading Card Game</a>.',
        'intro_text_2': 'You can also <a href="#">collaborate with us</a> by correcting or expanding the content. For basic information on how to edit a wiki, you can check our <a href="#">help</a> pages. If you have any questions or interesting proposals to share with other users, use the <a href="#">forum</a>.',
        'intro_text_3': 'You can communicate with other users in real time through our Discord server by clicking this logo:',
        'intro_text_4': 'Follow us on our <a href="#">Mastodon</a>, <a href="#">X</a>, <a href="#">Instagram</a> and <a href="#">MeWe</a> accounts. You can also use our <a href="#">Android app</a>.',
        
        // Panel de administración
        'admin_panel': 'Administration Panel',
        'admin_subtitle': 'Authentication testing and system management center',
        'back_home': '← Back to Home',
        
        // Secciones de prueba
        'test_login': 'Login',
        'test_login_desc': 'Test login with admin or normal user credentials.',
        'test_register': 'Register User',
        'test_register_desc': 'Create a new user in the system with data validation.',
        'test_profile': 'View Profile',
        'test_profile_desc': 'Get information about the current authenticated user.',
        'test_users': 'List Users',
        'test_users_desc': 'View all registered users in the system (requires admin).',
        'test_source': 'View Source Code',
        'test_source_desc': 'Examine the source code of project files.',
        'test_files': 'List Files',
        'test_files_desc': 'View all available files in the project.',
        
        // Botones
        'btn_test': 'Test',
        'btn_close': 'Close',
        'btn_verify': 'Verify',
        
        // Logs y resultados
        'activity_log': 'Activity Log',
        'clear_log': 'Clear Log',
        'results': 'Results',
        'loading': 'Loading...',
        'success': '[OK]',
        'error': '[ERROR]',
        'info': '[INFO]',
        
        // CAPTCHA
        'captcha_title': 'reCAPTCHA Verification',
        'captcha_desc': 'Please complete the security verification to continue',
        'captcha_verify': 'Verify and Continue',
        
        // Mensajes
        'select_file': 'Select a file',
        'no_token': 'No token available. Please login first.',
        'admin_required': 'Administrator permissions required',
    }
};

class I18n {
    constructor() {
        // Cargar idioma guardado o usar español por defecto
        this.currentLang = localStorage.getItem('language') || 'es';
        this.init();
    }
    
    init() {
        // Aplicar idioma guardado al cargar la página
        this.applyTranslations();
        
        // Actualizar selector de idioma si existe
        const langSelector = document.getElementById('language-selector');
        if (langSelector) {
            langSelector.value = this.currentLang;
        }
    }
    
    setLanguage(lang) {
        if (!translations[lang]) {
            console.error(`Language '${lang}' not found`);
            return;
        }
        
        // Agregar clase de transición
        document.body.classList.add('language-changing');
        
        this.currentLang = lang;
        localStorage.setItem('language', lang);
        
        // Aplicar traducciones después de una pequeña pausa para la animación
        setTimeout(() => {
            this.applyTranslations();
            
            // Actualizar atributo lang del HTML
            document.documentElement.lang = lang;
            
            // Remover clase de transición
            setTimeout(() => {
                document.body.classList.remove('language-changing');
            }, 200);
            
            // Disparar evento personalizado para que otros componentes sepan del cambio
            window.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
            
            // Mostrar notificación toast
            this.showLanguageToast(lang);
        }, 100);
    }
    
    applyTranslations() {
        // Traducir todos los elementos con data-i18n
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.translate(key);
            
            if (translation) {
                // Si el elemento tiene data-i18n-html, usar innerHTML
                if (element.hasAttribute('data-i18n-html')) {
                    element.innerHTML = translation;
                } else {
                    element.textContent = translation;
                }
            }
        });
        
        // Traducir placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            const translation = this.translate(key);
            if (translation) {
                element.placeholder = translation;
            }
        });
        
        // Traducir titles (tooltips)
        document.querySelectorAll('[data-i18n-title]').forEach(element => {
            const key = element.getAttribute('data-i18n-title');
            const translation = this.translate(key);
            if (translation) {
                element.title = translation;
            }
        });
    }
    
    translate(key) {
        const lang = translations[this.currentLang];
        return lang[key] || key;
    }
    
    t(key) {
        return this.translate(key);
    }
    
    showLanguageToast(lang) {
        // Crear toast notification
        const toast = document.createElement('div');
        toast.className = 'language-toast';
        toast.textContent = lang === 'es' ? '🇪🇸 Idioma cambiado a Español' : '🇬🇧 Language changed to English';
        
        // Estilos inline para el toast
        Object.assign(toast.style, {
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            background: 'linear-gradient(135deg, #2c5282 0%, #1e3a5f 100%)',
            color: 'white',
            padding: '15px 25px',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
            zIndex: '10000',
            fontSize: '14px',
            fontWeight: '600',
            opacity: '0',
            transform: 'translateY(20px)',
            transition: 'all 0.3s ease'
        });
        
        document.body.appendChild(toast);
        
        // Animar entrada
        setTimeout(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateY(0)';
        }, 10);
        
        // Animar salida y eliminar
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(20px)';
            setTimeout(() => toast.remove(), 300);
        }, 2500);
    }
}

// Crear instancia global
const i18n = new I18n();

// Función global para cambiar idioma
function changeLanguage(lang) {
    i18n.setLanguage(lang);
}

// Recargar traducciones cuando el DOM cambie (útil para contenido dinámico)
function reloadTranslations() {
    i18n.applyTranslations();
}

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { I18n, i18n, changeLanguage, reloadTranslations };
}
