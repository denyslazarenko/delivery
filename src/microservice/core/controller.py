import logging
import os

from src.microservice.core.adapters import LoadData, HereAdapter, RoutePlanner
from src.utils import ApiResponseStatus, ApiResponse, DataNotFoundException


class Controller(object):
    def __init__(self):
        self.loaded_data = LoadData(os.environ["DATA_PATH"])
        self.here_adapter = HereAdapter()
        self.route_planning = RoutePlanner(self.loaded_data, self.here_adapter)

    def get_routes(self):
        response = ApiResponse()
        resp = 0
        try:
            resp = self.route_planning.assign_drivers()
            total_count = len(resp)
            response.data = resp
            response.total_count = total_count
            response.status = ApiResponseStatus.SUCCESS
            response.request_string = f"/api/routes?"
        except DataNotFoundException as e:
            logging.info(e)
            response.status = ApiResponseStatus.INTERNAL_ERROR
            response.error_message = "Oops. There is no new data."
        if not resp:
            response.status = ApiResponseStatus.BAD_INPUT
            response.error_message = "Oops. Request failed."
        return response
