from flask import Blueprint

from src.microservice.core.controller import Controller

module = Blueprint("routes", __name__)
controller = Controller()


@module.route('/routes', methods=['GET'])
def routes():
    response = controller.get_routes()
    return response.to_json()


if __name__ == "__main__":
    result = routes()