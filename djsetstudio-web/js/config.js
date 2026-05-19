// API配置
const API_BASE_URL = 'http://localhost:5000/api';

// API端点
const API_ENDPOINTS = {
    // 认证
    register: `${API_BASE_URL}/auth/register`,
    login: `${API_BASE_URL}/auth/login`,
    me: `${API_BASE_URL}/auth/me`,

    // 歌曲
    tracks: `${API_BASE_URL}/tracks`,
    tracksSearch: `${API_BASE_URL}/tracks/search`,
    trackDetail: (id) => `${API_BASE_URL}/tracks/${id}`,
    trackRecommend: (id) => `${API_BASE_URL}/tracks/${id}/recommend`,

    // Sets
    sets: `${API_BASE_URL}/sets`,
    setDetail: (id) => `${API_BASE_URL}/sets/${id}`,
    setRecommend: (id) => `${API_BASE_URL}/sets/${id}/recommend`,
    setTracks: (id) => `${API_BASE_URL}/sets/${id}/tracks`,
};

// 本地存储键名
const STORAGE_KEYS = {
    token: 'djset_token',
    user: 'djset_user',
};
