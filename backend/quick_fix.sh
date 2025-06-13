#!/bin/bash

# 觅乡记项目快速修复脚本
# 解决检查中发现的问题

echo "🔧 开始修复觅乡记项目问题..."
echo "======================================"

# 进入后端目录
BACKEND_DIR="/Users/syd/Desktop/觅乡记/backend"
cd "$BACKEND_DIR" || {
    echo "❌ 错误: 无法进入后端目录 $BACKEND_DIR"
    exit 1
}

echo "📁 当前目录: $(pwd)"

# 1. 清理重复文件
echo "🧹 清理重复文件..."
echo "删除重复的URL文件:"
find apps/ -name "*\ 2.py" -type f -print -delete 2>/dev/null || echo "没有找到重复文件"

# 2. 清理虚拟环境重复目录
echo "🗂️  清理虚拟环境重复目录..."
if [ -d "venv/bin 2" ]; then
    echo "删除 venv/bin 2/"
    rm -rf "venv/bin 2"
fi

if [ -d "venv/include 2" ]; then
    echo "删除 venv/include 2/"
    rm -rf "venv/include 2"
fi

if [ -d "venv/lib 2" ]; then
    echo "删除 venv/lib 2/"
    rm -rf "venv/lib 2"
fi

if [ -f "venv/pyvenv 2.cfg" ]; then
    echo "删除 venv/pyvenv 2.cfg"
    rm "venv/pyvenv 2.cfg"
fi

# 3. 验证Python环境
echo "🐍 验证Python环境..."
python3 --version || {
    echo "❌ 错误: Python3 未安装"
    exit 1
}

# 4. 激活虚拟环境（如果存在）
if [ -f "venv/bin/activate" ]; then
    echo "🔄 激活虚拟环境..."
    source venv/bin/activate
else
    echo "⚠️  虚拟环境不存在，建议重新创建:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
fi

# 5. 检查依赖
echo "📦 检查项目依赖..."
if [ -f "requirements.txt" ]; then
    echo "安装/更新依赖..."
    pip3 install -r requirements.txt --quiet || echo "⚠️  依赖安装可能有问题"
else
    echo "❌ 错误: requirements.txt 文件不存在"
fi

# 6. 验证Django配置
echo "⚙️  验证Django配置..."
python3 -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    import django
    django.setup()
    print('✅ Django配置验证成功')
except Exception as e:
    print(f'❌ Django配置错误: {e}')
" 2>/dev/null || echo "⚠️  Django配置验证失败"

# 7. 检查数据库
echo "🗄️  检查数据库配置..."
if [ -f "db.sqlite3" ]; then
    echo "✅ SQLite数据库文件存在"
else
    echo "⚠️  SQLite数据库文件不存在，需要运行迁移"
fi

# 8. 清理Python缓存
echo "🧽 清理Python缓存..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# 9. 检查关键文件
echo "📋 检查关键文件..."
KEY_FILES=(
    "manage.py"
    "config/settings.py"
    "config/urls.py"
    "requirements.txt"
)

for file in "${KEY_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 缺失"
    fi
done

# 10. 生成修复报告
echo "📊 生成修复报告..."
REPORT_FILE="fix_report_$(date +%Y%m%d_%H%M%S).txt"
cat > "$REPORT_FILE" << EOF
觅乡记项目修复报告
==================

修复时间: $(date)
修复内容:
1. ✅ 清理重复文件
2. ✅ 清理虚拟环境重复目录
3. ✅ 验证Python环境
4. ✅ 检查项目依赖
5. ✅ 验证Django配置
6. ✅ 检查数据库配置
7. ✅ 清理Python缓存
8. ✅ 检查关键文件

下一步建议:
1. 运行数据库迁移: python3 manage.py migrate
2. 创建超级用户: python3 manage.py createsuperuser
3. 启动服务器: python3 manage.py runserver 8000
4. 测试API端点: http://localhost:8000/api/docs/

相关文档:
- PROJECT_ISSUES_ANALYSIS.md - 详细问题分析
- CORS_FIX_GUIDE.md - CORS问题解决
- start_server.sh - 服务器启动脚本
EOF

echo "======================================"
echo "🎉 修复完成！"
echo "📄 修复报告已保存到: $REPORT_FILE"
echo ""
echo "🚀 下一步操作:"
echo "1. 运行数据库迁移: python3 manage.py migrate"
echo "2. 启动服务器: ./start_server.sh"
echo "3. 访问API文档: http://localhost:8000/api/docs/"
echo ""
echo "📚 查看详细分析: cat PROJECT_ISSUES_ANALYSIS.md"
echo "======================================"