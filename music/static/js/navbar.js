// ============================================================
// 1. ПОДСВЕТКА ИКОНОК В НАВБАРЕ
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    var indicator = document.querySelector('.glow-indicator');
    var navIcons = document.querySelectorAll('.nav-icon');
    
    var activeIcon = document.querySelector('.nav-icon.active');
    if (activeIcon && indicator) {
        indicator.style.left = (activeIcon.offsetLeft + activeIcon.offsetWidth/2 - 27) + 'px';
    }
    navIcons.forEach(function(icon) {
        icon.addEventListener('click', function() {
            navIcons.forEach(function(i) { i.classList.remove('active'); });
            this.classList.add('active');
            if (indicator) {
                indicator.style.left = (this.offsetLeft + this.offsetWidth/2 - 27) + 'px';
            }
        });
    });
});