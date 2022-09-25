from datetime import datetime
from dataclasses import dataclass


@dataclass
class LocationIdentifier:
    id: int
    name: str
    latitude: float
    longitude: float


@dataclass
class Restaurant(LocationIdentifier):
    @classmethod
    def from_dict(cls, attrs):
        return cls(
            id=int(attrs["restaurant_id"]),
            name=attrs["restaurant_name"],
            latitude=float(attrs["restaurant_lat"]),
            longitude=float(attrs["restaurant_lng"]),
        )


@dataclass
class Customer(LocationIdentifier):
    @classmethod
    def from_dict(cls, attrs):
        return cls(
            id=int(attrs["customer_id"]),
            name=attrs["customer_name"],
            latitude=float(attrs["customer_lat"]),
            longitude=float(attrs["customer_lng"]),
        )


@dataclass
class Order:
    id: str
    ordered_at: datetime
    restaurant_id: int
    customer_id: int

    @classmethod
    def from_dict(cls, attrs):
        return cls(
            id=attrs["order_id"],
            ordered_at=datetime.strptime(attrs["ordered_at"], "%Y-%m-%dT%H:%M:%S"),
            restaurant_id=int(attrs["restaurant_id"]),
            customer_id=int(attrs["customer_id"]),
        )

@dataclass
class OrderDetails:
    order_id: str
    order_pickup_time: datetime
    order_delivery_time: datetime
    order_delivery_distance: int
    rider_name: str
    restaurant_id: int
    customer_id: int
    directions_to_customer: str


@dataclass
class Driver:
    id: str
    name: str
    order_details: OrderDetails = None

    @classmethod
    def from_dict(cls, attrs):
        return cls(
            id=attrs["rider_id"],
            name=attrs["name"]
        )


