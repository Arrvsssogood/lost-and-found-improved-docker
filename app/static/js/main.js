// Finders Keepers — Main JS

// Mobile nav toggle
const navToggle = document.getElementById('navToggle');
const navLinks = document.querySelector('.nav-links');

if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('open');
    });
}

// Auto-dismiss flash messages after 4 seconds
document.querySelectorAll('.flash').forEach(flash => {
    setTimeout(() => {
        flash.style.opacity = '0';
        flash.style.transform = 'translateX(40px)';
        flash.style.transition = 'all 0.4s ease';
        setTimeout(() => flash.remove(), 400);
    }, 4000);
});
