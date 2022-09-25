import os
from flask import Flask, redirect, url_for
from src.microservice.api import module


App = Flask(__name__,
               instance_relative_config=True)

app_settings = os.getenv('APP_SETTINGS')
App.config.from_object(app_settings)


App.register_blueprint(module, url_prefix="/api")


if __name__ == "__main__":
    App.run(host="0.0.0.0", port="5000")
