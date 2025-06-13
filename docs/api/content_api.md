# 觅乡记 - 内容与评价模块API

## 评价相关接口

### 发表评价

- **URL**: `/api/v1/reviews/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 发表评价

**请求参数**:
```json
{
  "order_id": 1,
  "target_type": "homestay", // homestay(民宿)/product(农产品)/attraction(景点)
  "target_id": 1,
  "rating": 5,
  "content": "环境优美，设施齐全，服务周到，非常推荐！",
  "images": ["base64编码的图片1", "base64编码的图片2"],
  "is_anonymous": false
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "评价发表成功",
  "data": {
    "id": 1,
    "order_id": 1,
    "target_type": "homestay",
    "target_id": 1,
    "target_name": "溪山隐居",
    "rating": 5,
    "content": "环境优美，设施齐全，服务周到，非常推荐！",
    "images": [
      "https://example.com/review_img1.jpg",
      "https://example.com/review_img2.jpg"
    ],
    "is_anonymous": false,
    "status": "approved",
    "created_at": "2023-05-05T10:30:00Z"
  }
}
```

### 获取评价列表

- **URL**: `/api/v1/reviews/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取评价列表

**请求参数**:
- `target_type`: 评价对象类型，可选值：`homestay`, `product`, `attraction`
- `target_id`: 评价对象ID
- `rating`: 评分筛选，可选值：`1`, `2`, `3`, `4`, `5`
- `has_image`: 是否有图片，可选值：`true`, `false`
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
        "user_id": 5,
        "username": "旅行者",
        "avatar": "https://example.com/avatar5.jpg",
        "target_type": "homestay",
        "target_id": 1,
        "target_name": "溪山隐居",
        "rating": 5,
        "content": "环境优美，设施齐全，服务周到，非常推荐！",
        "images": [
          "https://example.com/review_img1.jpg",
          "https://example.com/review_img2.jpg"
        ],
        "is_anonymous": false,
        "created_at": "2023-05-05T10:30:00Z",
        "reply": {
          "content": "感谢您的光临和好评，期待您再次入住！",
          "created_at": "2023-05-05T14:20:00Z"
        }
      },
      {
        "id": 2,
        "user_id": 6,
        "username": "匿名用户",
        "avatar": "https://example.com/default_avatar.jpg",
        "target_type": "homestay",
        "target_id": 1,
        "target_name": "溪山隐居",
        "rating": 4,
        "content": "风景很好，房间略小，但整体不错。",
        "images": [],
        "is_anonymous": true,
        "created_at": "2023-05-03T16:45:00Z",
        "reply": null
      }
    ],
    "total": 2,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 回复评价

- **URL**: `/api/v1/reviews/{id}/reply/`
- **方法**: `POST`
- **权限**: 需要认证，且用户类型为商户或管理员
- **描述**: 回复评价

**请求参数**:
```json
{
  "content": "感谢您的光临和好评，期待您再次入住！"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "回复成功",
  "data": {
    "id": 1,
    "review_id": 1,
    "content": "感谢您的光临和好评，期待您再次入住！",
    "created_at": "2023-05-05T14:20:00Z"
  }
}
```

## 游记相关接口

### 发布游记

- **URL**: `/api/v1/travel-notes/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 发布游记

**请求参数**:
```json
{
  "title": "太湖源村两日游记",
  "cover_image": "base64编码的图片",
  "content": "昨天和朋友一起去了临安区的太湖源村，感受了一下乡村的宁静与美好...",
  "village_id": 1,
  "images": [
    {
      "image": "base64编码的图片1",
      "caption": "村口全景"
    },
    {
      "image": "base64编码的图片2",
      "caption": "溪流风光"
    }
  ]
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "游记发布成功",
  "data": {
    "id": 1,
    "title": "太湖源村两日游记",
    "cover_image": "https://example.com/travel_note1_cover.jpg",
    "content": "昨天和朋友一起去了临安区的太湖源村，感受了一下乡村的宁静与美好...",
    "village_id": 1,
    "village_name": "太湖源村",
    "status": "pending",
    "created_at": "2023-05-10T09:30:00Z"
  }
}
```

### 获取游记列表

- **URL**: `/api/v1/travel-notes/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取游记列表

**请求参数**:
- `village_id`: 乡村ID
- `user_id`: 用户ID
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
        "user_id": 5,
        "username": "旅行者",
        "avatar": "https://example.com/avatar5.jpg",
        "title": "太湖源村两日游记",
        "cover_image": "https://example.com/travel_note1_cover.jpg",
        "summary": "昨天和朋友一起去了临安区的太湖源村，感受了一下乡村的宁静与美好...",
        "village_id": 1,
        "village_name": "太湖源村",
        "views": 120,
        "likes": 15,
        "created_at": "2023-05-10T09:30:00Z"
      },
      {
        "id": 2,
        "user_id": 6,
        "username": "村游客",
        "avatar": "https://example.com/avatar6.jpg",
        "title": "龙门古镇一日游",
        "cover_image": "https://example.com/travel_note2_cover.jpg",
        "summary": "龙门古镇有着悠久的历史文化，古建筑保存完好...",
        "village_id": 2,
        "village_name": "龙门古镇",
        "views": 85,
        "likes": 8,
        "created_at": "2023-05-08T14:20:00Z"
      }
    ],
    "total": 2,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 获取游记详情

- **URL**: `/api/v1/travel-notes/{id}/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取游记详情

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "user_id": 5,
    "username": "旅行者",
    "avatar": "https://example.com/avatar5.jpg",
    "title": "太湖源村两日游记",
    "cover_image": "https://example.com/travel_note1_cover.jpg",
    "content": "昨天和朋友一起去了临安区的太湖源村，感受了一下乡村的宁静与美好...(完整内容)",
    "village_id": 1,
    "village_name": "太湖源村",
    "region_full_name": "浙江省杭州市临安区",
    "views": 120,
    "likes": 15,
    "created_at": "2023-05-10T09:30:00Z",
    "images": [
      {
        "id": 1,
        "image_url": "https://example.com/travel_note1_img1.jpg",
        "caption": "村口全景"
      },
      {
        "id": 2,
        "image_url": "https://example.com/travel_note1_img2.jpg",
        "caption": "溪流风光"
      }
    ],
    "comments": [
      {
        "id": 1,
        "user_id": 6,
        "username": "村游客",
        "avatar": "https://example.com/avatar6.jpg",
        "content": "照片拍得真美，我也想去看看！",
        "created_at": "2023-05-10T10:15:00Z"
      }
    ]
  }
}
```

### 点赞游记

- **URL**: `/api/v1/travel-notes/{id}/like/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 点赞/取消点赞游记

**请求参数**:
```json
{
  "action": "like" // like(点赞)/unlike(取消点赞)
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "点赞成功",
  "data": {
    "id": 1,
    "likes": 16
  }
}
```

### 评论游记

- **URL**: `/api/v1/travel-notes/{id}/comments/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 评论游记

**请求参数**:
```json
{
  "content": "照片拍得真美，我也想去看看！"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "评论成功",
  "data": {
    "id": 1,
    "user_id": 6,
    "username": "村游客",
    "avatar": "https://example.com/avatar6.jpg",
    "content": "照片拍得真美，我也想去看看！",
    "created_at": "2023-05-10T10:15:00Z"
  }
}
```

## 问答相关接口

### 发布问题

- **URL**: `/api/v1/questions/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 发布问题

**请求参数**:
```json
{
  "village_id": 1,
  "title": "太湖源村有哪些特色美食推荐？",
  "content": "准备下周去太湖源村玩，想了解一下有哪些当地特色美食，谢谢！"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "问题发布成功",
  "data": {
    "id": 1,
    "village_id": 1,
    "village_name": "太湖源村",
    "title": "太湖源村有哪些特色美食推荐？",
    "content": "准备下周去太湖源村玩，想了解一下有哪些当地特色美食，谢谢！",
    "status": "approved",
    "created_at": "2023-05-12T11:30:00Z"
  }
}
```

### 获取问题列表

- **URL**: `/api/v1/questions/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取问题列表

**请求参数**:
- `village_id`: 乡村ID
- `user_id`: 用户ID
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
        "user_id": 5,
        "username": "旅行者",
        "avatar": "https://example.com/avatar5.jpg",
        "village_id": 1,
        "village_name": "太湖源村",
        "title": "太湖源村有哪些特色美食推荐？",
        "content": "准备下周去太湖源村玩，想了解一下有哪些当地特色美食，谢谢！",
        "views": 45,
        "answers_count": 2,
        "created_at": "2023-05-12T11:30:00Z"
      },
      {
        "id": 2,
        "user_id": 6,
        "username": "村游客",
        "avatar": "https://example.com/avatar6.jpg",
        "village_id": 1,
        "village_name": "太湖源村",
        "title": "太湖源村的民宿价格如何？",
        "content": "想去太湖源村住几天，请问那里的民宿价格大概是多少？",
        "views": 32,
        "answers_count": 1,
        "created_at": "2023-05-11T16:45:00Z"
      }
    ],
    "total": 2,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 获取问题详情

- **URL**: `/api/v1/questions/{id}/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取问题详情

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "user_id": 5,
    "username": "旅行者",
    "avatar": "https://example.com/avatar5.jpg",
    "village_id": 1,
    "village_name": "太湖源村",
    "title": "太湖源村有哪些特色美食推荐？",
    "content": "准备下周去太湖源村玩，想了解一下有哪些当地特色美食，谢谢！",
    "views": 45,
    "created_at": "2023-05-12T11:30:00Z",
    "answers": [
      {
        "id": 1,
        "user_id": 7,
        "username": "村民老王",
        "avatar": "https://example.com/avatar7.jpg",
        "content": "太湖源村的山核桃很有名，还有土鸡煲、笋干炖肉、农家豆腐等都是当地特色。",
        "is_accepted": true,
        "likes": 8,
        "created_at": "2023-05-12T13:20:00Z"
      },
      {
        "id": 2,
        "user_id": 8,
        "username": "民宿老板",
        "avatar": "https://example.com/avatar8.jpg",
        "content": "推荐尝尝溪边鱼馆的野生溪鱼，很新鲜。还有龙井茶叶烧饼也是当地特色。",
        "is_accepted": false,
        "likes": 5,
        "created_at": "2023-05-12T14:10:00Z"
      }
    ]
  }
}
```

### 回答问题

- **URL**: `/api/v1/questions/{id}/answers/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 回答问题

**请求参数**:
```json
{
  "content": "太湖源村的山核桃很有名，还有土鸡煲、笋干炖肉、农家豆腐等都是当地特色。"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "回答成功",
  "data": {
    "id": 1,
    "question_id": 1,
    "content": "太湖源村的山核桃很有名，还有土鸡煲、笋干炖肉、农家豆腐等都是当地特色。",
    "is_accepted": false,
    "likes": 0,
    "created_at": "2023-05-12T13:20:00Z"
  }
}
```

### 采纳答案

- **URL**: `/api/v1/answers/{id}/accept/`
- **方法**: `POST`
- **权限**: 需要认证，且为问题发布者
- **描述**: 采纳答案

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "采纳成功",
  "data": {
    "id": 1,
    "is_accepted": true,
    "updated_at": "2023-05-12T15:30:00Z"
  }
}
```

### 点赞答案

- **URL**: `/api/v1/answers/{id}/like/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 点赞/取消点赞答案

**请求参数**:
```json
{
  "action": "like" // like(点赞)/unlike(取消点赞)
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "点赞成功",
  "data": {
    "id": 1,
    "likes": 9
  }
}
```

## 资讯相关接口

### 获取资讯列表

- **URL**: `/api/v1/news/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取资讯列表

**请求参数**:
- `category`: 分类
- `keyword`: 关键词搜索
- `is_top`: 是否置顶，可选值：`true`, `false`
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

### 获取资讯详情

- **URL**: `/api/v1/news/{id}/`
- **方法**: `GET`
- **权限**: 无需认证
- **描述**: 获取资讯详情

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "title": "乡村振兴政策解读：2023年农村旅游发展新方向",
    "category": "政策",
    "cover_image": "https://example.com/news1.jpg",
    "summary": "近日，国家发布了关于乡村振兴战略的最新政策，对农村旅游发展提出了新的要求和方向...",
    "content": "近日，国家发布了关于乡村振兴战略的最新政策，对农村旅游发展提出了新的要求和方向...(完整内容)",
    "author": "乡村发展研究员",
    "source": "乡村振兴报",
    "views": 1246,
    "is_top": true,
    "created_at": "2023-05-15T09:00:00Z",
    "related_news": [
      {
        "id": 2,
        "title": "临安区太湖源村入选"中国最美乡村"名单",
        "cover_image": "https://example.com/news2.jpg",
        "created_at": "2023-05-14T10:30:00Z"
      }
    ]
  }
}
``` 