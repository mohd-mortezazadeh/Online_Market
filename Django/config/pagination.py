from collections import OrderedDict
from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next_link', self.get_next_link()),
            ('previous_link', self.get_previous_link()),
            ('count', self.page.paginator.count),
            ('page', self.page.number),
            ('num_page', self.page.paginator.num_pages),
            ('next' , self.page.next_page_number() if self.page.has_next() else None),
            ('previous' , self.page.previous_page_number() if self.page.has_previous() else None),
            ('last_page' , self.page.paginator.num_pages),
            ('results', data)
        ]))