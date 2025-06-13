from rest_framework.decorators import api_view
from apps.utils.permissions import merchant_api_permission
from apps.utils.response import ApiResponse
from apps.users.serializers import UserSerializer

@api_view(['GET', 'PUT'])
@merchant_api_permission
def get_user_info(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return ApiResponse.success(data=serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(data=serializer.data)
        return ApiResponse.error(message="数据验证失败")