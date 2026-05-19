# 部署指南

本目录包含DJset Studio项目的部署配置文件。

## 文件说明

- `nginx.conf` - Nginx配置文件
- `Dockerfile` - Docker镜像构建文件
- `docker-compose.yml` - Docker Compose编排配置
- `.env.example` - 环境变量示例
- `deploy.sh` - 自动部署脚本

## 快速部署（使用Docker）

### 前提条件

- 已安装Docker和Docker Compose
- 服务器至少2GB内存

### 部署步骤

1. **准备环境变量**

```bash
cd deployment
cp .env.example .env
# 编辑.env文件，修改密码和密钥
vim .env
```

2. **运行部署脚本**

```bash
chmod +x deploy.sh
./deploy.sh
```

3. **访问应用**

- Web前端: http://your-server-ip
- API接口: http://your-server-ip:5000/api

## 手动部署

### 1. 部署PostgreSQL数据库

```bash
docker run -d \
  --name djset_postgres \
  -e POSTGRES_DB=djsetstudio \
  -e POSTGRES_USER=djsetuser \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  postgres:15-alpine
```

### 2. 部署Flask后端

```bash
cd djsetstudio-backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export DATABASE_URL="postgresql://djsetuser:your_password@localhost:5432/djsetstudio"
export SECRET_KEY="your-secret-key"
export JWT_SECRET_KEY="your-jwt-secret"

# 初始化数据库
python init_db.py

# 启动服务（开发环境）
python app.py

# 或使用Gunicorn（生产环境）
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### 3. 部署Web前端

#### 方式1: 使用Nginx

```bash
# 复制前端文件到Nginx目录
sudo cp -r djsetstudio-web /var/www/

# 复制Nginx配置
sudo cp deployment/nginx.conf /etc/nginx/sites-available/djsetstudio
sudo ln -s /etc/nginx/sites-available/djsetstudio /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

#### 方式2: 使用Python SimpleHTTPServer（仅测试）

```bash
cd djsetstudio-web
python3 -m http.server 8000
```

### 4. 配置域名（可选）

修改 `nginx.conf` 中的 `server_name`：

```nginx
server_name your-domain.com;
```

### 5. 配置HTTPS（推荐）

使用Let's Encrypt获取免费SSL证书：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## 服务管理

### Docker Compose命令

```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 查看服务状态
docker-compose ps
```

### 更新部署

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build

# 重新初始化数据库（如果模型有变化）
docker exec djset_backend python init_db.py
```

## 监控和维护

### 查看日志

```bash
# 后端日志
docker-compose logs -f backend

# 数据库日志
docker-compose logs -f db

# Nginx日志
docker-compose logs -f nginx
```

### 备份数据库

```bash
# 导出数据库
docker exec djset_postgres pg_dump -U djsetuser djsetstudio > backup_$(date +%Y%m%d).sql

# 恢复数据库
cat backup_20250101.sql | docker exec -i djset_postgres psql -U djsetuser djsetstudio
```

### 性能优化

1. **数据库优化**
   - 添加适当的索引
   - 定期VACUUM
   - 监控慢查询

2. **后端优化**
   - 增加Gunicorn worker数量
   - 启用缓存（Redis）
   - 使用连接池

3. **前端优化**
   - 启用Nginx gzip压缩
   - 配置浏览器缓存
   - 使用CDN加速静态资源

## 常见问题

### 1. 数据库连接失败

检查数据库是否启动：
```bash
docker-compose ps
docker-compose logs db
```

### 2. 端口被占用

修改docker-compose.yml中的端口映射：
```yaml
ports:
  - "8000:5000"  # 将5000改为其他端口
```

### 3. CORS错误

检查后端的CORS配置和Nginx的CORS headers。

### 4. 静态文件404

确保Nginx配置中的root路径正确。

## 安全建议

1. ✅ 修改所有默认密码
2. ✅ 使用强密钥
3. ✅ 配置防火墙
4. ✅ 定期更新依赖
5. ✅ 使用HTTPS
6. ✅ 定期备份数据
7. ✅ 限制数据库远程访问
8. ✅ 配置日志轮转

## 技术支持

遇到问题请查看主项目README或提交Issue。
