# DJset Studio Android App

Android原生客户端应用，使用Kotlin + Retrofit + Material Design开发。

## 项目结构

```
app/
├── build.gradle                 # 应用级Gradle配置
├── src/main/
│   ├── AndroidManifest.xml     # Android清单文件
│   ├── java/com/djsetstudio/
│   │   ├── data/
│   │   │   ├── model/          # 数据模型
│   │   │   ├── api/            # API接口和Retrofit客户端
│   │   │   └── repository/     # 数据仓库
│   │   └── ui/                 # UI层（Activity/Fragment）
│   └── res/                    # 资源文件
```

## 技术栈

- **语言**: Kotlin
- **网络库**: Retrofit + OkHttp
- **异步处理**: Kotlin Coroutines
- **架构**: Repository Pattern
- **UI**: Material Design Components

## 配置说明

### 1. 修改API地址

在 `RetrofitClient.kt` 中修改 `BASE_URL`:

```kotlin
// 生产环境
private const val BASE_URL = "https://your-api-domain.com/api/"

// 本地测试（Android模拟器访问本机）
private const val BASE_URL = "http://10.0.2.2:5000/api/"

// 本地测试（真机访问，使用电脑的局域网IP）
private const val BASE_URL = "http://192.168.x.x:5000/api/"
```

### 2. 构建项目

```bash
# 使用Android Studio打开项目
# 或使用命令行构建

# 构建Debug版本
./gradlew assembleDebug

# 构建Release版本
./gradlew assembleRelease

# 安装到设备
./gradlew installDebug
```

### 3. 权限说明

应用需要以下权限：
- `INTERNET` - 网络访问
- `ACCESS_NETWORK_STATE` - 网络状态检测

## 主要功能

- ✅ 用户登录/注册
- ✅ 浏览DJ Sets列表
- ✅ 查看Set详情
- ✅ 搜索歌曲
- ✅ 智能推荐

## 使用说明

1. 首次打开需要登录
2. 登录后可以浏览所有Sets
3. 点击Set可以查看详细信息和曲目列表
4. 支持离线存储token，无需重复登录

## 开发说明

### 添加新功能

1. 在 `ApiService.kt` 中添加新的API接口
2. 在 `Repository` 中实现业务逻辑
3. 在 `Activity` 或 `Fragment` 中调用Repository方法

### 网络请求示例

```kotlin
lifecycleScope.launch {
    val result = repository.getSets()
    result.onSuccess { sets ->
        // 处理成功结果
    }.onFailure { error ->
        // 处理错误
    }
}
```

## 依赖库

- Retrofit: 2.9.0
- OkHttp: 4.12.0
- Kotlin Coroutines: 1.7.3
- Material Components: 1.11.0
- Glide: 4.16.0

## 注意事项

1. 确保后端API已启动并可访问
2. Android 9.0+ 需要在清单文件中允许明文流量（开发环境）
3. 建议使用HTTPS（生产环境）
4. Token会自动保存在SharedPreferences中

## 待实现功能

- [ ] RecyclerView Adapter实现
- [ ] Set详情页UI
- [ ] 登录页UI
- [ ] 搜索功能UI
- [ ] 推荐功能UI
- [ ] 下拉刷新
- [ ] 加载更多
- [ ] 错误重试

## 联系方式

遇到问题请查看项目主README或提交Issue。
