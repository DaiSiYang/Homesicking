# 觅乡记商户管理平台

觅乡记商户管理平台是为乡村旅游资源提供商（特产店、民宿等）设计的管理系统，帮助商户管理产品、订单和店铺信息。

## 功能特性

- 商户账户管理：注册、登录、个人信息设置
- 特产管理：添加、编辑、删除特产商品
- 民宿管理：添加、编辑、删除民宿房间
- 订单管理：查看、处理客户订单
- 数据统计：销售额、订单量等数据分析

## 技术栈

- Vue 3 + Vite
- Vue Router
- Pinia 状态管理
- Element Plus UI组件库
- Tailwind CSS
- ECharts 图表库
- Axios HTTP客户端

## 开发说明

### 环境要求

- Node.js 16+
- npm 7+

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

默认端口为3001，可通过`vite.config.js`修改。

### 构建生产版本

```bash
npm run build
```

## 模拟数据模式

系统支持模拟数据模式，当后端API不可用时，会自动切换到模拟数据模式。
可以通过`src/store/user.js`中的`useMockData`变量控制是否使用模拟数据。

## 项目结构

```
src/
├── api/            # API请求
├── assets/         # 静态资源
├── components/     # 公共组件
├── router/         # 路由配置
├── store/          # 状态管理
├── utils/          # 工具函数
└── views/          # 页面组件
    ├── auth/       # 认证相关页面
    ├── dashboard/  # 控制台
    ├── products/   # 特产管理
    ├── homestays/  # 民宿管理
    ├── orders/     # 订单管理
    ├── profile/    # 店铺信息
    └── settings/   # 账户设置
``` 