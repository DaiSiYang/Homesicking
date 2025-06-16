from rest_framework.response import Response
from rest_framework import status

class ApiResponse(Response):
    def __init__(self, data=None, code=200, message="操作成功", status_code=None, **kwargs):
        response_data = {
            "code": code,
            "message": message,
        }
        
        # 添加数据字段
        if data is not None:
            response_data["data"] = data
        else:
            response_data["data"] = None
            
        # 添加其他扩展参数
        response_data.update(kwargs)
        
        # 如果没有指定HTTP状态码，根据业务状态码自动设置
        if status_code is None:
            if 200 <= code < 300:
                status_code = status.HTTP_200_OK
            elif 400 <= code < 500:
                status_code = status.HTTP_400_BAD_REQUEST
            elif 500 <= code < 600:
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                status_code = status.HTTP_200_OK
        
        # 调用父类初始化
        super().__init__(data=response_data, status=status_code)

    @classmethod
    def success(cls, data=None, message="操作成功", code=200, **kwargs):
        """成功响应"""
        return cls(data=data, message=message, code=code, **kwargs)
    
    @classmethod
    def created(cls, data=None, message="创建成功", code=201, **kwargs):
        """创建成功响应"""
        return cls(data=data, message=message, code=code, status_code=status.HTTP_201_CREATED, **kwargs)
    
    @classmethod
    def error(cls, message="操作失败", code=400, data=None, **kwargs):
        """错误响应"""
        return cls(data=data, message=message, code=code, **kwargs)
    
    @classmethod
    def not_found(cls, message="资源不存在", code=404, **kwargs):
        """404响应"""
        return cls(data=None, message=message, code=code, status_code=status.HTTP_404_NOT_FOUND, **kwargs)
    
    @classmethod
    def unauthorized(cls, message="未授权访问", code=401, **kwargs):
        """401响应"""
        return cls(data=None, message=message, code=code, status_code=status.HTTP_401_UNAUTHORIZED, **kwargs)
    
    @classmethod
    def forbidden(cls, message="禁止访问", code=403, **kwargs):
        """403响应"""
        return cls(data=None, message=message, code=code, status_code=status.HTTP_403_FORBIDDEN, **kwargs)
    
    @classmethod
    def server_error(cls, message="服务器内部错误", code=500, **kwargs):
        """500响应"""
        return cls(data=None, message=message, code=code, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, **kwargs)