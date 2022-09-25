# -*- coding: utf-8 -*-
"""Standard response object to use in the app's routes."""

#  standard imports
from enum import Enum


class ApiResponseStatus(Enum):
    SUCCESS = 200
    BAD_INPUT = 400
    UNAUTHORIZED = 401
    INTERNAL_ERROR = 500
    DUPLICATE = 501


class ApiResponse(object):
    def __init__(self,
                 status: ApiResponseStatus = None,
                 data: dict = None,
                 error_message: str = None,
                 current_page: int = None,
                 per_page: int = None,
                 total_count: int = None,
                 request_string: str = None):
        self.status = status
        self.data = data
        self.error_message = error_message
        self.current_page = current_page,
        self.per_page = per_page,
        self.total_count = total_count
        self.request_string = request_string

    def to_json(self):
        if self.status != ApiResponseStatus.SUCCESS:
            return {
                "status": self.status.value,
                "error": self.error_message
            }
        else:
            if (self.per_page[0] is None) or (self.current_page[0] is None):
                return {"data": self.data}
            else:
                return {
                "data": self.data,
                "meta": {
                    "page": self.current_page,
                    "per_page": self.per_page,
                    "page_count": self._count_page_number(),
                    "total_count": self.total_count,
                    "Links": [
                        {"self": f"{self.request_string}&page={self.current_page}&per_page={self.per_page}"},
                        {"first": f"{self.request_string}&page=0&per_page={self.per_page}"},
                        {"previous": self._get_previous_page()},
                        {"next": self._get_next_page()},
                        {"last": f"{self.request_string}&page={self._count_page_number() - 1}&per_page={self.per_page}"},
                    ]
                 }
                }

    def _count_page_number(self):
        return round(self.total_count // self.per_page) + 1 if (self.total_count % self.per_page != 0) else self.total_count // self.per_page

    def _get_previous_page(self):
        return f"{self.request_string}&page={self.current_page - 1}&per_page={self.per_page}" if self.current_page - 1 >= 0 else None

    def _get_next_page(self):
        return f"{self.request_string}&page={self.current_page + 1}&per_page={self.per_page}" if self.current_page + 1 < self._count_page_number() else None

