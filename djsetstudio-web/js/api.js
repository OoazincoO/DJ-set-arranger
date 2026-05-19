// API调用工具模块

// 获取认证token
function getAuthToken() {
    return localStorage.getItem(STORAGE_KEYS.token);
}

// 设置认证token
function setAuthToken(token) {
    localStorage.setItem(STORAGE_KEYS.token, token);
}

// 清除认证token
function clearAuthToken() {
    localStorage.removeItem(STORAGE_KEYS.token);
    localStorage.removeItem(STORAGE_KEYS.user);
}

// 通用API请求函数
async function apiRequest(url, options = {}) {
    const token = getAuthToken();

    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(url, {
            ...options,
            headers,
        });

        if (response.status === 401) {
            // Token过期或无效，清除并跳转到登录页
            clearAuthToken();
            showPage('login');
            throw new Error('未授权，请重新登录');
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || '请求失败');
        }

        return data;
    } catch (error) {
        console.error('API请求错误:', error);
        throw error;
    }
}

// API调用方法
const api = {
    // 用户注册
    register: async (email, password, username) => {
        return apiRequest(API_ENDPOINTS.register, {
            method: 'POST',
            body: JSON.stringify({ email, password, username }),
        });
    },

    // 用户登录
    login: async (email, password) => {
        return apiRequest(API_ENDPOINTS.login, {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        });
    },

    // 获取当前用户信息
    getCurrentUser: async () => {
        return apiRequest(API_ENDPOINTS.me);
    },

    // 获取所有歌曲
    getTracks: async () => {
        return apiRequest(API_ENDPOINTS.tracks);
    },

    // 搜索歌曲
    searchTracks: async (params) => {
        const queryParams = new URLSearchParams();
        if (params.keyword) queryParams.append('keyword', params.keyword);
        if (params.artist) queryParams.append('artist', params.artist);
        if (params.genre) queryParams.append('genre', params.genre);
        if (params.min_bpm) queryParams.append('min_bpm', params.min_bpm);
        if (params.max_bpm) queryParams.append('max_bpm', params.max_bpm);

        const url = `${API_ENDPOINTS.tracksSearch}?${queryParams.toString()}`;
        return apiRequest(url);
    },

    // 创建歌曲
    createTrack: async (trackData) => {
        return apiRequest(API_ENDPOINTS.tracks, {
            method: 'POST',
            body: JSON.stringify(trackData),
        });
    },

    // 获取歌曲详情
    getTrack: async (id) => {
        return apiRequest(API_ENDPOINTS.trackDetail(id));
    },

    // 获取歌曲推荐
    getTrackRecommendations: async (id, limit = 10) => {
        const url = `${API_ENDPOINTS.trackRecommend(id)}?limit=${limit}`;
        return apiRequest(url);
    },

    // 删除歌曲
    deleteTrack: async (id) => {
        return apiRequest(API_ENDPOINTS.trackDetail(id), {
            method: 'DELETE',
        });
    },

    // 获取所有Sets
    getSets: async () => {
        return apiRequest(API_ENDPOINTS.sets);
    },

    // 创建Set
    createSet: async (setData) => {
        return apiRequest(API_ENDPOINTS.sets, {
            method: 'POST',
            body: JSON.stringify(setData),
        });
    },

    // 获取Set详情
    getSet: async (id) => {
        return apiRequest(API_ENDPOINTS.setDetail(id));
    },

    // 更新Set
    updateSet: async (id, setData) => {
        return apiRequest(API_ENDPOINTS.setDetail(id), {
            method: 'PUT',
            body: JSON.stringify(setData),
        });
    },

    // 删除Set
    deleteSet: async (id) => {
        return apiRequest(API_ENDPOINTS.setDetail(id), {
            method: 'DELETE',
        });
    },

    // 获取Set推荐
    getSetRecommendations: async (id, limit = 10) => {
        return apiRequest(API_ENDPOINTS.setRecommend(id), {
            method: 'POST',
            body: JSON.stringify({ limit }),
        });
    },

    // 获取Set的tracks
    getSetTracks: async (id) => {
        return apiRequest(API_ENDPOINTS.setTracks(id));
    },
};
