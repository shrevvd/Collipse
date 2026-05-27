document.querySelector('.nav-icon[data-tab="settings"]').addEventListener('click', function() {
    document.getElementById('settingsModal').style.display = 'flex';
});

document.getElementById('settingsModal').addEventListener('click', function(e) {
    if (e.target === this) this.style.display = 'none';
});