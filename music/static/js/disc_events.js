function playTrackFromData(data) {
    if (!data.audio_url) return;
    audio.src = data.audio_url;
    audio.play();
    currentTrackId = data.id;
    if (nowPlaying) {
        nowPlaying.textContent = data.title;
        nowPlaying.classList.remove('placeholder-text');
        nowPlaying.classList.add('placeholder-text-active');
    }
    updateDiscInfo(data);
    // Сразу сохраняем новое состояние
    saveFullPlayerState();
}

// Лайк
(function() {
    if (discLikeLink) {
        discLikeLink.addEventListener('click', function(e) {
            e.preventDefault();
            if (!currentTrackId) return;
            fetch('/track/' + currentTrackId + '/like/', {
                method: 'POST',
                headers: { 'X-CSRFToken': getCSRFToken() }
            })
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (data.status === 'liked') {
                    discLikeImg.src = discLikeImg.src.replace('HEART_EMPTY', 'HEART_FULL');
                } else if (data.status === 'unliked') {
                    discLikeImg.src = discLikeImg.src.replace('HEART_FULL', 'HEART_EMPTY');
                }
            });
        });
    }
})();

// Дизлайк
(function() {
    if (discDislikeLink) {
        discDislikeLink.addEventListener('click', function(e) {
            e.preventDefault();
            if (!currentTrackId) return;
            fetch('/track/' + currentTrackId + '/dislike/', {
                method: 'POST',
                headers: { 'X-CSRFToken': getCSRFToken() }
            })
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (data.status === 'disliked') {
                    discDislikeImg.src = discDislikeImg.src.replace('HEART_BROKEN.svg', 'DISLIKE_PRESSED.svg');
                    discLikeImg.src = discLikeImg.src.replace('HEART_FULL', 'HEART_EMPTY');
                    currentMode = 'all';
                    playNextTrack();
                } else if (data.status === 'undisliked') {
                    discDislikeImg.src = discDislikeImg.src.replace('DISLIKE_PRESSED.svg', 'HEART_BROKEN.svg');
                }
            });
        });
    }
})();

// Клик по трекам
(function() {
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.track-row').forEach(function(row) {
            row.addEventListener('click', function() {
                var audioUrl = this.dataset.audio;
                if (!audioUrl) return;
                if (currentTrackRow === this) {
                    audio.paused ? audio.play() : audio.pause();
                } else {
                    currentTrackRow = this;
                    var titleDiv = this.querySelector('div[style*="flex: 1"] div[style*="color: white"]');
                    var trackUrl = this.querySelector('.track-info-icon');
                    var id = null;
                    if (trackUrl) {
                        id = trackUrl.href.split('/track/')[1]?.split('/')[0];
                        if (id) currentTrackId = id;
                    }
                    // Используем API для получения полных данных о треке
                    if (id) {
                        fetch('/random-api/?track_id=' + id)
                            .then(function(r) { return r.json(); })
                            .then(function(data) {

                                playTrackFromData(data);

                                    if (currentMode === 'likes') {
                                        loadQueue(
                                            'likes',
                                            data.id
                                        );
                                    }
                                    else if (
                                        currentMode === 'recent'
                                    ) {
                                        loadQueue(
                                            'recent',
                                            data.id
                                        );
                                    }
                                    else {
                                        loadQueue(
                                            'recs',
                                            data.id
                                        );

                                    }
                                });
                    } else {
                        audio.src = audioUrl;
                        audio.play();
                        if (titleDiv && nowPlaying) {
                            nowPlaying.textContent = titleDiv.textContent.trim();
                            nowPlaying.classList.remove('placeholder-text');
                            nowPlaying.classList.add('placeholder-text-active');
                        }
                    }
                    localStorage.setItem('currentTrack', audioUrl);
                }
                saveFullPlayerState();
            });
        });
    });
})();

(function() {
    if (discPauseBtn) {
        discPauseBtn.addEventListener('click', function() {
            if (audio) {
                audio.paused ? audio.play() : audio.pause();
            }
        });
    }
})();

(function() {
    if (discPrevBtn) {
        discPrevBtn.addEventListener('click', function() {
            // Перезапустить текущий трек или переключить на предыдущий
            if (audio && audio.currentTime > 3) {
                audio.currentTime = 0;
            } else {
                playNextTrack(); // пока что просто следующий
            }
        });
    }
})();

(function() {
    if (discNextBtn) {
        discNextBtn.addEventListener('click', function() {
            playNextTrack();
        });
    }
})();

function updatePauseIcon() {
    if (!discPauseImg || !audio) return;
    if (audio.paused) {
        discPauseImg.src = discPauseImg.src.replace(/%D0%9F%D0%90%D0%A3%D0%97%D0%90\.svg/, 'PLAY_pause.svg');
    } else {
        discPauseImg.src = discPauseImg.src.replace(/PLAY_pause\.svg/, '%D0%9F%D0%90%D0%A3%D0%97%D0%90.svg');
    }
}

(function() {
    if (discPauseImg) {
        discPauseImg.addEventListener('click', function() {
            if (audio) {
                audio.paused ? audio.play() : audio.pause();
                updatePauseIcon();
            }
        });
    }
})();