from apscheduler.schedulers.blocking import BlockingScheduler
from main import AutoBlogPublisher
import logging

def run_auto_publishing():
    """스케줄러에서 호출되는 함수"""
    publisher = AutoBlogPublisher()
    publisher.run_daily_publishing()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    
    # 매일 오전 9시에 실행
    scheduler.add_job(
        run_auto_publishing,
        'cron',
        hour=9,
        minute=0,
        id='daily_blog_publish'
    )
    
    logging.info("스케줄러 시작 - 매일 오전 9시 자동 발행")
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logging.info("스케줄러 종료")
        scheduler.shutdown()
