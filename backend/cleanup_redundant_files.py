#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后端重构后的冗余文件清理脚本

使用方法：
1. 先运行备份: python cleanup_redundant_files.py --backup
2. 再运行清理: python cleanup_redundant_files.py --cleanup
3. 如需恢复: python cleanup_redundant_files.py --restore
"""

import os
import shutil
import argparse
from datetime import datetime
from pathlib import Path

class RedundantFileCleaner:
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.backup_dir = self.base_dir / 'backup' / f'cleanup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        
        # 定义需要删除的冗余文件
        self.redundant_files = [
            # 旧版认证相关文件
            'apps/users/views/auth_views.py',
            'apps/users/urls/auth_urls.py',
            
            # 混合业务路由文件（需要重构到对应端）
            'apps/users/urls/merchant_manage_urls.py',
            'apps/users/urls/merchant_urls.py',
        ]
        
        # 需要重构的文件（暂不删除，只是标记）
        self.files_to_refactor = [
            'apps/users/views/user_views.py',
            'apps/users/urls/user_urls.py', 
            'apps/users/views/favorite_views.py',
            'apps/users/urls/favorite_urls.py',
            'apps/users/views/merchant_views.py',
        ]
    
    def backup_files(self):
        """备份将要删除的文件"""
        print(f"🔄 开始备份文件到: {self.backup_dir}")
        
        # 创建备份目录
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        backup_count = 0
        for file_path in self.redundant_files:
            source_file = self.base_dir / file_path
            if source_file.exists():
                # 保持目录结构
                backup_file = self.backup_dir / file_path
                backup_file.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.copy2(source_file, backup_file)
                print(f"  ✅ 已备份: {file_path}")
                backup_count += 1
            else:
                print(f"  ⚠️  文件不存在: {file_path}")
        
        # 创建备份信息文件
        info_file = self.backup_dir / 'backup_info.txt'
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(f"备份时间: {datetime.now()}\n")
            f.write(f"备份文件数量: {backup_count}\n")
            f.write("\n备份的文件列表:\n")
            for file_path in self.redundant_files:
                f.write(f"- {file_path}\n")
        
        print(f"✅ 备份完成! 共备份 {backup_count} 个文件")
        return backup_count > 0
    
    def cleanup_files(self):
        """删除冗余文件"""
        print("🗑️  开始清理冗余文件...")
        
        deleted_count = 0
        for file_path in self.redundant_files:
            source_file = self.base_dir / file_path
            if source_file.exists():
                try:
                    source_file.unlink()
                    print(f"  ✅ 已删除: {file_path}")
                    deleted_count += 1
                except Exception as e:
                    print(f"  ❌ 删除失败: {file_path} - {e}")
            else:
                print(f"  ⚠️  文件不存在: {file_path}")
        
        print(f"✅ 清理完成! 共删除 {deleted_count} 个文件")
        
        # 显示需要手动重构的文件
        if self.files_to_refactor:
            print("\n📋 以下文件需要手动重构（未删除）:")
            for file_path in self.files_to_refactor:
                if (self.base_dir / file_path).exists():
                    print(f"  📝 {file_path}")
    
    def restore_files(self):
        """从最新备份恢复文件"""
        # 查找最新的备份目录
        backup_base = self.base_dir / 'backup'
        if not backup_base.exists():
            print("❌ 没有找到备份目录")
            return
        
        backup_dirs = [d for d in backup_base.iterdir() if d.is_dir() and d.name.startswith('cleanup_')]
        if not backup_dirs:
            print("❌ 没有找到清理备份")
            return
        
        latest_backup = max(backup_dirs, key=lambda x: x.name)
        print(f"🔄 从备份恢复文件: {latest_backup}")
        
        restored_count = 0
        for file_path in self.redundant_files:
            backup_file = latest_backup / file_path
            if backup_file.exists():
                target_file = self.base_dir / file_path
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.copy2(backup_file, target_file)
                print(f"  ✅ 已恢复: {file_path}")
                restored_count += 1
            else:
                print(f"  ⚠️  备份中没有: {file_path}")
        
        print(f"✅ 恢复完成! 共恢复 {restored_count} 个文件")
    
    def show_analysis(self):
        """显示清理分析"""
        print("📊 冗余文件清理分析")
        print("=" * 50)
        
        print("\n🔴 将要删除的冗余文件:")
        for file_path in self.redundant_files:
            exists = "✅" if (self.base_dir / file_path).exists() else "❌"
            print(f"  {exists} {file_path}")
        
        print("\n🟡 需要手动重构的文件:")
        for file_path in self.files_to_refactor:
            exists = "✅" if (self.base_dir / file_path).exists() else "❌"
            print(f"  {exists} {file_path}")
        
        print("\n📋 清理建议:")
        print("  1. 先运行 --backup 备份文件")
        print("  2. 再运行 --cleanup 清理冗余文件")
        print("  3. 测试系统功能是否正常")
        print("  4. 如有问题可运行 --restore 恢复")
        print("  5. 手动重构标记的文件")

def main():
    parser = argparse.ArgumentParser(description='清理后端重构后的冗余文件')
    parser.add_argument('--backup', action='store_true', help='备份将要删除的文件')
    parser.add_argument('--cleanup', action='store_true', help='删除冗余文件')
    parser.add_argument('--restore', action='store_true', help='从备份恢复文件')
    parser.add_argument('--analysis', action='store_true', help='显示清理分析')
    parser.add_argument('--dir', type=str, help='指定项目根目录')
    
    args = parser.parse_args()
    
    cleaner = RedundantFileCleaner(args.dir)
    
    if args.backup:
        cleaner.backup_files()
    elif args.cleanup:
        # 清理前先检查是否有备份
        backup_base = cleaner.base_dir / 'backup'
        if not backup_base.exists() or not any(backup_base.iterdir()):
            print("⚠️  建议先运行 --backup 备份文件")
            response = input("是否继续清理? (y/N): ")
            if response.lower() != 'y':
                print("❌ 取消清理")
                return
        
        cleaner.cleanup_files()
    elif args.restore:
        cleaner.restore_files()
    elif args.analysis:
        cleaner.show_analysis()
    else:
        cleaner.show_analysis()
        print("\n使用 --help 查看详细用法")

if __name__ == '__main__':
    main()