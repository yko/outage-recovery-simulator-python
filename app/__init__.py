from flask import Flask
import yaml
import logging

def create_app():
    app = Flask(__name__)

    # Load configuration from YAML file
    with open('config.yaml', 'r') as yamlfile:
        yamlconfig = yaml.safe_load(yamlfile)
        app.config.update(yamlconfig)

    # Import and register blueprints
    from .routes import main
    app.register_blueprint(main)

    # Setup logger
    handler = logging.FileHandler('app.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    return app
