import os
from app.api.V1 import create_app

app=create_app(os.getenv("CONFIG_STAGE") or "default")

if __name__ == '__main__':
    app.run(debug=True)
