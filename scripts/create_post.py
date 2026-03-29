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
from datetime import datetime, date, timezone, timedelta

# KST = UTC+9
KST = timezone(timedelta(hours=9))

def now_kst():
    """항상 KST 기준 현재 시각 반환"""
    return datetime.now(KST)

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
fortune_score     = csv("fortune_score.csv")          # ← 운세 지수
lucky_items       = csv("lucky_items_1000.csv")        # ← 행운의 아이템 (별자리용)
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

def _make_chinese_years(base_year: int) -> str:
    """base_year부터 12년 주기로 1940년 이후 ~ 미래 1주기 연도 생성."""
    START = 1940
    current_year = now_kst().year
    # base_year에서 START 이후 첫 해당 연도 찾기
    y = base_year
    while y < START:
        y += 12
    years = []
    while y <= current_year + 12:
        years.append(str(y))
        y += 12
    return ",".join(years)

# 각 띠의 기준 연도(1900년대 최초 해당 연도)
_CHINESE_BASE = {
    "rat":1900,"ox":1901,"tiger":1902,"rabbit":1903,
    "dragon":1904,"snake":1905,"horse":1906,"sheep":1907,
    "monkey":1908,"rooster":1909,"dog":1910,"pig":1911,
}

CHINESE = [
    {"en":"rat",     "kr":"쥐띠",    "year":_make_chinese_years(_CHINESE_BASE["rat"]),     "emoji":"🐭"},
    {"en":"ox",      "kr":"소띠",    "year":_make_chinese_years(_CHINESE_BASE["ox"]),      "emoji":"🐮"},
    {"en":"tiger",   "kr":"호랑이띠","year":_make_chinese_years(_CHINESE_BASE["tiger"]),   "emoji":"🐯"},
    {"en":"rabbit",  "kr":"토끼띠",  "year":_make_chinese_years(_CHINESE_BASE["rabbit"]),  "emoji":"🐰"},
    {"en":"dragon",  "kr":"용띠",    "year":_make_chinese_years(_CHINESE_BASE["dragon"]),  "emoji":"🐲"},
    {"en":"snake",   "kr":"뱀띠",    "year":_make_chinese_years(_CHINESE_BASE["snake"]),   "emoji":"🐍"},
    {"en":"horse",   "kr":"말띠",    "year":_make_chinese_years(_CHINESE_BASE["horse"]),   "emoji":"🐴"},
    {"en":"sheep",   "kr":"양띠",    "year":_make_chinese_years(_CHINESE_BASE["sheep"]),   "emoji":"🐑"},
    {"en":"monkey",  "kr":"원숭이띠","year":_make_chinese_years(_CHINESE_BASE["monkey"]),  "emoji":"🐵"},
    {"en":"rooster", "kr":"닭띠",    "year":_make_chinese_years(_CHINESE_BASE["rooster"]), "emoji":"🐓"},
    {"en":"dog",     "kr":"개띠",    "year":_make_chinese_years(_CHINESE_BASE["dog"]),     "emoji":"🐶"},
    {"en":"pig",     "kr":"돼지띠",  "year":_make_chinese_years(_CHINESE_BASE["pig"]),     "emoji":"🐷"},
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
    today = now_kst().strftime("%Y-%m-%d")
    for df in [daily_365, fortune_365]:
        if not df.empty and 'date' in df.columns:
            m = df[df['date'] == today]
            if not m.empty:
                return m.iloc[0]['fortune']
    return sentence()

def zodiac_fortune(kr_name):
    if not zodiac_kr.empty and 'zodiac' in zodiac_kr.columns:
        m = zodiac_kr[zodiac_kr['zodiac'] == kr_name]
        if not m.empty:
            text = m.sample(1).iloc[0]['fortune']
            # 줄바꿈을 HTML <br><br>로 변환
            return str(text).replace('\n\n', '<br><br>').replace('\n', '<br>')
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

def pick_score(name):
    """운세 지수 랜덤 선택"""
    if not fortune_score.empty and 'zodiac' in fortune_score.columns:
        m = fortune_score[fortune_score['zodiac'] == name]
        if not m.empty:
            row = m.sample(1).iloc[0]
            return int(row['total']), int(row['money']), int(row['health']), int(row['love'])
    # 백업 랜덤
    return random.randint(60,95), random.randint(45,99), random.randint(50,99), random.randint(40,99)

def score_bar(label, emoji, pct, color):
    """운세 지수 막대 그래프 HTML"""
    filled = round(pct / 10)
    bar = '█' * filled + '░' * (10 - filled)
    return f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px"><span style="min-width:70px;font-size:13px">{emoji} {label}</span><span style="font-family:monospace;color:{color};font-size:14px">{bar}</span><span style="font-size:13px;font-weight:700;color:{color}">{pct}%</span></div>'

def score_card(name):
    """운세 지수 카드 HTML"""
    total, money, health, love = pick_score(name)
    return f'''<div class="card" style="background:#f8f0ff">
    <span class="badge">📊 오늘의 운세 지수</span>
    <div style="margin-top:10px">
        {score_bar("종합운", "🌟", total,  "#6c3483")}
        {score_bar("금전운", "💰", money,  "#d4ac0d")}
        {score_bar("건강운", "💪", health, "#1e8449")}
        {score_bar("애정운", "❤️", love,   "#e74c3c")}
    </div>
</div>'''

def pick_lucky_item(zodiac_name):
    """별자리 행운의 아이템 선택"""
    if not lucky_items.empty and 'zodiac' in lucky_items.columns:
        m = lucky_items[lucky_items['zodiac'] == zodiac_name]
        if not m.empty:
            return m.sample(1).iloc[0]['item']
    return random.choice(['수정 팔찌', '네잎클로버', '파란 돌', '은반지', '향초'])

def pick_color():
    if not colors_200.empty and 'color' in colors_200.columns:
        return colors_200.sample(1).iloc[0]['color']
    return "골드"

def pick_number():
    if not numbers_500.empty and 'number' in numbers_500.columns:
        num = numbers_500.sample(1).iloc[0]['number']
        # 1~99 범위로 제한
        return str(int(num) % 99 + 1)
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
    today = now_kst().date()
    mon = today.strftime("%m/%d")
    sun_day = today.toordinal() - today.weekday() + 6
    sun = date.fromordinal(sun_day).strftime("%m/%d")
    return f"{mon} ~ {sun}"

def get_month():
    return now_kst().strftime("%Y년 %m월")

# ─────────────────────────────────────────
# 공통 CSS
# ─────────────────────────────────────────
def style():
    return """<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
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
.fortune-card{background:linear-gradient(135deg,#667eea,#764ba2);border-radius:20px;padding:28px;color:#fff;margin-bottom:16px}
.fortune-card .fc-emoji{font-size:48px;text-align:center;margin-bottom:10px}
.fortune-card .fc-title{font-size:22px;font-weight:900;text-align:center;margin-bottom:4px}
.fortune-card .fc-sub{font-size:13px;opacity:.8;text-align:center;margin-bottom:6px}
.fortune-card .fc-stars{color:#fde68a;text-align:center;font-size:14px;margin-bottom:16px}
.fortune-card .fc-text{background:rgba(255,255,255,.15);border-radius:12px;padding:16px;font-size:14px;line-height:1.85;margin-bottom:14px}
.fortune-card .fc-lucky{display:flex;gap:10px}
.fortune-card .fc-lucky-box{flex:1;background:rgba(255,255,255,.2);border-radius:10px;padding:10px;text-align:center}
.fortune-card .fc-lucky-lbl{font-size:11px;opacity:.8;margin-bottom:4px}
.fortune-card .fc-lucky-val{font-size:18px;font-weight:900}
.fortune-card .fc-watermark{font-size:11px;opacity:.5;text-align:center;margin-top:12px}
.save-btn{display:block;width:100%;background:#7c3aed;color:#fff;border:none;padding:14px;border-radius:12px;font-size:15px;font-weight:700;cursor:pointer;margin-bottom:16px}
.save-btn:hover{background:#6d28d9}
</style>
<script>
function saveFortuneCard(cardId, filename) {
    var el = document.getElementById(cardId);
    if (!el) { alert('카드를 찾을 수 없습니다'); return; }
    var btn = document.getElementById('savebtn-' + cardId);
    if (btn) { btn.textContent = '⏳ 저장 중...'; btn.disabled = true; }
    html2canvas(el, {scale:2, backgroundColor:null, useCORS:true, logging:false}).then(function(canvas) {
        var a = document.createElement('a');
        a.download = filename + '.png';
        a.href = canvas.toDataURL('image/png');
        a.click();
        if (btn) { btn.textContent = '📸 이미지 저장'; btn.disabled = false; }
    }).catch(function() {
        alert('저장 실패. 스크린샷을 이용해주세요.');
        if (btn) { btn.textContent = '📸 이미지 저장'; btn.disabled = false; }
    });
}
</script>"""

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
    title = seo_title(f"{today_str} 오늘의 명언")
    cat_badge = f" · {category}" if category and str(category) != 'nan' else ""
    meaning_html = f'<br><p style="font-size:14px;color:#666;line-height:1.8">{meaning}</p>' if meaning and str(meaning) != 'nan' else ""

    content = f"""{style()}
<div class="wrap">
  <div class="hero"><h1>📖 오늘의 명언</h1><p>{today_str}</p></div>
  <div class="card">
    <span class="badge">✨ 오늘의 명언{cat_badge}</span>
    <p style="font-size:17px;font-weight:700;line-height:1.9;color:#4a235a">❝ {quote} ❞</p>
    {meaning_html}
  </div>
  {site_link()}
  <div class="meta">※ 매일 자정 업데이트 · 오늘의 명언</div>
</div>"""
    return title, content, ["오늘의명언", "명언", "운세"]


def build_zodiac_post(z, today_str):
    fortune = zodiac_fortune(z['kr'])
    rating = stars()
    title = f"{z['kr']} {today_str} 오늘의 운세"
    card_id = f"fc-{z['en']}"

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

  <div id="{card_id}" class="fortune-card">
    <div class="fc-emoji">{z['emoji']}</div>
    <div class="fc-title">{z['kr']}</div>
    <div class="fc-sub">{today_str} · {z['date']}</div>
    <div class="fc-stars">{rating}</div>
    <div class="fc-text">{fortune}</div>
    <div class="fc-watermark">todayhoroscopelaboratory.blogspot.com · {today_str}</div>
  </div>

  <button id="savebtn-{card_id}" class="save-btn" onclick="saveFortuneCard('{card_id}', '{z['kr']}_운세_{today_str}')">📸 이미지 저장</button>

  {score_card(z['kr'])}

  <div class="card"><span class="badge">🔍 관련 키워드</span><div class="tag-cloud">{tag_html}</div></div>
  <div class="meta"><p>{z['kr']} ({z['date']})</p><p>※ 재미로 보는 운세 콘텐츠입니다</p></div>
  {site_link()}
</div>"""
    return title, content, ["별자리운세", z['kr'], "운세"]


def build_chinese_post(c, today_str):
    fortune = chinese_fortune(c['en'])
    rating = stars()
    title = f"{c['kr']} {today_str} 오늘의 띠운세"
    card_id = f"fc-{c['en']}"

    # 출생연도별 각각 다른 운세 (현재 연도 이하만 표시)
    current_year = now_kst().year
    years = [y for y in c['year'].split(',') if int(y) <= current_year]
    year_rows = ""
    for y in years:
        yr_fortune = chinese_fortune(c['en'])
        year_rows += f'''<div style="border-bottom:1px solid #ede9fe;padding:12px 0;display:flex;align-items:flex-start;gap:12px">
            <div style="min-width:72px;background:#7c3aed;color:#fff;border-radius:8px;padding:6px 10px;text-align:center;font-size:13px;font-weight:700">{y}년생</div>
            <div style="flex:1">
                <div style="font-size:13px;color:#444;line-height:1.7">{yr_fortune}</div>
            </div>
        </div>'''

    years_tags = [f"{y}년생 운세" for y in years[:4]]
    kw_list = [
        c['kr'], f"{c['kr']} 오늘운세", f"{c['kr']} 운세",
        f"{c['kr']} 오늘의운세", f"{c['kr']} 2026",
        f"{c['kr']} 띠운세", f"띠운세 {c['kr']}",
        f"{c['kr']} {today_str}", "오늘의운세", "띠운세", "운세"
    ] + years_tags
    tag_html = "".join(f'<span class="tag">{t}</span>' for t in kw_list)

    content = f"""{style()}
<div class="wrap">
  <div class="hero"><h1>{c['emoji']} {c['kr']} 오늘의 운세</h1><p>{today_str}</p></div>

  <div class="card">
    <span class="badge">{c['emoji']} {c['kr']} 출생연도별 오늘 운세</span>
    <div style="margin-top:8px">{year_rows}</div>
  </div>

  <div id="{card_id}" class="fortune-card">
    <div class="fc-emoji">{c['emoji']}</div>
    <div class="fc-title">{c['kr']}</div>
    <div class="fc-sub">{today_str}</div>
    <div class="fc-stars">{rating}</div>
    <div class="fc-text">{fortune}</div>
    <div class="fc-watermark">todayhoroscopelaboratory.blogspot.com · {today_str}</div>
  </div>

  <button id="savebtn-{card_id}" class="save-btn" onclick="saveFortuneCard('{card_id}', '{c['kr']}_운세_{today_str}')">📸 이미지 저장</button>

  {score_card(c['kr'])}

  <div class="card"><span class="badge">🔍 관련 키워드</span><div class="tag-cloud">{tag_html}</div></div>
  <div class="meta"><p>{c['kr']} 출생연도: {c['year']}</p><p>※ 재미로 보는 운세 콘텐츠입니다</p></div>
  {site_link()}
</div>"""
    return title, content, ["띠운세", c['kr'], "운세"]


def zodiac_weekly_fortune(kr_name):
    """주간 운세 CSV에서 가져오기"""
    if not zodiac_weekly.empty and 'zodiac' in zodiac_weekly.columns:
        m = zodiac_weekly[zodiac_weekly['zodiac'] == kr_name]
        if not m.empty:
            text = m.sample(1).iloc[0]['fortune']
            return str(text).replace('\n\n', '<br><br>').replace('\n', '<br>')
    return sentence()

def build_zodiac_weekly_post(today_str):
    """별자리별 주간운세 12개 개별 발행 — 매주 월요일"""
    week_range = get_week_range()
    month_str  = now_kst().strftime("%Y년 %m월")
    results = []
    for z in ZODIACS:
        fortune = zodiac_weekly_fortune(z['kr'])
        color   = pick_color()
        number  = pick_number()
        rating  = stars()
        # 제목: "양자리 2026년 03월 주간운세" — html fetchWeeklyPost 검색 키워드와 일치
        title = f"{z['kr']} {month_str} 주간운세 {week_range}"
        kw_list = [
            z['kr'], f"{z['kr']} 주간운세", f"{z['kr']} 이번주운세",
            "별자리 주간운세", f"{z['kr']} {month_str}", "주간운세", "별자리운세"
        ]
        tag_html = "".join(f'<span class="tag">{t}</span>' for t in kw_list)
        content_html = f"""{style()}
<div class="wrap">
  <div class="hero"><h1>📅 {z['emoji']} {z['kr']} 주간운세</h1><p>{week_range} · {z['date']}</p></div>
  <div class="card">
    <span class="badge">{z['emoji']} {z['kr']} ({z['date']}) {rating}</span>
    <p style="line-height:1.9">{fortune}</p>
    <div class="lucky">
      <div class="lucky-box"><div class="lbl">🎨 행운의 색</div><div class="val">{color}</div></div>
      <div class="lucky-box"><div class="lbl">🔢 행운의 숫자</div><div class="val">{number}</div></div>
    </div>
  </div>
  <div class="card"><span class="badge">🔍 관련 키워드</span><div class="tag-cloud">{tag_html}</div></div>
  {site_link()}
  <div class="meta">※ 재미로 보는 운세 콘텐츠입니다 · 매주 업데이트</div>
</div>"""
        results.append((title, content_html, ["별자리주간", z['kr'], "주간운세"]))
    return results


def build_chinese_monthly_post(today_str):
    """띠별 월간운세 12개 개별 발행 — 매월 1일"""
    month_str = get_month()
    results = []
    for c in CHINESE:
        fortune = chinese_fortune(c['en'])
        f1, _   = monthly_fortune_general()
        color   = pick_color()
        number  = pick_number()
        rating  = stars()
        periods = [("상순 (1~10일)", sentence()), ("중순 (11~20일)", sentence()), ("하순 (21~말일)", sentence())]
        period_html = "".join(
            f'<div class="week-day"><strong>{p}</strong><br>{s}</div>'
            for p, s in periods
        )
        # 제목: "쥐띠 2026년 03월 월간운세" — html fetchMonthlyPost 검색 키워드와 일치
        title = f"{c['kr']} {month_str} 월간운세"
        kw_list = [
            c['kr'], f"{c['kr']} 월간운세", f"{c['kr']} 이달운세",
            "띠별 월간운세", f"{c['kr']} {month_str}", "월간운세", "띠운세"
        ]
        tag_html = "".join(f'<span class="tag">{t}</span>' for t in kw_list)
        content_html = f"""{style()}
<div class="wrap">
  <div class="hero"><h1>🌙 {c['emoji']} {c['kr']} 월간운세</h1><p>{month_str}</p></div>
  <div class="card">
    <span class="badge">{c['emoji']} {c['kr']} ({c['year'].split(',')[0]}년생~) {rating}</span>
    <p>{fortune}</p><br><p>{f1}</p>
    <div class="lucky">
      <div class="lucky-box"><div class="lbl">🎨 이달의 색</div><div class="val">{color}</div></div>
      <div class="lucky-box"><div class="lbl">🔢 이달의 숫자</div><div class="val">{number}</div></div>
    </div>
    <br>{period_html}
  </div>
  <div class="card"><span class="badge">🔍 관련 키워드</span><div class="tag-cloud">{tag_html}</div></div>
  {site_link()}
  <div class="meta">※ 재미로 보는 운세 콘텐츠입니다 · 매월 업데이트</div>
</div>"""
        results.append((title, content_html, ["띠별월간", c['kr'], "월간운세"]))
    return results


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
    
    for attempt in range(1, 4):  # 최대 3회 재시도
        resp = requests.post(url,
            headers={"Authorization":f"Bearer {ACCESS_TOKEN}","Content-Type":"application/json"},
            json={"title":title,"content":content,"labels":labels}
        )
        if resp.status_code == 200:
            print(f"[{idx:02d}/{total}] ✅ {title[:45]}  →  200")
            time.sleep(3)   # 분당 쿼터 보호: 3초 간격
            return True
        elif resp.status_code == 429:
            wait = 60 * attempt  # 1분, 2분, 3분
            print(f"[{idx:02d}/{total}] ⏳ 429 쿼터 초과 — {wait}초 대기 후 재시도 ({attempt}/3)...")
            time.sleep(wait)
        else:
            print(f"[{idx:02d}/{total}] ❌ {title[:45]}  →  {resp.status_code}")
            print(f"        오류: {resp.text[:120]}")
            time.sleep(3)
            return False

    print(f"[{idx:02d}/{total}] ❌ {title[:45]}  →  3회 재시도 후 실패")
    return False


# ─────────────────────────────────────────
# 메인
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# ⑥ 운세SNS — 별자리 12개 통합 (간결 카드형)
# ─────────────────────────────────────────
def build_sns_zodiac_post(today_str):
    """별자리 12개를 한 포스트에 SNS 카드형으로"""
    title = f"✨ 오늘의 별자리 운세 전체 {today_str} — 12별자리 한눈에"

    cards_html = ""
    for z in ZODIACS:
        fortune = zodiac_fortune(z['kr'])
        # 100~200자 범위로 자르기
        plain = fortune.replace('<br><br>', ' ').replace('<br>', ' ').strip()
        # 문장 단위로 끊되 최소 100자 확보
        sentences = plain.split('. ')
        short = ''
        for s in sentences:
            candidate = (short + s + '. ').strip()
            if len(candidate) >= 100:
                short = candidate
                break
            short = candidate
        # 200자 초과 시 자르기
        if len(short) > 200:
            short = short[:197] + '…'
        # 너무 짧으면 원문 앞 150자
        if len(short) < 60:
            short = plain[:150] + ('…' if len(plain) > 150 else '')
        cards_html += f"""
<div style="display:flex;align-items:flex-start;gap:12px;padding:14px;margin-bottom:10px;
            background:#fff;border-radius:14px;box-shadow:0 2px 8px rgba(0,0,0,.06);
            border-left:4px solid #667eea">
  <div style="font-size:32px;line-height:1">{z['emoji']}</div>
  <div style="flex:1;min-width:0">
    <div style="font-weight:900;font-size:14px;color:#4c1d95">{z['kr']}
      <span style="font-size:11px;color:#888;font-weight:400"> {z['date']}</span>
    </div>
    <div style="font-size:13px;color:#444;line-height:1.7;margin:4px 0">{short}</div>
  </div>
</div>"""

    card_id = f"sns-zodiac-{today_str.replace(' ','').replace('년','').replace('월','').replace('일','')}"
    content_html = f"""{style()}
<div class="wrap">
  <div class="hero" style="background:linear-gradient(135deg,#667eea,#764ba2)">
    <h1>✨ 오늘의 별자리 운세</h1>
    <p>{today_str} · 12별자리 전체</p>
  </div>
  <div id="{card_id}" style="background:#f8f7ff;border-radius:16px;padding:16px;margin-bottom:16px">
    {cards_html}
    <div style="text-align:center;margin-top:8px;font-size:11px;color:#aaa">✨ hoholog.github.io · {today_str}</div>
  </div>
  <button id="savebtn-{card_id}" class="save-btn" onclick="saveFortuneCard('{card_id}', '별자리운세전체_{today_str}')">📸 이미지 저장</button>
  <div style="background:#eef2ff;border-radius:12px;padding:12px;font-size:12px;color:#666;text-align:center;margin-bottom:16px">
    🔮 각 별자리를 클릭하면 상세 운세를 확인할 수 있어요
  </div>
  <div class="card"><span class="badge">🔍 관련 키워드</span>
    <div class="tag-cloud">{''.join(f'<span class="tag">{k}</span>' for k in kw)}</div>
  </div>
  {site_link()}
  <div class="meta">※ 재미로 보는 운세 콘텐츠 · 매일 업데이트</div>
</div>"""

    kw = ["별자리운세", "오늘운세", "별자리", today_str,
          "양자리", "황소자리", "쌍둥이자리", "게자리", "사자자리", "처녀자리",
          "천칭자리", "전갈자리", "사수자리", "염소자리", "물병자리", "물고기자리",
          "12별자리운세", "별자리운세전체", "오늘의별자리", "별자리총정리",
          "오늘운세보기", "무료운세", "운세2026"]
    labels = ["별자리운세통합", "운세SNS", "운세", "별자리운세"]
    return title, content_html, labels


# ─────────────────────────────────────────
# ⑦ 운세SNS — 띠 12개 통합 (간결 카드형)
# ─────────────────────────────────────────
def build_sns_chinese_post(today_str):
    """띠 12개를 한 포스트에 SNS 카드형으로"""
    title = f"🐾 오늘의 띠별 운세 전체 {today_str} — 12띠 한눈에"

    cards_html = ""
    for c in CHINESE:
        fortune = chinese_fortune(c['en'])
        plain = str(fortune).strip()
        # 100~200자 범위로 자르기
        sentences = plain.split('. ')
        short = ''
        for s in sentences:
            candidate = (short + s + '. ').strip()
            if len(candidate) >= 100:
                short = candidate
                break
            short = candidate
        if len(short) > 200:
            short = short[:197] + '…'
        if len(short) < 60:
            short = plain[:150] + ('…' if len(plain) > 150 else '')
        # 대표 연도 3개만
        years_short = ', '.join(c['year'].split(',')[-3:]) + '년생'
        cards_html += f"""
<div style="display:flex;align-items:flex-start;gap:12px;padding:14px;margin-bottom:10px;
            background:#fff;border-radius:14px;box-shadow:0 2px 8px rgba(0,0,0,.06);
            border-left:4px solid #f59e0b">
  <div style="font-size:32px;line-height:1">{c['emoji']}</div>
  <div style="flex:1;min-width:0">
    <div style="font-weight:900;font-size:14px;color:#92400e">{c['kr']}
      <span style="font-size:11px;color:#888;font-weight:400"> {years_short}</span>
    </div>
    <div style="font-size:13px;color:#444;line-height:1.7;margin:4px 0">{short}</div>
  </div>
</div>"""

    card_id = f"sns-chinese-{today_str.replace(' ','').replace('년','').replace('월','').replace('일','')}"
    content_html = f"""{style()}
<div class="wrap">
  <div class="hero" style="background:linear-gradient(135deg,#f59e0b,#d97706)">
    <h1>🐾 오늘의 띠별 운세</h1>
    <p>{today_str} · 12띠 전체</p>
  </div>
  <div id="{card_id}" style="background:#fffbeb;border-radius:16px;padding:16px;margin-bottom:16px">
    {cards_html}
    <div style="text-align:center;margin-top:8px;font-size:11px;color:#aaa">🐾 hoholog.github.io · {today_str}</div>
  </div>
  <button id="savebtn-{card_id}" class="save-btn" onclick="saveFortuneCard('{card_id}', '띠별운세전체_{today_str}')">📸 이미지 저장</button>
  <div style="background:#fef3c7;border-radius:12px;padding:12px;font-size:12px;color:#666;text-align:center;margin-bottom:16px">
    🐾 각 띠를 클릭하면 출생연도별 상세 운세를 확인할 수 있어요
  </div>
  <div class="card"><span class="badge">🔍 관련 키워드</span>
    <div class="tag-cloud">{''.join(f'<span class="tag">{k}</span>' for k in kw)}</div>
  </div>
  {site_link()}
  <div class="meta">※ 재미로 보는 운세 콘텐츠 · 매일 업데이트</div>
</div>"""

    kw = ["띠운세", "오늘운세", "띠별운세", today_str,
          "쥐띠", "소띠", "호랑이띠", "토끼띠", "용띠", "뱀띠",
          "말띠", "양띠", "원숭이띠", "닭띠", "개띠", "돼지띠",
          "12띠운세", "띠운세전체", "오늘의띠운세", "띠운세총정리",
          "오늘운세보기", "무료운세", "운세2026"]
    labels = ["띠운세통합", "운세SNS", "운세", "띠운세"]
    return title, content_html, labels


def main():
    today_str = now_kst().strftime("%Y년 %m월 %d일")
    kst_now   = now_kst()
    posts = []

    # ① 오늘의 명언 1개
    posts.append(build_quote_post(today_str))

    # ② 별자리 운세 12개
    for z in ZODIACS:
        posts.append(build_zodiac_post(z, today_str))

    # ③ 띠 운세 12개
    for c in CHINESE:
        posts.append(build_chinese_post(c, today_str))

    # ⑥ 운세SNS — 별자리 통합 1개 (매일)
    posts.append(build_sns_zodiac_post(today_str))

    # ⑦ 운세SNS — 띠 통합 1개 (매일)
    posts.append(build_sns_chinese_post(today_str))

    # 수동 실행 시 강제 포함 옵션
    force_weekly  = os.environ.get("FORCE_WEEKLY",  "false").lower() == "true"
    force_monthly = os.environ.get("FORCE_MONTHLY", "false").lower() == "true"

    # ④ 별자리 주간운세 — 매주 월요일 or 강제 실행
    if kst_now.weekday() == 0 or force_weekly:
        posts.extend(build_zodiac_weekly_post(today_str))
        label = "강제 포함" if force_weekly and kst_now.weekday() != 0 else "월요일"
        print(f"📅 별자리 주간운세 12개 포함 ({label})")
    else:
        print("📅 주간운세 스킵 (월요일 아님)")

    # ⑤ 띠별 월간운세 — 매월 1일 or 강제 실행
    if kst_now.day == 1 or force_monthly:
        posts.extend(build_chinese_monthly_post(today_str))
        label = "강제 포함" if force_monthly and kst_now.day != 1 else "1일"
        print(f"📅 띠별 월간운세 12개 포함 ({label})")
    else:
        print("📅 월간운세 스킵 (1일 아님)")

    total = len(posts)
    weekly  = " + 별자리주간 12" if kst_now.weekday() == 0 else ""
    monthly = " + 띠별월간 12"   if kst_now.day == 1        else ""
    count   = 27 + (12 if kst_now.weekday() == 0 else 0) + (12 if kst_now.day == 1 else 0)
    print(f"\n🌟 {today_str} 운세 포스팅 시작 — 총 {total}개\n")
    print(f"구성: 오늘의명언 1 + 별자리 12 + 띠 12 + SNS통합 2{weekly}{monthly} = {count}개\n")

    success = 0
    for i, (title, content, labels) in enumerate(posts, 1):
        if post_blogger(title, content, labels, i, total):
            success += 1

    print(f"\n✅ 완료: {success}/{total}개 게시 성공")

if __name__ == "__main__":
    main()
