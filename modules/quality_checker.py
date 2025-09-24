import sqlite3
from difflib import SequenceMatcher
from config.settings import settings
import re
import logging


class QualityChecker:
    def __init__(self):
        self.duplicate_threshold = 0.7

    def check_content_quality(self, content, keyword):
        """종합 품질 검사 (완화된 기준)"""
        checks = {
            'length_check': self.check_length(content),
            'keyword_density': self.check_keyword_density(content, keyword),
            'html_structure': self.check_html_structure(content),
            'duplicate_check': self.check_duplicate(content),
            'content_quality': self.check_content_coherence(content)
        }
        
        text_only = re.sub(r'<[^>]+>', '', content)
        keyword_count = text_only.lower().count(keyword.lower())
        total_words = len(text_only.split())
        density = (keyword_count / total_words * 100) if total_words > 0 else 0
        
        logging.info(f"품질 검사 상세 정보:")
        logging.info(f"- 글자 수: {len(text_only)} (기준: 500-2500)")  # 기준 완화
        logging.info(f"- 키워드 밀도: {density:.2f}% ({keyword_count}번 사용)")
        logging.info(f"- HTML 태그: <h2/h3>: {'있음' if ('<h2>' in content or '<h3>' in content) else '없음'}, <p>: {'있음' if '<p>' in content else '없음'}")
        
        passed = all(checks.values())
        
        if not passed:
            failed_checks = [k for k, v in checks.items() if not v]
            logging.warning(f"품질 검사 실패: {failed_checks}")
        else:
            logging.info("✅ 모든 품질 검사 통과")
        
        return passed, checks

    def check_length(self, content):
        """글자 수 검사 (대폭 완화)"""
        text_only = re.sub(r'<[^>]+>', '', content)
        length = len(text_only)
        
        # 기준을 대폭 완화: 500-2500자
        min_length = 500
        max_length = 2500
        
        result = min_length <= length <= max_length
        if not result:
            logging.warning(f"길이 검사 실패: {length}자 (기준: {min_length}-{max_length})")
        else:
            logging.info(f"✅ 길이 검사 통과: {length}자")
        
        return result

    def check_keyword_density(self, content, keyword):
        """키워드 밀도 검사 (완화)"""
        text_only = re.sub(r'<[^>]+>', '', content).lower()
        keyword_lower = keyword.lower()
        
        keyword_count = text_only.count(keyword_lower)
        
        # 키워드의 일부분도 카운트
        if ' ' in keyword_lower:
            main_keyword = keyword_lower.split()[0]
            keyword_count += text_only.count(main_keyword) // 3  # 부분 매치는 1/3만 카운트
        
        total_words = len(text_only.split())
        if total_words == 0:
            return False
        
        density = (keyword_count / total_words) * 100
        
        # 밀도 기준 완화 (0.5% ~ 6.0%)
        result = 0.5 <= density <= 6.0
        
        if not result:
            logging.warning(f"키워드 밀도 검사 실패: {density:.2f}% (기준: 0.5-6.0%)")
        else:
            logging.info(f"✅ 키워드 밀도 검사 통과: {density:.2f}%")
        
        return result

    def check_html_structure(self, content):
        """HTML 구조 검사 (완화)"""
        has_heading = '<h2>' in content or '<h3>' in content or '<h1>' in content
        has_structure = '<p>' in content or '<li>' in content or '<div>' in content
        
        result = has_heading and has_structure
        
        if not result:
            logging.warning(f"HTML 구조 검사 실패: 제목태그={has_heading}, 구조태그={has_structure}")
        else:
            logging.info("✅ HTML 구조 검사 통과")
        
        return result

    def check_duplicate(self, content):
        """중복 콘텐츠 검사"""
        try:
            conn = sqlite3.connect(settings.DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='published_posts'
            """)
            
            if cursor.fetchone():
                cursor.execute("SELECT content FROM published_posts LIMIT 20")  # 검사 범위 축소
                existing_posts = cursor.fetchall()
                
                text_only = re.sub(r'<[^>]+>', '', content)
                
                for (existing_content,) in existing_posts:
                    existing_text = re.sub(r'<[^>]+>', '', existing_content)
                    
                    if len(text_only) < 200 or len(existing_text) < 200:
                        continue
                    
                    similarity = SequenceMatcher(None, text_only, existing_text).ratio()
                    if similarity > self.duplicate_threshold:
                        conn.close()
                        logging.warning(f"중복 콘텐츠 감지: 유사도 {similarity:.2f}")
                        return False
            
            conn.close()
            logging.info("✅ 중복 검사 통과")
            return True
            
        except Exception as e:
            logging.error(f"중복 검사 오류: {e}")
            return True

    def check_content_coherence(self, content):
        """내용 일관성 검사 (완화)"""
        text_only = re.sub(r'<[^>]+>', '', content)
        
        sentences = [s.strip() for s in text_only.split('.') if s.strip() and len(s.strip()) > 10]
        
        if len(sentences) < 3:  # 최소 3문장으로 완화
            logging.warning(f"문장 수 부족: {len(sentences)}개")
            return False
        
        # 반복 문장 검사 완화
        unique_sentences = set(sentences)
        uniqueness_ratio = len(unique_sentences) / len(sentences)
        
        if uniqueness_ratio < 0.5:  # 50%로 완화
            logging.warning(f"문장 유사도 높음: {uniqueness_ratio:.2f}")
            return False
        
        # 최소 단어 수 검사 완화
        words = text_only.split()
        if len(words) < 80:  # 80단어로 완화
            logging.warning(f"단어 수 부족: {len(words)}개")
            return False
        
        logging.info("✅ 내용 일관성 검사 통과")
        return True
