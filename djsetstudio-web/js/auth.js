// 认证模块

let isLoginMode = true;

// 初始化认证表单
function initAuth() {
    const authForm = document.getElementById('authForm');
    authForm.addEventListener('submit', handleAuthSubmit);

    // 检查是否已登录
    checkAuthStatus();
}

// 检查登录状态
function checkAuthStatus() {
    const token = getAuthToken();
    const authLink = document.getElementById('authLink');

    if (token) {
        const user = JSON.parse(localStorage.getItem(STORAGE_KEYS.user) || '{}');
        authLink.textContent = user.username || user.email || '用户';
        authLink.onclick = () => logout();
    } else {
        authLink.textContent = '登录';
        authLink.onclick = () => showPage('login');
    }
}

// 切换登录/注册模式
function toggleAuthMode() {
    isLoginMode = !isLoginMode;

    const authTitle = document.getElementById('authTitle');
    const authToggleText = document.getElementById('authToggleText');
    const usernameGroup = document.getElementById('usernameGroup');
    const submitButton = document.querySelector('#authForm button[type="submit"]');

    if (isLoginMode) {
        authTitle.textContent = '登录';
        authToggleText.textContent = '还没有账号？';
        usernameGroup.style.display = 'none';
        submitButton.textContent = '登录';
    } else {
        authTitle.textContent = '注册';
        authToggleText.textContent = '已有账号？';
        usernameGroup.style.display = 'block';
        submitButton.textContent = '注册';
    }
}

// 处理认证表单提交
async function handleAuthSubmit(e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const username = document.getElementById('username').value;

    try {
        let result;

        if (isLoginMode) {
            result = await api.login(email, password);
        } else {
            result = await api.register(email, password, username);
            // 注册成功后自动登录
            result = await api.login(email, password);
        }

        // 保存token和用户信息
        setAuthToken(result.access_token);
        localStorage.setItem(STORAGE_KEYS.user, JSON.stringify(result.user));

        // 更新UI
        checkAuthStatus();

        // 跳转到首页
        showPage('home');
        showMessage('success', isLoginMode ? '登录成功' : '注册成功');

        // 清空表单
        document.getElementById('authForm').reset();
    } catch (error) {
        showMessage('error', error.message);
    }
}

// 登出
function logout() {
    clearAuthToken();
    checkAuthStatus();
    showPage('home');
    showMessage('success', '已登出');
}

// 显示消息提示
function showMessage(type, message) {
    // 简单的alert提示，后续可以改为更美观的toast
    if (type === 'error') {
        alert('错误: ' + message);
    } else {
        alert(message);
    }
}

// 检查是否已登录
function isAuthenticated() {
    return !!getAuthToken();
}

// 需要登录才能访问的功能
function requireAuth(callback) {
    if (!isAuthenticated()) {
        showMessage('error', '请先登录');
        showPage('login');
        return false;
    }
    callback();
    return true;
}
