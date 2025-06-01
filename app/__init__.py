from flask import Flask
import yaml
from .logger import logger

def create_app():
    app = Flask(__name__)
    
    # Load configuration from YAML file
    with open('config.yaml', 'r') as yamlfile:
        yamlconfig = yaml.safe_load(yamlfile)
        app.config.update(yamlconfig)
    
    # Import and register blueprints
    from .routes import main
    app.register_blueprint(main)
    
    # Log application startup
    logger.info("Application initialized successfully")
    
    return app
