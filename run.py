import os
from app import create_app
from app.config import app_config

config_name = app_config['production']
app=create_app(config_name)

if __name__ == '__main__':
    app.run(debug=True)
