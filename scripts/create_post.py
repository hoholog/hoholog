"""
운세 자동화 - 하루 27개 포스팅
  1개  : 오늘의 명언
 12개  : 별자리 운세
 12개  : 띠 운세
  1개  : 별자리 주간 운세 (12별자리 통합)
  1개  : 띠별 월간 운세 (12띠 통합)
────────────────────────────────
 27개/일 × 30일 = 810개/월
"""

import os, random, time
import pandas as pd
import requests
from datetime import datetime, date

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
fortune_emotion   = csv("fortune_emotion_5000.csv")
fortune_1000      = csv("fortune_sentences_1000.csv")
fortune_4000      = csv("fortune_sentences_4000.csv")
daily_365         = csv("daily_fortunes_365.csv")
fortune_365       = csv("fortune_365_days.csv")
fortune_quotes    = csv("fortune_quotes_10000.csv")   # ← 오늘의명언용
zodiac_kr         = csv("zodiac_fortune_1000.csv")
zodiac12          = csv("zodiac12_fortune_1000.csv")
chinese_zodiac    = csv("chinese_zodiac_fortunes.csv")
colors_200        = csv("lucky_colors_200.csv")
numbers_500       = csv("lucky_numbers_500.csv")
seo_keywords      = csv("fortune_seo_keywords_3000.csv")
seo_patterns      = csv("seo_patterns.csv")

# 주간/월간 CSV
weekly_500        = csv("weekly_fortune_500.csv")
monthly_500       = csv("monthly_fortune_500.csv")
zodiac_weekly     = csv("zodiac_weekly_1000.csv")
zodiac_monthly    = csv("zodiac_monthly_1000.csv")
chinese_weekly    = csv("chinese_weekly_1000.csv")
chinese_monthly   = csv("chinese_monthly_1000.csv")

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
    {"en":"rat",     "kr":"쥐띠",    "year":"1960,1972,1984,1996,2008,2020","emoji":"🐭"},
    {"en":"ox",      "kr":"소띠",    "year":"1961,1973,1985,1997,2009,2021","emoji":"🐮"},
    {"en":"tiger",   "kr":"호랑이띠","year":"1962,1974,1986,1998,2010,2022","emoji":"🐯"},
    {"en":"rabbit",  "kr":"토끼띠",  "year":"1963,1975,1987,1999,2011,2023","emoji":"🐰"},
    {"en":"dragon",  "kr":"용띠",    "year":"1964,1976,1988,2000,2012,2024","emoji":"🐲"},
    {"en":"snake",   "kr":"뱀띠",    "year":"1965,1977,1989,2001,2013,2025","emoji":"🐍"},
    {"en":"horse",   "kr":"말띠",    "year":"1966,1978,1990,2002,2014,2026","emoji":"🐴"},
    {"en":"sheep",   "kr":"양띠",    "year":"1967,1979,1991,2003,2015,2027","emoji":"🐑"},
    {"en":"monkey",  "kr":"원숭이띠","year":"1968,1980,1992,2004,2016,2028","emoji":"🐵"},
    {"en":"rooster", "kr":"닭띠",    "year":"1969,1981,1993,2005,2017,2029","emoji":"🐓"},
    {"en":"dog",     "kr":"개띠",    "year":"1970,1982,1994,2006,2018,2030","emoji":"🐶"},
    {"en":"pig",     "kr":"돼지띠",  "year":"1971,1983,1995,2007,2019,2031","emoji":"🐷"},
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

def pick_quote():
    """fortune_quotes_10000.csv에서 오늘의 명언 랜덤 선택"""
    if not fortune_quotes.empty and 'quote_ko' in fortune_quotes.columns:
        row = fortune_quotes.sample(1).iloc[0]
        quote = row['quote_ko']
        meaning = row.get('meaning', '')
        category = row.get('category', '')
        return quote, meaning, category
    return sentence(), "", ""

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

def weekly_fortune_general():
    if not weekly_500.empty and 'sentence' in weekly_500.columns:
        row = weekly_500.sample(1).iloc[0]
        return row['sentence'], row.get('advice', '')
    return sentence(), ""

def monthly_fortune_general():
    if not monthly_500.empty and 'sentence' in monthly_500.columns:
        row = monthly_500.sample(1).iloc[0]
        return row['sentence'], row.get('advice', '')
    return sentence(), ""

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

def seo_kw(n=8):
    if not seo_keywords.empty and 'keyword' in seo_keywords.columns:
        return ", ".join(seo_keywords.sample(n)['keyword'].tolist())
    return ""

def stars():
    return random.choice(RATINGS)

def get_week_range():
    today = date.today()
    mon = today.strftime("%m/%d")
    sun_day = today.toordinal() - today.weekday() + 6
    sun = date.fromordinal(sun_day).strftime("%m/%d")
    return f"{mon} ~ {sun}"

def get_month():
    return datetime.now().strftime("%Y년 %m월")

# ─────────────────────────────────────────
# 공통 CSS
# ─────────────────────────────────────────
def style():
    return """<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Noto Sans KR',sans-serif;background:#f8f9ff;color:#333;padding:16px}
.wrap{max-width:720px;margin:auto}
.hero{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border-radius:18px;padding:36px 24px;text-align:center;margin-bottom:22px}
.hero h1{font-size:26px;margin-bottom:8px}
.hero p{opacity:.85;font-size:15px}
.card{background:#fff;border-radius:14px;padding:22px;margin-bottom:16px;box-shadow:0 2px 12px rgba(0,0,0,.07)}
.card p{font-size:15px;line-height:1.85;color:#444}
.badge{display:inline-block;background:#f0eaff;color:#6c3483;padding:3px 10px;border-radius:20px;font-size:12px;margin-bottom:10px}
.lucky{display:flex;gap:12px;flex-wrap:wrap;margin-top:14px}
.lucky-box{flex:1;min-width:120px;background:#f8f0ff;border-radius:10px;padding:14px;text-align:center}
.lucky-box .lbl{font-size:12px;color:#888;margin-bottom:4px}
.lucky-box .val{font-size:20px;font-weight:700;color:#6c3483}
.meta{color:#aaa;font-size:12px;text-align:center;padding:20px 0}
.tag-cloud{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.tag{background:#eef2ff;color:#5c6bc0;padding:4px 10px;border-radius:20px;font-size:11px}
.week-day{background:#fff9e6;border-left:4px solid #f7b731;padding:12px 16px;border-radius:8px;margin-bottom:10px;font-size:14px;line-height:1.7}
.game-link{background:linear-gradient(135deg,#4f46e5,#7c3aed);border-radius:14px;padding:20px;text-align:center;margin-top:20px}
.game-link p{font-size:13px;color:rgba(255,255,255,.8);margin-bottom:10px}
.game-link a{display:inline-block;background:#fff;color:#4f46e5;padding:10px 28px;border-radius:10px;text-decoration:none;font-weight:700;font-size:14px}
.game-link a:hover{background:#f0eaff}
</style>"""

def site_link():
    return """
<div class="game-link">
    <p>🎮 운세와 함께 즐기는 무료 게임</p>
    <a href="https://hoholog.github.io/hoholog/#index">🎮 호호로그게임 바로가기</a>
</div>"""

# ─────────────────────────────────────────
# HTML 빌더
# ─────────────────────────────────────────

def build_quote_post(today_str):
    quote, meaning, category = pick_quote()
    quote2, meaning2, _ = pick_quote()
    color = pick_color()
    number = pick_number()
    title = seo_title(f"{today_str} 오늘의 명언")
    cat_badge = f" · {category}" if category and str(category) != 'nan' else ""
    meaning_html = f'<br><p style="font-size:14px;color:#666;line-height:1.8">{meaning}</p>' if meaning and str(meaning) != 'nan' else ""
    meaning2_html = f'<br><p style="font-size:13px;color:#888;line-height:1.7">{meaning2}</p>' if meaning2 and str(meaning2) != 'nan' else ""

    content = f"""{style()}
<div class="wrap">
  <div class="hero"><h1>📖 오늘의 명언</h1><p>{today_str}</p></div>
  <div class="card">
    <span class="badge">✨ 오늘의 명언{cat_badge}</span>
    <p style="font-size:17px;font-weight:700;line-height:1.9;color:#4a235a">❝ {quote} ❞</p>
    {meaning_html}
    <div class="lucky">
      <div class="lucky-box"><div class="lbl">🎨 행운의 색</div><div class="val">{color}</div></div>
      <div class="lucky-box"><div class="lbl">🔢 행운의 숫자</div><div class="val">{number}</div></div>
    </div>
  </div>
  <div class="card">
    <span class="badge">🌟 한 줄 더</span>
    <p style="font-size:15px;line-height:1.85;color:#444">❝ {quote2} ❞</p>
    {meaning2_html}
  </div>
  {site_link()}
  <div class="meta">※ 매일 자정 업데이트 · 오늘의 명언</div>
</div>"""
    return title, content, ["오늘의명언", "명언", "운세"]


def build_zodiac_post(z, today_str):
    fortune = zodiac_fortune(z['kr'])
    color = pick_color()
    number = pick_number()
    rating = stars()
    title = seo_title(f"{z['kr']} {today_str}")

    # 별자리 관련 키워드
    kw_list = [
        z['kr'], f"{z['kr']} 오늘운세", f"{z['kr']} 운세",
        f"{z['kr']} 오늘의운세", f"{z['kr']} 2026",
        f"{z['kr']} 별자리운세", f"별자리 {z['kr']}",
        f"{z['kr']} {today_str}", f"{z['date']} 별자리",
        "오늘의운세", "별자리운세", "운세"
    ]
    tag_html = "".join(f'<span class="tag">{t}</span>' for t in kw_list)

    content = f"""{style()}
<div class="wrap">
  <div class="hero"><h1>{z['emoji']} {z['kr']} 오늘의 운세</h1><p>{today_str} · {z['date']}</p></div>
  <div class="card">
    <span class="badge">{z['kr']} 운세 {rating}</span>
    <p>{fortune}</p>
    <div class="lucky">
      <div class="lucky-box"><div class="lbl">🎨 행운의 색</div><div class="val">{color}</div></div>
      <div class="lucky-box"><div class="lbl">🔢 행운의 숫자</div><div class="val">{number}</div></div>
    </div>
  </div>
  <div class="card"><span class="badge">🔍 관련 키워드</span><div class="tag-cloud">{tag_html}</div></div>
  <div class="meta"><p>{z['kr']} ({z['date']})</p><p>※ 재미로 보는 운세 콘텐츠입니다</p></div>
  {site_link()}
</div>"""
    return title, content, ["별자리운세", z['kr'], "운세"]


def build_chinese_post(c, today_str):
    fortune = chinese_fortune(c['en'])
    color = pick_color()
    number = pick_number()
    rating = stars()
    title = seo_title(f"{c['kr']} {today_str}")

    # 띠 관련 키워드 (출생연도 포함)
    years = c['year'].split(',')
    year_tags = [f"{y}년생 운세" for y in years[:4]]
    kw_list = [
        c['kr'], f"{c['kr']} 오늘운세", f"{c['kr']} 운세",
        f"{c['kr']} 오늘의운세", f"{c['kr']} 2026",
        f"{c['kr']} 띠운세", f"띠운세 {c['kr']}",
        f"{c['kr']} {today_str}", "오늘의운세", "띠운세", "운세"
    ] + year_tags
    tag_html = "".join(f'<span class="tag">{t}</span>' for t in kw_list)

    content = f"""{style()}
<div class="wrap">
  <div class="hero"><h1>{c['emoji']} {c['kr']} 오늘의 운세</h1><p>{today_str}</p></div>
  <div class="card">
    <span class="badge">{c['kr']} 운세 {rating}</span>
    <p>{fortune}</p>
    <div class="lucky">
      <div class="lucky-box"><div class="lbl">🎨 행운의 색</div><div class="val">{color}</div></div>
      <div class="lucky-box"><div class="lbl">🔢 행운의 숫자</div><div class="val">{number}</div></div>
    </div>
  </div>
  <div class="card"><span class="badge">🔍 관련 키워드</span><div class="tag-cloud">{tag_html}</div></div>
  <div class="meta"><p>{c['kr']} 출생연도: {c['year']}</p><p>※ 재미로 보는 운세 콘텐츠입니다</p></div>
  {site_link()}
</div>"""
    return title, content, ["띠운세", c['kr'], "운세"]


def build_zodiac_weekly_post(today_str):
    """12별자리 주간운세 한 페이지"""
    week_range = get_week_range()
    title = f"별자리 주간운세 {week_range} 12별자리 이번 주 운세 총정리"

    cards_html = ""
    for z in ZODIACS:
        fortune = zodiac_fortune(z['kr'])
        color = pick_color()
        number = pick_number()
        rating = stars()
        days = ["월","화","수","목","금","토","일"]
        day_html = "".join(
            f'<div class="week-day"><strong>{d}요일</strong> — {sentence()[:35]}...</div>'
            for d in days
        )
        cards_html += f"""
  <div class="card">
    <span class="badge">{z['emoji']} {z['kr']} ({z['date']}) {rating}</span>
    <p>{fortune}</p>
    <div class="lucky">
      <div class="lucky-box"><div class="lbl">🎨 행운의 색</div><div class="val">{color}</div></div>
      <div class="lucky-box"><div class="lbl">🔢 행운의 숫자</div><div class="val">{number}</div></div>
    </div>
    <br>{day_html}
  </div>"""

    content = f"""{style()}
<div class="wrap">
  <div class="hero"><h1>📅 별자리 주간운세</h1><p>{week_range} 12별자리 총정리</p></div>
  {cards_html}
  {site_link()}
  <div class="meta">※ 재미로 보는 운세 콘텐츠입니다 · 매주 업데이트</div>
</div>"""
    return title, content, ["별자리주간", "주간운세", "별자리운세"]


def build_chinese_monthly_post(today_str):
    """12띠 월간운세 한 페이지"""
    month = get_month()
    title = f"{month} 띠별 월간운세 12띠 한달 운세 총정리"

    cards_html = ""
    for c in CHINESE:
        fortune = chinese_fortune(c['en'])
        f1, _ = monthly_fortune_general()
        color = pick_color()
        number = pick_number()
        rating = stars()
        periods = [("상순 (1~10일)", sentence()), ("중순 (11~20일)", sentence()), ("하순 (21~말일)", sentence())]
        period_html = "".join(
            f'<div class="week-day"><strong>{p}</strong><br>{s}</div>'
            for p, s in periods
        )
        cards_html += f"""
  <div class="card">
    <span class="badge">{c['emoji']} {c['kr']} ({c['year'].split(',')[0]}년생~) {rating}</span>
    <p>{fortune}</p><br><p>{f1}</p>
    <div class="lucky">
      <div class="lucky-box"><div class="lbl">🎨 이달의 행운의 색</div><div class="val">{color}</div></div>
      <div class="lucky-box"><div class="lbl">🔢 이달의 행운의 숫자</div><div class="val">{number}</div></div>
    </div>
    <br>{period_html}
  </div>"""

    content = f"""{style()}
<div class="wrap">
  <div class="hero"><h1>🌙 띠별 월간운세</h1><p>{month} 12띠 총정리</p></div>
  {cards_html}
  {site_link()}
  <div class="meta">※ 재미로 보는 운세 콘텐츠입니다 · 매월 업데이트</div>
</div>"""
    return title, content, ["띠별월간", "월간운세", "띠운세"]


# ─────────────────────────────────────────
# Refresh Token으로 Access Token 자동 발급
# ─────────────────────────────────────────
BLOG_ID       = os.environ.get("BLOG_ID","")
REFRESH_TOKEN = os.environ.get("BLOGGER_REFRESH_TOKEN","")
CLIENT_ID     = os.environ.get("GOOGLE_CLIENT_ID","")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET","")

def get_access_token():
    resp = requests.post("https://oauth2.googleapis.com/token", data={
        "grant_type":    "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })
    if resp.status_code == 200:
        print("🔑 Access Token 자동 갱신 완료")
        return resp.json().get("access_token","")
    else:
        print(f"❌ Token 갱신 실패: {resp.text[:120]}")
        return os.environ.get("BLOGGER_TOKEN","")

ACCESS_TOKEN = get_access_token() if REFRESH_TOKEN else os.environ.get("BLOGGER_TOKEN","")

def post_blogger(title, content, labels, idx, total):
    if not BLOG_ID or not ACCESS_TOKEN:
        print(f"[{idx:02d}/{total}] (테스트) {title[:50]}")
        return True

    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    resp = requests.post(url,
        headers={"Authorization":f"Bearer {ACCESS_TOKEN}","Content-Type":"application/json"},
        json={"title":title,"content":content,"labels":labels}
    )
    ok = resp.status_code == 200
    status = "✅" if ok else "❌"
    print(f"[{idx:02d}/{total}] {status} {title[:45]}  →  {resp.status_code}")
    if not ok:
        print(f"        오류: {resp.text[:120]}")
    time.sleep(1.2)
    return ok


# ─────────────────────────────────────────
# 메인
# ─────────────────────────────────────────
def main():
    today_str = datetime.now().strftime("%Y년 %m월 %d일")
    posts = []

    # ① 오늘의 명언 1개
    posts.append(build_quote_post(today_str))

    # ② 별자리 운세 12개
    for z in ZODIACS:
        posts.append(build_zodiac_post(z, today_str))

    # ③ 띠 운세 12개
    for c in CHINESE:
        posts.append(build_chinese_post(c, today_str))

    # ④ 별자리 주간운세 1개 (12별자리 통합)
    posts.append(build_zodiac_weekly_post(today_str))

    # ⑤ 띠별 월간운세 1개 (12띠 통합)
    posts.append(build_chinese_monthly_post(today_str))

    total = len(posts)
    print(f"\n🌟 {today_str} 운세 포스팅 시작 — 총 {total}개\n")
    print("구성: 오늘의명언 1 + 별자리 12 + 띠 12 + 별자리주간 1 + 띠별월간 1 = 27개\n")

    success = 0
    for i, (title, content, labels) in enumerate(posts, 1):
        if post_blogger(title, content, labels, i, total):
            success += 1

    print(f"\n✅ 완료: {success}/{total}개 게시 성공")

if __name__ == "__main__":
    main()
