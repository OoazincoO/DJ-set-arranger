? 系统设计文档（SDD）
项目名称：智能歌单生成与 DJ Set 展示平台  
版本：V1.3（整合版）  
编写人：坚铭  
日期：2025-12

1. 引言
1.1 文档目的
本系统设计文档用于描述系统的整体架构、模块设计、数据库结构、接口规范、部署方式等，为开发、测试和维护提供技术依据。

1.2 适用范围
适用于后端开发、前端开发、安卓开发、测试人员、项目管理人员。

2. 系统总体设计
2.1 系统架构概述
系统采用 前后端分离 + RESTful API + 跨平台客户端 的架构。

? 架构组成
Web 前端（在线网站）

Android 原生 App（真机运行）

Flask 后端 API 服务

PostgreSQL 数据库

Nginx 反向代理与静态资源托管

2.2 架构分层
表示层（Web / Android）
Web：HTML/CSS/JS（未来可升级为 React/Vue）

Android：Kotlin/Java + Retrofit

业务逻辑层（Flask Services）
用户服务

歌曲服务

推荐服务

Set 管理服务

数据访问层（SQLAlchemy ORM）
数据库模型

查询与事务管理

存储层（PostgreSQL）
用户表

歌曲表

Set 表

Set-Track 关联表

3. 模块设计
? 3.1 用户模块
功能：
注册、登录

Token 鉴权

用户信息管理

设计：
使用 JWT

密码使用 bcrypt 加密

Token 通过 Authorization Header 传递

? 3.2 歌曲模块
功能：
搜索歌曲

添加歌曲到曲库

获取歌曲详情

设计：
搜索使用模糊匹配

歌曲信息包含：名称、艺术家、BPM、风格、封面

支持分页

? 3.3 推荐模块
功能：
相似歌曲推荐

智能歌单生成

设计：
使用 embedding（如 Spotify 模型或自建标签体系）

相似度计算：Cosine Similarity

推荐数量可配置

? 3.4 DJ Set 模块
功能：
创建 Set

编辑 Set

展示 Set

曲目排序

设计：
Set 与 Track 多对多关系

支持封面上传（未来版本）

支持顺序字段 order

? 3.5 跨平台模块
3.5.1 Web 端（在线网站）
部署在服务器上

使用 Axios 调用后端 API

使用 HTTPS

3.5.2 Android 原生 App
使用 Retrofit 调用线上 API

与 Web 端共享账号体系

支持 Token 自动刷新（未来版本）

4. 数据库设计
4.1 ER 图（文字版）
Code
Users (1) —— (N) Sets —— (N) Set_Tracks —— (N) Tracks
4.2 表结构
users
字段	类型	描述
id	int	主键
email	string	邮箱
password	string	加密密码
created_at	datetime	注册时间
tracks
字段	类型	描述
id	int	主键
name	string	歌名
artist	string	艺术家
bpm	int	BPM
genre	string	风格
cover_url	string	封面链接
sets
字段	类型	描述
id	int	主键
user_id	int	所属用户
name	string	Set 名称
description	string	描述
cover_url	string	封面
created_at	datetime	创建时间
set_tracks
字段	类型	描述
id	int	主键
set_id	int	Set
track_id	int	Track
order	int	顺序
5. API 设计（核心）
? 用户相关
Code
POST /auth/register
POST /auth/login
GET  /auth/me
? 歌曲相关
Code
GET  /tracks/search
POST /tracks/add
GET  /tracks/{id}
? Set 相关
Code
POST /sets/create
GET  /sets/{id}
PUT  /sets/{id}
DELETE /sets/{id}
6. 部署设计（整合版）
? Web 端部署
使用 Nginx 托管静态资源

或使用 Vercel / Netlify

? 后端部署
使用 Gunicorn + Nginx

部署到云服务器（阿里云 / 腾讯云）

使用 HTTPS

? 数据库部署
PostgreSQL

使用 Docker 或云数据库