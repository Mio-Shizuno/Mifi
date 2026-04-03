import os
import sys
from dotenv import load_dotenv

# 添加父目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from main import create_app

app = create_app()

if __name__ == '__main__':
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )