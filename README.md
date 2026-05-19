# 🎧 DJset Studio - 智能歌单生成与DJ Set展示平台

一个跨平台的智能音乐管理平台，支持在线Web网站与Android原生App，提供歌曲搜索、智能推荐、DJ Set创建与展示等功能。

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Kotlin](https://img.shields.io/badge/Kotlin-1.9+-purple.svg)](https://kotlinlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 目录

- [项目概述](#项目概述)
- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [开发指南](#开发指南)
- [部署指南](#部署指南)
- [API文档](#api文档)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 🌟 项目概述

DJset Studio是一个专为DJ和音乐爱好者设计的智能音乐管理平台。它提供了强大的歌曲管理、智能推荐和Set展示功能，让你轻松构建属于自己的音乐世界。

### 设计文档

- [产品需求文档 (PRD)](DJsetstudio（PRD）.md)
- [系统设计文档 (SDD)](DJsetstudio(SDD).md)

## ✨ 功能特性

### 核心功能

- 🎵 **智能推荐** - 基于BPM和风格的智能歌曲推荐算法
- 📝 **Set管理** - 创建和管理你的DJ Set，支持曲目排序
- 🔍 **强大搜索** - 支持关键词、艺术家、风格、BPM多维度筛选
- 👤 **用户系统** - 安全的邮箱注册登录，JWT Token鉴权
- 🎨 **精美UI** - 现代化的深色主题界面设计
- 📱 **跨平台** - Web端 + Android原生App

### 推荐算法

- 基于种子歌曲的BPM相似度匹配（±10 BPM容差）
- 音乐风格（Genre）智能匹配
- 支持多首种子歌曲的综合推荐
- 智能补充推荐结果

## 🛠 技术栈

### 后端

- **框架**: Flask 3.0+
- **数据库**: PostgreSQL / SQLite
- **ORM**: SQLAlchemy
- **认证**: Flask-JWT-Extended
- **API**: RESTful API
- **服务器**: Gunicorn

### Web前端

- **核心**: HTML5 + CSS3 + JavaScript (ES6+)
- **样式**: 原生CSS，深色主题
- **请求**: Fetch API
- **架构**: 模块化设计

### Android App

- **语言**: Kotlin
- **网络**: Retrofit + OkHttp
- **异步**: Kotlin Coroutines
- **架构**: Repository Pattern
- **UI**: Material Design

### 部署

- **容器化**: Docker + Docker Compose
- **反向代理**: Nginx
- **HTTPS**: Let's Encrypt

## 📁 项目结构

```
myDJset/
├── djsetstudio-backend/        # Flask后端
│   ├── app.py                  # 应用入口
│   ├── models.py               # 数据模型
│   ├── routes/                 # 路由模块
│   │   ├── auth.py            # 认证接口
│   │   ├── tracks.py          # 歌曲接口
│   │   └── sets.py            # Set接口
│   ├── services/               # 业务逻辑
│   │   └── recommender.py     # 推荐算法
│   ├── config.py               # 配置文件
│   ├── extensions.py           # 扩展初始化
│   ├── init_db.py             # 数据库初始化
│   └── requirements.txt        # Python依赖
│
├── djsetstudio-web/            # Web前端
│   ├── index.html             # 主页面
│   ├── css/
│   │   └── style.css          # 样式文件
│   └── js/
│       ├── config.js          # 配置
│       ├── api.js             # API调用
│       ├── auth.js            # 认证模块
│       ├── tracks.js          # 歌曲模块
│       ├── sets.js            # Set模块
│       └── app.js             # 主应用
│
├── djsetstudio-android/        # Android App
│   ├── app/
│   │   ├── build.gradle       # 构建配置
│   │   └── src/main/
│   │       ├── AndroidManifest.xml
│   │       └── java/com/djsetstudio/
│   │           ├── data/      # 数据层
│   │           └── ui/        # UI层
│   └── README.md              # Android文档
│
├── deployment/                 # 部署配置
│   ├── nginx.conf             # Nginx配置
│   ├── Dockerfile             # Docker镜像
│   ├── docker-compose.yml     # 容器编排
│   ├── deploy.sh              # 部署脚本
│   └── README.md              # 部署文档
│
├── DJsetstudio（PRD）.md       # 产品需求文档
├── DJsetstudio(SDD).md        # 系统设计文档
└── README.md                   # 本文件
```

## 🚀 快速开始

### 前置要求

- Python 3.11+
- Node.js 16+ (可选，用于前端构建工具)
- PostgreSQL 14+ (生产环境)
- Android Studio (如果需要构建Android App)

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/djsetstudio.git
cd djsetstudio
```

### 2. 启动后端

```bash
cd djsetstudio-backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，配置数据库等参数

# 初始化数据库（创建示例数据）
python init_db.py

# 启动服务
python app.py
```

后端服务将在 http://localhost:5000 启动

### 3. 启动Web前端

```bash
cd djsetstudio-web

# 方式1: 使用Python SimpleHTTPServer
python -m http.server 8000

# 方式2: 使用Node.js http-server
npx http-server -p 8000

# 方式3: 直接用浏览器打开
# 打开 index.html 文件
```

Web前端将在 http://localhost:8000 启动

### 4. 配置Web前端API地址

编辑 `djsetstudio-web/js/config.js`：

```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

### 5. 测试访问

1. 访问 http://localhost:8000
2. 使用测试账号登录：
   - 邮箱: dj@example.com
   - 密码: password123

## 👨‍💻 开发指南

### 后端开发

#### 添加新的API接口

1. 在 `routes/` 目录创建或编辑路由文件
2. 定义路由和处理函数
3. 在 `routes/__init__.py` 中注册蓝图

示例：
```python
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

my_bp = Blueprint("my_module", __name__)

@my_bp.get("/my-endpoint")
@jwt_required()
def my_function():
    return {"message": "Hello"}, 200
```

#### 修改数据模型

1. 编辑 `models.py`
2. 运行数据库迁移（如果使用Flask-Migrate）
3. 重新初始化数据库

#### 改进推荐算法

编辑 `services/recommender.py`，修改推荐逻辑。

### 前端开发

#### 修改UI样式

编辑 `css/style.css`，使用CSS变量可快速修改主题：

```css
:root {
    --primary-color: #6366f1;
    --bg-color: #0f172a;
    /* ... */
}
```

#### 添加新功能

1. 在对应的JS模块中添加函数
2. 在HTML中添加UI元素
3. 绑定事件处理

### Android开发

详见 [djsetstudio-android/README.md](djsetstudio-android/README.md)

## 🌐 部署指南

### 使用Docker快速部署

```bash
cd deployment

# 配置环境变量
cp .env.example .env
# 编辑.env文件

# 运行部署脚本
chmod +x deploy.sh
./deploy.sh
```

### 手动部署

详见 [deployment/README.md](deployment/README.md)

### 生产环境建议

- ✅ 使用PostgreSQL数据库
- ✅ 配置HTTPS证书
- ✅ 启用防火墙
- ✅ 设置强密码和密钥
- ✅ 配置日志和监控
- ✅ 定期备份数据
- ✅ 限制CORS来源

## 📚 API文档

### 认证接口

#### 注册
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "username": "username"  // 可选
}
```

#### 登录
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### 获取当前用户
```http
GET /api/auth/me
Authorization: Bearer <token>
```

### 歌曲接口

#### 获取所有歌曲
```http
GET /api/tracks
```

#### 搜索歌曲
```http
GET /api/tracks/search?keyword=house&min_bpm=120&max_bpm=140&genre=House
```

#### 获取歌曲推荐
```http
GET /api/tracks/{id}/recommend?limit=10
```

### Set接口

#### 获取用户的所有Sets
```http
GET /api/sets
Authorization: Bearer <token>
```

#### 创建Set
```http
POST /api/sets
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "My Summer Mix",
  "description": "Perfect for beach parties",
  "track_ids": [1, 2, 3]
}
```

#### 获取Set详情
```http
GET /api/sets/{id}
Authorization: Bearer <token>
```

#### 更新Set
```http
PUT /api/sets/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Updated Name",
  "track_ids": [1, 2, 3, 4]
}
```

#### 删除Set
```http
DELETE /api/sets/{id}
Authorization: Bearer <token>
```

完整API文档请查看代码注释或使用API测试工具（如Postman）。

## 🤝 贡献指南

欢迎贡献代码、报告Bug或提出新功能建议！

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👥 作者

- **坚铭** - *初始工作* - [GitHub](https://github.com/yourusername)

## 🙏 致谢

- Flask团队提供的优秀Web框架
- Material Design团队的设计指南
- 所有开源贡献者

## 📞 联系方式

- 项目主页: https://github.com/yourusername/djsetstudio
- 问题反馈: https://github.com/yourusername/djsetstudio/issues
- 邮箱: your.email@example.com

---

⭐ 如果这个项目对你有帮助，请给一个Star支持一下！