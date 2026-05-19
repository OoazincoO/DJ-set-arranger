# 🎵 批量导入功能部署指南

## 📦 文件说明

本次更新包含以下文件：

1. **batch_import_update.py** - 后端更新脚本
2. **frontend_batch_import.js** - 前端功能代码
3. **batch_import_styles.css** - 前端样式代码
4. **DEPLOYMENT.md** - 本文档

---

## 🚀 服务器端部署步骤

### 步骤 1: 上传文件到服务器

```bash
# 在本地执行，将文件上传到服务器
scp batch_import_update.py your_user@your_server:/path/to/djsetstudio-backend/
```

### 步骤 2: 连接到服务器

```bash
ssh your_user@your_server
cd /path/to/djsetstudio-backend
```

### 步骤 3: 备份现有代码

```bash
# 创建备份目录
mkdir -p backups/$(date +%Y%m%d)

# 备份当前的 routes/tracks.py
cp routes/tracks.py backups/$(date +%Y%m%d)/tracks.py.backup
```

### 步骤 4: 运行更新脚本

```bash
# 确保在 djsetstudio-backend 目录下
python batch_import_update.py
```

**预期输出：**
```
============================================================
DJset Studio - 批量导入功能更新脚本
============================================================

✓ 已备份原文件到: routes/tracks.py.backup.20231219_143022
✓ 已更新 routes/tracks.py

新增的API接口:
  1. POST /api/tracks/batch - 批量创建歌曲
  2. GET /api/tracks/artist/<artist_name> - 获取艺术家的所有歌曲

✓ 更新完成！
```

### 步骤 5: 重启 Flask 应用

**方法 1: 使用 systemd（推荐）**
```bash
sudo systemctl restart djsetstudio
sudo systemctl status djsetstudio
```

**方法 2: 使用 Docker**
```bash
cd /path/to/deployment
docker-compose restart backend
docker-compose logs -f backend
```

**方法 3: 手动重启**
```bash
# 停止现有进程
pkill -f 'python.*app.py'

# 重新启动
cd /path/to/djsetstudio-backend
nohup python app.py > logs/app.log 2>&1 &
```

### 步骤 6: 测试后端 API

```bash
# 测试批量导入接口
curl -X POST http://your-server/api/tracks/batch \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "tracks": [
      {
        "title": "Test Song 1",
        "artist": "Test Artist",
        "bpm": 128,
        "genre": "House"
      },
      {
        "title": "Test Song 2",
        "artist": "Test Artist",
        "bpm": 130,
        "genre": "House"
      }
    ]
  }'

# 测试艺术家查询接口
curl http://your-server/api/tracks/artist/Test%20Artist
```

**预期响应：**
```json
{
  "created": 2,
  "skipped": 0,
  "items": [
    {
      "id": 123,
      "title": "Test Song 1",
      "artist": "Test Artist",
      "bpm": 128,
      "genre": "House",
      "cover_url": null
    },
    {
      "id": 124,
      "title": "Test Song 2",
      "artist": "Test Artist",
      "bpm": 130,
      "genre": "House",
      "cover_url": null
    }
  ],
  "skipped_items": []
}
```

---

## 💻 前端部署步骤

### 步骤 1: 更新 JavaScript 文件

**方法 1: 创建新的 JS 文件（推荐）**

```bash
# 将 frontend_batch_import.js 上传到服务器
scp frontend_batch_import.js your_user@your_server:/path/to/djsetstudio-web/js/batch-import.js
```

然后在 `index.html` 中添加引用：

```html
<!-- 在 </body> 标签前添加 -->
<script src="js/batch-import.js"></script>
```

**方法 2: 追加到现有文件**

```bash
# 在服务器上执行
cd /path/to/djsetstudio-web/js

# 备份原文件
cp tracks.js tracks.js.backup

# 追加新代码到 tracks.js
cat /path/to/frontend_batch_import.js >> tracks.js
```

### 步骤 2: 更新 CSS 样式

```bash
# 上传 CSS 文件
scp batch_import_styles.css your_user@your_server:/tmp/

# 在服务器上追加到现有样式文件
cd /path/to/djsetstudio-web/css
cp style.css style.css.backup
cat /tmp/batch_import_styles.css >> style.css
```

### 步骤 3: 更新 HTML 界面

在 `djsetstudio-web/index.html` 中添加批量导入按钮。

找到歌曲搜索部分，在搜索按钮后添加：

```html
<!-- 在搜索表单后添加 -->
<div class="actions" style="margin-top: 1rem;">
    <button class="btn btn-primary" onclick="showArtistImportDialog()">
        🎤 艺术家一键导入
    </button>
</div>
```

### 步骤 4: 修改搜索结果显示

在 `tracks.js` 的 `searchTracks()` 函数中，将：

```javascript
displayTracks(result.items, 'searchResults');
```

改为：

```javascript
renderTracksWithSelection(result.items, 'searchResults');
```

### 步骤 5: 清除浏览器缓存并测试

在浏览器中：
1. 打开开发者工具（F12）
2. 右键点击刷新按钮，选择"清空缓存并硬性重新加载"
3. 测试功能

---

## 🧪 功能测试清单

### 后端 API 测试

- [ ] POST /api/tracks/batch 接口可以批量创建歌曲
- [ ] 批量创建时会跳过已存在的歌曲
- [ ] 批量创建时会跳过标题为空的歌曲
- [ ] 一次最多只能创建 100 首歌曲
- [ ] GET /api/tracks/artist/<name> 可以搜索艺术家
- [ ] 艺术家搜索支持模糊匹配

### 前端功能测试

- [ ] 搜索结果显示复选框
- [ ] 可以单选/多选歌曲
- [ ] "全选"按钮工作正常
- [ ] 已选择数量正确显示
- [ ] "批量添加"按钮在未选择时禁用
- [ ] 批量添加成功后清空选择
- [ ] "艺术家一键导入"按钮显示
- [ ] 艺术家导入对话框正常打开
- [ ] 输入艺术家名称可以从 iTunes 获取歌曲
- [ ] 进度条显示正常
- [ ] 导入成功后刷新歌曲列表

---

## 🔧 故障排查

### 后端问题

**问题 1: 更新脚本找不到文件**
```bash
# 确认当前目录
pwd
# 应该在 djsetstudio-backend 目录下

# 检查文件结构
ls -la routes/tracks.py
```

**问题 2: Flask 应用无法启动**
```bash
# 查看错误日志
tail -f logs/app.log

# 或者
journalctl -u djsetstudio -f

# 检查语法错误
python -m py_compile routes/tracks.py
```

**问题 3: API 返回 404**
```bash
# 确认 Flask 应用已重启
ps aux | grep python | grep app.py

# 检查路由注册
grep "tracks_bp" app.py
```

### 前端问题

**问题 1: 功能按钮不显示**
- 检查浏览器控制台是否有 JavaScript 错误
- 确认 `batch-import.js` 已正确加载
- 清除浏览器缓存

**问题 2: 批量添加失败**
```javascript
// 在浏览器控制台执行
console.log(API_BASE_URL);  // 确认 API 地址正确
console.log(localStorage.getItem('token'));  // 确认已登录
```

**问题 3: 样式不正确**
- 检查 CSS 文件是否正确追加
- 确认没有 CSS 语法错误
- 清除浏览器缓存

---

## 📝 API 文档

### POST /api/tracks/batch

批量创建歌曲

**请求头：**
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**请求体：**
```json
{
  "tracks": [
    {
      "title": "歌曲标题",
      "artist": "艺术家名称",
      "bpm": 128,
      "genre": "音乐风格",
      "key": "音乐调性",
      "duration_sec": 180,
      "cover_url": "封面图片URL"
    }
  ]
}
```

**响应（201）：**
```json
{
  "created": 5,
  "skipped": 2,
  "items": [...],
  "skipped_items": [
    {
      "index": 3,
      "title": "重复的歌曲",
      "reason": "track already exists",
      "existing_id": 123
    }
  ]
}
```

### GET /api/tracks/artist/:artist_name

获取指定艺术家的所有歌曲

**响应（200）：**
```json
{
  "artist": "Martin Garrix",
  "items": [...],
  "count": 15
}
```

---

## 🔄 回滚方案

如果更新出现问题，可以快速回滚：

### 回滚后端

```bash
cd /path/to/djsetstudio-backend

# 查看备份文件
ls -la routes/tracks.py.backup.*

# 恢复最新备份
cp routes/tracks.py.backup.YYYYMMDD_HHMMSS routes/tracks.py

# 重启应用
sudo systemctl restart djsetstudio
```

### 回滚前端

```bash
cd /path/to/djsetstudio-web

# 恢复 JS
cp js/tracks.js.backup js/tracks.js

# 恢复 CSS
cp css/style.css.backup css/style.css

# 清除浏览器缓存并刷新
```

---

## 📞 支持

如果在部署过程中遇到问题：

1. 检查服务器日志
2. 确认 Python 版本 >= 3.11
3. 确认所有依赖已安装
4. 检查防火墙和端口配置

---

## ✅ 部署完成检查

部署完成后，确认以下功能正常：

- [ ] 后端 API 正常响应
- [ ] 批量导入功能可用
- [ ] 艺术家一键导入可用
- [ ] 原有功能未受影响
- [ ] 移动端界面正常
- [ ] 性能无明显下降

---

**祝您部署顺利！** 🎉
