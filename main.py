import logging
from datetime import datetime
from modules.keyword_collector import KeywordCollector
from modules.content_generator import ContentGenerator
from modules.quality_checker import QualityChecker
from modules.blog_publisher import BlogPublisher
from config.settings import settings
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 로깅 설정
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class AutoBlogPublisher:
    def __init__(self):
        self.keyword_collector = KeywordCollector()
        self.content_generator = ContentGenerator()
        self.quality_checker = QualityChecker()
        self.blog_publisher = BlogPublisher()
    
    def run_daily_publishing(self):
        """일일 자동 발행 실행"""
        start_time = datetime.now()
        logging.info("=== 자동 블로그 발행 시작 ===")
        
        try:
            # 1단계: 키워드 수집
            logging.info("키워드 수집 시작")
            
            # 구글 트렌드에서 키워드 수집
            google_keywords = self.keyword_collector.collect_google_trends()
            logging.info(f"구글 트렌드 수집 키워드: {google_keywords}")
            
            # 네이버 트렌드에서 키워드 수집
            naver_keywords = self.keyword_collector.collect_naver_trends()
            logging.info(f"네이버 트렌드 수집 키워드: {naver_keywords}")
            
            # 모든 키워드 통합 및 중복 제거
            all_collected_keywords = list(set(google_keywords + naver_keywords))
            
            # 키워드가 없는 경우 대체 키워드 사용
            if not all_collected_keywords:
                logging.warning("트렌드 수집 실패 - 대체 키워드 사용")
                all_collected_keywords = self.keyword_collector.get_fallback_keywords()
            
            logging.info(f"🔍 수집된 전체 키워드 ({len(all_collected_keywords)}개): {all_collected_keywords}")
            
            # 키워드 데이터베이스에 저장 (백업용)
            self.keyword_collector.save_keywords(all_collected_keywords)
            
            # 2단계: 수집된 키워드에서 직접 발행할 키워드 선택
            # 데이터베이스에서 다시 불러오지 않고, 수집된 키워드를 바로 사용
            daily_keywords = all_collected_keywords[:settings.DAILY_POST_LIMIT]
            
            if not daily_keywords:
                logging.warning("발행할 키워드가 없습니다.")
                return
            
            logging.info(f"📝 오늘 발행할 키워드 ({len(daily_keywords)}개): {daily_keywords}")
            logging.info(f"*** 수집된 키워드를 직접 사용하여 발행합니다 ***")
            
            # 3단계: 각 키워드별 포스트 생성 및 발행
            success_count = 0
            failed_keywords = []
            
            for i, keyword in enumerate(daily_keywords, 1):
                try:
                    logging.info(f"📰 키워드 '{keyword}' 처리 시작 ({i}/{len(daily_keywords)})")
                    
                    # 콘텐츠 생성
                    post_data = self.content_generator.generate_blog_post(keyword)
                    if not post_data:
                        logging.warning(f"키워드 '{keyword}' 콘텐츠 생성 실패")
                        failed_keywords.append(keyword)
                        continue
                    
                    # 품질 검사
                    quality_passed, quality_checks = self.quality_checker.check_content_quality(
                        post_data['content'], keyword
                    )
                    
                    if not quality_passed:
                        logging.warning(f"키워드 '{keyword}' 품질 검사 실패: {quality_checks}")
                        failed_keywords.append(keyword)
                        continue
                    
                    # 블로그 발행
                    if self.blog_publisher.publish_post(post_data):
                        # 데이터베이스에서 해당 키워드를 사용됨으로 표시
                        self.keyword_collector.mark_keyword_used(keyword)
                        success_count += 1
                        logging.info(f"✅ 키워드 '{keyword}' 발행 성공!")
                    else:
                        logging.error(f"키워드 '{keyword}' 발행 실패")
                        failed_keywords.append(keyword)
                    
                    # 발행 간격 조정 (티스토리 부하 방지)
                    if i < len(daily_keywords):  # 마지막이 아닌 경우만 대기
                        logging.info("다음 발행까지 30초 대기...")
                        time.sleep(30)
                    
                except Exception as e:
                    logging.error(f"키워드 '{keyword}' 처리 오류: {e}")
                    failed_keywords.append(keyword)
                    continue
            
            # 실행 결과 리포트
            end_time = datetime.now()
            duration = end_time - start_time
            
            # 상세 리포트 생성
            report = f"""
=== 자동 블로그 발행 완료 리포트 ===
📅 실행 시간: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
⏰ 소요 시간: {str(duration).split('.')[0]}
🔍 수집된 키워드: {len(all_collected_keywords)}개 - {all_collected_keywords}
📝 발행 처리한 키워드: {len(daily_keywords)}개 - {daily_keywords}
✅ 성공 발행: {success_count}개
❌ 실패: {len(failed_keywords)}개{' - ' + str(failed_keywords) if failed_keywords else ''}

발행 성공률: {(success_count / len(daily_keywords) * 100):.1f}%
*** 데이터베이스 선별 과정을 건너뛰고 수집된 키워드를 직접 사용했습니다 ***
"""
            
            logging.info(report)
            self.send_notification(report, success_count > 0)
            
        except Exception as e:
            error_msg = f"자동 발행 시스템 오류: {e}"
            logging.error(error_msg)
            self.send_notification(error_msg, False)
    
    def send_notification(self, message, is_success):
        """이메일 알림 발송"""
        try:
            # 이메일 설정이 있는 경우만 발송
            if not hasattr(settings, 'SMTP_USERNAME') or not settings.SMTP_USERNAME:
                logging.info("이메일 설정이 없어 알림을 건너뜁니다.")
                return
                
            msg = MIMEMultipart()
            msg['From'] = settings.SMTP_USERNAME
            msg['To'] = settings.NOTIFICATION_EMAIL
            msg['Subject'] = f"블로그 자동발행 {'성공' if is_success else '오류'} 알림"
            
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            logging.info("알림 이메일 발송 완료")
            
        except Exception as e:
            logging.error(f"알림 발송 실패: {e}")

if __name__ == "__main__":
    publisher = AutoBlogPublisher()
    publisher.run_daily_publishing()
