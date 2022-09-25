from typing import List

import numpy as np
from geopy.distance import geodesic
from datetime import timedelta

from src.microservice.core.adapters.here_adapter import HereAdapter
from src.microservice.core.adapters.load_data import LoadData
from src.microservice.core.data_model import OrderDetails


class RoutePlanner:
    def __init__(self, loaded_data: LoadData, geo_adapter: HereAdapter):
        self.data = loaded_data
        self.geo_adapter = geo_adapter
        self.distance_matrix = np.zeros((len(self.data.restaurants), len(self.data.customers)))
        self.finished_orders = set()
        self.generated_routes = []

    def calculate_distance_matrix(self):
        for i, restaurant in enumerate(self.data.restaurants.values()):
            for j, customer in enumerate(self.data.customers.values()):
                self.distance_matrix[i][j] = geodesic((restaurant.latitude, restaurant.longitude),
                                                      (customer.latitude, customer.longitude)).m

    def assign_drivers(self) -> List[OrderDetails]:
        self.calculate_distance_matrix()
        while not self.data.orders.empty():
            _, order = self.data.orders.get()
            if order.id not in self.finished_orders:
                self.finished_orders.add(order.id)
                _, driver = self.data.drivers.get()
                order_details = self.generate_driver_order_details(order, driver)
                driver.order_details = order_details
                self.data.drivers.put((driver.order_details.order_delivery_time, driver))
                self.generated_routes.append(order_details)
        return self.generated_routes

    def generate_driver_order_details(self, order, driver) -> OrderDetails:
        prev_order_delivery_time = driver.order_details.order_delivery_time
        cur_customer = driver.order_details.customer_id
        dist_to_next_restaurant = self.distance_matrix[order.restaurant_id, cur_customer]
        dist_to_next_customer = self.distance_matrix[order.restaurant_id, order.customer_id]
        next_order_delivery_distance = dist_to_next_restaurant + dist_to_next_customer
        next_restaurant = self.data.restaurants.get(order.restaurant_id)
        next_customer = self.data.customers.get(order.customer_id)
        directions_to_customer = self.geo_adapter.get_navigation((next_restaurant.latitude, next_restaurant.longitude),
                                                                 (next_customer.latitude, next_customer.longitude))
        return OrderDetails(order_id=order.id,
                            order_pickup_time=prev_order_delivery_time +
                                              timedelta(minutes=dist_to_next_restaurant // 100),
                            order_delivery_time=prev_order_delivery_time +
                                                timedelta(minutes=next_order_delivery_distance // 100),
                            order_delivery_distance=next_order_delivery_distance,
                            rider_name=driver.name,
                            restaurant_id=order.restaurant_id,
                            customer_id=order.customer_id,
                            directions_to_customer=directions_to_customer,
                            )


if __name__ == '__main__':
    loaded_data = LoadData()
    here_adapter = HereAdapter()
    route_planning = RoutePlanner(loaded_data, here_adapter)
    route_planning.assign_drivers()
    print(route_planning.generated_routes[10])
