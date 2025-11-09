/**
 * auth.js - Sistema de Autenticación para MonsterHunterWiki
 * Maneja login, registro, tokens JWT y estado de usuario
 */

// Configuración de la API
const API_BASE_URL = '/api/auth';

// Estado de autenticación
let authState = {
    token: localStorage.getItem('mh_token'),
    user: null,
    isAuthenticated: false
};

/**
 * Inicialización del sistema de autenticación
 */
document.addEventListener('DOMContentLoaded', function() {
    initAuthSystem();
    checkAuthStatus();
});

/**
 * Inicializa todos los event listeners del sistema de autenticación
 */
function initAuthSystem() {
    // Botón de acceder/crear cuenta - buscar de múltiples formas
    const loginLinks = document.querySelectorAll('.top-nav a');
    let loginLink = null;
    
    loginLinks.forEach(link => {
        if (link.textContent.includes('acceder') || link.textContent.includes('crear cuenta')) {
            loginLink = link;
        }
    });
    
    if (loginLink) {
        loginLink.href = '#';
        loginLink.addEventListener('click', (e) => {
            e.preventDefault();
            openAuthModal();
            console.log('Modal abierto desde el enlace');
        });
        console.log('Sistema de autenticación inicializado correctamente');
    } else {
        console.error('No se encontró el enlace de acceder/crear cuenta');
    }

    // Cerrar modal
    const closeBtn = document.getElementById('closeAuthModal');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeAuthModal);
    }

    // Cerrar modal al hacer click fuera
    const modal = document.getElementById('authModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeAuthModal();
            }
        });
    }

    // Pestañas de Login/Registro
    const authTabs = document.querySelectorAll('.auth-tab');
    authTabs.forEach(tab => {
        tab.addEventListener('click', () => switchAuthTab(tab.dataset.tab));
    });

    // Formulario de Login
    const loginForm = document.getElementById('loginFormElement');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Formulario de Registro
    const registerForm = document.getElementById('registerFormElement');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }

    // Botón de logout
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }

    // Botón de panel admin
    const adminPanelBtn = document.getElementById('adminPanelBtn');
    if (adminPanelBtn) {
        adminPanelBtn.addEventListener('click', openAdminPanel);
    }
    
    // Botón de minimizar panel
    const minimizeBtn = document.getElementById('minimizePanel');
    if (minimizeBtn) {
        minimizeBtn.addEventListener('click', toggleUserPanel);
    }
    
    // Botón de panel minimizado
    const minimizedBtn = document.getElementById('userPanelMinimized');
    if (minimizedBtn) {
        minimizedBtn.addEventListener('click', toggleUserPanel);
    }
}

/**
 * Verifica el estado de autenticación al cargar la página
 */
async function checkAuthStatus() {
    if (!authState.token) {
        updateUIForGuest();
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/me`, {
            headers: {
                'Authorization': `Bearer ${authState.token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            authState.user = data.user;
            authState.isAuthenticated = true;
            updateUIForAuthenticatedUser();
        } else {
            // Token inválido o expirado
            logout();
        }
    } catch (error) {
        console.error('Error verificando autenticación:', error);
        logout();
    }
}

/**
 * Abre el modal de autenticación
 */
function openAuthModal() {
    const modal = document.getElementById('authModal');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

/**
 * Cierra el modal de autenticación
 */
function closeAuthModal() {
    const modal = document.getElementById('authModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
        clearAuthMessages();
    }
}

/**
 * Cambia entre las pestañas de login y registro
 */
function switchAuthTab(tab) {
    // Actualizar pestañas
    document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
    document.querySelector(`[data-tab="${tab}"]`).classList.add('active');

    // Actualizar formularios
    document.querySelectorAll('.auth-form-container').forEach(f => f.classList.remove('active'));
    document.getElementById(tab === 'login' ? 'loginForm' : 'registerForm').classList.add('active');

    clearAuthMessages();
}

/**
 * Maneja el envío del formulario de login
 */
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value;
    
    if (!username || !password) {
        showAuthMessage('loginMessage', 'Por favor completa todos los campos', 'error');
        return;
    }

    showLoadingButton(e.target);
    clearAuthMessage('loginMessage');

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Login exitoso
            authState.token = data.token;
            authState.user = data.user;
            authState.isAuthenticated = true;
            localStorage.setItem('mh_token', data.token);

            showAuthMessage('loginMessage', '✅ ¡Bienvenido de vuelta!', 'success');
            
            setTimeout(() => {
                closeAuthModal();
                updateUIForAuthenticatedUser();
                e.target.reset();
            }, 1000);
        } else {
            showAuthMessage('loginMessage', data.error || 'Error al iniciar sesión', 'error');
        }
    } catch (error) {
        console.error('Error en login:', error);
        showAuthMessage('loginMessage', 'Error de conexión. Intenta de nuevo.', 'error');
    } finally {
        hideLoadingButton(e.target);
    }
}

/**
 * Maneja el envío del formulario de registro
 */
async function handleRegister(e) {
    e.preventDefault();
    
    const username = document.getElementById('registerUsername').value.trim();
    const email = document.getElementById('registerEmail').value.trim();
    const password = document.getElementById('registerPassword').value;
    const passwordConfirm = document.getElementById('registerPasswordConfirm').value;
    
    // Validaciones básicas
    if (!username || !email || !password || !passwordConfirm) {
        showAuthMessage('registerMessage', 'Por favor completa todos los campos', 'error');
        return;
    }

    if (username.length < 3) {
        showAuthMessage('registerMessage', 'El usuario debe tener al menos 3 caracteres', 'error');
        return;
    }

    if (password.length < 6) {
        showAuthMessage('registerMessage', 'La contraseña debe tener al menos 6 caracteres', 'error');
        return;
    }

    if (password !== passwordConfirm) {
        showAuthMessage('registerMessage', 'Las contraseñas no coinciden', 'error');
        return;
    }

    showLoadingButton(e.target);
    clearAuthMessage('registerMessage');

    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Registro exitoso
            showAuthMessage('registerMessage', 
                '✅ ¡Cuenta creada! Ahora puedes iniciar sesión.', 'success');
            
            setTimeout(() => {
                switchAuthTab('login');
                document.getElementById('loginUsername').value = username;
                e.target.reset();
            }, 2000);
        } else {
            showAuthMessage('registerMessage', data.error || 'Error al crear cuenta', 'error');
        }
    } catch (error) {
        console.error('Error en registro:', error);
        showAuthMessage('registerMessage', 'Error de conexión. Intenta de nuevo.', 'error');
    } finally {
        hideLoadingButton(e.target);
    }
}

/**
 * Maneja el cierre de sesión
 */
function handleLogout() {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        logout();
    }
}

/**
 * Cierra la sesión del usuario
 */
function logout() {
    authState.token = null;
    authState.user = null;
    authState.isAuthenticated = false;
    localStorage.removeItem('mh_token');
    document.body.classList.remove('user-logged-in');
    updateUIForGuest();
}

/**
 * Actualiza la UI para usuario autenticado
 */
function updateUIForAuthenticatedUser() {
    // Ocultar enlace de login
    const loginLink = document.querySelector('.top-nav a');
    const loginLinks = document.querySelectorAll('.top-nav a');
    loginLinks.forEach(link => {
        if (link.textContent.includes('acceder') || link.textContent.includes('crear cuenta')) {
            link.style.display = 'none';
        }
    });

    // Actualizar "no has accedido"
    const topNavLinks = document.querySelectorAll('.top-nav a');
    topNavLinks.forEach(link => {
        if (link.textContent.includes('no has accedido')) {
            link.textContent = authState.user.username;
            link.style.fontWeight = 'bold';
            link.style.color = 'var(--accent-color)';
        }
    });

    // Mostrar panel de usuario en la parte inferior
    const userPanel = document.getElementById('userPanel');
    if (userPanel) {
        userPanel.style.display = 'flex';
        document.getElementById('currentUsername').textContent = authState.user.username;
        document.getElementById('miniUsername').textContent = authState.user.username;
        
        // Agregar clase al body para padding inferior
        document.body.classList.add('user-logged-in');
        
        const roleSpan = document.getElementById('currentUserRole');
        if (authState.user.role === 'admin') {
            roleSpan.textContent = '👑 ADMIN';
            roleSpan.classList.add('admin-role');
            document.getElementById('adminPanelBtn').style.display = 'block';
        } else {
            roleSpan.textContent = '👤 Usuario';
            roleSpan.style.color = '#4A9EFF';
        }
    }

    // Habilitar pestaña "Ver código fuente" si es admin
    if (authState.user.role === 'admin') {
        enableSourceCodeTab();
    }

    console.log('Usuario autenticado:', authState.user);
}

/**
 * Actualiza la UI para usuario invitado
 */
function updateUIForGuest() {
    const loginLinks = document.querySelectorAll('.top-nav a');
    loginLinks.forEach(link => {
        if (link.textContent.includes('acceder') || link.textContent.includes('crear cuenta')) {
            link.style.display = '';
        }
    });

    const topNavLinks = document.querySelectorAll('.top-nav a');
    topNavLinks.forEach(link => {
        if (link.textContent === authState.user?.username) {
            link.textContent = 'no has accedido';
            link.style.fontWeight = 'normal';
            link.style.color = '';
        }
    });

    const userPanel = document.getElementById('userPanel');
    if (userPanel) {
        userPanel.style.display = 'none';
    }
    
    const minimizedPanel = document.getElementById('userPanelMinimized');
    if (minimizedPanel) {
        minimizedPanel.style.display = 'none';
    }

    document.body.classList.remove('user-logged-in');
    disableSourceCodeTab();
}

/**
 * Habilita la pestaña de ver código fuente (solo para admins)
 */
function enableSourceCodeTab() {
    const sourceTab = document.querySelector('.tab[href*="código"]');
    if (sourceTab) {
        sourceTab.style.opacity = '1';
        sourceTab.style.pointerEvents = 'auto';
        sourceTab.addEventListener('click', handleSourceCodeView);
    }
}

/**
 * Deshabilita la pestaña de ver código fuente
 */
function disableSourceCodeTab() {
    const sourceTab = document.querySelector('.tab[href*="código"]');
    if (sourceTab) {
        sourceTab.style.opacity = '0.5';
        sourceTab.style.pointerEvents = 'none';
    }
}

/**
 * Maneja la visualización de código fuente (requiere admin + CAPTCHA)
 */
async function handleSourceCodeView(e) {
    e.preventDefault();
    
    if (!authState.isAuthenticated || authState.user.role !== 'admin') {
        alert('❌ Solo los administradores pueden ver el código fuente');
        return;
    }

    // Aquí implementaremos el flujo de CAPTCHA y visualización de código
    alert('🚧 Función de visualización de código fuente próximamente...');
}

/**
 * Abre el panel de administración
 */
function openAdminPanel() {
    // Redirigir a la página de pruebas/admin
    window.location.href = '/test-auth';
}

/**
 * Alterna entre panel expandido y minimizado
 */
function toggleUserPanel() {
    const panel = document.getElementById('userPanel');
    const minimized = document.getElementById('userPanelMinimized');
    
    if (panel.style.display === 'none') {
        // Expandir
        panel.style.display = 'flex';
        minimized.style.display = 'none';
    } else {
        // Minimizar
        panel.style.display = 'none';
        minimized.style.display = 'block';
        
        // Actualizar nombre en botón minimizado
        document.getElementById('miniUsername').textContent = authState.user.username;
        
        // Agregar clase si es admin
        if (authState.user.role === 'admin') {
            minimized.classList.add('admin-minimized');
        }
    }
}

/**
 * Muestra un mensaje de estado en el formulario
 */
function showAuthMessage(elementId, message, type) {
    const messageElement = document.getElementById(elementId);
    if (messageElement) {
        messageElement.textContent = message;
        messageElement.className = `auth-message ${type}`;
        messageElement.style.display = 'block';
    }
}

/**
 * Limpia los mensajes de error/éxito
 */
function clearAuthMessage(elementId) {
    const messageElement = document.getElementById(elementId);
    if (messageElement) {
        messageElement.textContent = '';
        messageElement.style.display = 'none';
    }
}

/**
 * Limpia todos los mensajes de autenticación
 */
function clearAuthMessages() {
    clearAuthMessage('loginMessage');
    clearAuthMessage('registerMessage');
}

/**
 * Muestra el estado de carga en un botón
 */
function showLoadingButton(form) {
    const button = form.querySelector('button[type="submit"]');
    if (button) {
        button.disabled = true;
        button.querySelector('.btn-text').style.display = 'none';
        button.querySelector('.btn-loading').style.display = 'inline';
    }
}

/**
 * Oculta el estado de carga en un botón
 */
function hideLoadingButton(form) {
    const button = form.querySelector('button[type="submit"]');
    if (button) {
        button.disabled = false;
        button.querySelector('.btn-text').style.display = 'inline';
        button.querySelector('.btn-loading').style.display = 'none';
    }
}

/**
 * Obtiene el token de autenticación actual
 */
function getAuthToken() {
    return authState.token;
}

/**
 * Obtiene el usuario actual
 */
function getCurrentUser() {
    return authState.user;
}

/**
 * Verifica si el usuario es admin
 */
function isAdmin() {
    return authState.isAuthenticated && authState.user && authState.user.role === 'admin';
}

// Exportar funciones para uso global
window.authSystem = {
    getToken: getAuthToken,
    getUser: getCurrentUser,
    isAdmin: isAdmin,
    logout: logout
};
