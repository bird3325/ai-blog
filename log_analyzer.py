# 로그 분석 스크립트 (log_analyzer.py)
import sqlite3
from config.settings import settings
import pandas as pd

def analyze_performance():
    conn = sqlite3.connect(settings.DATABASE_PATH)
    
    # 발행 성공률 분석
    success_rate = pd.read_sql_query("""
        SELECT DATE(published_at) as date, COUNT(*) as posts
        FROM published_posts 
        GROUP BY DATE(published_at)
        ORDER BY date DESC
    """, conn)
    
    print("최근 발행 현황:")
    print(success_rate.head(7))
    
    conn.close()

if __name__ == "__main__":
    analyze_performance()
