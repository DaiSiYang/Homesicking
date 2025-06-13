# 觅乡记 - 订单与支付模块API

## 购物车相关接口

### 获取购物车列表

- **URL**: `/api/v1/cart/`
- **方法**: `GET`
- **权限**: 需要认证
- **描述**: 获取用户购物车列表

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "item_type": "homestay",
        "item_id": 1,
        "sku_id": null,
        "quantity": 1,
        "check_in_date": "2023-05-01",
        "check_out_date": "2023-05-03",
        "item_info": {
          "id": 1,
          "name": "溪景大床房",
          "homestay_id": 1,
          "homestay_name": "溪山隐居",
          "cover_image": "https://example.com/room1_1.jpg",
          "price": 298,
          "max_guests": 2,
          "bed_info": "1.8米大床1张"
        },
        "subtotal": 596,
        "created_at": "2023-04-25T10:30:00Z"
      },
      {
        "id": 2,
        "item_type": "product",
        "item_id": 1,
        "sku_id": 1,
        "quantity": 2,
        "check_in_date": null,
        "check_out_date": null,
        "item_info": {
          "id": 1,
          "name": "太湖源山核桃",
          "cover_image": "https://example.com/product1.jpg",
          "sku_name": "小包装",
          "attributes": {
            "规格": "250g"
          },
          "price": 60
        },
        "subtotal": 120,
        "created_at": "2023-04-25T10:35:00Z"
      }
    ],
    "total_amount": 716,
    "total_items": 2
  }
}
```

### 添加商品到购物车

- **URL**: `/api/v1/cart/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 添加商品到购物车

**请求参数**:
```json
{
  "item_type": "homestay",
  "item_id": 1,
  "sku_id": null,
  "quantity": 1,
  "check_in_date": "2023-05-01",
  "check_out_date": "2023-05-03"
}
```

或者:

```json
{
  "item_type": "product",
  "item_id": 1,
  "sku_id": 1,
  "quantity": 2
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "添加成功",
  "data": {
    "id": 1,
    "item_type": "homestay",
    "item_id": 1,
    "sku_id": null,
    "quantity": 1,
    "check_in_date": "2023-05-01",
    "check_out_date": "2023-05-03",
    "created_at": "2023-04-25T10:30:00Z"
  }
}
```

### 更新购物车商品

- **URL**: `/api/v1/cart/{id}/`
- **方法**: `PATCH`
- **权限**: 需要认证
- **描述**: 更新购物车商品数量

**请求参数**:
```json
{
  "quantity": 3
}
```

或者:

```json
{
  "check_in_date": "2023-05-02",
  "check_out_date": "2023-05-04"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "id": 1,
    "item_type": "homestay",
    "item_id": 1,
    "sku_id": null,
    "quantity": 1,
    "check_in_date": "2023-05-02",
    "check_out_date": "2023-05-04",
    "updated_at": "2023-04-25T11:30:00Z"
  }
}
```

### 删除购物车商品

- **URL**: `/api/v1/cart/{id}/`
- **方法**: `DELETE`
- **权限**: 需要认证
- **描述**: 从购物车中删除商品

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "删除成功",
  "data": null
}
```

### 清空购物车

- **URL**: `/api/v1/cart/clear/`
- **方法**: `DELETE`
- **权限**: 需要认证
- **描述**: 清空购物车

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "清空成功",
  "data": null
}
```

## 订单相关接口

### 创建订单

- **URL**: `/api/v1/orders/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 创建订单

**请求参数**:
```json
{
  "cart_ids": [1, 2],
  "contact_name": "张三",
  "contact_phone": "13812345678",
  "remark": "请提前准备好房间"
}
```

或者直接创建订单:

```json
{
  "order_type": "homestay",
  "items": [
    {
      "item_type": "homestay",
      "item_id": 1,
      "quantity": 1,
      "check_in_date": "2023-05-01",
      "check_out_date": "2023-05-03"
    }
  ],
  "contact_name": "张三",
  "contact_phone": "13812345678",
  "remark": "请提前准备好房间"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "订单创建成功",
  "data": {
    "order_id": 1,
    "order_no": "2023042500001",
    "total_amount": 716,
    "payment_url": "/api/v1/payment/pay?order_no=2023042500001"
  }
}
```

### 获取订单列表

- **URL**: `/api/v1/orders/`
- **方法**: `GET`
- **权限**: 需要认证
- **描述**: 获取用户订单列表

**请求参数**:
- `order_type`: 订单类型，可选值：`homestay`, `product`
- `status`: 订单状态，可选值：`pending_payment`, `paid`, `confirmed`, `completed`, `cancelled`
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
        "order_no": "2023042500001",
        "order_type": "homestay",
        "merchant_id": 3,
        "merchant_name": "山水民宿",
        "total_amount": 716,
        "status": "pending_payment",
        "contact_name": "张三",
        "contact_phone": "13812345678",
        "created_at": "2023-04-25T10:40:00Z",
        "items_preview": [
          {
            "item_name": "溪景大床房",
            "item_cover": "https://example.com/room1_1.jpg",
            "check_in_date": "2023-05-01",
            "check_out_date": "2023-05-03"
          }
        ]
      },
      {
        "id": 2,
        "order_no": "2023042400001",
        "order_type": "product",
        "merchant_id": 4,
        "merchant_name": "青山农家",
        "total_amount": 120,
        "status": "paid",
        "contact_name": "张三",
        "contact_phone": "13812345678",
        "created_at": "2023-04-24T15:20:00Z",
        "items_preview": [
          {
            "item_name": "土蜂蜜",
            "item_cover": "https://example.com/product2.jpg",
            "quantity": 1
          }
        ]
      }
    ],
    "total": 2,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 获取订单详情

- **URL**: `/api/v1/orders/{id}/`
- **方法**: `GET`
- **权限**: 需要认证
- **描述**: 获取订单详情

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "order_no": "2023042500001",
    "order_type": "homestay",
    "user_id": 5,
    "merchant_id": 3,
    "merchant_name": "山水民宿",
    "total_amount": 716,
    "status": "pending_payment",
    "payment_method": null,
    "payment_time": null,
    "contact_name": "张三",
    "contact_phone": "13812345678",
    "remark": "请提前准备好房间",
    "created_at": "2023-04-25T10:40:00Z",
    "updated_at": "2023-04-25T10:40:00Z",
    "items": [
      {
        "id": 1,
        "item_type": "homestay",
        "item_id": 1,
        "item_name": "溪景大床房",
        "item_cover": "https://example.com/room1_1.jpg",
        "homestay_id": 1,
        "homestay_name": "溪山隐居",
        "price": 298,
        "quantity": 1,
        "check_in_date": "2023-05-01",
        "check_out_date": "2023-05-03",
        "nights": 2,
        "subtotal": 596
      },
      {
        "id": 2,
        "item_type": "product",
        "item_id": 1,
        "sku_id": 1,
        "item_name": "太湖源山核桃",
        "item_cover": "https://example.com/product1.jpg",
        "sku_name": "小包装",
        "price": 60,
        "quantity": 2,
        "subtotal": 120
      }
    ],
    "homestay_order": {
      "homestay_id": 1,
      "homestay_name": "溪山隐居",
      "room_type_id": 1,
      "room_type_name": "溪景大床房",
      "guest_count": 2,
      "check_in_date": "2023-05-01",
      "check_out_date": "2023-05-03",
      "nights": 2,
      "check_in_status": "not_checked_in",
      "guest_names": "张三，李四"
    },
    "product_order": null,
    "timeline": [
      {
        "time": "2023-04-25T10:40:00Z",
        "status": "created",
        "description": "订单创建成功"
      }
    ]
  }
}
```

### 取消订单

- **URL**: `/api/v1/orders/{id}/cancel/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 取消订单

**请求参数**:
```json
{
  "reason": "行程有变，无法如期入住"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "订单取消成功",
  "data": {
    "id": 1,
    "order_no": "2023042500001",
    "status": "cancelled",
    "updated_at": "2023-04-25T11:30:00Z"
  }
}
```

### 申请退款

- **URL**: `/api/v1/orders/{id}/refund/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 申请订单退款

**请求参数**:
```json
{
  "reason": "有急事，无法如期入住",
  "refund_type": "full" // full(全额退款)/partial(部分退款)
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "退款申请提交成功",
  "data": {
    "id": 1,
    "order_id": 1,
    "order_no": "2023042500001",
    "refund_no": "R2023042500001",
    "refund_amount": 716,
    "status": "pending",
    "created_at": "2023-04-25T11:35:00Z"
  }
}
```

## 支付相关接口

### 支付订单

- **URL**: `/api/v1/payment/pay/`
- **方法**: `POST`
- **权限**: 需要认证
- **描述**: 支付订单（模拟支付）

**请求参数**:
```json
{
  "order_no": "2023042500001",
  "payment_method": "wechat" // wechat(微信)/alipay(支付宝)/bank_card(银行卡)
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "支付成功",
  "data": {
    "order_id": 1,
    "order_no": "2023042500001",
    "payment_method": "wechat",
    "payment_time": "2023-04-25T11:40:00Z",
    "status": "paid"
  }
}
```

### 获取支付状态

- **URL**: `/api/v1/payment/status/`
- **方法**: `GET`
- **权限**: 需要认证
- **描述**: 获取订单支付状态

**请求参数**:
- `order_no`: 订单编号

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "order_no": "2023042500001",
    "status": "paid",
    "payment_method": "wechat",
    "payment_time": "2023-04-25T11:40:00Z"
  }
}
```

### 获取退款状态

- **URL**: `/api/v1/payment/refund/{refund_no}/`
- **方法**: `GET`
- **权限**: 需要认证
- **描述**: 获取退款状态

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "refund_no": "R2023042500001",
    "order_no": "2023042500001",
    "refund_amount": 716,
    "status": "processing",
    "reason": "有急事，无法如期入住",
    "created_at": "2023-04-25T11:35:00Z",
    "updated_at": "2023-04-25T11:50:00Z"
  }
}
```

## 商户订单管理接口

### 获取商户订单列表

- **URL**: `/api/v1/merchant/orders/`
- **方法**: `GET`
- **权限**: 需要认证，且用户类型为商户
- **描述**: 获取商户订单列表

**请求参数**:
- `order_type`: 订单类型，可选值：`homestay`, `product`
- `status`: 订单状态，可选值：`paid`, `confirmed`, `completed`, `cancelled`
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
        "order_no": "2023042500001",
        "order_type": "homestay",
        "user_id": 5,
        "username": "travel123",
        "total_amount": 716,
        "status": "paid",
        "contact_name": "张三",
        "contact_phone": "13812345678",
        "created_at": "2023-04-25T10:40:00Z",
        "items_preview": [
          {
            "item_name": "溪景大床房",
            "item_cover": "https://example.com/room1_1.jpg",
            "check_in_date": "2023-05-01",
            "check_out_date": "2023-05-03"
          }
        ]
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10,
    "pages": 1
  }
}
```

### 确认订单

- **URL**: `/api/v1/merchant/orders/{id}/confirm/`
- **方法**: `POST`
- **权限**: 需要认证，且用户类型为商户
- **描述**: 商户确认订单

**请求参数**:
```json
{
  "remark": "已确认预订，期待您的光临"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "订单确认成功",
  "data": {
    "id": 1,
    "order_no": "2023042500001",
    "status": "confirmed",
    "updated_at": "2023-04-25T14:30:00Z"
  }
}
```

### 确认入住

- **URL**: `/api/v1/merchant/orders/{id}/check-in/`
- **方法**: `POST`
- **权限**: 需要认证，且用户类型为商户
- **描述**: 确认订单入住状态

**请求参数**:
```json
{
  "guest_names": "张三，李四"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "确认入住成功",
  "data": {
    "id": 1,
    "order_id": 1,
    "check_in_status": "checked_in",
    "guest_names": "张三，李四",
    "check_in_time": "2023-05-01T14:00:00Z"
  }
}
```

### 确认离店

- **URL**: `/api/v1/merchant/orders/{id}/check-out/`
- **方法**: `POST`
- **权限**: 需要认证，且用户类型为商户
- **描述**: 确认订单离店状态

**请求参数**:
```json
{
  "remark": "客人已离店，房间状态良好"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "确认离店成功",
  "data": {
    "id": 1,
    "order_id": 1,
    "check_in_status": "checked_out",
    "check_out_time": "2023-05-03T12:00:00Z"
  }
}
```

### 处理退款申请

- **URL**: `/api/v1/merchant/refunds/{id}/process/`
- **方法**: `POST`
- **权限**: 需要认证，且用户类型为商户
- **描述**: 处理退款申请

**请求参数**:
```json
{
  "action": "approve", // approve(同意)/reject(拒绝)
  "remark": "同意退款",
  "refund_amount": 716 // 退款金额，仅在部分退款时使用
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "退款申请处理成功",
  "data": {
    "id": 1,
    "refund_no": "R2023042500001",
    "status": "approved",
    "refund_amount": 716,
    "remark": "同意退款",
    "updated_at": "2023-04-25T15:30:00Z"
  }
}
``` 