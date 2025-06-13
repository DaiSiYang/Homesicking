from rest_framework.pagination import PageNumberPagination
from .response import ApiResponse


class StandardResultsSetPagination(PageNumberPagination):
    """
    标准分页类
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return ApiResponse(data={
            'results': data,
            'count': self.page.paginator.count,
            'page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'pages': self.page.paginator.num_pages
        })