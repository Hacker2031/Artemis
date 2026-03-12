// ============================================================
// ARTEMIS ERP - Utilidades Globais
// ============================================================

// ------------- Dark Mode Global (localStorage) -------------
(function() {
    const DARK_KEY = 'artemis_dark_mode';

    function applyDarkMode(on) {
        if (on) {
            document.body.classList.add('dark-mode-variables');
        } else {
            document.body.classList.remove('dark-mode-variables');
        }
        // sincroniza ícones
        const light = document.querySelector('.dark-mode span:nth-child(1)');
        const dark  = document.querySelector('.dark-mode span:nth-child(2)');
        if (light && dark) {
            if (on) {
                light.classList.remove('active');
                dark.classList.add('active');
            } else {
                light.classList.add('active');
                dark.classList.remove('active');
            }
        }
    }

    // Aplica logo que a página carrega
    const saved = localStorage.getItem(DARK_KEY) === 'true';
    document.addEventListener('DOMContentLoaded', function() {
        applyDarkMode(saved);

        const btn = document.querySelector('.dark-mode');
        if (btn) {
            btn.addEventListener('click', function() {
                const isDark = document.body.classList.contains('dark-mode-variables');
                localStorage.setItem(DARK_KEY, String(!isDark));
                applyDarkMode(!isDark);
            });
        }
    });
})();

// ------------- Marcar link ativo no sidebar -------------
document.addEventListener('DOMContentLoaded', function() {
    const current = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.sidebar a').forEach(link => {
        const href = link.getAttribute('href');
        if (href === current) {
            link.classList.add('active');
        }
    });
});
