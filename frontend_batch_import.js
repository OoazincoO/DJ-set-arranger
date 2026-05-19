/**
 * 批量导入功能 - 前端代码
 *
 * 使用方法：
 * 1. 将此代码添加到 djsetstudio-web/js/tracks.js 文件末尾
 * 2. 或者创建新文件 djsetstudio-web/js/batch-import.js 并在 index.html 中引入
 */

// ==================== 批量导入相关功能 ====================

// 存储选中的歌曲（用于批量添加）
let selectedTracks = new Set();

/**
 * 批量创建歌曲
 */
async function batchCreateTracks(tracksData) {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('请先登录');
        }

        const response = await fetch(`${API_BASE_URL}/tracks/batch`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ tracks: tracksData })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || '批量添加失败');
        }

        return await response.json();
    } catch (error) {
        console.error('批量添加歌曲失败:', error);
        throw error;
    }
}

/**
 * 获取艺术家的所有歌曲
 */
async function getTracksByArtist(artistName) {
    try {
        const response = await fetch(
            `${API_BASE_URL}/tracks/artist/${encodeURIComponent(artistName)}`
        );

        if (!response.ok) {
            throw new Error('获取艺术家歌曲失败');
        }

        return await response.json();
    } catch (error) {
        console.error('获取艺术家歌曲失败:', error);
        throw error;
    }
}

/**
 * 切换歌曲选中状态
 */
function toggleTrackSelection(trackData) {
    const trackKey = `${trackData.title}-${trackData.artist}`;

    if (selectedTracks.has(trackKey)) {
        selectedTracks.delete(trackKey);
    } else {
        selectedTracks.set(trackKey, trackData);
    }

    updateBatchActionButtons();
}

/**
 * 全选/取消全选
 */
function toggleSelectAll(tracks) {
    if (selectedTracks.size === tracks.length) {
        // 取消全选
        selectedTracks.clear();
    } else {
        // 全选
        tracks.forEach(track => {
            const trackKey = `${track.title}-${track.artist}`;
            selectedTracks.set(trackKey, track);
        });
    }

    updateBatchActionButtons();
    renderTracksWithSelection(tracks);
}

/**
 * 更新批量操作按钮状态
 */
function updateBatchActionButtons() {
    const batchAddBtn = document.getElementById('batchAddBtn');
    const selectedCountEl = document.getElementById('selectedCount');

    if (batchAddBtn) {
        batchAddBtn.disabled = selectedTracks.size === 0;
    }

    if (selectedCountEl) {
        selectedCountEl.textContent = selectedTracks.size;
    }
}

/**
 * 渲染带选择框的歌曲列表
 */
function renderTracksWithSelection(tracks, containerId = 'searchResults') {
    const container = document.getElementById(containerId);

    if (!tracks || tracks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>未找到相关歌曲</h3>
                <p>请尝试其他搜索条件</p>
            </div>
        `;
        return;
    }

    // 添加批量操作工具栏
    const toolbar = `
        <div class="batch-toolbar">
            <label class="checkbox-label">
                <input type="checkbox"
                       id="selectAllCheckbox"
                       onchange="toggleSelectAll(${JSON.stringify(tracks).replace(/"/g, '&quot;')})">
                <span>全选</span>
            </label>
            <span class="selected-info">
                已选择 <strong id="selectedCount">0</strong> 首歌曲
            </span>
            <button id="batchAddBtn"
                    class="btn btn-primary"
                    onclick="handleBatchAdd()"
                    disabled>
                批量添加到歌曲库
            </button>
        </div>
    `;

    container.innerHTML = toolbar + tracks.map(track => {
        const trackKey = `${track.title}-${track.artist}`;
        const isSelected = selectedTracks.has(trackKey);

        return `
            <div class="track-card ${isSelected ? 'selected' : ''}" data-track-key="${trackKey}">
                <label class="track-checkbox">
                    <input type="checkbox"
                           ${isSelected ? 'checked' : ''}
                           onchange='toggleTrackSelection(${JSON.stringify(track).replace(/'/g, "\\'")}); renderTracksWithSelection(${JSON.stringify(tracks).replace(/'/g, "\\'")})'>
                </label>
                <img src="${track.cover_url || track.artworkUrl100 || 'https://via.placeholder.com/300x300?text=No+Cover'}"
                     alt="${track.title}" class="track-cover">
                <div class="track-info">
                    <div class="track-title">${track.title || track.trackName}</div>
                    <div class="track-artist">${track.artist || track.artistName || '未知艺术家'}</div>
                    <div class="track-meta">
                        ${track.bpm ? `<span>BPM: ${track.bpm}</span>` : ''}
                        ${track.genre || track.primaryGenreName ? `<span>${track.genre || track.primaryGenreName}</span>` : ''}
                        ${track.trackTimeMillis ? `<span>${Math.floor(track.trackTimeMillis / 1000 / 60)}:${String(Math.floor(track.trackTimeMillis / 1000) % 60).padStart(2, '0')}</span>` : ''}
                    </div>
                </div>
            </div>
        `;
    }).join('');

    updateBatchActionButtons();
}

/**
 * 处理批量添加
 */
async function handleBatchAdd() {
    if (selectedTracks.size === 0) {
        showMessage('warning', '请先选择要添加的歌曲');
        return;
    }

    if (!requireAuth(() => {})) return;

    const tracksArray = Array.from(selectedTracks.values());

    // 转换为后端需要的格式
    const tracksData = tracksArray.map(track => ({
        title: track.title || track.trackName,
        artist: track.artist || track.artistName,
        bpm: track.bpm || null,
        genre: track.genre || track.primaryGenreName || null,
        duration_sec: track.duration_sec || (track.trackTimeMillis ? Math.floor(track.trackTimeMillis / 1000) : null),
        cover_url: track.cover_url || track.artworkUrl100 || null,
        key: track.key || null
    }));

    try {
        showMessage('info', `正在添加 ${tracksData.length} 首歌曲...`);

        const result = await batchCreateTracks(tracksData);

        showMessage('success',
            `成功添加 ${result.created} 首歌曲` +
            (result.skipped > 0 ? `，跳过 ${result.skipped} 首（已存在或数据不完整）` : '')
        );

        // 清空选择
        selectedTracks.clear();
        updateBatchActionButtons();

        // 刷新歌曲列表
        if (typeof loadTracks === 'function') {
            await loadTracks();
        }

    } catch (error) {
        console.error('批量添加失败:', error);
        showMessage('error', '批量添加失败: ' + error.message);
    }
}

/**
 * 显示艺术家导入对话框
 */
function showArtistImportDialog() {
    if (!requireAuth(() => {})) return;

    const dialogHtml = `
        <div id="artistImportModal" class="modal active">
            <div class="modal-content">
                <span class="close" onclick="closeArtistImportDialog()">&times;</span>
                <h2>艺术家一键导入</h2>
                <p>输入艺术家名称，从 iTunes 获取该艺术家的所有歌曲并批量导入</p>

                <form id="artistImportForm" onsubmit="handleArtistImport(event)">
                    <div class="form-group">
                        <label for="artistImportName">艺术家名称</label>
                        <input type="text"
                               id="artistImportName"
                               class="form-control"
                               placeholder="例如: Martin Garrix"
                               required>
                    </div>

                    <div class="form-group">
                        <label for="importLimit">导入数量限制</label>
                        <input type="number"
                               id="importLimit"
                               class="form-control"
                               value="50"
                               min="1"
                               max="100">
                        <small>最多一次导入 100 首歌曲</small>
                    </div>

                    <div class="modal-actions">
                        <button type="button" class="btn btn-secondary" onclick="closeArtistImportDialog()">
                            取消
                        </button>
                        <button type="submit" class="btn btn-primary">
                            开始导入
                        </button>
                    </div>
                </form>

                <div id="artistImportProgress" style="display: none;">
                    <div class="progress-bar">
                        <div class="progress-fill" id="importProgressBar"></div>
                    </div>
                    <p id="importProgressText">正在导入...</p>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', dialogHtml);
}

/**
 * 关闭艺术家导入对话框
 */
function closeArtistImportDialog() {
    const modal = document.getElementById('artistImportModal');
    if (modal) {
        modal.remove();
    }
}

/**
 * 处理艺术家导入
 */
async function handleArtistImport(event) {
    event.preventDefault();

    const artistName = document.getElementById('artistImportName').value.trim();
    const limit = parseInt(document.getElementById('importLimit').value) || 50;

    if (!artistName) {
        showMessage('warning', '请输入艺术家名称');
        return;
    }

    const form = document.getElementById('artistImportForm');
    const progress = document.getElementById('artistImportProgress');
    const progressBar = document.getElementById('importProgressBar');
    const progressText = document.getElementById('importProgressText');

    try {
        // 显示进度
        form.style.display = 'none';
        progress.style.display = 'block';
        progressText.textContent = '正在从 iTunes 搜索歌曲...';
        progressBar.style.width = '30%';

        // 从 iTunes API 搜索艺术家的歌曲
        const itunesResponse = await fetch(
            `https://itunes.apple.com/search?term=${encodeURIComponent(artistName)}&entity=song&limit=${limit}`
        );

        if (!itunesResponse.ok) {
            throw new Error('iTunes API 请求失败');
        }

        const itunesData = await itunesResponse.json();

        if (!itunesData.results || itunesData.results.length === 0) {
            throw new Error('未找到该艺术家的歌曲');
        }

        progressText.textContent = `找到 ${itunesData.results.length} 首歌曲，正在导入...`;
        progressBar.style.width = '60%';

        // 转换为后端格式
        const tracksData = itunesData.results.map(track => ({
            title: track.trackName,
            artist: track.artistName,
            genre: track.primaryGenreName,
            duration_sec: track.trackTimeMillis ? Math.floor(track.trackTimeMillis / 1000) : null,
            cover_url: track.artworkUrl100 ? track.artworkUrl100.replace('100x100', '600x600') : null,
        }));

        // 批量创建
        const result = await batchCreateTracks(tracksData);

        progressBar.style.width = '100%';
        progressText.textContent = '导入完成！';

        // 显示结果
        setTimeout(() => {
            closeArtistImportDialog();
            showMessage('success',
                `成功导入 ${result.created} 首歌曲` +
                (result.skipped > 0 ? `，跳过 ${result.skipped} 首（已存在或数据不完整）` : '')
            );

            // 刷新歌曲列表
            if (typeof loadTracks === 'function') {
                loadTracks();
            }
        }, 1000);

    } catch (error) {
        console.error('艺术家导入失败:', error);
        progressText.textContent = '导入失败: ' + error.message;
        progressText.style.color = 'var(--error-color)';

        setTimeout(() => {
            form.style.display = 'block';
            progress.style.display = 'none';
            progressText.style.color = '';
        }, 3000);
    }
}

// ==================== 样式（添加到 CSS 文件）====================
/**
 * 将以下 CSS 添加到 djsetstudio-web/css/style.css 文件末尾
 */

const batchImportStyles = `
/* 批量导入工具栏 */
.batch-toolbar {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: var(--card-bg);
    border-radius: 8px;
    margin-bottom: 1rem;
    border: 2px solid var(--primary-color);
}

.checkbox-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    user-select: none;
}

.checkbox-label input[type="checkbox"] {
    width: 18px;
    height: 18px;
    cursor: pointer;
}

.selected-info {
    flex: 1;
    color: var(--text-secondary);
}

.selected-info strong {
    color: var(--primary-color);
    font-size: 1.2em;
}

/* 歌曲卡片选择状态 */
.track-card {
    position: relative;
    transition: all 0.3s ease;
}

.track-card.selected {
    border: 2px solid var(--primary-color);
    background: rgba(99, 102, 241, 0.1);
}

.track-checkbox {
    position: absolute;
    top: 10px;
    left: 10px;
    z-index: 10;
    background: rgba(0, 0, 0, 0.7);
    padding: 5px;
    border-radius: 4px;
}

.track-checkbox input[type="checkbox"] {
    width: 20px;
    height: 20px;
    cursor: pointer;
}

/* 进度条 */
.progress-bar {
    width: 100%;
    height: 8px;
    background: var(--bg-secondary);
    border-radius: 4px;
    overflow: hidden;
    margin: 1rem 0;
}

.progress-fill {
    height: 100%;
    background: var(--primary-color);
    transition: width 0.3s ease;
}

#artistImportProgress {
    padding: 1rem 0;
}

#importProgressText {
    text-align: center;
    color: var(--text-secondary);
    margin-top: 0.5rem;
}
`;

// 导出函数供其他模块使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        batchCreateTracks,
        getTracksByArtist,
        toggleTrackSelection,
        toggleSelectAll,
        handleBatchAdd,
        showArtistImportDialog,
        handleArtistImport
    };
}
