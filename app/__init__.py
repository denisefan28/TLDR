from flask import Flask
from .routes import main_bp

# import os
# os.environ["IMAGEMAGICK_BINARY"] = "/opt/homebrew/bin/convert"

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    return app