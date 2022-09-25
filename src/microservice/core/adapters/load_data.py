import json
from datetime import datetime
from queue import PriorityQueue
from typing import Dict

from src.microservice.core.data_model import Restaurant, Customer, Order, Driver, OrderDetails


class LoadData:
    def __init__(self, data_path):
        # TODO here we should read data from Google Container
        self._data_path = data_path
        self._restaurants = dict()
        self._customers = dict()
        self._orders = None
        self._drivers = None

    @property
    def restaurants(self) -> Dict:
        if not self._restaurants:
            with open(self._data_path + '/lunch_rush_restaurants.json') as f:
                raw_restaurants = json.load(f)
            for raw_restaurant in raw_restaurants:
                restaurant = Restaurant.from_dict(raw_restaurant)
                self._restaurants[restaurant.id] = restaurant
            self._restaurants[0] = Restaurant(id=0,
                                              name="Delivery Hero HQ",
                                              latitude=52.5247553,
                                              longitude=13.3908602
                                              )
        return self._restaurants

    @property
    def customers(self) -> Dict:
        if not self._customers:
            with open(self._data_path + '/lunch_rush_customers.json') as f:
                raw_customers = json.load(f)
            for raw_customer in raw_customers:
                customer = Customer.from_dict(raw_customer)
                self._customers[customer.id] = customer
            self._customers[0] = Customer(id=0,
                                          name="Delivery Hero HQ",
                                          latitude=52.5247553,
                                          longitude=13.3908602
                                          )
        return self._customers

    @property
    def orders(self) -> PriorityQueue[(datetime, Order)]:
        # TODO it should read only once??
        if not self._orders:
            self._orders = PriorityQueue()
            with open(self._data_path + '/lunch_rush_orders.json') as f:
                raw_orders = json.load(f)
            for raw_order in raw_orders:
                order = Order.from_dict(raw_order)
                self._orders.put((order.ordered_at, order))
                # TODO last 3 orders should send drivers to HQ
        return self._orders

    @property
    def drivers(self) -> PriorityQueue[(int, Driver)]:
        if not self._drivers:
            self._drivers = PriorityQueue()
            with open(self._data_path + '/lunch_rush_riders.json') as f:
                raw_drivers = json.load(f)
            for raw_driver in raw_drivers:
                driver = Driver.from_dict(raw_driver)
                time_now = datetime.now()
                driver.order_details = OrderDetails(order_id="",
                                                    order_pickup_time=time_now,
                                                    order_delivery_time=time_now,
                                                    order_delivery_distance=0,
                                                    rider_name=driver.name,
                                                    restaurant_id=0,
                                                    customer_id=0,
                                                    directions_to_customer="",
                                                    )
                self._drivers.put((time_now, driver))
        return self._drivers
