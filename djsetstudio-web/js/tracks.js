// 歌曲管理模块

// 初始化歌曲模块
function initTracks() {
    const addTrackForm = document.getElementById('addTrackForm');
    addTrackForm.addEventListener('submit', handleAddTrack);
}

// 加载歌曲列表
async function loadTracks() {
    try {
        const result = await api.getTracks();
        displayTracks(result.items, 'tracksList');
    } catch (error) {
        console.error('加载歌曲列表失败:', error);
        showMessage('error', '加载歌曲列表失败');
    }
}

// 搜索歌曲
async function searchTracks() {
    const keyword = document.getElementById('searchKeyword').value;
    const genre = document.getElementById('searchGenre').value;
    const minBpm = document.getElementById('searchMinBpm').value;
    const maxBpm = document.getElementById('searchMaxBpm').value;

    const params = {};
    if (keyword) params.keyword = keyword;
    if (genre) params.genre = genre;
    if (minBpm) params.min_bpm = minBpm;
    if (maxBpm) params.max_bpm = maxBpm;

    try {
        const result = await api.searchTracks(params);
        displayTracks(result.items, 'searchResults');

        if (result.items.length === 0) {
            document.getElementById('searchResults').innerHTML = `
                <div class="empty-state">
                    <h3>未找到相关歌曲</h3>
                    <p>请尝试其他搜索条件</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('搜索失败:', error);
        showMessage('error', '搜索失败');
    }
}

// 显示歌曲列表
function displayTracks(tracks, containerId) {
    const container = document.getElementById(containerId);

    if (!tracks || tracks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>暂无歌曲</h3>
                <p>添加一些歌曲开始吧</p>
            </div>
        `;
        return;
    }

    container.innerHTML = tracks.map(track => `
        <div class="track-card">
            <img src="${track.cover_url || 'https://via.placeholder.com/300x300?text=No+Cover'}"
                 alt="${track.title}" class="track-cover">
            <div class="track-info">
                <div class="track-title">${track.title}</div>
                <div class="track-artist">${track.artist || '未知艺术家'}</div>
                <div class="track-meta">
                    ${track.bpm ? `<span>BPM: ${track.bpm}</span>` : ''}
                    ${track.genre ? `<span>${track.genre}</span>` : ''}
                </div>
                <div class="track-actions">
                    <button class="btn btn-secondary" onclick="showTrackRecommendations(${track.id})">
                        推荐
                    </button>
                    ${isAuthenticated() ? `
                        <button class="btn btn-danger" onclick="deleteTrack(${track.id})">
                            删除
                        </button>
                    ` : ''}
                </div>
            </div>
        </div>
    `).join('');
}

// 显示添加歌曲模态框
function showAddTrackModal() {
    if (!requireAuth(() => {})) return;
    showModal('addTrackModal');
}

// 处理添加歌曲
async function handleAddTrack(e) {
    e.preventDefault();

    const trackData = {
        title: document.getElementById('trackTitle').value,
        artist: document.getElementById('trackArtist').value,
        bpm: parseFloat(document.getElementById('trackBpm').value) || null,
        genre: document.getElementById('trackGenre').value,
        key: document.getElementById('trackKey').value,
        duration_sec: parseInt(document.getElementById('trackDuration').value) || null,
        cover_url: document.getElementById('trackCover').value,
    };

    try {
        await api.createTrack(trackData);
        showMessage('success', '歌曲添加成功');
        closeModal('addTrackModal');
        document.getElementById('addTrackForm').reset();

        // 刷新歌曲列表
        await loadTracks();
    } catch (error) {
        console.error('添加歌曲失败:', error);
        showMessage('error', '添加歌曲失败: ' + error.message);
    }
}

// 删除歌曲
async function deleteTrack(trackId) {
    if (!confirm('确定要删除这首歌曲吗？')) return;

    try {
        await api.deleteTrack(trackId);
        showMessage('success', '歌曲已删除');
        await loadTracks();
    } catch (error) {
        console.error('删除歌曲失败:', error);
        showMessage('error', '删除歌曲失败');
    }
}

// 显示歌曲推荐
async function showTrackRecommendations(trackId) {
    try {
        const result = await api.getTrackRecommendations(trackId);

        if (result.items.length === 0) {
            showMessage('info', '暂无推荐');
            return;
        }

        // 创建一个简单的推荐弹窗
        const modalHtml = `
            <div id="recommendModal" class="modal active">
                <div class="modal-content">
                    <span class="close" onclick="closeRecommendModal()">&times;</span>
                    <h2>相似歌曲推荐</h2>
                    <div class="tracks-grid">
                        ${result.items.map(track => `
                            <div class="track-card">
                                <img src="${track.cover_url || 'https://via.placeholder.com/300x300?text=No+Cover'}"
                                     alt="${track.title}" class="track-cover">
                                <div class="track-info">
                                    <div class="track-title">${track.title}</div>
                                    <div class="track-artist">${track.artist || '未知艺术家'}</div>
                                    <div class="track-meta">
                                        ${track.bpm ? `<span>BPM: ${track.bpm}</span>` : ''}
                                        ${track.genre ? `<span>${track.genre}</span>` : ''}
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
    } catch (error) {
        console.error('获取推荐失败:', error);
        showMessage('error', '获取推荐失败');
    }
}

// 关闭推荐模态框
function closeRecommendModal() {
    const modal = document.getElementById('recommendModal');
    if (modal) {
        modal.remove();
    }
}
