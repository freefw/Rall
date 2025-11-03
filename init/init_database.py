#!/usr/bin/env python3
"""
邮件自动回复系统 - 数据库初始化脚本
独立运行此脚本以创建初始化的数据库文件
默认管理员账号: admin / admin123
"""

import sqlite3
import hashlib
import os
from datetime import datetime

# 数据库文件路径
DB_FILE = 'email_auto_reply.db'

def md5_hash(password: str) -> str:
    """使用MD5加密密码"""
    return hashlib.md5(password.encode()).hexdigest()

def init_database():
    """初始化数据库"""
    
    # 如果数据库文件已存在，先删除
    if os.path.exists(DB_FILE):
        print(f"警告: 数据库文件 {DB_FILE} 已存在，将被覆盖...")
        os.remove(DB_FILE)
    
    # 创建数据库连接
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    print("正在创建数据库表...")
    
    # 创建管理员表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    
    # 创建邮箱配置表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            imap_server TEXT NOT NULL,
            imap_port INTEGER NOT NULL,
            smtp_server TEXT NOT NULL,
            smtp_port INTEGER NOT NULL,
            password TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    
    # 创建回复内容配置表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reply_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_name TEXT NOT NULL DEFAULT '自动回复系统',
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    
    # 创建日志表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            email_account TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    
    # 创建已处理邮件记录表（防止重复回复）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_account TEXT NOT NULL,
            message_id TEXT NOT NULL,
            sender TEXT NOT NULL,
            subject TEXT,
            processed_at TEXT NOT NULL,
            UNIQUE(email_account, message_id)
        )
    ''')
    
    print("正在插入初始数据...")
    
    # 插入默认管理员账号
    now = datetime.now().isoformat()
    default_password = md5_hash('admin123')
    cursor.execute('''
        INSERT INTO admin_users (username, password, created_at, updated_at)
        VALUES (?, ?, ?, ?)
    ''', ('admin', default_password, now, now))
    
    # 插入默认回复内容
    cursor.execute('''
        INSERT INTO reply_config (sender_name, subject, content, updated_at)
        VALUES (?, ?, ?, ?)
    ''', (
        '自动回复系统',
        '自动回复',
        '您好！\n\n感谢您的来信。这是一封自动回复邮件。\n\n我们已经收到您的邮件，会尽快处理并回复您。\n\n祝好！',
        now
    ))
    
    # 提交更改
    conn.commit()
    
    print(f"\n✅ 数据库初始化成功！")
    print(f"📁 数据库文件: {os.path.abspath(DB_FILE)}")
    print(f"\n默认管理员账号:")
    print(f"  用户名: admin")
    print(f"  密码: admin123")
    print(f"\n⚠️  请在首次登录后修改默认密码！")
    
    # 关闭连接
    conn.close()

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ 数据库初始化失败: {str(e)}")
        exit(1)
