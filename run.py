import os
from app import create_app
from app.config import  app_config

app=create_app(production)


if __name__ == '__main__':
    app.run(debug=True)
