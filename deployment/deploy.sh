#!/bin/bash

# DJset Studio 部署脚本

echo "========================================"
echo "DJset Studio 部署脚本"
echo "========================================"

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: 未安装Docker，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: 未安装docker-compose，请先安装docker-compose"
    exit 1
fi

# 检查.env文件
if [ ! -f .env ]; then
    echo "警告: 未找到.env文件"
    echo "正在从.env.example创建.env文件..."
    cp .env.example .env
    echo "请编辑.env文件并配置相关参数，然后重新运行此脚本"
    exit 1
fi

# 停止并删除旧容器
echo ""
echo "停止旧容器..."
docker-compose down

# 构建并启动服务
echo ""
echo "启动服务..."
docker-compose up -d --build

# 等待数据库启动
echo ""
echo "等待数据库启动..."
sleep 5

# 初始化数据库
echo ""
echo "初始化数据库..."
docker exec djset_backend python init_db.py

# 显示服务状态
echo ""
echo "========================================"
echo "部署完成！"
echo "========================================"
echo ""
docker-compose ps

echo ""
echo "访问地址:"
echo "- Web前端: http://localhost"
echo "- API文档: http://localhost/api/"
echo ""
echo "查看日志: docker-compose logs -f"
echo "停止服务: docker-compose down"
