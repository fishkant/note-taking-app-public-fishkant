from dotenv import load_dotenv
import os

# 加載環境變數
load_dotenv()

# Supabase 配置
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

# 如果環境變數未設置，使用默認值
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# SQLAlchemy 配置
SQLALCHEMY_DATABASE_URI = DATABASE_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False