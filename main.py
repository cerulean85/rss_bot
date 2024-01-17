#import feedparser
import datetime
from PyKakao import Message


api = Message(service_key="30d6cd4b6693baaf973782ee211dd9da")

# 1. access_token Redirect
#auth_url = api.get_url_for_generating_code()
#print(auth_url)

# 2. access_token Extract
#access_token = api.get_access_token_by_redirected_url(auth_url)
#access_token = "LSKmidtsmuLOwdi4O1haFtvwRl-L8yPASyHmPwYEPo5CZvN_kvRsgMWGElAKPXWaAAABjRcrathUdd9ffL_GXA"
#print(access_token)

#. Extracted access_token을 변수에 넣기
access_token="B82qrU3fwEKxvQ9gQ0mehu2h9UfHvy62BsIKPXKYAAABjRcsbT7DukuslKNZWg"
api.set_access_token(access_token)
#exit()
# auth_url = api.get_url_for_generating_code()
# print(auth_url)
# exit()
# url = "https://localhost:5000/?code=6h1XnCfNnTIn_TQ2WKLUhMI8Qfnlf1ImkrZDfDpPFhpEyRCeI7yeZKWwLKIKPXLrAAABjHXEjNqYFzyUYZmfhQ"
# access_token = api.get_access_token_by_redirected_url(url)
# url = "https://fs.jtbc.co.kr/RSS/entertainment.xml" # jtbc 연예

today = datetime.datetime.now()


# 이름	RSS 주소
# https://taking.kr/korea-it-technology-blog-list-with-rss/
# 무신사(MUSINSA) 기술블로그	https://medium.com/feed/musinsa-tech
# 네이버 D2 기술블로그	https://d2.naver.com/d2.atom
# 마켓컬리 기술블로그	https://helloworld.kurly.com/feed.xml
# 우아한형제들 기술블로그	https://techblog.woowahan.com/feed
# 카카오엔터프라이즈 기술블로그	https://tech.kakaoenterprise.com/feed
# 데브시스터즈 기술블로그	https://tech.devsisters.com/rss.xml
# 라인(LINE) 기술블로그	https://engineering.linecorp.com/ko/feed/index.html
# 쿠팡(Coupang) 기술블로그	https://medium.com/feed/coupang-engineering
# 당근마켓 기술블로그	https://medium.com/feed/daangn
# 토스(Toss) 기술블로그	https://toss.tech/rss.xml
# 직방 기술블로그	https://medium.com/feed/zigbang
# 왓챠(Watcha) 기술블로그	https://medium.com/feed/watcha
# 뱅크샐러드(banksalad) 기술블로그	https://blog.banksalad.com/rss.xml
# Hyperconnect 기술블로그	https://hyperconnect.github.io/feed.xml
# 요기요(yogiyo) 기술블로그	https://techblog.yogiyo.co.kr/feed
# 쏘카(Socar) 기술블로그	https://tech.socarcorp.kr/feed
# 리디(RIDI) 기술블로그	https://www.ridicorp.com/feed
# NHN Toast 기술블로그	https://meetup.toast.com/rss
# GeekNews - 개발/기술/스타트업 뉴스 서비스	https://news.hada.io/rss/news
# 개발자 블로그 서비스 - Velog	https://v2.velog.io/rss/
# 월간 개발자 뉴스레터 - 개발자스럽다	https://blog.gaerae.com/feeds/posts/default?alt=rss
# IT 관련 뉴스 제공 블로그 - 44BITS	https://www.44bits.io/ko/feed/all

urls = [
    "https://www.mk.co.kr/rss/30100041/",
    "https://fs.jtbc.co.kr/RSS/entertainment.xml",
    "https://d2.naver.com/d2.atom",
    "https://www.itworld.co.kr/rss/feed/index.php"
]

max_repeat_count = 5
for url in urls:
    contents = ""
    repeat_count = 0
    feeds = feedparser.parse(url)
    for i in range(0, len(feeds["entries"])):
        title = feeds["entries"][i]["title"]
        description = feeds["entries"][i]["description"][0:30]
        link = feeds["entries"][i]["link"]
        feed = f"{title} ({link})\n\n"
        contents += feed

        repeat_count = repeat_count + 1
        if repeat_count == max_repeat_count:
            break

    print(contents)
    api.send_message_to_me('text', text=contents, link={})