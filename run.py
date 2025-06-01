from app import create_app
from app.logger import logger

app = create_app()

if __name__ == '__main__':
    logger.info("Starting application server")
    app.run(debug=False)
    logger.info("Application server stopped")
