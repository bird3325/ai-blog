import google.generativeai as genai
from config.settings import settings
from config.blog_templates import BlogTemplates
import logging
import re
import time
import random
from datetime import datetime, timedelta


class ContentGenerator:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.templates = BlogTemplates()
        
        # 할당량 관리를 위한 변수들
        self.last_request_time = None
        self.daily_request_count = 0
        self.last_reset_date = datetime.now().date()
        self.min_request_interval = 7
        self.max_daily_requests = 200

    def check_rate_limit(self):
        """API 할당량 확인 및 대기"""
        current_date = datetime.now().date()
        
        if current_date != self.last_reset_date:
            self.daily_request_count = 0
            self.last_reset_date = current_date
            logging.info("일일 API 할당량 리셋됨")
        
        if self.daily_request_count >= self.max_daily_requests:
            logging.error(f"일일 API 요청 한도 초과: {self.daily_request_count}/{self.max_daily_requests}")
            raise Exception("일일 API 요청 한도 초과")
        
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.min_request_interval:
                wait_time = self.min_request_interval - elapsed
                logging.info(f"API 속도 제한으로 {wait_time:.1f}초 대기...")
                time.sleep(wait_time)
        
        self.last_request_time = time.time()
        self.daily_request_count += 1
        
        logging.info(f"API 요청 #{self.daily_request_count}/{self.max_daily_requests}")

    def generate_blog_post(self, keyword):
        """키워드 기반 블로그 포스트 생성 (키워드 밀도 최적화)"""
        max_attempts = 1
        
        for attempt in range(max_attempts):
            try:
                logging.info(f"콘텐츠 생성 시도 {attempt + 1}/{max_attempts}: {keyword}")
                
                # API 할당량 확인
                try:
                    self.check_rate_limit()
                except Exception as e:
                    logging.error(f"API 할당량 문제: {e}")
                    return self.generate_fallback_content(keyword)
                
                prompt = self.create_optimized_prompt(keyword)
                
                # API 호출
                response = self.call_gemini_api_with_retry(prompt)
                
                if response and response.text:
                    # HTML 구조화
                    html_content = self.format_to_html(response.text, keyword)
                    
                    # 키워드 밀도 최적화 (핵심 수정 부분)
                    html_content = self.optimize_keyword_density(html_content, keyword)
                    
                    # 콘텐츠 후처리
                    html_content = self.enhance_content(html_content, keyword)
                    
                    if self.validate_content(html_content, keyword):
                        logging.info(f"콘텐츠 생성 성공: {keyword}")
                        return {
                            'title': self.generate_title(keyword),
                            'content': html_content,
                            'tags': self.generate_tags(keyword),
                            'category': 'IT 트렌드'
                        }
                    else:
                        logging.warning(f"품질 검사 실패 - 대체 콘텐츠 생성")
                        return self.generate_fallback_content(keyword)
                
            except Exception as e:
                if "429" in str(e) or "quota" in str(e).lower():
                    logging.error(f"API 할당량 초과 - 대체 콘텐츠 생성: {e}")
                    return self.generate_fallback_content(keyword)
                else:
                    logging.error(f"콘텐츠 생성 오류 ({keyword}, 시도 {attempt + 1}): {e}")
        
        logging.error(f"API 콘텐츠 생성 실패 - 대체 콘텐츠 사용: {keyword}")
        return self.generate_fallback_content(keyword)

    def optimize_keyword_density(self, content, keyword):
        """키워드 밀도 최적화 (2-4% 범위로 조정)"""
        text_only = re.sub(r'<[^>]+>', '', content)
        words = text_only.split()
        total_words = len(words)
        
        if total_words == 0:
            return content
        
        # 현재 키워드 출현 횟수 계산 (대소문자 구분 없이)
        keyword_lower = keyword.lower()
        current_count = text_only.lower().count(keyword_lower)
        
        # 목표 키워드 밀도: 2-3%
        target_density = 2.5  # 2.5%
        target_count = max(2, int(total_words * target_density / 100))
        
        logging.info(f"키워드 밀도 분석 - 현재: {current_count}회({current_count/total_words*100:.2f}%), 목표: {target_count}회({target_density}%)")
        
        if current_count > target_count:
            # 키워드가 너무 많은 경우 - 일부 키워드를 대체어로 변경
            content = self.reduce_keyword_density(content, keyword, current_count, target_count)
        elif current_count < target_count:
            # 키워드가 부족한 경우 - 자연스럽게 키워드 추가
            content = self.increase_keyword_density(content, keyword, current_count, target_count)
        
        # 최종 확인
        final_text = re.sub(r'<[^>]+>', '', content)
        final_count = final_text.lower().count(keyword_lower)
        final_density = (final_count / len(final_text.split())) * 100 if final_text.split() else 0
        
        logging.info(f"키워드 밀도 최적화 완료 - 최종: {final_count}회({final_density:.2f}%)")
        
        return content

    def reduce_keyword_density(self, content, keyword, current_count, target_count):
        """키워드 밀도 감소 - 일부 키워드를 대체어로 변경"""
        excess_count = current_count - target_count
        
        # 키워드 대체어 생성
        alternatives = self.generate_keyword_alternatives(keyword)
        
        # 키워드를 대체어로 랜덤하게 교체
        for i in range(min(excess_count, len(alternatives))):
            # 대소문자를 구분하지 않고 첫 번째로 찾은 키워드를 대체어로 교체
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            content = pattern.sub(alternatives[i], content, count=1)
        
        return content

    def increase_keyword_density(self, content, keyword, current_count, target_count):
        """키워드 밀도 증가 - 자연스럽게 키워드 추가"""
        needed_count = target_count - current_count
        
        # 키워드를 자연스럽게 포함할 수 있는 문구들
        natural_phrases = [
            f"{keyword}의 발전",
            f"{keyword} 기술",
            f"{keyword} 솔루션",
            f"{keyword} 플랫폼",
            f"{keyword} 서비스",
            f"{keyword} 도구",
            f"{keyword} 시스템",
            f"{keyword} 환경"
        ]
        
        # 마지막 문단에 자연스럽게 추가
        paragraphs = content.split('</p>')
        if len(paragraphs) > 1 and needed_count > 0:
            last_paragraph = paragraphs[-2]  # 마지막에서 두 번째 (</p> 분리 때문)
            
            for i in range(min(needed_count, len(natural_phrases))):
                addition = f" {natural_phrases[i]}에 대한 이해가 중요합니다."
                last_paragraph += addition
            
            paragraphs[-2] = last_paragraph
            content = '</p>'.join(paragraphs)
        
        return content

    def generate_keyword_alternatives(self, keyword):
        """키워드 대체어 생성"""
        # 일반적인 대체어
        general_alternatives = [
            "이 기술", "해당 솔루션", "이 도구", "관련 기술", "해당 플랫폼",
            "이 서비스", "관련 시스템", "해당 도구", "이 솔루션", "관련 서비스"
        ]
        
        # 키워드별 특화 대체어
        specific_alternatives = {}
        
        # AI/인공지능 관련
        if any(term in keyword.lower() for term in ['ai', '인공지능', '머신러닝', 'chatgpt']):
            specific_alternatives = ["AI 기술", "인공지능 시스템", "머신러닝 모델", "AI 솔루션", "지능형 시스템"]
        
        # 프로그래밍/개발 관련
        elif any(term in keyword.lower() for term in ['프로그래밍', '개발', '코딩', 'javascript', 'python']):
            specific_alternatives = ["개발 기술", "프로그래밍 언어", "코딩 도구", "개발 환경", "프로그래밍 프레임워크"]
        
        # 클라우드 관련
        elif any(term in keyword.lower() for term in ['클라우드', 'aws', 'azure', 'gcp']):
            specific_alternatives = ["클라우드 서비스", "클라우드 플랫폼", "클라우드 인프라", "클라우드 솔루션", "클라우드 환경"]
        
        # 블록체인 관련
        elif any(term in keyword.lower() for term in ['블록체인', '암호화폐', 'nft', '비트코인']):
            specific_alternatives = ["블록체인 기술", "분산원장 기술", "암호화 기술", "디지털 자산", "탈중앙화 시스템"]
        
        # 특화 대체어가 있으면 우선 사용, 없으면 일반 대체어 사용
        alternatives = specific_alternatives if specific_alternatives else general_alternatives
        
        return alternatives[:5]  # 최대 5개만 사용

    def call_gemini_api_with_retry(self, prompt, max_retries=2):
        """재시도 로직이 있는 Gemini API 호출"""
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response
            except Exception as e:
                if "429" in str(e):
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 10
                        logging.warning(f"API 할당량 초과 - {wait_time}초 후 재시도...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise e
                else:
                    raise e
        return None

    def generate_fallback_content(self, keyword):
        """API 할당량 초과 시 대체 콘텐츠 생성"""
        logging.info(f"대체 콘텐츠 생성 시작: {keyword}")
        
        template_content = self.create_template_content(keyword)
        
        # 대체 콘텐츠도 키워드 밀도 최적화
        template_content = self.optimize_keyword_density(template_content, keyword)
        
        return {
            'title': self.generate_title(keyword),
            'content': template_content,
            'tags': self.generate_tags(keyword),
            'category': 'IT 트렌드'
        }

    def create_template_content(self, keyword):
        """템플릿 기반 콘텐츠 생성 (키워드 밀도 고려)"""
        # 키워드를 적절히 분산하여 포함하는 템플릿
        template = f"""
<h2>{keyword} 기술 개요</h2>
<p>2025년 현재 IT 업계에서 가장 주목받고 있는 기술 중 하나가 바로 이 혁신적인 솔루션입니다. 현대적인 개발 환경에서 이러한 기술의 중요성은 날로 증가하고 있으며, 다양한 분야에서 혁신적인 변화를 가져오고 있습니다.</p>

<h3>주요 특징과 장점</h3>
<p>이 기술의 가장 큰 장점은 효율성과 확장성에 있습니다. 기존 방식과 비교했을 때 더 나은 성능과 사용자 경험을 제공합니다. 특히 현대적인 개발 프로세스에서 생산성 향상에 크게 기여하고 있습니다.</p>

<h3>시장 동향과 전망</h3>
<p>시장 분석에 따르면 관련 기술의 성장률은 지속적으로 상승세를 보이고 있습니다. 주요 기업들이 이러한 솔루션을 도입하면서 관련 생태계가 빠르게 확장되고 있으며, 향후 몇 년간 이러한 추세는 계속될 것으로 예상됩니다.</p>

<h3>실무 활용 방안</h3>
<p>실제 프로젝트에 적용할 때는 단계적 접근이 중요합니다. 먼저 기본적인 개념을 이해하고, 소규모 프로젝트에서 테스트한 후 점진적으로 확장하는 것이 좋습니다. 성공적인 도입을 위해서는 팀원들의 충분한 교육과 준비가 필요합니다.</p>

<h3>학습 리소스와 도구</h3>
<p>학습과 개발을 위한 다양한 도구들이 제공되고 있습니다. 온라인 문서, 튜토리얼, 커뮤니티 포럼 등을 통해 최신 정보를 얻을 수 있으며, 실습 환경도 쉽게 구축할 수 있습니다.</p>

<h3>결론 및 향후 전망</h3>
<p>이러한 기술 발전은 단순한 트렌드를 넘어서 IT 산업의 패러다임을 바꾸고 있는 중요한 요소입니다. 지속적인 학습과 실습을 통해 관련 기술을 마스터한다면, 경쟁력 있는 개발자로 성장할 수 있을 것입니다. 미래는 밝으며, 이에 대한 준비를 지금부터 시작하는 것이 중요합니다.</p>
"""
        
        # 키워드를 적절한 위치에 삽입 (2-3회만)
        template = template.replace("이 혁신적인 솔루션", keyword, 1)
        template = template.replace("이러한 기술", f"{keyword} 기술", 1)
        template = template.replace("관련 기술", keyword, 1)
        
        return template

    def create_optimized_prompt(self, keyword):
        """최적화된 프롬프트 생성 (키워드 밀도 가이드라인 포함)"""
        return f"""
{keyword}에 대한 한국어 블로그 포스트를 작성해주세요.

중요한 요구사항:
- 길이: 1000-1200자
- '{keyword}' 키워드를 정확히 4-5회만 사용 (과도한 반복 금지)
- 자연스럽고 읽기 쉬운 문체
- HTML 태그: h2, h3, p 사용
- 5개 섹션으로 구성

키워드 사용 가이드라인:
- '{keyword}'를 과도하게 반복하지 마세요
- 대신 "이 기술", "해당 솔루션", "관련 도구" 등의 대체 표현 사용
- 자연스러운 문맥에서만 키워드 포함

실용적이고 전문적인 내용으로 작성해주세요.
"""

    def format_to_html(self, content, keyword):
        """텍스트를 HTML 구조로 변환"""
        lines = content.strip().split('\n')
        html_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('#'):
                level = min(line.count('#'), 3)
                title = line.lstrip('#').strip()
                html_lines.append(f'<h{level}>{title}</h{level}>')
            elif len(line) > 10:
                html_lines.append(f'<p>{line}</p>')
        
        return '\n'.join(html_lines)

    def enhance_content(self, content, keyword):
        """콘텐츠 후처리"""
        text_only = re.sub(r'<[^>]+>', '', content)
        if len(text_only) < 800:
            # 키워드를 포함하지 않는 추가 문단
            additional = "\n<p>이러한 기술 발전은 IT 업계 전반에 긍정적인 영향을 미치고 있습니다. 더 나은 사용자 경험과 비즈니스 가치를 창출할 수 있는 새로운 기회를 제공하고 있습니다.</p>"
            content += additional
        
        return content

    def generate_title(self, keyword):
        """동적 제목 생성"""
        title_templates = [
            f"{keyword} 완벽 가이드 2025",
            f"{keyword} 최신 동향과 활용법", 
            f"2025년 {keyword} 트렌드 분석",
            f"{keyword} 실무 활용 전략",
            f"{keyword} 마스터하기"
        ]
        return random.choice(title_templates)

    def validate_content(self, content, keyword):
        """기본 품질 검증"""
        text_only = re.sub(r'<[^>]+>', '', content)
        return (
            len(text_only) >= 700 and
            keyword.lower() in text_only.lower() and
            ('<h2>' in content or '<h3>' in content) and
            '<p>' in content
        )

    def generate_tags(self, keyword):
        """관련 태그 생성"""
        base_tags = [keyword, 'IT트렌드', '기술동향', '2025']
        
        if 'AI' in keyword or '인공지능' in keyword:
            base_tags.extend(['머신러닝', '딥러닝'])
        elif '프로그래밍' in keyword or '개발' in keyword:
            base_tags.extend(['코딩', '소프트웨어'])
        elif '클라우드' in keyword:
            base_tags.extend(['AWS', 'Azure'])
        
        return base_tags[:6]
