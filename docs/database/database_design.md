# 觅乡记 - 数据库设计

## 数据库概述

本项目使用MySQL作为数据库系统，通过Django ORM进行数据库操作。以下是各主要实体及其关系的设计。

## 核心实体

### 用户相关

#### User（用户）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| username | VARCHAR(150) | 用户名 |
| email | VARCHAR(254) | 电子邮件 |
| password | VARCHAR(128) | 密码（加密存储） |
| phone | VARCHAR(20) | 手机号码 |
| avatar | VARCHAR(255) | 头像URL |
| bio | TEXT | 个人简介 |
| user_type | ENUM | 用户类型（游客/商户/管理员） |
| is_active | BOOLEAN | 是否激活 |
| is_verified | BOOLEAN | 是否通过验证 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### UserProfile（用户资料）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| user_id | INT | 外键，关联User |
| real_name | VARCHAR(50) | 真实姓名 |
| id_card | VARCHAR(50) | 身份证号（加密存储） |
| gender | ENUM | 性别 |
| birthday | DATE | 生日 |
| address | VARCHAR(255) | 地址 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### MerchantProfile（商户资料）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| user_id | INT | 外键，关联User |
| business_name | VARCHAR(100) | 商户名称 |
| business_license | VARCHAR(255) | 营业执照图片URL |
| contact_person | VARCHAR(50) | 联系人 |
| contact_phone | VARCHAR(20) | 联系电话 |
| address | VARCHAR(255) | 商户地址 |
| description | TEXT | 商户描述 |
| status | ENUM | 状态（待审核/已通过/已拒绝） |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 地点相关

#### Region（区域）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| name | VARCHAR(100) | 区域名称 |
| code | VARCHAR(20) | 区域编码 |
| parent_id | INT | 外键，上级区域ID |
| level | ENUM | 级别（省/市/县） |
| is_hot | BOOLEAN | 是否热门 |
| status | ENUM | 状态 |

#### Village（乡村）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| name | VARCHAR(100) | 乡村名称 |
| region_id | INT | 外键，所属区域 |
| intro | TEXT | 简介 |
| description | TEXT | 详细描述 |
| cover_image | VARCHAR(255) | 封面图URL |
| location | POINT | 地理位置 |
| features | TEXT | 特色标签（JSON格式） |
| views | INT | 浏览量 |
| rating | DECIMAL(2,1) | 平均评分 |
| status | ENUM | 状态（待审核/已通过/已拒绝） |
| is_recommended | BOOLEAN | 是否推荐 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### VillageGallery（乡村图库）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| village_id | INT | 外键，关联Village |
| image_url | VARCHAR(255) | 图片URL |
| caption | VARCHAR(255) | 图片说明 |
| order | INT | 排序 |

#### Attraction（景点）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| name | VARCHAR(100) | 景点名称 |
| village_id | INT | 外键，所属乡村 |
| intro | TEXT | 简介 |
| description | TEXT | 详细描述 |
| cover_image | VARCHAR(255) | 封面图URL |
| location | POINT | 地理位置 |
| opening_hours | VARCHAR(255) | 开放时间 |
| ticket_price | DECIMAL(10,2) | 票价 |
| status | ENUM | 状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### AttractionGallery（景点图库）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| attraction_id | INT | 外键，关联Attraction |
| image_url | VARCHAR(255) | 图片URL |
| caption | VARCHAR(255) | 图片说明 |
| order | INT | 排序 |

### 住宿相关

#### Homestay（民宿）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| name | VARCHAR(100) | 民宿名称 |
| merchant_id | INT | 外键，关联商户 |
| village_id | INT | 外键，所属乡村 |
| intro | TEXT | 简介 |
| description | TEXT | 详细描述 |
| cover_image | VARCHAR(255) | 封面图URL |
| location | POINT | 地理位置 |
| address | VARCHAR(255) | 详细地址 |
| facilities | TEXT | 设施（JSON格式） |
| rules | TEXT | 入住规则 |
| min_price | DECIMAL(10,2) | 最低价格 |
| max_price | DECIMAL(10,2) | 最高价格 |
| rating | DECIMAL(2,1) | 平均评分 |
| views | INT | 浏览量 |
| status | ENUM | 状态 |
| is_recommended | BOOLEAN | 是否推荐 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### HomestayGallery（民宿图库）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| homestay_id | INT | 外键，关联Homestay |
| image_url | VARCHAR(255) | 图片URL |
| caption | VARCHAR(255) | 图片说明 |
| order | INT | 排序 |

#### RoomType（房型）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| homestay_id | INT | 外键，关联民宿 |
| name | VARCHAR(100) | 房型名称 |
| description | TEXT | 描述 |
| max_guests | INT | 最大入住人数 |
| bed_info | VARCHAR(255) | 床位信息 |
| area | INT | 面积（平方米） |
| price | DECIMAL(10,2) | 价格 |
| inventory | INT | 库存数量 |
| status | ENUM | 状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### RoomGallery（房型图库）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| room_type_id | INT | 外键，关联RoomType |
| image_url | VARCHAR(255) | 图片URL |
| caption | VARCHAR(255) | 图片说明 |
| order | INT | 排序 |

#### RoomPrice（房价日历）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| room_type_id | INT | 外键，关联RoomType |
| date | DATE | 日期 |
| price | DECIMAL(10,2) | 当日价格 |
| inventory | INT | 当日库存 |
| status | ENUM | 状态（可预订/已满） |

### 餐饮相关

#### Food（美食）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| name | VARCHAR(100) | 美食名称 |
| merchant_id | INT | 外键，关联商户 |
| village_id | INT | 外键，所属乡村 |
| category | VARCHAR(50) | 分类 |
| intro | TEXT | 简介 |
| description | TEXT | 详细描述 |
| cover_image | VARCHAR(255) | 封面图URL |
| price | DECIMAL(10,2) | 价格 |
| status | ENUM | 状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### FoodGallery（美食图库）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| food_id | INT | 外键，关联Food |
| image_url | VARCHAR(255) | 图片URL |
| caption | VARCHAR(255) | 图片说明 |
| order | INT | 排序 |

### 农产品相关

#### Product（农产品）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| name | VARCHAR(100) | 产品名称 |
| merchant_id | INT | 外键，关联商户 |
| village_id | INT | 外键，所属乡村 |
| category | VARCHAR(50) | 分类 |
| intro | TEXT | 简介 |
| description | TEXT | 详细描述 |
| cover_image | VARCHAR(255) | 封面图URL |
| price | DECIMAL(10,2) | 价格 |
| inventory | INT | 库存 |
| sales | INT | 销量 |
| rating | DECIMAL(2,1) | 平均评分 |
| is_recommended | BOOLEAN | 是否推荐 |
| status | ENUM | 状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### ProductGallery（产品图库）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| product_id | INT | 外键，关联Product |
| image_url | VARCHAR(255) | 图片URL |
| caption | VARCHAR(255) | 图片说明 |
| order | INT | 排序 |

#### ProductSku（产品SKU）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| product_id | INT | 外键，关联Product |
| sku_name | VARCHAR(100) | SKU名称 |
| attributes | TEXT | 属性（JSON格式） |
| price | DECIMAL(10,2) | 价格 |
| inventory | INT | 库存 |
| status | ENUM | 状态 |

### 订单相关

#### Cart（购物车）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| user_id | INT | 外键，关联User |
| item_type | ENUM | 项目类型（民宿/农产品） |
| item_id | INT | 项目ID |
| sku_id | INT | SKU ID（农产品适用） |
| quantity | INT | 数量 |
| check_in_date | DATE | 入住日期（民宿适用） |
| check_out_date | DATE | 离店日期（民宿适用） |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### Order（订单）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| order_no | VARCHAR(50) | 订单编号 |
| user_id | INT | 外键，关联User |
| merchant_id | INT | 外键，关联商户 |
| order_type | ENUM | 订单类型（民宿/农产品） |
| total_amount | DECIMAL(10,2) | 总金额 |
| status | ENUM | 状态（待支付/已支付/已确认/已完成/已取消） |
| payment_method | VARCHAR(50) | 支付方式 |
| payment_time | DATETIME | 支付时间 |
| contact_name | VARCHAR(50) | 联系人 |
| contact_phone | VARCHAR(20) | 联系电话 |
| remark | TEXT | 备注 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### OrderItem（订单项）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| order_id | INT | 外键，关联Order |
| item_type | ENUM | 项目类型（民宿/农产品） |
| item_id | INT | 项目ID |
| sku_id | INT | SKU ID（农产品适用） |
| item_name | VARCHAR(100) | 项目名称 |
| item_cover | VARCHAR(255) | 项目封面图 |
| price | DECIMAL(10,2) | 单价 |
| quantity | INT | 数量 |
| check_in_date | DATE | 入住日期（民宿适用） |
| check_out_date | DATE | 离店日期（民宿适用） |
| subtotal | DECIMAL(10,2) | 小计 |

#### HomestayOrder（民宿订单扩展）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| order_id | INT | 外键，关联Order |
| homestay_id | INT | 外键，关联Homestay |
| room_type_id | INT | 外键，关联RoomType |
| guest_count | INT | 入住人数 |
| check_in_date | DATE | 入住日期 |
| check_out_date | DATE | 离店日期 |
| nights | INT | 入住晚数 |
| check_in_status | ENUM | 入住状态（未入住/已入住/已离店） |
| guest_names | TEXT | 入住人姓名 |

#### ProductOrder（农产品订单扩展）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| order_id | INT | 外键，关联Order |
| delivery_method | ENUM | 配送方式（自提/邮寄） |
| delivery_status | ENUM | 配送状态 |
| address | TEXT | 收货地址 |
| tracking_no | VARCHAR(50) | 物流单号 |

### 评价相关

#### Review（评价）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| user_id | INT | 外键，关联User |
| order_id | INT | 外键，关联Order |
| target_type | ENUM | 评价对象类型（民宿/农产品/景点） |
| target_id | INT | 评价对象ID |
| rating | INT | 评分（1-5） |
| content | TEXT | 评价内容 |
| images | TEXT | 图片URL列表（JSON格式） |
| status | ENUM | 状态（待审核/已通过/已拒绝） |
| is_anonymous | BOOLEAN | 是否匿名 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### ReviewReply（评价回复）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| review_id | INT | 外键，关联Review |
| user_id | INT | 外键，关联User |
| content | TEXT | 回复内容 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 内容相关

#### TravelNote（游记）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| user_id | INT | 外键，关联User |
| title | VARCHAR(255) | 标题 |
| cover_image | VARCHAR(255) | 封面图URL |
| content | TEXT | 内容 |
| village_id | INT | 外键，关联Village |
| views | INT | 浏览量 |
| likes | INT | 点赞数 |
| status | ENUM | 状态（待审核/已通过/已拒绝） |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### TravelNoteImage（游记图片）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| travel_note_id | INT | 外键，关联TravelNote |
| image_url | VARCHAR(255) | 图片URL |
| caption | VARCHAR(255) | 图片说明 |
| order | INT | 排序 |

#### Question（问答）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| user_id | INT | 外键，关联User |
| village_id | INT | 外键，关联Village |
| title | VARCHAR(255) | 问题标题 |
| content | TEXT | 问题内容 |
| status | ENUM | 状态 |
| views | INT | 浏览量 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### Answer（答案）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| question_id | INT | 外键，关联Question |
| user_id | INT | 外键，关联User |
| content | TEXT | 答案内容 |
| is_accepted | BOOLEAN | 是否被采纳 |
| likes | INT | 点赞数 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### News（资讯）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| title | VARCHAR(255) | 标题 |
| category | VARCHAR(50) | 分类 |
| cover_image | VARCHAR(255) | 封面图URL |
| summary | TEXT | 摘要 |
| content | TEXT | 内容 |
| author | VARCHAR(100) | 作者 |
| source | VARCHAR(100) | 来源 |
| views | INT | 浏览量 |
| is_top | BOOLEAN | 是否置顶 |
| status | ENUM | 状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 系统相关

#### Tag（标签）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| name | VARCHAR(50) | 标签名 |
| category | VARCHAR(50) | 分类 |
| status | ENUM | 状态 |

#### TagRelation（标签关联）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| tag_id | INT | 外键，关联Tag |
| target_type | ENUM | 目标类型 |
| target_id | INT | 目标ID |

#### Banner（轮播图）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| title | VARCHAR(255) | 标题 |
| image_url | VARCHAR(255) | 图片URL |
| link_url | VARCHAR(255) | 链接URL |
| position | VARCHAR(50) | 位置 |
| order | INT | 排序 |
| status | ENUM | 状态 |
| start_time | DATETIME | 开始时间 |
| end_time | DATETIME | 结束时间 |

#### Favorite（收藏）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| user_id | INT | 外键，关联User |
| target_type | ENUM | 目标类型 |
| target_id | INT | 目标ID |
| created_at | DATETIME | 创建时间 |

#### Notification（通知）
| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 主键 |
| user_id | INT | 外键，关联User |
| type | ENUM | 类型 |
| title | VARCHAR(255) | 标题 |
| content | TEXT | 内容 |
| is_read | BOOLEAN | 是否已读 |
| created_at | DATETIME | 创建时间 |

## 表关系图

以上表格之间存在如下主要关系：

- User 与 UserProfile/MerchantProfile：一对一关系
- Region 与 Village：一对多关系
- Village 与 Attraction/Homestay/Food/Product：一对多关系
- Merchant 与 Homestay/Food/Product：一对多关系
- Homestay 与 RoomType：一对多关系
- RoomType 与 RoomPrice：一对多关系
- User 与 Order：一对多关系
- Order 与 OrderItem：一对多关系
- User 与 Review/TravelNote/Question：一对多关系

## 索引设计

为提高查询效率，需要在以下字段上建立索引：

- User 表：username, email, phone
- Village 表：name, region_id, is_recommended
- Homestay 表：name, merchant_id, village_id, is_recommended
- Product 表：name, merchant_id, village_id, is_recommended
- Order 表：order_no, user_id, merchant_id, status
- Review 表：user_id, target_type, target_id
- Tag 表：name, category
- 所有关联表的外键字段 