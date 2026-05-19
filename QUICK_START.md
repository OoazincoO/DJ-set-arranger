# 🎵 批量导入功能 - 快速开始

## 📦 包含文件

本更新包含以下文件，已生成在您的项目根目录：

```
myDJset/
├── batch_import_update.py          # 后端更新脚本（Python）
├── frontend_batch_import.js        # 前端功能代码（JavaScript）
├── batch_import_styles.css         # 前端样式代码（CSS）
├── deploy_batch_import.sh          # 一键部署脚本（Linux/Mac）
├── DEPLOYMENT.md                   # 详细部署文档
└── QUICK_START.md                  # 本文件
```

---

## ⚡ 最快部署方式（5分钟）

### 在服务器上执行：

```bash
# 1. 进入项目目录
cd /path/to/myDJset

# 2. 给部署脚本执行权限
chmod +x deploy_batch_import.sh

# 3. 运行一键部署脚本
./deploy_batch_import.sh

# 4. 完成！
```

脚本会自动：
- ✅ 备份现有文件
- ✅ 更新后端代码
- ✅ 更新前端代码
- ✅ 重启应用
- ✅ 测试 API

---

## 🎯 功能演示

### 功能 1: 搜索结果批量添加

**使用步骤：**

1. 在网站上搜索歌曲（例如搜索 "Martin Garrix"）
2. 搜索结果显示后，每首歌曲左上角会有复选框
3. 勾选想要添加的歌曲（或点击"全选"）
4. 点击"批量添加到歌曲库"按钮
5. 等待几秒，完成！

**截图示意：**
```
┌─────────────────────────────────────────┐
│ [ ✓ 全选 ]  已选择 5 首  [批量添加]     │
├─────────────────────────────────────────┤
│ [✓] 🎵 Animals - Martin Garrix          │
│ [✓] 🎵 Scared To Be Lonely - Martin..   │
│ [ ] 🎵 In The Name Of Love - Martin..   │
│ [✓] 🎵 Byte - Martin Garrix              │
│ [✓] 🎵 Poison - Martin Garrix            │
└─────────────────────────────────────────┘
```

### 功能 2: 艺术家一键导入

**使用步骤：**

1. 点击页面上的"🎤 艺术家一键导入"按钮
2. 在弹出框中输入艺术家名称（例如 "Tiësto"）
3. 设置导入数量限制（默认 50 首，最多 100 首）
4. 点击"开始导入"
5. 系统自动从 iTunes 获取该艺术家的歌曲并导入
6. 完成！

**流程示意：**
```
输入艺术家 → 从iTunes搜索 → 批量导入 → 完成
   Tiësto      找到50首歌      添加到库     ✓
```

---

## 🧪 快速测试

### 测试后端 API（在服务器上）

```bash
# 获取 JWT Token（先登录）
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"dj@example.com","password":"password123"}' \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

# 测试批量导入
curl -X POST http://localhost:5000/api/tracks/batch \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "tracks": [
      {"title": "Test Song 1", "artist": "Test Artist", "bpm": 128},
      {"title": "Test Song 2", "artist": "Test Artist", "bpm": 130}
    ]
  }'

# 测试艺术家查询
curl http://localhost:5000/api/tracks/artist/Test%20Artist
```

### 测试前端界面（在浏览器中）

1. 打开浏览器开发者工具（F12）
2. 访问您的网站
3. 清除缓存（Ctrl+Shift+R 或 Cmd+Shift+R）
4. 在控制台中输入：

```javascript
// 测试批量导入函数是否加载
typeof batchCreateTracks
// 应该返回 "function"

// 测试艺术家导入函数
typeof showArtistImportDialog
// 应该返回 "function"
```

---

## 📖 API 文档速查

### POST /api/tracks/batch

批量创建歌曲（最多 100 首）

```bash
curl -X POST {API_URL}/tracks/batch \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "tracks": [
      {
        "title": "必填 - 歌曲标题",
        "artist": "艺术家名称",
        "bpm": 128,
        "genre": "House",
        "key": "Am",
        "duration_sec": 180,
        "cover_url": "图片URL"
      }
    ]
  }'
```

**成功响应：**
```json
{
  "created": 5,
  "skipped": 0,
  "items": [...],
  "skipped_items": []
}
```

### GET /api/tracks/artist/{artist_name}

获取艺术家的所有歌曲

```bash
curl {API_URL}/tracks/artist/Martin%20Garrix
```

---

## ❓ 常见问题

### Q1: 部署后前端界面没有变化？

**解决方法：**
1. 清除浏览器缓存（Ctrl+Shift+Delete）
2. 硬性刷新（Ctrl+F5）
3. 检查浏览器控制台是否有 JavaScript 错误

### Q2: 批量添加失败，提示"请先登录"？

**解决方法：**
1. 确保已登录账号
2. 检查 JWT Token 是否过期
3. 重新登录后再试

### Q3: iTunes API 搜索不到歌曲？

**可能原因：**
1. 艺术家名称拼写错误
2. iTunes 没有该艺术家的歌曲
3. 网络连接问题

**解决方法：**
- 尝试使用英文名称
- 尝试不同的关键词

### Q4: 批量添加时部分歌曲被跳过？

**这是正常的！**系统会自动跳过：
- 标题为空的歌曲
- 已存在的歌曲（相同标题+艺术家）

查看响应中的 `skipped_items` 了解详情。

### Q5: 如何回滚更新？

```bash
# 备份文件在 backups/ 目录
ls backups/

# 恢复指定日期的备份
BACKUP_DATE=20231219_143022  # 替换为你的备份时间

cp backups/$BACKUP_DATE/tracks.py djsetstudio-backend/routes/tracks.py
cp backups/$BACKUP_DATE/tracks.js.frontend djsetstudio-web/js/tracks.js
cp backups/$BACKUP_DATE/style.css djsetstudio-web/css/style.css

# 重启应用
sudo systemctl restart djsetstudio
```

---

## 🎨 自定义样式

如果您想修改批量导入界面的样式：

编辑 `djsetstudio-web/css/style.css`，找到批量导入相关的 CSS：

```css
/* 修改主题色 */
.batch-toolbar {
    border: 2px solid #YOUR_COLOR;
}

/* 修改选中状态 */
.track-card.selected {
    background: rgba(YOUR_R, YOUR_G, YOUR_B, 0.1);
}
```

---

## 📊 使用统计

部署后，您可以通过以下方式监控使用情况：

```bash
# 查看批量导入日志
tail -f djsetstudio-backend/logs/app.log | grep batch

# 统计批量导入次数
grep "POST /api/tracks/batch" djsetstudio-backend/logs/access.log | wc -l

# 查看最近的批量导入
grep "POST /api/tracks/batch" djsetstudio-backend/logs/access.log | tail -10
```

---

## 🚀 进阶使用

### 通过命令行批量导入

创建一个 JSON 文件 `tracks.json`：

```json
{
  "tracks": [
    {"title": "Song 1", "artist": "Artist 1", "bpm": 128},
    {"title": "Song 2", "artist": "Artist 2", "bpm": 130},
    {"title": "Song 3", "artist": "Artist 3", "bpm": 125}
  ]
}
```

然后执行：

```bash
TOKEN="your_jwt_token"

curl -X POST http://your-server/api/tracks/batch \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d @tracks.json
```

### 从 CSV 转换并导入

```python
import csv
import json
import requests

# 读取 CSV
tracks = []
with open('tracks.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tracks.append({
            'title': row['title'],
            'artist': row['artist'],
            'bpm': float(row['bpm']) if row.get('bpm') else None,
            'genre': row.get('genre'),
        })

# 批量导入
response = requests.post(
    'http://your-server/api/tracks/batch',
    headers={
        'Authorization': f'Bearer {your_token}',
        'Content-Type': 'application/json'
    },
    json={'tracks': tracks}
)

print(response.json())
```

---

## 📝 更新日志

### v1.0 - 2024-12-19

**新增功能：**
- ✨ 搜索结果批量添加（支持全选/多选）
- ✨ 艺术家一键导入（从 iTunes）
- ✨ 批量创建 API（最多 100 首）
- ✨ 自动去重（跳过已存在歌曲）
- ✨ 进度提示和错误处理

**后端改进：**
- POST /api/tracks/batch - 批量创建歌曲
- GET /api/tracks/artist/:name - 查询艺术家歌曲

**前端改进：**
- 搜索结果页面添加复选框
- 批量操作工具栏
- 艺术家导入对话框
- 进度条显示

---

## 🤝 获取帮助

如果遇到问题：

1. **查看详细文档**: 阅读 `DEPLOYMENT.md`
2. **检查日志**: `tail -f djsetstudio-backend/logs/app.log`
3. **测试 API**: 使用上面提供的测试命令
4. **回滚更新**: 使用备份文件恢复

---

## 🎉 完成！

恭喜您成功部署批量导入功能！现在您可以：

- ✅ 快速批量添加搜索结果
- ✅ 一键导入整个艺术家的歌曲库
- ✅ 节省大量手动添加时间

**享受更高效的音乐管理体验！** 🎧
