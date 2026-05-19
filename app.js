let currentUser = null;
let searchTimeout = null;

document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

async function initApp() {
    const token = API.getToken();

    if (token) {
        try {
            currentUser = await API.auth.getMe();
            showMainPage();
        } catch (error) {
            API.clearToken();
            showLoginPage();
        }
    } else {
        showLoginPage();
    }

    setupEventListeners();
}

function setupEventListeners() {
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('register-form').addEventListener('submit', handleRegister);
    document.getElementById('show-register').addEventListener('click', (e) => {
        e.preventDefault();
        showPage('register-page');
    });
    document.getElementById('show-login').addEventListener('click', (e) => {
        e.preventDefault();
        showPage('login-page');
    });

    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    document.getElementById('add-track-btn').addEventListener('click', () => openTrackModal());
    document.getElementById('create-set-btn').addEventListener('click', () => openSetModal());
    document.getElementById('search-btn').addEventListener('click', handleUnifiedSearch);
    document.getElementById('track-form').addEventListener('submit', handleTrackSubmit);
    document.getElementById('set-form').addEventListener('submit', handleSetSubmit);

    // Real-time search as you type
    document.getElementById('search-input').addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            handleUnifiedSearch();
        }, 300);
    });

    // Enter key to search
    document.getElementById('search-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleUnifiedSearch();
        }
    });

    document.querySelectorAll('.modal .close').forEach(closeBtn => {
        closeBtn.addEventListener('click', () => {
            closeBtn.closest('.modal').classList.remove('active');
        });
    });
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const data = await API.auth.login(email, password);
        currentUser = data.user;
        showMainPage();
    } catch (error) {
        alert('登录失败: ' + error.message);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    try {
        await API.auth.register(email, password, username);
        alert('注册成功！请登录');
        showPage('login-page');
    } catch (error) {
        alert('注册失败: ' + error.message);
    }
}

function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');
}

function showLoginPage() {
    showPage('login-page');
    document.getElementById('nav-user').innerHTML = '';
}

function showMainPage() {
    showPage('main-page');
    document.getElementById('nav-user').innerHTML = `
        <span>👤 ${currentUser.username || currentUser.email}</span>
        <button class="btn-logout" onclick="handleLogout()">登出</button>
    `;
    loadTracks();
}

function handleLogout() {
    API.auth.logout();
    currentUser = null;
    showLoginPage();
}

function switchTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');

    if (tabName === 'tracks') {
        loadTracks();
    } else if (tabName === 'sets') {
        loadSets();
    }
}

async function loadTracks() {
    try {
        const tracks = await API.tracks.getAll();
        renderLocalTracks(tracks);
        document.getElementById('itunes-results-section').style.display = 'none';
    } catch (error) {
        console.error('加载歌曲失败:', error);
    }
}

function renderLocalTracks(tracks) {
    const container = document.getElementById('local-tracks-list');

    if (tracks.length === 0) {
        container.innerHTML = '<p class="empty-msg">暂无歌曲，试试搜索添加吧！</p>';
        return;
    }

    container.innerHTML = tracks.map(track => `
        <div class="track-card">
            ${track.cover_url ? `<img src="${track.cover_url}" class="track-cover" alt="${track.title}">` : '<div class="track-cover-placeholder">🎵</div>'}
            <div class="track-info-wrapper">
                <h3>${track.title}</h3>
                <p>🎤 ${track.artist}</p>
                <div class="track-meta">
                    ${track.genre ? `<span>🎵 ${track.genre}</span>` : ''}
                    ${track.bpm ? `<span>💓 ${track.bpm} BPM</span>` : ''}
                    ${track.duration ? `<span>⏱️ ${Math.floor(track.duration / 60)}:${(track.duration % 60).toString().padStart(2, '0')}</span>` : ''}
                </div>
                <div class="card-actions">
                    <button class="btn-recommend" onclick="showRecommendations(${track.id})">推荐</button>
                    <button class="btn-delete" onclick="deleteTrack(${track.id})">删除</button>
                </div>
            </div>
        </div>
    `).join('');
}

async function handleUnifiedSearch() {
    const keyword = document.getElementById('search-input').value.trim();

    if (!keyword) {
        loadTracks();
        return;
    }

    // Show loading
    document.getElementById('local-tracks-list').innerHTML = '<p class="loading">搜索中...</p>';
    document.getElementById('itunes-results-section').style.display = 'block';
    document.getElementById('itunes-tracks-list').innerHTML = '<p class="loading">搜索iTunes中...</p>';

    // Search both local and iTunes in parallel
    try {
        const [localTracks, itunesTracks] = await Promise.all([
            API.tracks.search({ keyword }),
            API.music.search(keyword, 8)
        ]);

        renderLocalTracks(localTracks);
        renderItunesTracks(itunesTracks);
    } catch (error) {
        console.error('搜索失败:', error);
    }
}

function renderItunesTracks(tracks) {
    const section = document.getElementById('itunes-results-section');
    const container = document.getElementById('itunes-tracks-list');

    if (tracks.length === 0) {
        section.style.display = 'none';
        return;
    }

    section.style.display = 'block';
    container.innerHTML = tracks.map(track => {
        const trackJson = JSON.stringify(track).replace(/'/g, "&#39;").replace(/"/g, "&quot;");
        return `
        <div class="track-card itunes-track" onclick='addFromItunes(${JSON.stringify(track)})'>
            <img src="${track.cover_url}" class="track-cover" alt="${track.title}">
            <div class="track-info-wrapper">
                <h3>${track.title}</h3>
                <p>🎤 ${track.artist}</p>
                <div class="track-meta">
                    ${track.genre ? `<span>🎵 ${track.genre}</span>` : ''}
                    ${track.duration ? `<span>⏱️ ${Math.floor(track.duration / 60)}:${(track.duration % 60).toString().padStart(2, '0')}</span>` : ''}
                </div>
                <div class="add-hint">
                    <span>➕ 点击添加到歌曲库</span>
                </div>
            </div>
        </div>
    `}).join('');
}

async function addFromItunes(track) {
    const trackData = {
        title: track.title,
        artist: track.artist,
        genre: track.genre,
        duration: track.duration,
        cover_url: track.cover_url
    };

    try {
        await API.tracks.create(trackData);
        alert(`✅ "${track.title}" 已添加到歌曲库！`);
        // Refresh search results
        handleUnifiedSearch();
    } catch (error) {
        alert('添加失败: ' + error.message);
    }
}

async function showRecommendations(trackId) {
    try {
        const tracks = await API.tracks.getRecommendations(trackId, 5);
        if (tracks.length === 0) {
            alert('暂无推荐歌曲');
        } else {
            alert(`为您推荐:\n${tracks.map(t => `${t.title} - ${t.artist}`).join('\n')}`);
        }
    } catch (error) {
        alert('获取推荐失败');
    }
}

async function deleteTrack(id) {
    if (!confirm('确定要删除这首歌吗？')) return;

    try {
        await API.tracks.delete(id);
        const keyword = document.getElementById('search-input').value.trim();
        if (keyword) {
            handleUnifiedSearch();
        } else {
            loadTracks();
        }
    } catch (error) {
        alert('删除失败: ' + error.message);
    }
}

function openTrackModal() {
    document.getElementById('track-modal').classList.add('active');
}

async function handleTrackSubmit(e) {
    e.preventDefault();

    const trackData = {
        title: document.getElementById('track-title').value,
        artist: document.getElementById('track-artist').value,
        genre: document.getElementById('track-genre').value,
        bpm: parseInt(document.getElementById('track-bpm').value) || null,
        duration: parseInt(document.getElementById('track-duration').value) || null,
        cover_url: document.getElementById('track-cover-url').value || null
    };

    try {
        await API.tracks.create(trackData);
        document.getElementById('track-modal').classList.remove('active');
        document.getElementById('track-form').reset();
        loadTracks();
    } catch (error) {
        alert('添加失败: ' + error.message);
    }
}

async function loadSets() {
    try {
        const sets = await API.sets.getAll();
        renderSets(sets);
    } catch (error) {
        console.error('加载Sets失败:', error);
    }
}

function renderSets(sets) {
    const container = document.getElementById('sets-list');

    if (sets.length === 0) {
        container.innerHTML = '<p class="empty-msg">暂无Sets</p>';
        return;
    }

    container.innerHTML = sets.map(set => `
        <div class="set-card">
            <h3>${set.name}</h3>
            <p>${set.description || '无描述'}</p>
            <p>📀 ${set.track_count} 首歌曲</p>
            <div class="card-actions">
                <button class="btn-delete" onclick="deleteSet(${set.id})">删除</button>
            </div>
        </div>
    `).join('');
}

function openSetModal() {
    document.getElementById('set-modal').classList.add('active');
}

async function handleSetSubmit(e) {
    e.preventDefault();

    const setData = {
        name: document.getElementById('set-name').value,
        description: document.getElementById('set-description').value,
        track_ids: []
    };

    try {
        await API.sets.create(setData);
        document.getElementById('set-modal').classList.remove('active');
        document.getElementById('set-form').reset();
        loadSets();
    } catch (error) {
        alert('创建失败: ' + error.message);
    }
}

async function deleteSet(id) {
    if (!confirm('确定要删除这个Set吗？')) return;

    try {
        await API.sets.delete(id);
        loadSets();
    } catch (error) {
        alert('删除失败: ' + error.message);
    }
}
