"""
운세 자동화 - 하루 25개 포스팅
  1개  : 오늘의 운세 (종합)
 12개  : 별자리 운세 (양자리 ~ 물고기자리)
 12개  : 띠 운세 (쥐띠 ~ 돼지띠)
────────────────────────────────
 25개/일 × 30일 = 750개/월
"""

import os, random, time
import pandas as pd
import requests
from datetime import datetime, date

# ─────────────────────────────────────────
# 경로 설정
# ─────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, '..', 'data')

def csv(name):
    try:
        return pd.read_csv(os.path.join(DATA, name))
    except:
        return pd.DataFrame()

# ─────────────────────────────────────────
# CSV 로드
# ─────────────────────────────────────────
fortune_emotion  = csv("fortune_emotion_5000.csv")
fortune_1000     = csv("fortune_sentences_1000.csv")
fortune_4000     = csv("fortune_sentences_4000.csv")
daily_365        = csv("daily_fortunes_365.csv")
fortune_365      = csv("fortune_365_days.csv")
zodiac_kr        = csv("zodiac_fortune_1000.csv")
zodiac12         = csv("zodiac12_fortune_1000.csv")
chinese_zodiac   = csv("chinese_zodiac_fortunes.csv")
colors_200       = csv("lucky_colors_200.csv")
numbers_500      = csv("lucky_numbers_500.csv")
seo_keywords     = csv("fortune_seo_keywords_3000.csv")
seo_patterns     = csv("seo_patterns.csv")

# ─────────────────────────────────────────
# 정적 데이터
# ─────────────────────────────────────────
ZODIACS = [
    {"en":"aries",       "kr":"양자리",    "date":"3/21~4/19",  "emoji":"♈"},
    {"en":"taurus",      "kr":"황소자리",  "date":"4/20~5/20",  "emoji":"♉"},
    {"en":"gemini",      "kr":"쌍둥이자리","date":"5/21~6/21",  "emoji":"♊"},
    {"en":"cancer",      "kr":"게자리",    "date":"6/22~7/22",  "emoji":"♋"},
    {"en":"leo",         "kr":"사자자리",  "date":"7/23~8/22",  "emoji":"♌"},
    {"en":"virgo",       "kr":"처녀자리",  "date":"8/23~9/22",  "emoji":"♍"},
    {"en":"libra",       "kr":"천칭자리",  "date":"9/23~10/22", "emoji":"♎"},
    {"en":"scorpio",     "kr":"전갈자리",  "date":"10/23~11/21","emoji":"♏"},
    {"en":"sagittarius", "kr":"사수자리",  "date":"11/22~12/21","emoji":"♐"},
    {"en":"capricorn",   "kr":"염소자리",  "date":"12/22~1/19", "emoji":"♑"},
    {"en":"aquarius",    "kr":"물병자리",  "date":"1/20~2/18",  "emoji":"♒"},
    {"en":"pisces",      "kr":"물고기자리","date":"2/19~3/20",  "emoji":"♓"},
]

CHINESE = [
    {"en":"rat",     "kr":"쥐띠",    "year":"1924,1936,1948,1960,1972,1984,1996,2008,2020","emoji":"🐭"},
    {"en":"ox",      "kr":"소띠",    "year":"1925,1937,1949,1961,1973,1985,1997,2009,2021","emoji":"🐮"},
    {"en":"tiger",   "kr":"호랑이띠","year":"1926,1938,1950,1962,1974,1986,1998,2010,2022","emoji":"🐯"},
    {"en":"rabbit",  "kr":"토끼띠",  "year":"1927,1939,1951,1963,1975,1987,1999,2011,2023","emoji":"🐰"},
    {"en":"dragon",  "kr":"용띠",    "year":"1928,1940,1952,1964,1976,1988,2000,2012,2024","emoji":"🐲"},
    {"en":"snake",   "kr":"뱀띠",    "year":"1929,1941,1953,1965,1977,1989,2001,2013,2025","emoji":"🐍"},
    {"en":"horse",   "kr":"말띠",    "year":"1930,1942,1954,1966,1978,1990,2002,2014,2026","emoji":"🐴"},
    {"en":"sheep",   "kr":"양띠",    "year":"1931,1943,1955,1967,1979,1991,2003,2015,2027","emoji":"🐑"},
    {"en":"monkey",  "kr":"원숭이띠","year":"1932,1944,1956,1968,1980,1992,2004,2016,2028","emoji":"🐵"},
    {"en":"rooster", "kr":"닭띠",    "year":"1933,1945,1957,1969,1981,1993,2005,2017,2029","emoji":"🐓"},
    {"en":"dog",     "kr":"개띠",    "year":"1934,1946,1958,1970,1982,1994,2006,2018,2030","emoji":"🐶"},
    {"en":"pig",     "kr":"돼지띠",  "year":"1935,1947,1959,1971,1983,1995,2007,2019,2031","emoji":"🐷"},
]

RATINGS = ["★★★☆☆","★★★★☆","★★★★★","★★☆☆☆","★★★★☆","★★★☆☆"]

# ─────────────────────────────────────────
# 유틸 함수
# ─────────────────────────────────────────
def sentence():
    pool = []
    for df in [fortune_emotion, fortune_1000, fortune_4000]:
        if not df.empty and 'sentence' in df.columns:
            pool += df['sentence'].dropna().tolist()
    return random.choice(pool) if pool else "오늘도 좋은 하루 되세요."

def daily_fortune():
    today = date.today().strftime("%Y-%m-%d")
    for df in [daily_365, fortune_365]:
        if not df.empty and 'date' in df.columns:
            m = df[df['date'] == today]
            if not m.empty:
                return m.iloc[0]['fortune']
    return sentence()

def zodiac_fortune(kr_name):
    for df in [zodiac_kr, zodiac12]:
        if not df.empty and 'zodiac' in df.columns:
            m = df[df['zodiac'] == kr_name]
            if not m.empty:
                return m.sample(1).iloc[0]['fortune']
    return sentence()

def chinese_fortune(en_name):
    if not chinese_zodiac.empty:
        m = chinese_zodiac[chinese_zodiac['animal_zodiac'] == en_name]
        if not m.empty:
            return m.sample(1).iloc[0]['fortune']
    return sentence()

def pick_color():
    if not colors_200.empty and 'color' in colors_200.columns:
        return colors_200.sample(1).iloc[0]['color']
    return "골드"

def pick_number():
    if not numbers_500.empty and 'number' in numbers_500.columns:
        return str(numbers_500.sample(1).iloc[0]['number'])
    return str(random.randint(1, 99))

def seo_title(target):
    if not seo_patterns.empty:
        p = seo_patterns.sample(1).iloc[0]['pattern']
        return p.replace("{대상}", target)
    return f"{target} 오늘의 운세"

def seo_keywords_str(n=8):
    if not seo_keywords.empty and 'keyword' in seo_keywords.columns:
        return ", ".join(seo_keywords.sample(n)['keyword'].tolist())
    return ""

def stars():
    return random.choice(RATINGS)

def style():
    return """
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Noto Sans KR',sans-serif;background:#f8f9ff;color:#333;padding:16px}
.wrap{max-width:720px;margin:auto}
.hero{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border-radius:18px;padding:36px 24px;text-align:center;margin-bottom:22px}
.hero h1{font-size:26px;margin-bottom:8px}
.hero p{opacity:.85;font-size:15px}
.card{background:#fff;border-radius:14px;padding:22px;margin-bottom:16px;box-shadow:0 2px 12px rgba(0,0,0,.07)}
.card h2{font-size:18px;margin-bottom:12px;color:#5b2d8e}
.card p{font-size:15px;line-height:1.85;color:#444}
.badge{display:inline-block;background:#f0eaff;color:#6c3483;padding:3px 10px;border-radius:20px;font-size:12px;margin-bottom:8px}
.lucky{display:flex;gap:12px;flex-wrap:wrap;margin-top:14px}
.lucky-box{flex:1;min-width:120px;background:#f8f0ff;border-radius:10px;padding:14px;text-align:center}
.lucky-box .lbl{font-size:12px;color:#888;margin-bottom:4px}
.lucky-box .val{font-size:20px;font-weight:700;color:#6c3483}
.stars{color:#f4a61e;font-size:13px;margin-left:6px}
.meta{color:#aaa;font-size:12px;text-align:center;padding:20px 0}
.tag-cloud{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.tag{background:#eef2ff;color:#5c6bc0;padding:4px 10px;border-radius:20px;font-size:11px}
</style>"""

# ─────────────────────────────────────────
# HTML 빌더
# ─────────────────────────────────────────

def build_today_post(today_str):
    """① 오늘의 운세 종합 1개"""
    f1 = daily_fortune()
    f2 = sentence()
    color = pick_color()
    number = pick_number()
    kw = seo_keywords_str(12)
    title = seo_title(f"{today_str} 오늘의 운세")
    tags = [t.strip() for t in kw.split(",")][:10]
    tag_html = "".join(f'<span class="tag">{t}</span>' for t in tags)

    content = f"""
{style()}
<div class="wrap">
  <div class="hero">
    <h1>🌟 오늘의 운세</h1>
    <p>{today_str}</p>
  </div>
  <div class="card">
    <span class="badge">📖 오늘의 메시지</span>
    <p>{f1}</p>
    <br>
    <p>{f2}</p>
    <div class="lucky">
      <div class="lucky-box"><div class="lbl">🎨 행운의 색</div><div class="val">{color}</div></div>
      <div class="lucky-box"><div class="lbl">🔢 행운의 숫자</div><div class="val">{number}</div></div>
    </div>
  </div>
  <div class="card">
    <span class="badge">🔍 관련 키워드</span>
    <div class="tag-cloud">{tag_html}</div>
  </div>
  <div class="meta">※ 재미로 보는 운세 콘텐츠입니다 · 매일 자정 업데이트</div>
</div>"""
    return title, content, ["오늘의운세","daily","운세"]


def build_zodiac_post(z, today_str):
    """② 별자리 운세 12개"""
    fortune = zodiac_fortune(z['kr'])
    color   = pick_color()
    number  = pick_number()
    rating  = stars()
    kw      = seo_keywords_str(6)
    target  = f"{z['kr']} {today_str}"
    title   = seo_title(target)

    content = f"""
{style()}
<div class="wrap">
  <div class="hero">
    <h1>{z['emoji']} {z['kr']} 오늘의 운세</h1>
    <p>{today_str} · {z['date']}</p>
  </div>
  <div class="card">
    <span class="badge">{z['kr']} 운세 {rating}</span>
    <p>{fortune}</p>
    <div class="lucky">
      <div class="lucky-box"><div class="lbl">🎨 행운의 색</div><div class="val">{color}</div></div>
      <div class="lucky-box"><div class="lbl">🔢 행운의 숫자</div><div class="val">{number}</div></div>
    </div>
  </div>
  <div class="meta">
    <p>· {z['kr']} ({z['date']})</p>
    <p>※ 재미로 보는 운세 콘텐츠입니다 · 매일 자정 업데이트</p>
  </div>
</div>"""
    return title, content, ["별자리운세", z['kr'], "오늘의운세"]


def build_chinese_post(c, today_str):
    """③ 띠 운세 12개"""
    fortune = chinese_fortune(c['en'])
    color   = pick_color()
    number  = pick_number()
    rating  = stars()
    kw      = seo_keywords_str(6)
    target  = f"{c['kr']} {today_str}"
    title   = seo_title(target)

    content = f"""
{style()}
<div class="wrap">
  <div class="hero">
    <h1>{c['emoji']} {c['kr']} 오늘의 운세</h1>
    <p>{today_str} · {c['year']}</p>
  </div>
  <div class="card">
    <span class="badge">{c['kr']} 운세 {rating}</span>
    <p>{fortune}</p>
    <div class="lucky">
      <div class="lucky-box"><div class="lbl">🎨 행운의 색</div><div class="val">{color}</div></div>
      <div class="lucky-box"><div class="lbl">🔢 행운의 숫자</div><div class="val">{number}</div></div>
    </div>
  </div>
  <div class="meta">
    <p>· {c['kr']} 해당 출생연도: {c['year']}</p>
    <p>※ 재미로 보는 운세 콘텐츠입니다 · 매일 자정 업데이트</p>
  </div>
</div>"""
    return title, content, ["띠운세", c['kr'], "오늘의운세"]


# ─────────────────────────────────────────
# Blogger 전송
# ─────────────────────────────────────────
BLOG_ID = os.environ.get("BLOG_ID","")
TOKEN   = os.environ.get("BLOGGER_TOKEN","")

def post_blogger(title, content, labels, idx, total):
    if not BLOG_ID or not TOKEN:
        print(f"[{idx:02d}/{total}] (테스트) {title[:50]}")
        return True

    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    resp = requests.post(url,
        headers={"Authorization":f"Bearer {TOKEN}","Content-Type":"application/json"},
        json={"title":title,"content":content,"labels":labels}
    )
    ok = resp.status_code == 200
    status = "✅" if ok else "❌"
    print(f"[{idx:02d}/{total}] {status} {title[:45]}  →  {resp.status_code}")
    if not ok:
        print(f"        오류: {resp.text[:120]}")
    time.sleep(1.2)   # API rate limit 방지
    return ok


# ─────────────────────────────────────────
# 메인
# ─────────────────────────────────────────
def main():
    today_str = datetime.now().strftime("%Y년 %m월 %d일")
    posts = []   # (title, content, labels)

    # ① 오늘의 운세 1개
    posts.append(build_today_post(today_str))

    # ② 별자리 12개
    for z in ZODIACS:
        posts.append(build_zodiac_post(z, today_str))

    # ③ 띠 12개
    for c in CHINESE:
        posts.append(build_chinese_post(c, today_str))

    total = len(posts)
    print(f"\n🌟 {today_str} 운세 포스팅 시작 — 총 {total}개\n")

    success = 0
    for i, (title, content, labels) in enumerate(posts, 1):
        if post_blogger(title, content, labels, i, total):
            success += 1

    print(f"\n✅ 완료: {success}/{total}개 게시 성공")

if __name__ == "__main__":
    main()
