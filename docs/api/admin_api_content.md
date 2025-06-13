# 觅乡记 - 管理后台API (内容管理部分)

## 通用说明

管理后台API仅供平台管理员使用，所有接口均需要管理员权限。

基础URL: `/api/v1/admin/`

## 乡村管理接口

### 获取乡村列表

- **URL**: `/api/v1/admin/villages/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取乡村列表

**请求参数**:
- `region_id`: 区域ID
- `status`: 状态，可选值：`pending`, `approved`, `rejected`
- `is_recommended`: 是否推荐，可选值：`true`, `false`
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
        "name": "太湖源村",
        "region_id": 112,
        "region_name": "临安区",
        "region_full_name": "浙江省杭州市临安区",
        "cover_image": "https://example.com/village1.jpg",
        "intro": "浙江省杭州市临安区著名的乡村旅游目的地",
        "views": 12345,
        "status": "approved",
        "is_recommended": true,
        "created_at": "2023-01-10T10:00:00Z"
      },
      {
        "id": 2,
        "name": "龙门古镇",
        "region_id": 112,
        "region_name": "临安区",
        "region_full_name": "浙江省杭州市临安区",
        "cover_image": "https://example.com/village2.jpg",
        "intro": "保存完好的古建筑群，有着悠久的历史文化",
        "views": 10234,
        "status": "approved",
        "is_recommended": true,
        "created_at": "2023-01-15T14:00:00Z"
      }
    ],
    "total": 2,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 创建乡村

- **URL**: `/api/v1/admin/villages/`
- **方法**: `POST`
- **权限**: 需要管理员权限
- **描述**: 创建乡村信息

**请求参数**:
```json
{
  "name": "西溪村",
  "region_id": 112,
  "intro": "位于杭州市临安区的美丽乡村",
  "description": "西溪村环境优美，民风淳朴，是休闲度假的好去处...",
  "cover_image": "base64编码的图片",
  "location": {
    "latitude": 30.25,
    "longitude": 119.75
  },
  "features": ["山水", "民宿", "户外"],
  "status": "approved",
  "is_recommended": false
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "乡村创建成功",
  "data": {
    "id": 3,
    "name": "西溪村",
    "region_id": 112,
    "region_name": "临安区",
    "cover_image": "https://example.com/village3.jpg",
    "status": "approved",
    "created_at": "2023-05-16T14:30:00Z"
  }
}
```

### 审核乡村

- **URL**: `/api/v1/admin/villages/{id}/review/`
- **方法**: `POST`
- **权限**: 需要管理员权限
- **描述**: 审核乡村信息

**请求参数**:
```json
{
  "action": "approve", // approve(通过)/reject(拒绝)
  "reason": "内容符合要求"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "审核成功",
  "data": {
    "id": 3,
    "name": "西溪村",
    "status": "approved",
    "updated_at": "2023-05-16T15:30:00Z"
  }
}
```

### 设置推荐状态

- **URL**: `/api/v1/admin/villages/{id}/recommend/`
- **方法**: `PATCH`
- **权限**: 需要管理员权限
- **描述**: 设置乡村推荐状态

**请求参数**:
```json
{
  "is_recommended": true
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "推荐状态已更新",
  "data": {
    "id": 3,
    "name": "西溪村",
    "is_recommended": true,
    "updated_at": "2023-05-16T16:30:00Z"
  }
}
```

## 民宿管理接口

### 获取民宿列表

- **URL**: `/api/v1/admin/homestays/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取民宿列表

**请求参数**:
- `village_id`: 乡村ID
- `merchant_id`: 商户ID
- `status`: 状态，可选值：`pending`, `approved`, `rejected`
- `is_recommended`: 是否推荐，可选值：`true`, `false`
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
        "name": "溪山隐居",
        "merchant_id": 1,
        "merchant_name": "山水民宿",
        "village_id": 1,
        "village_name": "太湖源村",
        "cover_image": "https://example.com/homestay1.jpg",
        "intro": "位于溪边的特色民宿",
        "min_price": 298,
        "max_price": 698,
        "status": "approved",
        "is_recommended": true,
        "created_at": "2023-01-20T10:00:00Z"
      },
      {
        "id": 2,
        "name": "山林别院",
        "merchant_id": 2,
        "merchant_name": "青山农家",
        "village_id": 1,
        "village_name": "太湖源村",
        "cover_image": "https://example.com/homestay2.jpg",
        "intro": "掩映在山林间的特色民宿",
        "min_price": 358,
        "max_price": 758,
        "status": "approved",
        "is_recommended": true,
        "created_at": "2023-01-25T14:00:00Z"
      }
    ],
    "total": 2,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 审核民宿

- **URL**: `/api/v1/admin/homestays/{id}/review/`
- **方法**: `POST`
- **权限**: 需要管理员权限
- **描述**: 审核民宿信息

**请求参数**:
```json
{
  "action": "approve", // approve(通过)/reject(拒绝)
  "reason": "内容符合要求"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "审核成功",
  "data": {
    "id": 3,
    "name": "竹林小筑",
    "status": "approved",
    "updated_at": "2023-05-17T10:30:00Z"
  }
}
```

### 设置推荐状态

- **URL**: `/api/v1/admin/homestays/{id}/recommend/`
- **方法**: `PATCH`
- **权限**: 需要管理员权限
- **描述**: 设置民宿推荐状态

**请求参数**:
```json
{
  "is_recommended": true
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "推荐状态已更新",
  "data": {
    "id": 3,
    "name": "竹林小筑",
    "is_recommended": true,
    "updated_at": "2023-05-17T11:30:00Z"
  }
}
```

## 农产品管理接口

### 获取农产品列表

- **URL**: `/api/v1/admin/products/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取农产品列表

**请求参数**:
- `village_id`: 乡村ID
- `merchant_id`: 商户ID
- `category`: 分类
- `status`: 状态，可选值：`pending`, `approved`, `rejected`
- `is_recommended`: 是否推荐，可选值：`true`, `false`
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
        "name": "太湖源山核桃",
        "merchant_id": 1,
        "merchant_name": "山水民宿",
        "village_id": 1,
        "village_name": "太湖源村",
        "category": "坚果",
        "cover_image": "https://example.com/product1.jpg",
        "intro": "当地特产，营养丰富",
        "price": 60,
        "status": "approved",
        "is_recommended": true,
        "created_at": "2023-02-10T10:00:00Z"
      },
      {
        "id": 2,
        "name": "土蜂蜜",
        "merchant_id": 2,
        "merchant_name": "青山农家",
        "village_id": 1,
        "village_name": "太湖源村",
        "category": "蜂蜜",
        "cover_image": "https://example.com/product2.jpg",
        "intro": "纯天然野生土蜂蜜",
        "price": 120,
        "status": "approved",
        "is_recommended": true,
        "created_at": "2023-02-15T14:00:00Z"
      }
    ],
    "total": 2,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 审核农产品

- **URL**: `/api/v1/admin/products/{id}/review/`
- **方法**: `POST`
- **权限**: 需要管理员权限
- **描述**: 审核农产品信息

**请求参数**:
```json
{
  "action": "approve", // approve(通过)/reject(拒绝)
  "reason": "内容符合要求"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "审核成功",
  "data": {
    "id": 3,
    "name": "龙井茶",
    "status": "approved",
    "updated_at": "2023-05-17T14:30:00Z"
  }
}
```

### 设置推荐状态

- **URL**: `/api/v1/admin/products/{id}/recommend/`
- **方法**: `PATCH`
- **权限**: 需要管理员权限
- **描述**: 设置农产品推荐状态

**请求参数**:
```json
{
  "is_recommended": true
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "推荐状态已更新",
  "data": {
    "id": 3,
    "name": "龙井茶",
    "is_recommended": true,
    "updated_at": "2023-05-17T15:30:00Z"
  }
}
```

## 评价管理接口

### 获取评价列表

- **URL**: `/api/v1/admin/reviews/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取评价列表

**请求参数**:
- `target_type`: 评价对象类型，可选值：`homestay`, `product`, `attraction`
- `target_id`: 评价对象ID
- `status`: 状态，可选值：`pending`, `approved`, `rejected`
- `rating`: 评分，可选值：`1`, `2`, `3`, `4`, `5`
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
        "user_id": 3,
        "username": "user1",
        "target_type": "homestay",
        "target_id": 1,
        "target_name": "溪山隐居",
        "rating": 5,
        "content": "环境优美，设施齐全，服务周到，非常推荐！",
        "images": [
          "https://example.com/review_img1.jpg",
          "https://example.com/review_img2.jpg"
        ],
        "status": "approved",
        "created_at": "2023-05-05T10:30:00Z",
        "has_reply": true
      },
      {
        "id": 2,
        "user_id": 4,
        "username": "user2",
        "target_type": "product",
        "target_id": 1,
        "target_name": "太湖源山核桃",
        "rating": 5,
        "content": "非常新鲜的山核桃，口感香脆，很满意！",
        "images": [],
        "status": "approved",
        "created_at": "2023-05-10T14:20:00Z",
        "has_reply": true
      }
    ],
    "total": 2,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 审核评价

- **URL**: `/api/v1/admin/reviews/{id}/review/`
- **方法**: `POST`
- **权限**: 需要管理员权限
- **描述**: 审核评价

**请求参数**:
```json
{
  "action": "approve", // approve(通过)/reject(拒绝)
  "reason": "内容符合要求"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "审核成功",
  "data": {
    "id": 3,
    "status": "approved",
    "updated_at": "2023-05-18T10:30:00Z"
  }
}
```

## 游记管理接口

### 获取游记列表

- **URL**: `/api/v1/admin/travel-notes/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取游记列表

**请求参数**:
- `village_id`: 乡村ID
- `user_id`: 用户ID
- `status`: 状态，可选值：`pending`, `approved`, `rejected`
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
        "user_id": 3,
        "username": "user1",
        "title": "太湖源村两日游记",
        "cover_image": "https://example.com/travel_note1_cover.jpg",
        "village_id": 1,
        "village_name": "太湖源村",
        "views": 120,
        "likes": 15,
        "status": "approved",
        "created_at": "2023-05-10T09:30:00Z"
      },
      {
        "id": 2,
        "user_id": 4,
        "username": "user2",
        "title": "龙门古镇一日游",
        "cover_image": "https://example.com/travel_note2_cover.jpg",
        "village_id": 2,
        "village_name": "龙门古镇",
        "views": 85,
        "likes": 8,
        "status": "pending",
        "created_at": "2023-05-12T14:20:00Z"
      }
    ],
    "total": 2,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 审核游记

- **URL**: `/api/v1/admin/travel-notes/{id}/review/`
- **方法**: `POST`
- **权限**: 需要管理员权限
- **描述**: 审核游记

**请求参数**:
```json
{
  "action": "approve", // approve(通过)/reject(拒绝)
  "reason": "内容符合要求"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "审核成功",
  "data": {
    "id": 2,
    "title": "龙门古镇一日游",
    "status": "approved",
    "updated_at": "2023-05-18T11:30:00Z"
  }
}
```

## 问答管理接口

### 获取问题列表

- **URL**: `/api/v1/admin/questions/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取问题列表

**请求参数**:
- `village_id`: 乡村ID
- `user_id`: 用户ID
- `status`: 状态，可选值：`pending`, `approved`, `rejected`
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
        "user_id": 3,
        "username": "user1",
        "village_id": 1,
        "village_name": "太湖源村",
        "title": "太湖源村有哪些特色美食推荐？",
        "views": 45,
        "answers_count": 2,
        "status": "approved",
        "created_at": "2023-05-12T11:30:00Z"
      },
      {
        "id": 2,
        "user_id": 4,
        "username": "user2",
        "village_id": 1,
        "village_name": "太湖源村",
        "title": "太湖源村的民宿价格如何？",
        "views": 32,
        "answers_count": 1,
        "status": "pending",
        "created_at": "2023-05-13T16:45:00Z"
      }
    ],
    "total": 2,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 审核问题

- **URL**: `/api/v1/admin/questions/{id}/review/`
- **方法**: `POST`
- **权限**: 需要管理员权限
- **描述**: 审核问题

**请求参数**:
```json
{
  "action": "approve", // approve(通过)/reject(拒绝)
  "reason": "内容符合要求"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "审核成功",
  "data": {
    "id": 2,
    "title": "太湖源村的民宿价格如何？",
    "status": "approved",
    "updated_at": "2023-05-18T14:30:00Z"
  }
}
```

## 资讯管理接口

### 获取资讯列表

- **URL**: `/api/v1/admin/news/`
- **方法**: `GET`
- **权限**: 需要管理员权限
- **描述**: 获取资讯列表

**请求参数**:
- `category`: 分类
- `status`: 状态，可选值：`draft`, `published`
- `is_top`: 是否置顶，可选值：`true`, `false`
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
        "title": "乡村振兴政策解读：2023年农村旅游发展新方向",
        "category": "政策",
        "cover_image": "https://example.com/news1.jpg",
        "summary": "近日，国家发布了关于乡村振兴战略的最新政策，对农村旅游发展提出了新的要求和方向...",
        "author": "乡村发展研究员",
        "source": "乡村振兴报",
        "views": 1245,
        "status": "published",
        "is_top": true,
        "created_at": "2023-05-15T09:00:00Z"
      },
      {
        "id": 2,
        "title": "临安区太湖源村入选"中国最美乡村"名单",
        "category": "乡村动态",
        "cover_image": "https://example.com/news2.jpg",
        "summary": "日前，文化和旅游部公布了2023年"中国最美乡村"名单，浙江省杭州市临安区太湖源村成功入选...",
        "author": "文旅记者",
        "source": "杭州日报",
        "views": 980,
        "status": "published",
        "is_top": false,
        "created_at": "2023-05-14T10:30:00Z"
      }
    ],
    "total": 2,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 创建资讯

- **URL**: `/api/v1/admin/news/`
- **方法**: `POST`
- **权限**: 需要管理员权限
- **描述**: 创建资讯

**请求参数**:
```json
{
  "title": "乡村旅游发展论坛将在杭州举行",
  "category": "活动",
  "cover_image": "base64编码的图片",
  "summary": "由文化和旅游部主办的第五届全国乡村旅游发展论坛将于下月在杭州举行...",
  "content": "由文化和旅游部主办的第五届全国乡村旅游发展论坛将于下月在杭州举行...(完整内容)",
  "author": "文旅编辑",
  "source": "中国旅游报",
  "status": "published",
  "is_top": false
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "资讯创建成功",
  "data": {
    "id": 3,
    "title": "乡村旅游发展论坛将在杭州举行",
    "category": "活动",
    "status": "published",
    "created_at": "2023-05-18T16:30:00Z"
  }
}
```

### 更新资讯

- **URL**: `/api/v1/admin/news/{id}/`
- **方法**: `PUT`
- **权限**: 需要管理员权限
- **描述**: 更新资讯

**请求参数**:
```json
{
  "title": "第五届全国乡村旅游发展论坛将在杭州举行",
  "category": "活动",
  "cover_image": "base64编码的图片",
  "summary": "由文化和旅游部主办的第五届全国乡村旅游发展论坛将于下月在杭州举行...",
  "content": "由文化和旅游部主办的第五届全国乡村旅游发展论坛将于下月在杭州举行...(更新后的完整内容)",
  "author": "文旅编辑",
  "source": "中国旅游报",
  "status": "published",
  "is_top": true
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "资讯更新成功",
  "data": {
    "id": 3,
    "title": "第五届全国乡村旅游发展论坛将在杭州举行",
    "category": "活动",
    "status": "published",
    "is_top": true,
    "updated_at": "2023-05-18T17:30:00Z"
  }
}
```

### 设置置顶状态

- **URL**: `/api/v1/admin/news/{id}/top/`
- **方法**: `PATCH`
- **权限**: 需要管理员权限
- **描述**: 设置资讯置顶状态

**请求参数**:
```json
{
  "is_top": true
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "置顶状态已更新",
  "data": {
    "id": 3,
    "title": "第五届全国乡村旅游发展论坛将在杭州举行",
    "is_top": true,
    "updated_at": "2023-05-18T18:30:00Z"
  }
}
``` 