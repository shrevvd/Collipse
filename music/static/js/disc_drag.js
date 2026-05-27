// ============================================================
// 2. DRAG ДИСКА
// ============================================================
(function() {
    if (!disc || !wrapper) return;
    
    var savedLeft = localStorage.getItem('discLeft');
    var savedBottom = localStorage.getItem('discBottom');
    if (savedLeft && savedBottom) {
        wrapper.style.left = savedLeft;
        wrapper.style.bottom = savedBottom;
    }
    
    var isDragging = false, startX, startY, startLeft, startBottom;
    
    disc.addEventListener('mousedown', function(e) {
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        var style = window.getComputedStyle(wrapper);
        startLeft = parseInt(style.left) || 0;
        startBottom = parseInt(style.bottom) || 0;
        e.preventDefault();
    });
    
    document.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        wrapper.style.left = (startLeft + e.clientX - startX) + 'px';
        wrapper.style.bottom = (startBottom + startY - e.clientY) + 'px';
        localStorage.setItem('discLeft', wrapper.style.left);
        localStorage.setItem('discBottom', wrapper.style.bottom);
    });
    
    document.addEventListener('mouseup', function() { isDragging = false; });
})();