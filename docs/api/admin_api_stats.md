# 觅乡记 - 管理后台API (数据统计部分)

## 通用说明

管理后台API仅供平台管理员使用，所有接口均需要管理员权限。

基础URL: `/api/v1/admin/stats/`

## 概览统计接口

### 获取平台概览数据

- **URL**: `/api/v1/admin/stats/overview/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取平台概览数据

**请求参数**:
- `period`: 统计周期，可选值：`today`, `yesterday`, `last_7_days`, `last_30_days`, `this_month`, `last_month`，默认为`last_30_days`

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "user_stats": {
      "total_users": 5000,
      "new_users": 150,
      "active_users": 1200,
      "user_increase_rate": 0.12
    },
    "merchant_stats": {
      "total_merchants": 200,
      "new_merchants": 10,
      "active_merchants": 150,
      "merchant_increase_rate": 0.08
    },
    "content_stats": {
      "total_villages": 100,
      "total_homestays": 300,
      "total_products": 500,
      "total_travel_notes": 800,
      "total_questions": 600,
      "total_reviews": 1500
    },
    "order_stats": {
      "total_orders": 2000,
      "completed_orders": 1800,
      "total_revenue": 500000,
      "average_order_value": 250
    },
    "visit_stats": {
      "total_visits": 50000,
      "unique_visitors": 20000,
      "page_views": 150000,
      "bounce_rate": 0.25
    }
  }
}
```

### 获取平台趋势数据

- **URL**: `/api/v1/admin/stats/trends/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取平台趋势数据

**请求参数**:
- `type`: 统计类型，可选值：`users`, `merchants`, `orders`, `revenue`, `visits`
- `period`: 统计周期，可选值：`daily`, `weekly`, `monthly`，默认为`daily`
- `start_date`: 开始日期，格式：YYYY-MM-DD
- `end_date`: 结束日期，格式：YYYY-MM-DD

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "type": "users",
    "period": "daily",
    "start_date": "2023-04-01",
    "end_date": "2023-04-30",
    "data_points": [
      {
        "date": "2023-04-01",
        "total_users": 4800,
        "new_users": 20,
        "active_users": 1100
      },
      {
        "date": "2023-04-02",
        "total_users": 4820,
        "new_users": 25,
        "active_users": 1050
      },
      // ... 更多数据点
      {
        "date": "2023-04-30",
        "total_users": 5000,
        "new_users": 15,
        "active_users": 1200
      }
    ]
  }
}
```

## 用户统计接口

### 获取用户统计数据

- **URL**: `/api/v1/admin/stats/users/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取用户统计数据

**请求参数**:
- `period`: 统计周期，可选值：`today`, `yesterday`, `last_7_days`, `last_30_days`, `this_month`, `last_month`，默认为`last_30_days`

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total_users": 5000,
    "user_types": {
      "tourist": 4700,
      "merchant": 200,
      "admin": 100
    },
    "user_status": {
      "active": 4800,
      "inactive": 200
    },
    "new_users": {
      "total": 150,
      "by_day": [
        {
          "date": "2023-04-01",
          "count": 20
        },
        {
          "date": "2023-04-02",
          "count": 25
        },
        // ... 更多数据点
      ]
    },
    "active_users": {
      "total": 1200,
      "by_day": [
        {
          "date": "2023-04-01",
          "count": 1100
        },
        {
          "date": "2023-04-02",
          "count": 1050
        },
        // ... 更多数据点
      ]
    },
    "user_retention": {
      "day1": 0.8,
      "day7": 0.5,
      "day30": 0.3
    }
  }
}
```

### 获取用户地区分布

- **URL**: `/api/v1/admin/stats/users/regions/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取用户地区分布统计

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "regions": [
      {
        "region_name": "浙江省",
        "count": 1500,
        "percentage": 0.3
      },
      {
        "region_name": "江苏省",
        "count": 1000,
        "percentage": 0.2
      },
      {
        "region_name": "上海市",
        "count": 800,
        "percentage": 0.16
      },
      {
        "region_name": "北京市",
        "count": 500,
        "percentage": 0.1
      },
      {
        "region_name": "广东省",
        "count": 400,
        "percentage": 0.08
      },
      {
        "region_name": "其他",
        "count": 800,
        "percentage": 0.16
      }
    ]
  }
}
```

## 订单统计接口

### 获取订单统计数据

- **URL**: `/api/v1/admin/stats/orders/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取订单统计数据

**请求参数**:
- `period`: 统计周期，可选值：`today`, `yesterday`, `last_7_days`, `last_30_days`, `this_month`, `last_month`，默认为`last_30_days`
- `order_type`: 订单类型，可选值：`all`, `homestay`, `product`，默认为`all`

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total_orders": 2000,
    "order_types": {
      "homestay": 1200,
      "product": 800
    },
    "order_status": {
      "pending_payment": 100,
      "paid": 200,
      "confirmed": 300,
      "completed": 1300,
      "cancelled": 100
    },
    "total_revenue": 500000,
    "revenue_by_type": {
      "homestay": 400000,
      "product": 100000
    },
    "average_order_value": 250,
    "order_trends": {
      "by_day": [
        {
          "date": "2023-04-01",
          "count": 60,
          "revenue": 15000
        },
        {
          "date": "2023-04-02",
          "count": 65,
          "revenue": 16500
        },
        // ... 更多数据点
      ]
    },
    "top_products": [
      {
        "id": 1,
        "name": "太湖源山核桃",
        "orders_count": 100,
        "revenue": 6000
      },
      {
        "id": 2,
        "name": "土蜂蜜",
        "orders_count": 80,
        "revenue": 9600
      },
      // ... 更多产品
    ],
    "top_homestays": [
      {
        "id": 1,
        "name": "溪山隐居",
        "orders_count": 50,
        "revenue": 15000
      },
      {
        "id": 2,
        "name": "山林别院",
        "orders_count": 40,
        "revenue": 14000
      },
      // ... 更多民宿
    ]
  }
}
```

### 获取退款统计数据

- **URL**: `/api/v1/admin/stats/refunds/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取退款统计数据

**请求参数**:
- `period`: 统计周期，可选值：`today`, `yesterday`, `last_7_days`, `last_30_days`, `this_month`, `last_month`，默认为`last_30_days`

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total_refunds": 100,
    "refund_amount": 25000,
    "refund_rate": 0.05,
    "refund_status": {
      "pending": 20,
      "processing": 30,
      "approved": 40,
      "rejected": 10
    },
    "refund_reasons": [
      {
        "reason": "行程变更",
        "count": 40,
        "percentage": 0.4
      },
      {
        "reason": "天气原因",
        "count": 25,
        "percentage": 0.25
      },
      {
        "reason": "商品问题",
        "count": 20,
        "percentage": 0.2
      },
      {
        "reason": "其他",
        "count": 15,
        "percentage": 0.15
      }
    ],
    "refund_trends": {
      "by_day": [
        {
          "date": "2023-04-01",
          "count": 3,
          "amount": 750
        },
        {
          "date": "2023-04-02",
          "count": 4,
          "amount": 1000
        },
        // ... 更多数据点
      ]
    }
  }
}
```

## 内容统计接口

### 获取乡村统计数据

- **URL**: `/api/v1/admin/stats/villages/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取乡村统计数据

**请求参数**:
- `period`: 统计周期，可选值：`today`, `yesterday`, `last_7_days`, `last_30_days`, `this_month`, `last_month`，默认为`last_30_days`

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total_villages": 100,
    "village_status": {
      "pending": 5,
      "approved": 90,
      "rejected": 5
    },
    "top_villages_by_views": [
      {
        "id": 1,
        "name": "太湖源村",
        "views": 12345
      },
      {
        "id": 2,
        "name": "龙门古镇",
        "views": 10234
      },
      // ... 更多乡村
    ],
    "top_villages_by_orders": [
      {
        "id": 1,
        "name": "太湖源村",
        "orders_count": 500,
        "revenue": 150000
      },
      {
        "id": 2,
        "name": "龙门古镇",
        "orders_count": 400,
        "revenue": 120000
      },
      // ... 更多乡村
    ],
    "region_distribution": [
      {
        "region_name": "浙江省杭州市",
        "count": 30,
        "percentage": 0.3
      },
      {
        "region_name": "浙江省湖州市",
        "count": 15,
        "percentage": 0.15
      },
      // ... 更多地区
    ]
  }
}
```

### 获取民宿统计数据

- **URL**: `/api/v1/admin/stats/homestays/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取民宿统计数据

**请求参数**:
- `period`: 统计周期，可选值：`today`, `yesterday`, `last_7_days`, `last_30_days`, `this_month`, `last_month`，默认为`last_30_days`

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total_homestays": 300,
    "homestay_status": {
      "pending": 20,
      "approved": 270,
      "rejected": 10
    },
    "top_homestays_by_views": [
      {
        "id": 1,
        "name": "溪山隐居",
        "views": 5678
      },
      {
        "id": 2,
        "name": "山林别院",
        "views": 4567
      },
      // ... 更多民宿
    ],
    "top_homestays_by_orders": [
      {
        "id": 1,
        "name": "溪山隐居",
        "orders_count": 50,
        "revenue": 15000
      },
      {
        "id": 2,
        "name": "山林别院",
        "orders_count": 40,
        "revenue": 14000
      },
      // ... 更多民宿
    ],
    "price_distribution": [
      {
        "price_range": "0-200",
        "count": 50,
        "percentage": 0.17
      },
      {
        "price_range": "200-400",
        "count": 150,
        "percentage": 0.5
      },
      {
        "price_range": "400-600",
        "count": 70,
        "percentage": 0.23
      },
      {
        "price_range": "600+",
        "count": 30,
        "percentage": 0.1
      }
    ],
    "occupancy_rate": 0.75,
    "average_rating": 4.7
  }
}
```

### 获取用户内容统计数据

- **URL**: `/api/v1/admin/stats/user-content/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取用户生成内容统计数据

**请求参数**:
- `period`: 统计周期，可选值：`today`, `yesterday`, `last_7_days`, `last_30_days`, `this_month`, `last_month`，默认为`last_30_days`
- `content_type`: 内容类型，可选值：`all`, `reviews`, `travel_notes`, `questions`，默认为`all`

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "reviews": {
      "total": 1500,
      "pending": 50,
      "approved": 1400,
      "rejected": 50,
      "average_rating": 4.6,
      "with_images": 600,
      "new_reviews": 100,
      "by_day": [
        {
          "date": "2023-04-01",
          "count": 30
        },
        {
          "date": "2023-04-02",
          "count": 35
        },
        // ... 更多数据点
      ]
    },
    "travel_notes": {
      "total": 800,
      "pending": 30,
      "approved": 750,
      "rejected": 20,
      "total_views": 50000,
      "total_likes": 8000,
      "new_travel_notes": 50,
      "by_day": [
        {
          "date": "2023-04-01",
          "count": 10
        },
        {
          "date": "2023-04-02",
          "count": 12
        },
        // ... 更多数据点
      ]
    },
    "questions": {
      "total": 600,
      "pending": 20,
      "approved": 560,
      "rejected": 20,
      "total_answers": 1800,
      "new_questions": 30,
      "by_day": [
        {
          "date": "2023-04-01",
          "count": 8
        },
        {
          "date": "2023-04-02",
          "count": 7
        },
        // ... 更多数据点
      ]
    }
  }
}
```

## 商户统计接口

### 获取商户统计数据

- **URL**: `/api/v1/admin/stats/merchants/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取商户统计数据

**请求参数**:
- `period`: 统计周期，可选值：`today`, `yesterday`, `last_7_days`, `last_30_days`, `this_month`, `last_month`，默认为`last_30_days`

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total_merchants": 200,
    "merchant_status": {
      "active": 180,
      "inactive": 20
    },
    "new_merchants": {
      "total": 10,
      "by_day": [
        {
          "date": "2023-04-01",
          "count": 1
        },
        {
          "date": "2023-04-02",
          "count": 2
        },
        // ... 更多数据点
      ]
    },
    "top_merchants_by_revenue": [
      {
        "id": 1,
        "business_name": "山水民宿",
        "orders_count": 100,
        "revenue": 30000
      },
      {
        "id": 2,
        "business_name": "青山农家",
        "orders_count": 80,
        "revenue": 24000
      },
      // ... 更多商户
    ],
    "top_merchants_by_rating": [
      {
        "id": 3,
        "business_name": "溪畔农庄",
        "avg_rating": 4.9,
        "reviews_count": 50
      },
      {
        "id": 1,
        "business_name": "山水民宿",
        "avg_rating": 4.8,
        "reviews_count": 120
      },
      // ... 更多商户
    ],
    "region_distribution": [
      {
        "region_name": "浙江省杭州市",
        "count": 80,
        "percentage": 0.4
      },
      {
        "region_name": "浙江省湖州市",
        "count": 30,
        "percentage": 0.15
      },
      // ... 更多地区
    ]
  }
}
```

### 获取商户商品统计数据

- **URL**: `/api/v1/admin/stats/merchant-products/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取商户商品统计数据

**请求参数**:
- `period`: 统计周期，可选值：`today`, `yesterday`, `last_7_days`, `last_30_days`, `this_month`, `last_month`，默认为`last_30_days`

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total_products": {
      "homestay": 300,
      "product": 500
    },
    "product_status": {
      "homestay": {
        "pending": 20,
        "approved": 270,
        "rejected": 10
      },
      "product": {
        "pending": 30,
        "approved": 450,
        "rejected": 20
      }
    },
    "new_products": {
      "homestay": 15,
      "product": 25
    },
    "product_categories": {
      "homestay": [
        {
          "category": "民宿",
          "count": 200,
          "percentage": 0.67
        },
        {
          "category": "农家乐",
          "count": 100,
          "percentage": 0.33
        }
      ],
      "product": [
        {
          "category": "坚果",
          "count": 100,
          "percentage": 0.2
        },
        {
          "category": "蜂蜜",
          "count": 80,
          "percentage": 0.16
        },
        {
          "category": "茶叶",
          "count": 120,
          "percentage": 0.24
        },
        {
          "category": "水果",
          "count": 150,
          "percentage": 0.3
        },
        {
          "category": "其他",
          "count": 50,
          "percentage": 0.1
        }
      ]
    }
  }
}
``` 