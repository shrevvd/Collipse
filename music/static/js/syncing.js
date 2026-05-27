// ============================================================
// НОВАЯ СИСТЕМА СОХРАНЕНИЯ И ВОССТАНОВЛЕНИЯ
// ============================================================

//  собирает и сохраняет ВСЁ состояние плеера
function saveFullPlayerState() {
    if (!audio || !audio.src) return;

    var state = {
        audioUrl: audio.src,            // Ссылка на трек
        currentTime: audio.currentTime, // Текущее время в секундах
        isPlaying: !audio.paused,       // true = играет, false = пауза
        title: nowPlaying ? nowPlaying.textContent : '',
        coverUrl: null,                 // Обложка (пока null, но будем обновлять)
        isLiked: false,                 // Лайк (пока null, но будем обновлять)
        isDisliked: false,              // Дизлайк (пока null, но будем обновлять)
        trackId: currentTrackId         // ID текущего трека
    };

    // Получаем текущую обложку с диска
    var coverImg = document.querySelector('.disc-cover-spin img');
    if (coverImg && coverImg.src) {
        state.coverUrl = coverImg.src;
    }

    // Получаем статус лайка/дизлайка по иконкам
    if (discLikeImg && discLikeImg.src.includes('HEART_FULL')) {
        state.isLiked = true;
    }
    if (discDislikeImg && discDislikeImg.src.includes('DISLIKE_PRESSED')) {
        state.isDisliked = true;
    }

    localStorage.setItem('collipsePlayerState', JSON.stringify(state));
}

function saveQueueState() {

    localStorage.setItem(
        'collipseQueue',
        JSON.stringify(queue)
    );

    localStorage.setItem(
        'collipseQueueIndex',
        queueIndex
    );

    localStorage.setItem(
        'collipseMode',
        currentMode
    );
}

// Функция восстановления состояния плеера
function restorePlayerState() {
    var savedState = localStorage.getItem('collipsePlayerState');
    if (!savedState || !audio) {
        return;
    }

    try {
        var state = JSON.parse(savedState);
        // ---------- UI ----------
        if (state.title && nowPlaying) {
            nowPlaying.textContent = state.title;
            nowPlaying.classList.remove('placeholder-text');
            nowPlaying.classList.add('placeholder-text-active');
        }
        if (state.coverUrl) {
            var coverImg = document.querySelector('.disc-cover-spin img');
            if (coverImg) {
                coverImg.src = state.coverUrl;
            }
        }
        if (state.trackId) {
            currentTrackId = state.trackId;
            if (discInfoLink) {
                discInfoLink.href = '/track/' + currentTrackId + '/';
            }
            if (discLikeLink) {
                discLikeLink.href = '/track/' + currentTrackId + '/like/';
            }
            if (discDislikeLink) {
                discDislikeLink.href = '/track/' + currentTrackId + '/dislike/';
            }
        }
        if (state.isLiked && discLikeImg) {
            discLikeImg.src = discLikeImg.src.replace(
                'HEART_EMPTY',
                'HEART_FULL'
            );
        }
        if (state.isDisliked && discDislikeImg) {
            discDislikeImg.src = discDislikeImg.src.replace(
                'HEART_BROKEN.svg',
                'DISLIKE_PRESSED.svg'
            );
        }
        // ---------- AUDIO ----------
        if (!state.audioUrl) {
            return;
        }
        audio.src = state.audioUrl;
        audio.load();
        var restored = false;
        function restorePosition() {
            if (restored) return;
            restored = true;
            var targetTime = Number(state.currentTime) || 0;
            try {
                if (targetTime > 0) {
                    audio.currentTime = targetTime;
                }
            } catch (e) {
                console.log('Seek failed', e);
            }
            if (state.isPlaying) {
                audio.play().catch(function(err) {
                    console.log('Autoplay blocked', err);
                });
            }
        }
        audio.addEventListener('loadedmetadata', restorePosition, {
            once: true
        });
        audio.addEventListener('canplay', restorePosition, {
            once: true
        });
        // запасной вариант
        setTimeout(function() {
            restorePosition();
        }, 1000);

    } catch (e) {
        console.error('Restore player failed:', e);
    }
}

function updateDiscInfo(data) {
    if (data.cover_url) {
        var coverImg = document.querySelector('.disc-cover-spin img');
        if (coverImg) coverImg.src = data.cover_url;
    }
    if (discLikeImg) {
        discLikeImg.src = data.is_liked ? discLikeImg.src.replace('HEART_EMPTY', 'HEART_FULL') : discLikeImg.src.replace('HEART_FULL', 'HEART_EMPTY');
    }
    if (discDislikeImg) {
        discDislikeImg.src = data.is_disliked ? discDislikeImg.src.replace('HEART_BROKEN.svg', 'DISLIKE_PRESSED.svg') : discDislikeImg.src.replace('DISLIKE_PRESSED.svg', 'HEART_BROKEN.svg');
    }
    if (discInfoLink) discInfoLink.href = '/track/' + data.id + '/';
    if (discLikeLink) discLikeLink.href = '/track/' + data.id + '/like/';
    if (discDislikeLink) discDislikeLink.href = '/track/' + data.id + '/dislike/';
}

// Синхронизировать иконку при запуске трека из любого места
(function() {
    if (audio) {

        audio.addEventListener('play', function() {
            updatePauseIcon();
            saveFullPlayerState();
        });

        audio.addEventListener('pause', function() {
            updatePauseIcon();
            saveFullPlayerState();
        });

        // сохраняем позицию каждые 2 секунды
        audio.addEventListener('timeupdate', function() {

            if (!audio.paused) {

                if (
                    !window.lastSave ||
                    Date.now() - window.lastSave > 2000
                ) {

                    window.lastSave = Date.now();
                    saveFullPlayerState();

                }
            }
        });

        audio.addEventListener('ended', function() {
            playNextTrack();
        });

    }
})();
