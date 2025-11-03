# 数据库初始化说明

## 运行初始化脚本

在 `init` 目录下运行以下命令：

\`\`\`bash
python3 init_database.py
\`\`\`

## 生成的数据库

脚本会在当前目录生成 `email_auto_reply.db` 文件。

## 默认账号

- **用户名**: `admin`
- **密码**: `admin123`

⚠️ **重要**: 请在首次登录后立即修改默认密码！

## 数据库结构

### admin_users (管理员表)
- id: 主键
- username: 用户名（唯一）
- password: 密码（MD5加密）
- created_at: 创建时间
- updated_at: 更新时间

### email_accounts (邮箱配置表)
- id: 主键
- email: 邮箱地址（唯一）
- imap_server: IMAP服务器地址
- imap_port: IMAP端口
- smtp_server: SMTP服务器地址
- smtp_port: SMTP端口
- password: 邮箱密码
- is_active: 是否启用（1=启用，0=禁用）
- created_at: 创建时间
- updated_at: 更新时间

### reply_config (回复内容配置表)
- id: 主键
- subject: 回复邮件主题
- content: 回复邮件内容
- updated_at: 更新时间

### logs (日志表)
- id: 主键
- level: 日志级别（INFO/WARNING/ERROR）
- message: 日志消息
- email_account: 相关邮箱账号
- created_at: 创建时间

### processed_emails (已处理邮件记录表)
- id: 主键
- email_account: 邮箱账号
- message_id: 邮件唯一标识
- sender: 发件人
- subject: 邮件主题
- processed_at: 处理时间
