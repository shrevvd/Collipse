function loadQueue(mode, currentId = null, append = false) {

    currentMode = mode;

    let url =
        '/queue-api/?mode=' + mode;

    if (currentId) {
        url += '&current=' + currentId;
    }

    if (
        append &&
        queue.length > 0
    ) {
        url += '&exclude=' +
            queue.map(function(t) {
                return t.id;
            }).join(',');
    }

    fetch(url)
        .then(function(r) {
            return r.json();
        })
        .then(function(data) {

            // новая очередь
            if (!append) {
                queue = data;
                queueIndex = 0;
            }

            // догрузка
            else {
                if (data.length > 0) {
                    queue = queue.concat(data);
                } else {
                    // всё закончилось
                    queueIndex = 0;
                    shuffleQueue();
                }
            }
            renderQueue();
            saveQueueState();
        });
}

function shuffleQueue() {
    for (
        let i = queue.length - 1;
        i > 0;
        i--
    ) {
        const j =
            Math.floor(
                Math.random() * (i + 1)
            );
        [queue[i], queue[j]] =
        [queue[j], queue[i]];
    }
    renderQueue();
}

function playNextTrack() {
    if (queue.length === 0) {
        return;
    }
    // заранее догружаем
    if (
        queue.length - queueIndex <= 2
    ) {
        loadQueue(
            currentMode,
            currentTrackId,
            true
        );
    }
    // конец очереди
    if (
        queueIndex >= queue.length
    ) {
        queueIndex = 0;
        shuffleQueue();
    }
    playTrackFromData(
        queue[queueIndex]
    );
    queueIndex++;
    renderQueue();
    saveQueueState();
}

// восстановление очереди
(function() {
    try {

        queue = JSON.parse(
            localStorage.getItem('collipseQueue')
        ) || [];

        queueIndex = Number(
            localStorage.getItem('collipseQueueIndex')
        ) || 0;

        currentMode =
            localStorage.getItem('collipseMode')
            || 'recs';

    }
    catch(e){

        queue = [];
        queueIndex = 0;
        currentMode = 'recs';

    }
})();

function shuffleQueue() {
    for (let i = queue.length - 1; i > 0; i--) {
        let j = Math.floor(
            Math.random() * (i + 1)
        );

        [queue[i], queue[j]] = [
            queue[j],
            queue[i]
        ];
    }
    saveQueueState();
}

// Показать/скрыть панель очереди
(function() {
    if (discQueueLink) {
        discQueueLink.addEventListener('click', function(e) {
            e.preventDefault();
            var panel = document.getElementById('queuePanel');
            panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        });
    }
})();

// Отрисовать очередь в панели
function renderQueue() {
    var list = document.getElementById('queueList');
    if (!list) return;
    if (queue.length === 0) {
        list.innerHTML =
            '<p style="color:#79787A;">Queue is empty</p>';
        return;
    }
    var html = '';
    queue.forEach(function(track, index) {
        var active =
            index === queueIndex - 1;
        html += `
            <div
                style="
                    padding:10px 12px;
                    margin-bottom:6px;
                    border-radius:12px;
                    ${
                        active
                        ? 'background:#443F4B;color:white;'
                        : 'background:transparent;color:#aaa;'
                    }
                "
            >
                <div>${track.title}</div>
                <div style="font-size:11px;opacity:.7;">
                    ${track.artist}
                </div>
            </div>
        `;
    });

    list.innerHTML = html;
}

// Удалить трек из очереди
function removeFromQueue(index) {
    queue.splice(index, 1);
    renderQueue();
}

// Добавить трек в очередь
function addToQueue(track) {
    queue.push(track);
    renderQueue();
}