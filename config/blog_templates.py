from datetime import datetime
import random

class BlogTemplates:
    def __init__(self):
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        
    def get_title_template(self, keyword):
        """제목 템플릿 생성"""
        title_formats = [
            f"{keyword} 최신 트렌드 분석 {self.current_year}",
            f"{keyword}의 모든 것 - {self.current_year}년 완벽 가이드",
            f"지금 주목받는 {keyword}, 왜 중요할까?",
            f"{keyword} 동향 분석과 전망 {self.current_year}",
            f"{keyword}이 바꿀 미래 - 전문가 분석",
            f"{self.current_year}년 {keyword} 핵심 정리",
            f"{keyword} 완전 정복 - 초보자도 이해하는 가이드",
            f"IT 전문가가 말하는 {keyword}의 진실",
        ]
        return random.choice(title_formats)
    
    def get_intro_template(self, keyword):
        """도입부 템플릿"""
        intro_templates = [
            f"최근 IT 업계에서 가장 뜨거운 화제는 단연 {keyword}입니다. {self.current_year}년 들어 더욱 주목받고 있는 {keyword}에 대해 자세히 알아보겠습니다.",
            
            f"{keyword}가 우리 일상과 비즈니스 환경을 어떻게 변화시키고 있는지 궁금하지 않으신가요? 오늘은 {keyword}의 핵심 개념부터 최신 동향까지 모든 것을 정리해드리겠습니다.",
            
            f"디지털 전환 시대, {keyword}는 더 이상 선택이 아닌 필수가 되었습니다. {self.current_year}년 현재 {keyword} 시장의 주요 변화와 전망을 살펴보겠습니다.",
            
            f"IT 산업의 패러다임을 바꾸고 있는 {keyword}, 과연 무엇이 특별할까요? 전문가의 시각에서 {keyword}의 현재와 미래를 분석해보겠습니다.",
        ]
        return random.choice(intro_templates)
    
    def get_main_content_template(self, keyword):
        """본문 구조 템플릿"""
        template = f"""
<h2>{keyword}란 무엇인가?</h2>
<p>{keyword}는 {{basic_definition}}로 정의할 수 있습니다. 최근 몇 년간 급속한 발전을 보이며 다양한 분야에서 활용되고 있습니다.</p>

<h3>주요 특징 및 장점</h3>
<ul>
<li><strong>혁신성</strong>: {keyword}는 기존 방식과는 완전히 다른 접근법을 제시합니다</li>
<li><strong>효율성</strong>: 업무 프로세스를 대폭 개선하여 생산성을 높입니다</li>
<li><strong>확장성</strong>: 다양한 규모의 비즈니스에 적용 가능합니다</li>
<li><strong>미래지향성</strong>: {self.current_year}년 이후 더욱 중요해질 핵심 기술입니다</li>
</ul>

<h3>{self.current_year}년 {keyword} 시장 동향</h3>
<p>올해 {keyword} 시장은 전년 대비 상당한 성장을 보이고 있습니다. 주요 기업들의 투자가 늘어나면서 관련 기술 발전도 가속화되고 있습니다.</p>

<p>특히 국내 시장에서는 {{market_trend}} 등의 변화가 두드러지게 나타나고 있으며, 이는 {keyword}의 대중화를 더욱 앞당기고 있습니다.</p>

<h3>{keyword} 활용 분야</h3>
<p>{keyword}는 현재 다음과 같은 분야에서 활발히 활용되고 있습니다:</p>
<ul>
<li>기업 업무 자동화</li>
<li>고객 서비스 개선</li>
<li>데이터 분석 및 인사이트 도출</li>
<li>새로운 비즈니스 모델 창출</li>
</ul>

<h3>전문가 전망 및 미래 전망</h3>
<p>업계 전문가들은 {keyword}가 향후 3-5년 내에 {{expert_prediction}}할 것으로 예측하고 있습니다. 이는 우리의 생활과 업무 방식에 근본적인 변화를 가져올 것으로 보입니다.</p>

<p>특히 {self.current_year + 1}년에는 {{future_prediction}} 등의 발전이 기대되며, 이에 따른 새로운 기회들이 창출될 것으로 전망됩니다.</p>
"""
        return template
    
    def get_conclusion_template(self, keyword):
        """결론부 템플릿"""
        conclusion_templates = [
            f"{keyword}는 단순한 기술 트렌드를 넘어 우리 사회 전반에 영향을 미치는 핵심 동력이 되고 있습니다. {self.current_year}년 현재의 변화 속도를 고려할 때, 이에 대한 이해와 준비는 선택이 아닌 필수라고 할 수 있겠습니다.",
            
            f"결론적으로 {keyword}는 미래 경쟁력의 핵심 요소입니다. 지금부터라도 관련 동향을 주시하고 준비한다면, 다가올 변화에 성공적으로 대응할 수 있을 것입니다.",
            
            f"이처럼 {keyword}는 우리 일상과 비즈니스 환경을 빠르게 변화시키고 있습니다. 지속적인 관심과 학습을 통해 이 기회를 놓치지 않기를 바랍니다.",
        ]
        return random.choice(conclusion_templates)
    
    def get_seo_meta_template(self, keyword):
        """SEO 메타 태그 템플릿"""
        return {
            'meta_description': f"{keyword} {self.current_year}년 최신 트렌드 분석과 전망. {keyword}의 핵심 특징, 활용 사례, 미래 전망까지 전문가가 정리한 완벽 가이드를 확인해보세요.",
            'meta_keywords': f"{keyword}, IT트렌드, {self.current_year}, 기술분석, 디지털트랜스포메이션, 최신기술",
            'og_title': f"{keyword} 완벽 분석 - {self.current_year}년 최신 트렌드",
            'og_description': f"{keyword}에 대한 모든 것을 담은 전문가 분석 리포트. 지금 확인해보세요!"
        }
    
    def get_category_mapping(self, keyword):
        """키워드별 카테고리 매핑"""
        category_map = {
            # AI 관련
            'AI': 'AI/머신러닝',
            '인공지능': 'AI/머신러닝', 
            'ChatGPT': 'AI/머신러닝',
            '머신러닝': 'AI/머신러닝',
            '딥러닝': 'AI/머신러닝',
            
            # 블록체인 관련
            '블록체인': '블록체인/암호화폐',
            '암호화폐': '블록체인/암호화폐',
            'NFT': '블록체인/암호화폐',
            '비트코인': '블록체인/암호화폐',
            'DeFi': '블록체인/암호화폐',
            
            # 메타버스/VR/AR
            '메타버스': '메타버스/VR',
            'VR': '메타버스/VR',
            'AR': '메타버스/VR',
            '가상현실': '메타버스/VR',
            '증강현실': '메타버스/VR',
            
            # 클라우드/개발
            '클라우드': '클라우드/개발',
            'AWS': '클라우드/개발',
            '도커': '클라우드/개발',
            '쿠버네티스': '클라우드/개발',
            '개발': '클라우드/개발',
            
            # 보안
            '사이버보안': 'IT보안',
            '보안': 'IT보안',
            '해킹': 'IT보안',
            
            # 기본 카테고리
            'default': 'IT 트렌드'
        }
        
        keyword_lower = keyword.lower()
        for key, category in category_map.items():
            if key.lower() in keyword_lower:
                return category
        
        return category_map['default']
    
    def get_related_tags(self, keyword):
        """관련 태그 생성"""
        base_tags = [keyword, 'IT트렌드', str(self.current_year), '기술분석']
        
        # 키워드별 관련 태그
        tag_mapping = {
            'AI': ['머신러닝', '딥러닝', 'ChatGPT', '자동화'],
            '인공지능': ['AI', '머신러닝', '딥러닝', '자동화'],
            '블록체인': ['암호화폐', '웹3.0', 'NFT', 'DeFi'],
            '메타버스': ['VR', 'AR', '가상현실', '디지털트윈'],
            '클라우드': ['AWS', '서버리스', '마이크로서비스', 'DevOps'],
            'IoT': ['사물인터넷', '스마트홈', '센서', '연결성'],
            '빅데이터': ['데이터분석', '데이터사이언스', '애널리틱스', 'BI'],
            '사이버보안': ['정보보안', '해킹', '보안솔루션', '암호화']
        }
        
        # 키워드와 매칭되는 태그 추가
        for key, tags in tag_mapping.items():
            if key.lower() in keyword.lower():
                base_tags.extend(tags[:3])  # 최대 3개 추가
                break
        
        # 일반적인 IT 태그 추가
        general_tags = ['디지털전환', '혁신기술', '미래기술', '스타트업', '테크트렌드']
        base_tags.extend(random.sample(general_tags, 2))
        
        # 중복 제거 후 최대 8개 반환
        unique_tags = list(dict.fromkeys(base_tags))[:8]
        return unique_tags
    
    def get_content_structure_template(self, keyword, content_type='standard'):
        """콘텐츠 구조 템플릿"""
        if content_type == 'guide':
            return self._get_guide_template(keyword)
        elif content_type == 'news':
            return self._get_news_template(keyword)
        elif content_type == 'comparison':
            return self._get_comparison_template(keyword)
        else:
            return self._get_standard_template(keyword)
    
    def _get_standard_template(self, keyword):
        """표준 분석 템플릿"""
        return {
            'sections': [
                {'type': 'intro', 'title': f'{keyword} 개요'},
                {'type': 'features', 'title': '주요 특징'},
                {'type': 'trends', 'title': f'{self.current_year}년 동향'},
                {'type': 'applications', 'title': '활용 분야'},
                {'type': 'future', 'title': '미래 전망'},
                {'type': 'conclusion', 'title': '결론'}
            ]
        }
    
    def _get_guide_template(self, keyword):
        """가이드 형식 템플릿"""
        return {
            'sections': [
                {'type': 'intro', 'title': f'{keyword} 시작하기'},
                {'type': 'basics', 'title': '기본 개념 이해'},
                {'type': 'step_by_step', 'title': '단계별 접근법'},
                {'type': 'best_practices', 'title': '모범 사례'},
                {'type': 'common_mistakes', 'title': '주의사항'},
                {'type': 'resources', 'title': '참고 자료'}
            ]
        }
    
    def _get_news_template(self, keyword):
        """뉴스 분석 템플릿"""
        return {
            'sections': [
                {'type': 'breaking', 'title': f'{keyword} 최신 소식'},
                {'type': 'analysis', 'title': '시장 분석'},
                {'type': 'impact', 'title': '산업 파급효과'},
                {'type': 'expert_opinion', 'title': '전문가 의견'},
                {'type': 'outlook', 'title': '향후 전망'}
            ]
        }
    
    def _get_comparison_template(self, keyword):
        """비교 분석 템플릿"""
        return {
            'sections': [
                {'type': 'intro', 'title': f'{keyword} 비교 분석'},
                {'type': 'comparison_table', 'title': '주요 특성 비교'},
                {'type': 'pros_cons', 'title': '장단점 분석'},
                {'type': 'use_cases', 'title': '적용 사례'},
                {'type': 'recommendation', 'title': '선택 가이드'}
            ]
        }
    
    def get_html_wrapper_template(self):
        """HTML 래퍼 템플릿"""
        return """
<div class="blog-post-content">
    <div class="post-intro">
        {intro_content}
    </div>
    
    <div class="post-main">
        {main_content}
    </div>
    
    <div class="post-conclusion">
        {conclusion_content}
    </div>
    
    <div class="post-tags">
        <p><strong>관련 태그:</strong> {tags}</p>
    </div>
</div>

<style>
.blog-post-content {
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.6;
}

.blog-post-content h2 {
    color: #2c5aa0;
    border-bottom: 2px solid #e9ecef;
    padding-bottom: 10px;
    margin-top: 30px;
}

.blog-post-content h3 {
    color: #495057;
    margin-top: 25px;
}

.blog-post-content ul, .blog-post-content ol {
    margin: 15px 0;
    padding-left: 20px;
}

.blog-post-content li {
    margin: 8px 0;
}

.blog-post-content p {
    margin: 15px 0;
    text-align: justify;
}

.post-tags {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 5px;
    margin-top: 30px;
    border-left: 3px solid #2c5aa0;
}
</style>
"""
    
    def get_keyword_variations(self, keyword):
        """키워드 변형 생성 (SEO 최적화)"""
        variations = [keyword]
        
        # 영어-한글 변환
        eng_to_kor = {
            'AI': '인공지능',
            'IoT': '사물인터넷',
            'VR': '가상현실',
            'AR': '증강현실',
            'Big Data': '빅데이터',
            'Cloud': '클라우드',
            'Blockchain': '블록체인'
        }
        
        kor_to_eng = {v: k for k, v in eng_to_kor.items()}
        
        if keyword in eng_to_kor:
            variations.append(eng_to_kor[keyword])
        elif keyword in kor_to_eng:
            variations.append(kor_to_eng[keyword])
        
        # 관련 키워드 추가
        if 'AI' in keyword or '인공지능' in keyword:
            variations.extend(['머신러닝', '딥러닝', 'ChatGPT'])
        elif '블록체인' in keyword:
            variations.extend(['암호화폐', 'NFT', '웹3.0'])
        elif '메타버스' in keyword:
            variations.extend(['VR', 'AR', '가상현실'])
        
        return list(set(variations))[:5]  # 최대 5개 반환
    
    def format_publish_time(self):
        """발행 시간 포맷"""
        now = datetime.now()
        return {
            'formatted_date': now.strftime('%Y년 %m월 %d일'),
            'formatted_time': now.strftime('%H:%M'),
            'iso_date': now.isoformat(),
            'timestamp': int(now.timestamp())
        }
    
    def get_social_sharing_template(self, title, keyword):
        """소셜 미디어 공유 템플릿"""
        return {
            'twitter': f"📈 {title}\n\n#{keyword} #{self.current_year}IT트렌드 #기술분석\n\n자세한 내용 👉",
            'facebook': f"🔥 최신 IT 트렌드 분석!\n\n{title}\n\n{keyword}에 대한 전문가 분석과 미래 전망을 확인해보세요!",
            'linkedin': f"IT 업계 전문가들이 주목하는 {keyword}에 대한 심층 분석입니다.\n\n{title}\n\n#ITTrends #{keyword} #TechAnalysis"
        }
