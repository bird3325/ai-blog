import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # 티스토리 설정
    TISTORY_EMAIL = os.getenv('TISTORY_EMAIL')
    TISTORY_PASSWORD = os.getenv('TISTORY_PASSWORD')
    TISTORY_BLOG_URL = os.getenv('TISTORY_BLOG_URL')
    
    # AI 설정
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # 이메일 알림 설정 (선택사항)
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL', '')
    
    # 글 생성 설정 (완화된 기준)
    POST_MIN_LENGTH = 500   # 500자로 완화
    POST_MAX_LENGTH = 2500  # 2500자로 확대
    KEYWORD_DENSITY = 2.0   # 2.0%로 완화
    DAILY_POST_LIMIT = 3    # 일일 3개로 제한
    
    # 스케줄링 설정
    PUBLISH_HOUR = 9
    PUBLISH_MINUTE = 0
    
    # 데이터베이스
    DATABASE_PATH = 'data/keywords.db'
    
    # 로그 설정
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'data/logs/auto_blog.log'

settings = Settings()
