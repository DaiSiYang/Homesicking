#!/bin/bash

# 觅乡记后端服务器启动脚本
# 用于解决Django服务器启动和CORS问题

echo "🚀 启动觅乡记后端服务器..."
echo "======================================"

# 进入后端目录
BACKEND_DIR="/Users/syd/Desktop/觅乡记/backend"
cd "$BACKEND_DIR" || {
    echo "❌ 错误: 无法进入后端目录 $BACKEND_DIR"
    exit 1
}

echo "📁 当前目录: $(pwd)"

# 检查Python版本
echo "🐍 检查Python版本..."
python3 --version || {
    echo "❌ 错误: Python3 未安装或不在PATH中"
    exit 1
}

# 检查Django是否安装
echo "🔧 检查Django安装..."
python3 -c "import django; print(f'Django版本: {django.get_version()}')" || {
    echo "⚠️  Django未安装，正在安装依赖..."
    pip3 install -r requirements.txt
}

# 检查端口占用
echo "🔍 检查端口8000占用情况..."
PORT_CHECK=$(lsof -i :8000 2>/dev/null)
if [ ! -z "$PORT_CHECK" ]; then
    echo "⚠️  端口8000被占用:"
    echo "$PORT_CHECK"
    echo "正在尝试终止占用进程..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    sleep 2
fi

# 数据库迁移
echo "📊 执行数据库迁移..."
python3 manage.py migrate --run-syncdb || {
    echo "⚠️  数据库迁移失败，尝试创建数据库..."
    python3 manage.py migrate
}

# 创建超级用户（如果不存在）
echo "👤 检查超级用户..."
python3 manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('创建超级用户: admin/admin123')
else:
    print('超级用户已存在')
" 2>/dev/null

# 收集静态文件
echo "📦 收集静态文件..."
python3 manage.py collectstatic --noinput --clear 2>/dev/null || echo "静态文件收集跳过"

# 检查CORS配置
echo "🌐 验证CORS配置..."
python3 -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from django.conf import settings
print(f'CORS_ALLOW_ALL_ORIGINS: {getattr(settings, "CORS_ALLOW_ALL_ORIGINS", False)}')
print(f'CORS_ALLOW_CREDENTIALS: {getattr(settings, "CORS_ALLOW_CREDENTIALS", False)}')
" || echo "CORS配置检查失败"

echo "======================================"
echo "🎯 启动Django开发服务器..."
echo "服务器地址: http://localhost:8000"
echo "API文档: http://localhost:8000/api/docs/"
echo "管理后台: http://localhost:8000/admin/"
echo "按 Ctrl+C 停止服务器"
echo "======================================"

# 启动服务器
exec python3 manage.py runserver 0.0.0.0:8000 --noreload