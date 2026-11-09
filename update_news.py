import urllib.request
import xml.etree.ElementTree as ET
import re

# F1 공식 뉴스 RSS 피드 주소
RSS_URL = "https://www.formula1.com/content/fom-website/en/latest/all.xml"

def fetch_f1_news():
    req = urllib.request.Request(
        RSS_URL, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    
    html_items = ""
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            # 상위 5개 최신 뉴스만 가져오기
            for item in root.findall('.//item')[:5]:
                title = item.find('title').text if item.find('title') is not None else 'F1 Latest News'
                link = item.find('link').text if item.find('link') is not None else 'https://www.formula1.com'
                pub_date = item.find('pubDate').text[:16] if item.find('pubDate') is not None else ''
                description = item.find('description').text if item.find('description') is not None else ''
                
                # HTML 태그 제거 및 정돈
                clean_desc = re.sub('<[^<]+?>', '', description)[:150] + "..."

                html_items += f'''
      <article class="news-card">
        <div class="news-tag">LATEST NEWS</div>
        <h3 class="news-title">{title}</h3>
        <p class="news-summary">{clean_desc}</p>
        <div class="news-footer">
          <span>{pub_date}</span>
          <a href="{link}" target="_blank" class="news-source-link">원문 기사 보러가기 (Formula1.com) &rarr;</a>
        </div>
      </article>
'''
    except Exception as e:
        print(f"뉴스 수집 중 오류 발생: {e}")
        
    return html_items

def update_index_html():
    news_html = fetch_f1_news()
    if not news_html:
        return

    # 기존 index.html 읽기
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 뉴스 영역 자동 교체 ( news-feed 태그 사이 내용 업데이트 )
    start_marker = '<div class="news-feed">'
    end_marker = '</div>\n  </div>'
    
    if start_marker in content and end_marker in content:
        parts = content.split(start_marker)
        rest = parts[1].split(end_marker)
        new_content = parts[0] + start_marker + "\n" + news_html + "\n    " + end_marker + rest[1]
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("index.html 뉴스 업데이트 완료!")

if __name__ == "__main__":
    update_index_html()
