// Set管理模块

let currentSetId = null;
let currentSetTracks = []; // 当前Set中的歌曲ID列表
let searchTimeout = null;

// 创建Set时的歌曲输入状态
let trackInputRows = []; // [{id, trackId, trackData}]
let trackInputCounter = 0;
let currentRecommendRowId = null;

// 初始化Sets模块
function initSets() {
    const createSetForm = document.getElementById('createSetForm');
    createSetForm.addEventListener('submit', handleCreateSet);

    // 点击页面其他地方关闭推荐弹窗
    document.addEventListener('click', (e) => {
        const popup = document.getElementById('recommendPopup');
        if (popup && popup.style.display !== 'none') {
            if (!popup.contains(e.target) && !e.target.classList.contains('btn-recommend')) {
                closeRecommendPopup();
            }
        }
    });
}

// 添加歌曲输入行
function addTrackInputRow(preselectedTrack = null) {
    const container = document.getElementById('trackInputList');
    const rowId = ++trackInputCounter;

    const rowData = {
        id: rowId,
        trackId: preselectedTrack ? preselectedTrack.id : null,
        trackData: preselectedTrack || null
    };
    trackInputRows.push(rowData);

    const rowEl = document.createElement('div');
    rowEl.className = 'track-input-row';
    rowEl.id = `track-row-${rowId}`;
    rowEl.innerHTML = `
        <span class="order-num">${trackInputRows.length}</span>
        <div class="search-wrapper">
            <input type="text"
                   id="track-search-${rowId}"
                   placeholder="搜索歌曲名称或艺术家..."
                   oninput="handleTrackInputSearch(${rowId}, this.value)"
                   onfocus="handleTrackInputFocus(${rowId})"
                   ${preselectedTrack ? `value="${preselectedTrack.title} - ${preselectedTrack.artist || ''}" class="has-track"` : ''}
                   data-track-id="${preselectedTrack ? preselectedTrack.id : ''}"
            >
            <div class="track-search-results" id="track-results-${rowId}"></div>
        </div>
        <button type="button" class="btn-recommend" onclick="showTrackRecommend(${rowId}, event)" ${!preselectedTrack ? 'disabled' : ''}>推荐</button>
        <button type="button" class="btn-remove" onclick="removeTrackInputRow(${rowId})">X</button>
    `;

    container.appendChild(rowEl);

    // 如果没有预选歌曲，自动聚焦输入框
    if (!preselectedTrack) {
        setTimeout(() => {
            document.getElementById(`track-search-${rowId}`).focus();
        }, 100);
    }
}

// 移除歌曲输入行
function removeTrackInputRow(rowId) {
    const rowEl = document.getElementById(`track-row-${rowId}`);
    if (rowEl) {
        rowEl.remove();
        trackInputRows = trackInputRows.filter(r => r.id !== rowId);
        updateTrackRowNumbers();
    }
}

// 更新行号
function updateTrackRowNumbers() {
    const container = document.getElementById('trackInputList');
    const rows = container.querySelectorAll('.track-input-row');
    rows.forEach((row, index) => {
        const orderNum = row.querySelector('.order-num');
        if (orderNum) orderNum.textContent = index + 1;
    });
}

// 处理歌曲搜索输入
function handleTrackInputSearch(rowId, keyword) {
    const resultsContainer = document.getElementById(`track-results-${rowId}`);
    const input = document.getElementById(`track-search-${rowId}`);

    // 清除之前选中的歌曲
    const row = trackInputRows.find(r => r.id === rowId);
    if (row) {
        row.trackId = null;
        row.trackData = null;
    }
    input.classList.remove('has-track');
    input.dataset.trackId = '';

    // 禁用推荐按钮
    const recommendBtn = document.querySelector(`#track-row-${rowId} .btn-recommend`);
    if (recommendBtn) recommendBtn.disabled = true;

    if (!keyword || keyword.length < 2) {
        resultsContainer.innerHTML = '';
        resultsContainer.style.display = 'none';
        return;
    }

    // 防抖处理
    if (searchTimeout) clearTimeout(searchTimeout);
    searchTimeout = setTimeout(async () => {
        try {
            const result = await api.searchTracks({ keyword });
            if (result.items && result.items.length > 0) {
                resultsContainer.innerHTML = result.items.slice(0, 8).map(track => `
                    <div class="search-result-item" onclick="selectTrackForRow(${rowId}, ${JSON.stringify(track).replace(/"/g, '&quot;')})">
                        <div class="result-info">
                            <span class="result-title">${track.title}</span>
                            <span class="result-artist">${track.artist || '未知艺术家'}</span>
                        </div>
                        <div class="result-meta">
                            ${track.bpm ? `${track.bpm} BPM` : ''} ${track.key ? `Key: ${track.key}` : ''}
                        </div>
                    </div>
                `).join('');
                resultsContainer.style.display = 'block';
            } else {
                resultsContainer.innerHTML = '<div class="no-results">未找到歌曲</div>';
                resultsContainer.style.display = 'block';
            }
        } catch (error) {
            console.error('搜索失败:', error);
        }
    }, 300);
}

// 处理输入框聚焦
function handleTrackInputFocus(rowId) {
    const input = document.getElementById(`track-search-${rowId}`);
    if (input.value.length >= 2 && !input.dataset.trackId) {
        handleTrackInputSearch(rowId, input.value);
    }
}

// 选择歌曲填入行
function selectTrackForRow(rowId, track) {
    const input = document.getElementById(`track-search-${rowId}`);
    const resultsContainer = document.getElementById(`track-results-${rowId}`);

    input.value = `${track.title} - ${track.artist || '未知'}`;
    input.classList.add('has-track');
    input.dataset.trackId = track.id;
    resultsContainer.style.display = 'none';

    // 更新状态
    const row = trackInputRows.find(r => r.id === rowId);
    if (row) {
        row.trackId = track.id;
        row.trackData = track;
    }

    // 启用推荐按钮
    const recommendBtn = document.querySelector(`#track-row-${rowId} .btn-recommend`);
    if (recommendBtn) recommendBtn.disabled = false;
}

// 显示推荐歌曲
async function showTrackRecommend(rowId, event) {
    event.stopPropagation();

    const row = trackInputRows.find(r => r.id === rowId);
    if (!row || !row.trackId) {
        showMessage('warning', '请先选择一首歌曲');
        return;
    }

    currentRecommendRowId = rowId;
    const popup = document.getElementById('recommendPopup');
    const content = document.getElementById('recommendPopupContent');

    // 定位弹窗
    const btn = event.target;
    const rect = btn.getBoundingClientRect();
    popup.style.top = `${rect.bottom + 10}px`;
    popup.style.left = `${Math.min(rect.left, window.innerWidth - 370)}px`;
    popup.style.display = 'block';

    // 显示加载状态
    content.innerHTML = '<div class="recommend-loading">加载推荐中...</div>';

    try {
        const result = await api.getTrackRecommendations(row.trackId, 10);
        if (result.items && result.items.length > 0) {
            content.innerHTML = result.items.map(track => `
                <div class="recommend-item" onclick="addRecommendedTrack(${JSON.stringify(track).replace(/"/g, '&quot;')})">
                    <img src="${track.cover_url || 'https://via.placeholder.com/48x48?text=No'}" alt="${track.title}">
                    <div class="recommend-info">
                        <div class="recommend-title">${track.title}</div>
                        <div class="recommend-artist">${track.artist || '未知'}</div>
                        <div class="recommend-meta">
                            ${track.bpm ? `${track.bpm} BPM` : ''} ${track.key ? `| Key: ${track.key}` : ''}
                        </div>
                    </div>
                </div>
            `).join('');
        } else {
            content.innerHTML = '<div class="recommend-empty">暂无推荐歌曲</div>';
        }
    } catch (error) {
        console.error('获取推荐失败:', error);
        content.innerHTML = '<div class="recommend-empty">获取推荐失败</div>';
    }
}

// 添加推荐的歌曲到下一行
function addRecommendedTrack(track) {
    closeRecommendPopup();
    addTrackInputRow(track);
    showMessage('success', `已添加: ${track.title}`);
}

// 关闭推荐弹窗
function closeRecommendPopup() {
    const popup = document.getElementById('recommendPopup');
    popup.style.display = 'none';
    currentRecommendRowId = null;
}

// 搜索歌曲用于添加到Set
async function searchTracksForSet(keyword) {
    const resultsContainer = document.getElementById('setTrackSearchResults');

    if (!keyword || keyword.length < 2) {
        resultsContainer.innerHTML = '';
        resultsContainer.style.display = 'none';
        return;
    }

    // 防抖处理
    if (searchTimeout) clearTimeout(searchTimeout);
    searchTimeout = setTimeout(async () => {
        try {
            const result = await api.searchTracks({ keyword });
            if (result.items && result.items.length > 0) {
                resultsContainer.innerHTML = result.items.slice(0, 10).map(track => `
                    <div class="search-result-item" onclick="addExistingTrackToSet(${track.id}, '${track.title.replace(/'/g, "\\'")}', '${(track.artist || '').replace(/'/g, "\\'")}')">
                        <div class="result-info">
                            <span class="result-title">${track.title}</span>
                            <span class="result-artist">${track.artist || '未知艺术家'}</span>
                        </div>
                        <div class="result-meta">
                            ${track.bpm ? `${track.bpm} BPM` : ''} ${track.genre || ''}
                        </div>
                    </div>
                `).join('');
                resultsContainer.style.display = 'block';
            } else {
                resultsContainer.innerHTML = '<div class="no-results">未找到歌曲</div>';
                resultsContainer.style.display = 'block';
            }
        } catch (error) {
            console.error('搜索失败:', error);
        }
    }, 300);
}

// 添加已存在的歌曲到Set
async function addExistingTrackToSet(trackId, title, artist) {
    if (!currentSetId) return;

    // 检查是否已在Set中
    if (currentSetTracks.includes(trackId)) {
        showMessage('warning', '该歌曲已在Set中');
        return;
    }

    try {
        // 添加到tracks列表
        currentSetTracks.push(trackId);

        // 更新Set
        await api.updateSet(currentSetId, { track_ids: currentSetTracks });

        showMessage('success', `已添加: ${title}`);

        // 清空搜索
        document.getElementById('setTrackSearch').value = '';
        document.getElementById('setTrackSearchResults').style.display = 'none';

        // 刷新Set详情
        await viewSetDetail(currentSetId);
    } catch (error) {
        console.error('添加歌曲失败:', error);
        showMessage('error', '添加歌曲失败');
        // 回滚
        currentSetTracks = currentSetTracks.filter(id => id !== trackId);
    }
}

// 手动录入新歌曲并添加到Set
async function addNewTrackToSet() {
    if (!currentSetId) return;

    const title = document.getElementById('newTrackTitle').value.trim();
    const artist = document.getElementById('newTrackArtist').value.trim();
    const bpm = document.getElementById('newTrackBpm').value;
    const genre = document.getElementById('newTrackGenre').value;
    const key = document.getElementById('newTrackKey').value.trim();

    if (!title) {
        showMessage('error', '请输入歌曲名称');
        return;
    }

    try {
        // 先创建歌曲
        const trackData = {
            title,
            artist: artist || null,
            bpm: bpm ? parseInt(bpm) : null,
            genre: genre || null,
            key: key || null,
            cover_url: `https://via.placeholder.com/300x300/${getRandomColor()}/fff?text=${encodeURIComponent(title.substring(0, 10))}`
        };

        const newTrack = await api.createTrack(trackData);

        // 添加到Set
        currentSetTracks.push(newTrack.id);
        await api.updateSet(currentSetId, { track_ids: currentSetTracks });

        showMessage('success', `已创建并添加: ${title}`);

        // 清空表单
        document.getElementById('newTrackTitle').value = '';
        document.getElementById('newTrackArtist').value = '';
        document.getElementById('newTrackBpm').value = '';
        document.getElementById('newTrackGenre').value = '';
        document.getElementById('newTrackKey').value = '';

        // 刷新Set详情
        await viewSetDetail(currentSetId);
    } catch (error) {
        console.error('创建歌曲失败:', error);
        showMessage('error', '创建歌曲失败: ' + error.message);
    }
}

// 从Set中移除歌曲
async function removeTrackFromSet(trackId) {
    if (!currentSetId) return;

    if (!confirm('确定要从Set中移除这首歌曲吗？')) return;

    try {
        currentSetTracks = currentSetTracks.filter(id => id !== trackId);
        await api.updateSet(currentSetId, { track_ids: currentSetTracks });
        showMessage('success', '已移除歌曲');
        await viewSetDetail(currentSetId);
    } catch (error) {
        console.error('移除歌曲失败:', error);
        showMessage('error', '移除歌曲失败');
    }
}

// 获取随机颜色
function getRandomColor() {
    const colors = ['FF6B6B', '4ECDC4', '45B7D1', '96CEB4', 'FFEAA7', 'DDA0DD', '98D8C8', '9B59B6', '3498DB', 'E74C3C', '1ABC9C', '8E44AD', '2980B9', '27AE60', 'F39C12'];
    return colors[Math.floor(Math.random() * colors.length)];
}

// 加载Sets列表
async function loadSets() {
    if (!requireAuth(() => {})) return;

    try {
        const result = await api.getSets();
        displaySets(result.items);
    } catch (error) {
        console.error('加载Sets失败:', error);
        showMessage('error', '加载Sets失败');
    }
}

// 显示Sets列表
function displaySets(sets) {
    const container = document.getElementById('setsList');

    if (!sets || sets.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>暂无Set</h3>
                <p>创建你的第一个DJ Set吧</p>
            </div>
        `;
        return;
    }

    container.innerHTML = sets.map(set => `
        <div class="set-card" onclick="viewSetDetail(${set.id})">
            <img src="${set.cover_url || 'https://via.placeholder.com/400x400?text=DJ+Set'}"
                 alt="${set.name}" class="set-cover">
            <div class="set-info">
                <div class="set-name">${set.name}</div>
                <div class="set-description">${set.description || '暂无描述'}</div>
                <div class="set-meta">
                    ${set.track_count} 首歌曲 • ${new Date(set.created_at).toLocaleDateString()}
                </div>
            </div>
        </div>
    `).join('');
}

// 查看Set详情
async function viewSetDetail(setId) {
    currentSetId = setId;

    try {
        const set = await api.getSet(setId);

        // 更新页面标题和描述
        document.getElementById('setDetailTitle').textContent = set.name;
        document.getElementById('setDetailDescription').textContent = set.description || '暂无描述';

        // 更新当前tracks列表
        currentSetTracks = (set.tracks || []).map(t => t.id);

        // 显示tracks
        displaySetTracks(set.tracks || []);

        // 切换到详情页
        showPage('setDetail');
    } catch (error) {
        console.error('加载Set详情失败:', error);
        showMessage('error', '加载Set详情失败');
    }
}

// 显示Set中的tracks
function displaySetTracks(tracks) {
    const container = document.getElementById('setDetailTracks');

    if (!tracks || tracks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>此Set暂无歌曲，使用上方面板添加歌曲</p>
            </div>
        `;
        return;
    }

    container.innerHTML = `
        <h3>🎵 歌曲列表 (${tracks.length}首)</h3>
        ${tracks.map((track, index) => `
            <div class="track-item">
                <span class="track-item-order">${index + 1}</span>
                <div class="track-item-info">
                    <div class="track-title">${track.title}</div>
                    <div class="track-artist">${track.artist || '未知艺术家'}</div>
                    <div class="track-meta">
                        ${track.bpm ? `BPM: ${track.bpm}` : ''}
                        ${track.genre ? `• ${track.genre}` : ''}
                        ${track.key ? `• Key: ${track.key}` : ''}
                    </div>
                </div>
                <button class="btn btn-sm btn-danger" onclick="removeTrackFromSet(${track.id})">移除</button>
            </div>
        `).join('')}
    `;
}

// 显示创建Set模态框
function showCreateSetModal() {
    if (!requireAuth(() => {})) return;

    // 重置状态
    trackInputRows = [];
    trackInputCounter = 0;
    document.getElementById('trackInputList').innerHTML = '';
    document.getElementById('createSetForm').reset();
    document.getElementById('createSetModalTitle').textContent = '创建新Set';

    // 恢复表单为创建模式
    const form = document.getElementById('createSetForm');
    form.onsubmit = handleCreateSet;

    // 添加第一行空的歌曲输入
    addTrackInputRow();

    showModal('createSetModal');
}

// 处理创建Set
async function handleCreateSet(e) {
    e.preventDefault();

    // 收集选中的歌曲ID
    const selectedTrackIds = trackInputRows
        .filter(row => row.trackId)
        .map(row => row.trackId);

    const setData = {
        name: document.getElementById('setName').value,
        description: document.getElementById('setDescription').value,
        cover_url: document.getElementById('setCover').value,
        track_ids: selectedTrackIds,
    };

    try {
        const result = await api.createSet(setData);
        showMessage('success', `Set创建成功，包含 ${selectedTrackIds.length} 首歌曲`);
        closeModal('createSetModal');
        document.getElementById('createSetForm').reset();

        // 清理状态
        trackInputRows = [];
        trackInputCounter = 0;

        // 刷新Sets列表
        await loadSets();

        // 跳转到新创建的Set详情页
        viewSetDetail(result.id);
    } catch (error) {
        console.error('创建Set失败:', error);
        showMessage('error', '创建Set失败: ' + error.message);
    }
}

// 显示编辑Set模态框
async function showEditSetModal() {
    if (!currentSetId) return;

    try {
        const set = await api.getSet(currentSetId);

        // 重置歌曲输入状态
        trackInputRows = [];
        trackInputCounter = 0;
        document.getElementById('trackInputList').innerHTML = '';

        // 填充表单
        document.getElementById('setName').value = set.name;
        document.getElementById('setDescription').value = set.description || '';
        document.getElementById('setCover').value = set.cover_url || '';
        document.getElementById('createSetModalTitle').textContent = '编辑Set';

        // 加载现有歌曲到输入行
        if (set.tracks && set.tracks.length > 0) {
            set.tracks.forEach(track => {
                addTrackInputRow(track);
            });
        } else {
            addTrackInputRow();
        }

        // 修改表单提交处理为更新而不是创建
        const form = document.getElementById('createSetForm');
        form.onsubmit = async (e) => {
            e.preventDefault();

            // 收集选中的歌曲ID
            const selectedTrackIds = trackInputRows
                .filter(row => row.trackId)
                .map(row => row.trackId);

            const setData = {
                name: document.getElementById('setName').value,
                description: document.getElementById('setDescription').value,
                cover_url: document.getElementById('setCover').value,
                track_ids: selectedTrackIds,
            };

            try {
                await api.updateSet(currentSetId, setData);
                showMessage('success', 'Set更新成功');
                closeModal('createSetModal');

                // 清理状态
                trackInputRows = [];
                trackInputCounter = 0;

                // 重新加载详情
                await viewSetDetail(currentSetId);

                // 恢复表单为创建模式
                form.onsubmit = handleCreateSet;
            } catch (error) {
                console.error('更新Set失败:', error);
                showMessage('error', '更新Set失败: ' + error.message);
            }
        };

        showModal('createSetModal');
    } catch (error) {
        console.error('加载Set信息失败:', error);
        showMessage('error', '加载Set信息失败');
    }
}

// 删除当前Set
async function deleteCurrentSet() {
    if (!currentSetId) return;

    if (!confirm('确定要删除这个Set吗？此操作不可恢复。')) return;

    try {
        await api.deleteSet(currentSetId);
        showMessage('success', 'Set已删除');
        currentSetId = null;
        showPage('sets');
        await loadSets();
    } catch (error) {
        console.error('删除Set失败:', error);
        showMessage('error', '删除Set失败');
    }
}

// 加载推荐歌曲
async function loadRecommendations() {
    if (!currentSetId) return;

    try {
        const result = await api.getSetRecommendations(currentSetId, 10);
        displayRecommendations(result.items);
    } catch (error) {
        console.error('加载推荐失败:', error);
        showMessage('error', '加载推荐失败');
    }
}

// 显示推荐歌曲
function displayRecommendations(tracks) {
    const container = document.getElementById('recommendationsList');

    if (!tracks || tracks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>暂无推荐</p>
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
            </div>
        </div>
    `).join('');
}

// 导出到全局作用域，以便HTML中的内联事件处理器可以访问
window.initSets = initSets;
window.loadSets = loadSets;
window.showCreateSetModal = showCreateSetModal;
window.viewSetDetail = viewSetDetail;
window.showEditSetModal = showEditSetModal;
window.deleteCurrentSet = deleteCurrentSet;
window.loadRecommendations = loadRecommendations;
window.searchTracksForSet = searchTracksForSet;
window.addExistingTrackToSet = addExistingTrackToSet;
window.addNewTrackToSet = addNewTrackToSet;
window.removeTrackFromSet = removeTrackFromSet;
window.addTrackInputRow = addTrackInputRow;
window.removeTrackInputRow = removeTrackInputRow;
window.handleTrackInputSearch = handleTrackInputSearch;
window.handleTrackInputFocus = handleTrackInputFocus;
window.selectTrackForRow = selectTrackForRow;
window.showTrackRecommend = showTrackRecommend;
window.addRecommendedTrack = addRecommendedTrack;
window.closeRecommendPopup = closeRecommendPopup;
