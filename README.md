# 邮件自动回复系统

一个功能完整的邮件自动回复管理系统，支持多邮箱账号管理、自定义回复内容、实时日志监控。

## 功能特性

- 🔐 **安全认证** - 基于会话的登录系统
- 📧 **多邮箱管理** - 支持添加和管理多个邮箱账号
- 🤖 **自动回复** - 自动检测未读邮件并发送预设回复
- ⚙️ **灵活配置** - 自定义回复主题和内容
- 📊 **实时日志** - 完整的操作日志记录和查看
- ⏰ **定时任务** - 支持定时自动处理邮件

## 快速开始

### 1. 数据库初始化

首先运行数据库初始化脚本：

\`\`\`bash
cd init
python init_database.py
\`\`\`

这将创建 `email_auto_reply.db` 数据库文件，默认管理员账号：
- 用户名：`admin`
- 密码：`admin123`

### 2. 安装依赖

\`\`\`bash
npm install
\`\`\`

### 3. 配置环境变量

创建 `.env.local` 文件：

\`\`\`env
NEXT_PUBLIC_BASE_URL=http://localhost:3000
\`\`\`

### 4. 启动开发服务器

\`\`\`bash
npm run dev
\`\`\`

访问 http://localhost:3000 即可使用系统。

## 日志系统

### 日志存储

日志系统使用文件持久化存储，日志文件位于：

\`\`\`
/logs/app.log
\`\`\`

### 日志特性

- ✅ **自动持久化** - 日志自动保存到文件系统
- ✅ **内存缓存** - 快速读取最新日志
- ✅ **自动清理** - 最多保留 1000 条日志
- ✅ **分级记录** - 支持 INFO、WARNING、ERROR 三个级别
- ✅ **实时查看** - 在仪表盘实时查看系统日志
- ✅ **一键清空** - 支持清空所有历史日志

### 日志 API

#### 获取所有日志
\`\`\`bash
GET /api/logs
\`\`\`

#### 按级别筛选
\`\`\`bash
GET /api/logs?level=ERROR
GET /api/logs?level=WARNING
GET /api/logs?level=INFO
\`\`\`

#### 按邮箱账号筛选
\`\`\`bash
GET /api/logs?account=example@gmail.com
\`\`\`

#### 获取最近N条日志
\`\`\`bash
GET /api/logs?limit=50
\`\`\`

#### 清空所有日志
\`\`\`bash
DELETE /api/logs
\`\`\`

## 定时任务

### 手动触发

在仪表盘点击"立即处理"按钮，或访问：

\`\`\`bash
POST /api/process-emails
\`\`\`

### 服务器定时任务

使用 crontab 设置定时任务（每15分钟执行一次）：

\`\`\`bash
*/15 * * * * curl -X GET https://你的域名/api/process-emails
\`\`\`

### Vercel Cron Job

如果部署在 Vercel，系统已配置自动定时任务（每5分钟执行一次）：

\`\`\`json
{
  "crons": [{
    "path": "/api/cron",
    "schedule": "*/5 * * * *"
  }]
}
\`\`\`

## 邮箱配置

### 支持的邮箱服务

系统支持所有提供 IMAP/SMTP 服务的邮箱，常见配置：

#### Gmail
- IMAP: `imap.gmail.com:993`
- SMTP: `smtp.gmail.com:465`
- 需要开启"应用专用密码"

#### QQ邮箱
- IMAP: `imap.qq.com:993`
- SMTP: `smtp.qq.com:465`
- 需要开启IMAP/SMTP服务并获取授权码

#### 163邮箱
- IMAP: `imap.163.com:993`
- SMTP: `smtp.163.com:465`
- 需要开启IMAP/SMTP服务并获取授权码

## 项目结构

\`\`\`
├── app/
│   ├── api/              # API 路由
│   │   ├── auth/         # 认证相关
│   │   ├── email-accounts/  # 邮箱管理
│   │   ├── logs/         # 日志查询
│   │   ├── reply-config/ # 回复配置
│   │   ├── process-emails/  # 邮件处理
│   │   └── cron/         # 定时任务
│   ├── dashboard/        # 仪表盘页面
│   ├── login/            # 登录页面
│   └── page.tsx          # 首页
├── components/
│   └── dashboard/        # 仪表盘组件
├── lib/
│   ├── email-processor.ts  # 邮件处理核心逻辑
│   └── logger.ts         # 日志管理系统
├── init/
│   ├── init_database.py  # 数据库初始化脚本
│   └── README.md         # 初始化说明
└── logs/
    └── app.log           # 系统日志文件
\`\`\`

## 技术栈

- **框架**: Next.js 16 (App Router)
- **UI**: React 19 + Tailwind CSS v4
- **组件库**: shadcn/ui
- **邮件处理**: imap + nodemailer
- **数据库**: SQLite (开发中使用 mock 数据)
- **部署**: Vercel

## 注意事项

1. **邮箱安全**：建议使用应用专用密码，不要使用邮箱主密码
2. **日志管理**：定期清理日志文件，避免占用过多磁盘空间
3. **定时任务**：根据实际需求调整定时任务频率
4. **错误处理**：查看日志中的 ERROR 级别信息排查问题

## 开发说明

### 添加新的日志

在代码中使用日志系统：

\`\`\`typescript
import { logInfo, logWarning, logError } from '@/lib/logger'

// 记录信息
logInfo('操作成功', 'user@example.com')

// 记录警告
logWarning('配置缺失')

// 记录错误
logError('连接失败', 'user@example.com')
\`\`\`

### 自定义日志配置

编辑 `lib/logger.ts` 修改：
- `maxLogs`: 最大日志条数（默认 1000）
- `logFilePath`: 日志文件路径

## 许可证

MIT
