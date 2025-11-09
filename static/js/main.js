// JavaScript principal para MonsterHunterWiki

// Búsqueda en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch(this.value);
            }
        });
    }
    
    // Botones de búsqueda
    const searchButtons = document.querySelectorAll('.search-btn');
    searchButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const input = document.getElementById('searchInput');
            if (input) {
                performSearch(input.value);
            }
        });
    });
});

function performSearch(query) {
    if (query.trim()) {
        console.log('Buscando:', query);
        // Aquí puedes implementar la lógica de búsqueda
        // Por ahora solo hace un log
        alert('Funcionalidad de búsqueda: ' + query);
    }
}

// Animaciones suaves al hacer scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Efecto hover en las cajas de enlaces
document.querySelectorAll('.link-box').forEach(box => {
    box.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px) scale(1.02)';
    });
    
    box.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// Cargar estadísticas desde la API
function loadStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            console.log('Estadísticas cargadas:', data);
            if (data.total_articles) {
                const articleCount = document.getElementById('articleCount');
                if (articleCount) {
                    articleCount.textContent = data.total_articles.toLocaleString('es-ES');
                }
            }
        })
        .catch(error => {
            console.error('Error cargando estadísticas:', error);
        });
}

// Ejecutar al cargar la página
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadStats);
} else {
    loadStats();
}
