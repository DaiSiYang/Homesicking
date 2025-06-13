# 觅乡记 - 资源模块API

## 区域相关接口

### 获取区域列表

- **URL**: `/api/v1/regions/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取区域列表，支持省市县三级查询

**请求参数**:
- `parent_id`: 父级区域ID，不传则获取省级区域
- `level`: 区域级别，可选值：`province`, `city`, `county`
- `is_hot`: 是否热门区域，可选值：`true`, `false`

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 1,
      "name": "浙江省",
      "code": "330000",
      "level": "province",
      "parent_id": null,
      "is_hot": true
    },
    {
      "id": 2,
      "name": "江苏省",
      "code": "320000",
      "level": "province",
      "parent_id": null,
      "is_hot": true
    }
  ]
}
```

### 获取区域详情

- **URL**: `/api/v1/regions/{id}/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取区域详情

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 11,
    "name": "杭州市",
    "code": "330100",
    "level": "city",
    "parent_id": 1,
    "parent_name": "浙江省",
    "is_hot": true,
    "children": [
      {
        "id": 111,
        "name": "西湖区",
        "code": "330106",
        "level": "county"
      },
      {
        "id": 112,
        "name": "临安区",
        "code": "330112",
        "level": "county"
      }
    ]
  }
}
```

## 乡村相关接口

### 获取乡村列表

- **URL**: `/api/v1/villages/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取乡村列表

**请求参数**:
- `region_id`: 区域ID
- `keyword`: 关键词搜索
- `is_recommended`: 是否推荐，可选值：`true`, `false`
- `page`: 页码，默认1
- `page_size`: 每页数量，默认10

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "results": [
      {
        "id": 1,
        "name": "太湖源村",
        "region_id": 112,
        "region_name": "临安区",
        "cover_image": "https://example.com/village1.jpg",
        "intro": "浙江省杭州市临安区著名的乡村旅游目的地",
        "features": ["山水", "民宿", "户外"],
        "rating": 4.8,
        "is_recommended": true
      },
      {
        "id": 2,
        "name": "龙门古镇",
        "region_id": 112,
        "region_name": "临安区",
        "cover_image": "https://example.com/village2.jpg",
        "intro": "保存完好的古建筑群，有着悠久的历史文化",
        "features": ["古镇", "文化", "美食"],
        "rating": 4.6,
        "is_recommended": true
      }
    ],
    "total": 15,
    "page": 1,
    "page_size": 10,
    "pages": 2
  }
}
```

### 获取乡村详情

- **URL**: `/api/v1/villages/{id}/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取乡村详情

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "name": "太湖源村",
    "region_id": 112,
    "region_name": "临安区",
    "region_full_name": "浙江省杭州市临安区",
    "intro": "浙江省杭州市临安区著名的乡村旅游目的地",
    "description": "太湖源村位于浙江省杭州市临安区太湖源镇，是钱塘江源头所在地...",
    "cover_image": "https://example.com/village1.jpg",
    "location": {
      "latitude": 30.23,
      "longitude": 119.72
    },
    "features": ["山水", "民宿", "户外"],
    "views": 12345,
    "rating": 4.8,
    "is_recommended": true,
    "gallery": [
      {
        "id": 1,
        "image_url": "https://example.com/village1_1.jpg",
        "caption": "村口全景"
      },
      {
        "id": 2,
        "image_url": "https://example.com/village1_2.jpg",
        "caption": "太湖源风光"
      }
    ],
    "attractions": [
      {
        "id": 1,
        "name": "太湖源",
        "cover_image": "https://example.com/attraction1.jpg",
        "intro": "钱塘江的源头，自然风光优美"
      },
      {
        "id": 2,
        "name": "天目山",
        "cover_image": "https://example.com/attraction2.jpg",
        "intro": "国家级自然保护区，生物多样性丰富"
      }
    ],
    "homestays": [
      {
        "id": 1,
        "name": "溪山隐居",
        "cover_image": "https://example.com/homestay1.jpg",
        "intro": "位于溪边的特色民宿",
        "min_price": 298
      }
    ],
    "products": [
      {
        "id": 1,
        "name": "太湖源山核桃",
        "cover_image": "https://example.com/product1.jpg",
        "intro": "当地特产，营养丰富",
        "price": 60
      }
    ],
    "foods": [
      {
        "id": 1,
        "name": "农家土菜",
        "cover_image": "https://example.com/food1.jpg",
        "intro": "使用当地食材制作的特色菜肴",
        "price": 128
      }
    ]
  }
}
```

### 获取乡村景点列表

- **URL**: `/api/v1/villages/{village_id}/attractions/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取乡村景点列表

**请求参数**:
- `page`: 页码，默认1
- `page_size`: 每页数量，默认10

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "results": [
      {
        "id": 1,
        "name": "太湖源",
        "village_id": 1,
        "village_name": "太湖源村",
        "cover_image": "https://example.com/attraction1.jpg",
        "intro": "钱塘江的源头，自然风光优美",
        "ticket_price": 50,
        "opening_hours": "08:00-17:00"
      },
      {
        "id": 2,
        "name": "天目山",
        "village_id": 1,
        "village_name": "太湖源村",
        "cover_image": "https://example.com/attraction2.jpg",
        "intro": "国家级自然保护区，生物多样性丰富",
        "ticket_price": 80,
        "opening_hours": "08:00-16:30"
      }
    ],
    "total": 5,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 获取景点详情

- **URL**: `/api/v1/attractions/{id}/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取景点详情

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "name": "太湖源",
    "village_id": 1,
    "village_name": "太湖源村",
    "intro": "钱塘江的源头，自然风光优美",
    "description": "太湖源是钱塘江的源头，位于浙江省杭州市临安区太湖源村...",
    "cover_image": "https://example.com/attraction1.jpg",
    "location": {
      "latitude": 30.24,
      "longitude": 119.73
    },
    "opening_hours": "08:00-17:00",
    "ticket_price": 50,
    "gallery": [
      {
        "id": 1,
        "image_url": "https://example.com/attraction1_1.jpg",
        "caption": "源头全景"
      },
      {
        "id": 2,
        "image_url": "https://example.com/attraction1_2.jpg",
        "caption": "溪流风光"
      }
    ],
    "reviews": [
      {
        "id": 1,
        "user_id": 5,
        "username": "旅行者",
        "avatar": "https://example.com/avatar5.jpg",
        "rating": 5,
        "content": "风景秀丽，环境优美，值得一游！",
        "created_at": "2023-01-10T09:30:00Z"
      }
    ]
  }
}
```

## 民宿相关接口

### 获取民宿列表

- **URL**: `/api/v1/homestays/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取民宿列表

**请求参数**:
- `village_id`: 乡村ID
- `region_id`: 区域ID
- `keyword`: 关键词搜索
- `min_price`: 最低价格
- `max_price`: 最高价格
- `is_recommended`: 是否推荐，可选值：`true`, `false`
- `page`: 页码，默认1
- `page_size`: 每页数量，默认10

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "results": [
      {
        "id": 1,
        "name": "溪山隐居",
        "merchant_id": 3,
        "merchant_name": "山水民宿",
        "village_id": 1,
        "village_name": "太湖源村",
        "cover_image": "https://example.com/homestay1.jpg",
        "intro": "位于溪边的特色民宿",
        "address": "浙江省杭州市临安区太湖源村28号",
        "min_price": 298,
        "max_price": 698,
        "rating": 4.9,
        "is_recommended": true
      },
      {
        "id": 2,
        "name": "山林别院",
        "merchant_id": 4,
        "merchant_name": "青山农家",
        "village_id": 1,
        "village_name": "太湖源村",
        "cover_image": "https://example.com/homestay2.jpg",
        "intro": "掩映在山林间的特色民宿",
        "address": "浙江省杭州市临安区太湖源村15号",
        "min_price": 358,
        "max_price": 758,
        "rating": 4.7,
        "is_recommended": true
      }
    ],
    "total": 8,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 获取民宿详情

- **URL**: `/api/v1/homestays/{id}/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取民宿详情

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "name": "溪山隐居",
    "merchant_id": 3,
    "merchant_name": "山水民宿",
    "village_id": 1,
    "village_name": "太湖源村",
    "region_full_name": "浙江省杭州市临安区",
    "intro": "位于溪边的特色民宿",
    "description": "溪山隐居位于太湖源村溪边，远离喧嚣，环境清幽...",
    "cover_image": "https://example.com/homestay1.jpg",
    "address": "浙江省杭州市临安区太湖源村28号",
    "location": {
      "latitude": 30.23,
      "longitude": 119.72
    },
    "facilities": ["WiFi", "空调", "热水", "厨房", "停车场"],
    "rules": "禁止吸烟，安静休息，爱护环境",
    "min_price": 298,
    "max_price": 698,
    "rating": 4.9,
    "views": 5678,
    "gallery": [
      {
        "id": 1,
        "image_url": "https://example.com/homestay1_1.jpg",
        "caption": "外观"
      },
      {
        "id": 2,
        "image_url": "https://example.com/homestay1_2.jpg",
        "caption": "客厅"
      },
      {
        "id": 3,
        "image_url": "https://example.com/homestay1_3.jpg",
        "caption": "卧室"
      }
    ],
    "room_types": [
      {
        "id": 1,
        "name": "溪景大床房",
        "description": "面向溪流的大床房，带独立卫浴",
        "max_guests": 2,
        "bed_info": "1.8米大床1张",
        "area": 30,
        "price": 298,
        "inventory": 3,
        "gallery": [
          {
            "id": 1,
            "image_url": "https://example.com/room1_1.jpg",
            "caption": "室内全景"
          },
          {
            "id": 2,
            "image_url": "https://example.com/room1_2.jpg",
            "caption": "卫浴"
          }
        ]
      },
      {
        "id": 2,
        "name": "山景家庭房",
        "description": "面向山景的家庭房，适合一家三口",
        "max_guests": 3,
        "bed_info": "1.8米大床1张，1.2米单人床1张",
        "area": 45,
        "price": 458,
        "inventory": 2,
        "gallery": [
          {
            "id": 3,
            "image_url": "https://example.com/room2_1.jpg",
            "caption": "室内全景"
          },
          {
            "id": 4,
            "image_url": "https://example.com/room2_2.jpg",
            "caption": "卫浴"
          }
        ]
      }
    ],
    "reviews": [
      {
        "id": 1,
        "user_id": 5,
        "username": "旅行者",
        "avatar": "https://example.com/avatar5.jpg",
        "rating": 5,
        "content": "环境优美，设施齐全，服务周到，非常推荐！",
        "created_at": "2023-01-15T14:30:00Z",
        "reply": {
          "content": "感谢您的光临和好评，期待您再次入住！",
          "created_at": "2023-01-15T16:20:00Z"
        }
      }
    ]
  }
}
```

### 获取房价日历

- **URL**: `/api/v1/room-types/{room_type_id}/prices/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取房型价格日历

**请求参数**:
- `start_date`: 开始日期，格式：YYYY-MM-DD
- `end_date`: 结束日期，格式：YYYY-MM-DD

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "room_type_id": 1,
    "room_type_name": "溪景大床房",
    "base_price": 298,
    "prices": [
      {
        "date": "2023-05-01",
        "price": 298,
        "inventory": 3,
        "status": "available"
      },
      {
        "date": "2023-05-02",
        "price": 298,
        "inventory": 3,
        "status": "available"
      },
      {
        "date": "2023-05-03",
        "price": 358,
        "inventory": 2,
        "status": "available"
      },
      {
        "date": "2023-05-04",
        "price": 458,
        "inventory": 1,
        "status": "available"
      },
      {
        "date": "2023-05-05",
        "price": 458,
        "inventory": 0,
        "status": "sold_out"
      }
    ]
  }
}
```

## 农产品相关接口

### 获取农产品列表

- **URL**: `/api/v1/products/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取农产品列表

**请求参数**:
- `village_id`: 乡村ID
- `region_id`: 区域ID
- `category`: 分类
- `keyword`: 关键词搜索
- `min_price`: 最低价格
- `max_price`: 最高价格
- `is_recommended`: 是否推荐，可选值：`true`, `false`
- `page`: 页码，默认1
- `page_size`: 每页数量，默认10

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "results": [
      {
        "id": 1,
        "name": "太湖源山核桃",
        "merchant_id": 3,
        "merchant_name": "山水民宿",
        "village_id": 1,
        "village_name": "太湖源村",
        "category": "坚果",
        "cover_image": "https://example.com/product1.jpg",
        "intro": "当地特产，营养丰富",
        "price": 60,
        "rating": 4.8,
        "is_recommended": true
      },
      {
        "id": 2,
        "name": "土蜂蜜",
        "merchant_id": 4,
        "merchant_name": "青山农家",
        "village_id": 1,
        "village_name": "太湖源村",
        "category": "蜂蜜",
        "cover_image": "https://example.com/product2.jpg",
        "intro": "纯天然野生土蜂蜜",
        "price": 120,
        "rating": 4.9,
        "is_recommended": true
      }
    ],
    "total": 10,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 获取农产品详情

- **URL**: `/api/v1/products/{id}/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取农产品详情

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "name": "太湖源山核桃",
    "merchant_id": 3,
    "merchant_name": "山水民宿",
    "village_id": 1,
    "village_name": "太湖源村",
    "region_full_name": "浙江省杭州市临安区",
    "category": "坚果",
    "intro": "当地特产，营养丰富",
    "description": "太湖源山核桃产自临安区太湖源村深山，无污染，营养丰富...",
    "cover_image": "https://example.com/product1.jpg",
    "price": 60,
    "inventory": 100,
    "sales": 500,
    "rating": 4.8,
    "views": 3456,
    "gallery": [
      {
        "id": 1,
        "image_url": "https://example.com/product1_1.jpg",
        "caption": "包装"
      },
      {
        "id": 2,
        "image_url": "https://example.com/product1_2.jpg",
        "caption": "特写"
      }
    ],
    "skus": [
      {
        "id": 1,
        "sku_name": "小包装",
        "attributes": {
          "规格": "250g"
        },
        "price": 60,
        "inventory": 50
      },
      {
        "id": 2,
        "sku_name": "中包装",
        "attributes": {
          "规格": "500g"
        },
        "price": 110,
        "inventory": 30
      },
      {
        "id": 3,
        "sku_name": "大包装",
        "attributes": {
          "规格": "1kg"
        },
        "price": 210,
        "inventory": 20
      }
    ],
    "reviews": [
      {
        "id": 1,
        "user_id": 5,
        "username": "美食家",
        "avatar": "https://example.com/avatar5.jpg",
        "rating": 5,
        "content": "非常新鲜的山核桃，口感香脆，很满意！",
        "created_at": "2023-01-20T10:30:00Z",
        "reply": {
          "content": "感谢您的好评，欢迎再次购买！",
          "created_at": "2023-01-20T11:20:00Z"
        }
      }
    ]
  }
}
```

## 美食相关接口

### 获取美食列表

- **URL**: `/api/v1/foods/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取美食列表

**请求参数**:
- `village_id`: 乡村ID
- `region_id`: 区域ID
- `category`: 分类
- `keyword`: 关键词搜索
- `page`: 页码，默认1
- `page_size`: 每页数量，默认10

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "results": [
      {
        "id": 1,
        "name": "农家土菜",
        "merchant_id": 3,
        "merchant_name": "山水民宿",
        "village_id": 1,
        "village_name": "太湖源村",
        "category": "农家菜",
        "cover_image": "https://example.com/food1.jpg",
        "intro": "使用当地食材制作的特色菜肴",
        "price": 128
      },
      {
        "id": 2,
        "name": "野生鱼宴",
        "merchant_id": 4,
        "merchant_name": "青山农家",
        "village_id": 1,
        "village_name": "太湖源村",
        "category": "鱼类",
        "cover_image": "https://example.com/food2.jpg",
        "intro": "溪水中捕捞的野生鱼，鲜美可口",
        "price": 168
      }
    ],
    "total": 6,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 获取美食详情

- **URL**: `/api/v1/foods/{id}/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取美食详情

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "name": "农家土菜",
    "merchant_id": 3,
    "merchant_name": "山水民宿",
    "village_id": 1,
    "village_name": "太湖源村",
    "region_full_name": "浙江省杭州市临安区",
    "category": "农家菜",
    "intro": "使用当地食材制作的特色菜肴",
    "description": "农家土菜采用太湖源村当地种植的有机蔬菜和放养家禽，保持原汁原味...",
    "cover_image": "https://example.com/food1.jpg",
    "price": 128,
    "gallery": [
      {
        "id": 1,
        "image_url": "https://example.com/food1_1.jpg",
        "caption": "全家福"
      },
      {
        "id": 2,
        "image_url": "https://example.com/food1_2.jpg",
        "caption": "特色菜"
      }
    ]
  }
}
``` 