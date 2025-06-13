#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多端API端点测试脚本

用于测试重构后的用户端、商户端、管理端API是否正常工作
"""

import requests
import json
from datetime import datetime

class MultiAPITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        
    def log_test(self, test_name, success, message, response_data=None):
        """记录测试结果"""
        result = {
            'test_name': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'response_data': response_data
        }
        self.test_results.append(result)
        
        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {message}")
        
    def test_endpoint(self, method, url, data=None, headers=None, expected_status=None):
        """测试单个端点"""
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method.upper() == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                return False, f"不支持的HTTP方法: {method}"
                
            # 检查状态码
            if expected_status and response.status_code != expected_status:
                return False, f"状态码错误: 期望{expected_status}, 实际{response.status_code}"
                
            # 尝试解析JSON响应
            try:
                response_data = response.json()
            except:
                response_data = response.text
                
            return True, f"状态码: {response.status_code}", response_data
            
        except requests.exceptions.ConnectionError:
            return False, "连接失败 - 请确保服务器正在运行"
        except Exception as e:
            return False, f"请求异常: {str(e)}"
    
    def test_user_api(self):
        """测试用户端API"""
        print("\n🔵 测试用户端API...")
        
        # 测试用户注册
        test_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        success, message, data = self.test_endpoint(
            'POST', 
            f"{self.base_url}/api/v1/user/auth/register/",
            data=test_data
        )
        self.log_test("用户注册", success, message, data)
        
        # 测试用户登录
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        success, message, data = self.test_endpoint(
            'POST',
            f"{self.base_url}/api/v1/user/auth/login/",
            data=login_data
        )
        self.log_test("用户登录", success, message, data)
        
        # 如果登录成功，获取token进行后续测试
        token = None
        if success and data and isinstance(data, dict):
            token = data.get('data', {}).get('token') or data.get('token')
            
        if token:
            headers = {'Authorization': f'Bearer {token}'}
            
            # 测试用户个人资料
            success, message, data = self.test_endpoint(
                'GET',
                f"{self.base_url}/api/v1/user/profile/me/",
                headers=headers
            )
            self.log_test("用户个人资料", success, message, data)
    
    def test_merchant_api(self):
        """测试商户端API"""
        print("\n🟡 测试商户端API...")
        
        # 测试商户注册
        test_data = {
            "username": "testmerchant",
            "email": "merchant@example.com",
            "password": "merchantpass123",
            "business_name": "测试商户"
        }
        
        success, message, data = self.test_endpoint(
            'POST',
            f"{self.base_url}/api/v1/merchant/auth/register/",
            data=test_data
        )
        self.log_test("商户注册", success, message, data)
        
        # 测试商户登录
        login_data = {
            "username": "testmerchant",
            "password": "merchantpass123"
        }
        
        success, message, data = self.test_endpoint(
            'POST',
            f"{self.base_url}/api/v1/merchant/auth/login/",
            data=login_data
        )
        self.log_test("商户登录", success, message, data)
        
        # 如果登录成功，测试商户仪表板
        token = None
        if success and data and isinstance(data, dict):
            token = data.get('data', {}).get('token') or data.get('token')
            
        if token:
            headers = {'Authorization': f'Bearer {token}'}
            
            # 测试商户仪表板
            success, message, data = self.test_endpoint(
                'GET',
                f"{self.base_url}/api/v1/merchant/dashboard/stats/",
                headers=headers
            )
            self.log_test("商户仪表板", success, message, data)
    
    def test_admin_api(self):
        """测试管理端API"""
        print("\n🔴 测试管理端API...")
        
        # 测试管理员登录
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        success, message, data = self.test_endpoint(
            'POST',
            f"{self.base_url}/api/v1/admin/auth/login/",
            data=login_data
        )
        self.log_test("管理员登录", success, message, data)
        
        # 如果登录成功，测试管理功能
        token = None
        if success and data and isinstance(data, dict):
            token = data.get('data', {}).get('token') or data.get('token')
            
        if token:
            headers = {'Authorization': f'Bearer {token}'}
            
            # 测试用户管理
            success, message, data = self.test_endpoint(
                'GET',
                f"{self.base_url}/api/v1/admin/users/",
                headers=headers
            )
            self.log_test("用户管理", success, message, data)
    
    def test_legacy_api(self):
        """测试Legacy API兼容性"""
        print("\n🔄 测试Legacy API兼容性...")
        
        # 测试地区API
        success, message, data = self.test_endpoint(
            'GET',
            f"{self.base_url}/api/legacy/regions/"
        )
        self.log_test("Legacy地区API", success, message, data)
        
        # 测试村庄API
        success, message, data = self.test_endpoint(
            'GET',
            f"{self.base_url}/api/legacy/villages/"
        )
        self.log_test("Legacy村庄API", success, message, data)
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始多端API测试...")
        print(f"测试服务器: {self.base_url}")
        print("=" * 50)
        
        # 运行各端测试
        self.test_user_api()
        self.test_merchant_api()
        self.test_admin_api()
        self.test_legacy_api()
        
        # 生成测试报告
        self.generate_report()
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 50)
        print("📊 测试报告")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests} ✅")
        print(f"失败: {failed_tests} ❌")
        print(f"成功率: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n❌ 失败的测试:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test_name']}: {result['message']}")
        
        # 保存详细报告到文件
        report_file = f"api_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'success_rate': passed_tests/total_tests*100
                },
                'test_results': self.test_results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 详细报告已保存到: {report_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='测试多端API端点')
    parser.add_argument('--url', default='http://localhost:8000', help='服务器URL')
    parser.add_argument('--user', action='store_true', help='只测试用户端API')
    parser.add_argument('--merchant', action='store_true', help='只测试商户端API')
    parser.add_argument('--admin', action='store_true', help='只测试管理端API')
    parser.add_argument('--legacy', action='store_true', help='只测试Legacy API')
    
    args = parser.parse_args()
    
    tester = MultiAPITester(args.url)
    
    if args.user:
        tester.test_user_api()
    elif args.merchant:
        tester.test_merchant_api()
    elif args.admin:
        tester.test_admin_api()
    elif args.legacy:
        tester.test_legacy_api()
    else:
        tester.run_all_tests()
    
    if not any([args.user, args.merchant, args.admin, args.legacy]):
        tester.generate_report()

if __name__ == '__main__':
    main()