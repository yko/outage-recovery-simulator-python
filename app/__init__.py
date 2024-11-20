from flask import Flask
import yaml
import logging

def create_app():
    app = Flask(__name__)

    # Load configuration from YAML file
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
        app.config.update(config)

    # Import and register blueprints
    from .routes import api as main_blueprint  # More descriptive name
    app.register_blueprint(main_blueprint)

    # Setup logger
    log_file_handler = logging.FileHandler('app.log')
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
    log_file_handler.setFormatter(log_formatter)
    app.logger.addHandler(log_file_handler)
    app.logger.setLevel(logging.INFO)

    return app
