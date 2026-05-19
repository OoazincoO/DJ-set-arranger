// 主应用模块

// 页面切换
function showPage(pageId) {
    // 隐藏所有页面
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });

    // 显示目标页面
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add('active');
    }

    // 根据页面加载数据
    switch (pageId) {
        case 'tracks':
            loadTracks();
            break;
        case 'sets':
            loadSets();
            break;
        case 'home':
            // 首页不需要加载数据
            break;
    }

    // 滚动到顶部
    window.scrollTo(0, 0);
}

// 显示模态框
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

// 关闭模态框
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// 点击模态框外部关闭
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', function() {
    console.log('DJset Studio 初始化...');

    // 初始化各模块
    initAuth();
    initTracks();
    initSets();

    // 显示首页
    showPage('home');

    console.log('DJset Studio 初始化完成');
});

// 全局错误处理
window.addEventListener('error', function(e) {
    console.error('全局错误:', e.error);
});

// 添加一些便利的全局函数
window.showPage = showPage;
window.showModal = showModal;
window.closeModal = closeModal;
