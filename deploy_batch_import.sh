#!/bin/bash

###############################################################################
# DJset Studio - 批量导入功能一键部署脚本
#
# 使用方法：
# 1. 上传此脚本和相关文件到服务器
# 2. chmod +x deploy_batch_import.sh
# 3. ./deploy_batch_import.sh
###############################################################################

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否在正确的目录
check_directory() {
    print_info "检查当前目录..."

    if [ ! -d "djsetstudio-backend" ]; then
        print_error "未找到 djsetstudio-backend 目录"
        print_error "请在项目根目录下运行此脚本"
        exit 1
    fi

    if [ ! -d "djsetstudio-web" ]; then
        print_error "未找到 djsetstudio-web 目录"
        exit 1
    fi

    print_success "目录检查通过"
}

# 备份现有文件
backup_files() {
    print_info "创建备份..."

    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"

    # 备份后端文件
    if [ -f "djsetstudio-backend/routes/tracks.py" ]; then
        cp djsetstudio-backend/routes/tracks.py "$BACKUP_DIR/tracks.py"
        print_success "已备份 tracks.py"
    fi

    # 备份前端文件
    if [ -f "djsetstudio-web/js/tracks.js" ]; then
        cp djsetstudio-web/js/tracks.js "$BACKUP_DIR/tracks.js.frontend"
        print_success "已备份 tracks.js"
    fi

    if [ -f "djsetstudio-web/css/style.css" ]; then
        cp djsetstudio-web/css/style.css "$BACKUP_DIR/style.css"
        print_success "已备份 style.css"
    fi

    print_success "备份完成，保存在 $BACKUP_DIR"
}

# 更新后端
update_backend() {
    print_info "更新后端代码..."

    cd djsetstudio-backend

    if [ ! -f "../batch_import_update.py" ]; then
        print_error "未找到 batch_import_update.py 文件"
        exit 1
    fi

    python ../batch_import_update.py

    if [ $? -eq 0 ]; then
        print_success "后端更新成功"
    else
        print_error "后端更新失败"
        exit 1
    fi

    cd ..
}

# 更新前端 JavaScript
update_frontend_js() {
    print_info "更新前端 JavaScript..."

    if [ ! -f "frontend_batch_import.js" ]; then
        print_error "未找到 frontend_batch_import.js 文件"
        exit 1
    fi

    # 复制到 Web 目录
    cp frontend_batch_import.js djsetstudio-web/js/batch-import.js
    print_success "JavaScript 文件已复制"

    # 检查是否需要更新 index.html
    if ! grep -q "batch-import.js" djsetstudio-web/index.html; then
        print_warning "请手动在 index.html 中添加以下代码："
        echo ""
        echo '<script src="js/batch-import.js"></script>'
        echo ""
    else
        print_success "index.html 已包含引用"
    fi
}

# 更新前端 CSS
update_frontend_css() {
    print_info "更新前端 CSS..."

    if [ ! -f "batch_import_styles.css" ]; then
        print_error "未找到 batch_import_styles.css 文件"
        exit 1
    fi

    # 追加到现有 CSS
    cat batch_import_styles.css >> djsetstudio-web/css/style.css
    print_success "CSS 样式已更新"
}

# 重启 Flask 应用
restart_flask() {
    print_info "重启 Flask 应用..."

    # 尝试不同的重启方式
    if systemctl is-active --quiet djsetstudio; then
        print_info "使用 systemd 重启..."
        sudo systemctl restart djsetstudio
        sleep 2

        if systemctl is-active --quiet djsetstudio; then
            print_success "Flask 应用重启成功"
        else
            print_error "Flask 应用重启失败"
            print_info "请手动重启应用"
        fi
    elif [ -f "deployment/docker-compose.yml" ]; then
        print_info "使用 Docker Compose 重启..."
        cd deployment
        docker-compose restart backend
        cd ..
        print_success "Docker 容器重启成功"
    else
        print_warning "未检测到自动重启方式"
        print_info "请手动重启 Flask 应用"
        print_info "方法 1: sudo systemctl restart djsetstudio"
        print_info "方法 2: cd djsetstudio-backend && pkill -f app.py && nohup python app.py &"
    fi
}

# 测试 API
test_api() {
    print_info "测试 API 端点..."

    # 等待应用启动
    sleep 3

    # 测试健康检查
    if curl -s http://localhost:5000/health > /dev/null; then
        print_success "API 健康检查通过"
    else
        print_warning "无法连接到 API，请检查应用是否正常运行"
    fi
}

# 显示完成信息
show_completion() {
    echo ""
    echo "=========================================="
    print_success "批量导入功能部署完成！"
    echo "=========================================="
    echo ""
    print_info "新增功能："
    echo "  1. ✅ 搜索结果批量添加"
    echo "  2. ✅ 艺术家一键导入"
    echo ""
    print_info "新增 API："
    echo "  • POST /api/tracks/batch - 批量创建歌曲"
    echo "  • GET /api/tracks/artist/<name> - 获取艺术家歌曲"
    echo ""
    print_info "前端界面："
    echo "  • 搜索结果页面新增复选框和全选功能"
    echo "  • 新增\"艺术家一键导入\"按钮"
    echo ""
    print_warning "请注意："
    echo "  1. 在浏览器中清除缓存后访问网站"
    echo "  2. 检查 index.html 是否包含 batch-import.js 引用"
    echo "  3. 查看 DEPLOYMENT.md 了解详细文档"
    echo ""
    print_info "测试命令："
    echo "  curl -X POST http://your-server/api/tracks/batch \\"
    echo "    -H 'Content-Type: application/json' \\"
    echo "    -H 'Authorization: Bearer TOKEN' \\"
    echo "    -d '{\"tracks\": [{\"title\": \"Test\", \"artist\": \"Artist\"}]}'"
    echo ""
    print_info "回滚方法："
    echo "  备份文件保存在: $BACKUP_DIR"
    echo "  执行: cp $BACKUP_DIR/* 到对应位置"
    echo ""
}

# 主函数
main() {
    echo ""
    echo "╔════════════════════════════════════════════╗"
    echo "║  DJset Studio - 批量导入功能部署脚本       ║"
    echo "╚════════════════════════════════════════════╝"
    echo ""

    # 检查目录
    check_directory

    # 备份文件
    backup_files

    # 更新后端
    update_backend

    # 更新前端
    update_frontend_js
    update_frontend_css

    # 重启应用
    restart_flask

    # 测试 API
    test_api

    # 显示完成信息
    show_completion
}

# 执行主函数
main
