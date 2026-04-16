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
# GitHub Actions에서 DATA_DIR 환경변수로 경로 오버라이드 가능
if os.environ.get('DATA_DIR'):
    DATA = os.environ['DATA_DIR']

# ─────────────────────────────────────────
# 포스트 타입별 대표 이미지 URL
# GitHub raw URL 형식:
#   https://raw.githubusercontent.com/{유저명}/{저장소명}/main/data/파일명.png
# ※ 아래 _GITHUB_RAW 의 {유저명}/{저장소명} 을 실제 값으로 교체하세요
# ─────────────────────────────────────────
IMG = {
    "zodiac":  "https://i.ibb.co/hFTQc66p/todayhoroscopelaboratory03.png",  # 별자리 오늘 운세
    "chinese": "https://i.ibb.co/ccxKySzq/todayhoroscopelaboratory04.png",  # 띠 오늘 운세
    "weekly":  "https://i.ibb.co/PZyr5FvY/todayhoroscopelaboratory05.png",  # 주간운세 (띠+별자리)
    "monthly": "https://i.ibb.co/Dfqdzbd2/todayhoroscopelaboratory06.png",  # 띠별 월간운세
}

def post_img(key):
    """포스트 상단 히어로 아래 삽입용 이미지 HTML"""
    url = IMG.get(key, "")
    if not url:
        return ""
    return (
        '<div style="text-align:center;margin-bottom:20px">'
        f'<img src="{url}" alt="오늘의운세로그" '
        'style="width:100%;max-width:680px;border-radius:16px;'
        'box-shadow:0 4px 20px rgba(0,0,0,0.12)" '
        "onerror=\"this.style.display='none'\">"
        '</div>'
    )

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
    mon_day = today.toordinal() - today.weekday()   # 이번 주 월요일
    mon = date.fromordinal(mon_day).strftime("%m/%d")
    sun = date.fromordinal(mon_day + 6).strftime("%m/%d")
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
.share-btn-main{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;background:#f3f4f6;color:#333;border:none;padding:14px;border-radius:12px;font-size:15px;font-weight:700;cursor:pointer;margin-bottom:10px}
.share-btn-main:hover{background:#e5e7eb}
.share-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:9000;align-items:flex-end}
.share-overlay.open{display:flex}
.share-sheet{background:#fff;border-radius:20px 20px 0 0;padding:20px 16px 32px;width:100%;max-width:480px;margin:0 auto;animation:slideUp .25s ease}
@keyframes slideUp{from{transform:translateY(100%)}to{transform:translateY(0)}}
.sheet-title{text-align:center;font-size:13px;color:#888;margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid #f0f0f0}
.sheet-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:16px}
.sheet-item{display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;border:none;background:none;padding:0}
.sheet-icon{width:52px;height:52px;border-radius:16px;display:flex;align-items:center;justify-content:center}
.sheet-item span{font-size:11px;color:#444;font-weight:600}
.sheet-cancel{display:block;width:100%;background:#f3f4f6;border:none;border-radius:12px;padding:13px;font-size:15px;font-weight:700;color:#333;cursor:pointer;margin-top:4px}
.sheet-cancel:hover{background:#e5e7eb}
</style>
<script>
function saveFortuneCard(cardId, filename) {
    var el = document.getElementById(cardId);
    if (!el) { alert('카드를 찾을 수 없습니다'); return; }
    var btn = document.getElementById('savebtn-' + cardId);
    if (btn) { btn.textContent = '⏳ 저장 중...'; btn.disabled = true; }

    var isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
    var isAndroid = /android/i.test(navigator.userAgent);

    html2canvas(el, {scale:2, backgroundColor:'#ffffff', useCORS:true, logging:false}).then(function(canvas) {

        // ── iOS Safari: Web Share API로 사진첩 저장 ──
        if (isIOS && navigator.share && navigator.canShare) {
            canvas.toBlob(function(blob) {
                var file = new File([blob], filename + '.png', {type:'image/png'});
                if (navigator.canShare({files:[file]})) {
                    navigator.share({files:[file], title:filename})
                    .then(function() {
                        if (btn) { btn.textContent = '📸 이미지 저장'; btn.disabled = false; }
                    })
                    .catch(function(e) {
                        if (e.name !== 'AbortError') { fallbackDownload(canvas, filename); }
                        if (btn) { btn.textContent = '📸 이미지 저장'; btn.disabled = false; }
                    });
                } else {
                    fallbackDownload(canvas, filename);
                    if (btn) { btn.textContent = '📸 이미지 저장'; btn.disabled = false; }
                }
            }, 'image/png');
            return;
        }

        // ── Android / PC: Blob URL로 직접 다운로드 ──
        canvas.toBlob(function(blob) {
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = filename + '.png';
            document.body.appendChild(a);
            a.click();
            setTimeout(function() {
                URL.revokeObjectURL(url);
                document.body.removeChild(a);
            }, 300);
            if (btn) { btn.textContent = '📸 이미지 저장'; btn.disabled = false; }
        }, 'image/png');

    }).catch(function() {
        alert('저장 실패. 스크린샷을 이용해주세요.');
        if (btn) { btn.textContent = '📸 이미지 저장'; btn.disabled = false; }
    });
}

function fallbackDownload(canvas, filename) {
    canvas.toBlob(function(blob) {
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = filename + '.png';
        document.body.appendChild(a);
        a.click();
        setTimeout(function() { URL.revokeObjectURL(url); document.body.removeChild(a); }, 300);
    }, 'image/png');
}
</script>"""

def share_buttons(card_id, filename):
    """공유하기 버튼 → 바텀시트
    핵심 수정:
    - __fortuneShareInited 가드 제거 → fortOpenSheet를 항상 window에 즉시 정의
    - 바텀시트 DOM/CSS는 최초 1회만 생성 (id 체크 방식으로 안전하게)
    - 버튼 onclick에서 직접 window.fortOpenSheet 호출 → ReferenceError 방지
    """
    return f"""
<button class="share-btn-main" onclick="if(window.fortOpenSheet){{window.fortOpenSheet('{card_id}','{filename}')}}else{{alert('잠시 후 다시 시도해주세요');}}" ontouchstart="" style="cursor:pointer;touch-action:manipulation">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
  공유하기
</button>
<button id="savebtn-{card_id}" class="save-btn" onclick="saveFortuneCard('{card_id}', '{filename}')">📸 이미지 저장</button>
<script>
(function(){{
  /* ── CSS: 최초 1회만 삽입 ── */
  if (!document.getElementById('__fort_css')) {{
    var css = document.createElement('style');
    css.id = '__fort_css';
    css.textContent =
      '.fort-ov{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;' +
      'background:rgba(0,0,0,.52);z-index:2147483647;align-items:flex-end;justify-content:center}}' +
      '.fort-ov.on{{display:flex!important}}' +
      '.fort-sh{{background:#fff;border-radius:20px 20px 0 0;padding:22px 16px 38px;' +
      'width:100%;max-width:480px;box-sizing:border-box;' +
      'animation:fortUp .25s cubic-bezier(.4,0,.2,1)}}' +
      '@keyframes fortUp{{from{{transform:translateY(100%)}}to{{transform:translateY(0)}}}}' +
      '.fort-ttl{{text-align:center;font-size:13px;color:#888;margin-bottom:18px;' +
      'padding-bottom:14px;border-bottom:1px solid #f0f0f0}}' +
      '.fort-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:14px}}' +
      '.fort-btn{{display:flex;flex-direction:column;align-items:center;gap:5px;' +
      'border:none;background:none;cursor:pointer;padding:10px 4px;' +
      '-webkit-tap-highlight-color:rgba(0,0,0,.08);touch-action:manipulation;' +
      'user-select:none;-webkit-user-select:none;min-width:58px}}' +
      '.fort-ico{{width:56px;height:56px;border-radius:16px;display:flex;' +
      'align-items:center;justify-content:center;flex-shrink:0}}' +
      '.fort-btn span{{font-size:10px;color:#444;font-weight:600;text-align:center;line-height:1.3;word-break:keep-all}}' +
      '.fort-cancel{{display:block;width:100%;background:#f3f4f6;border:none;' +
      'border-radius:12px;padding:14px;font-size:15px;font-weight:700;color:#333;' +
      'cursor:pointer;-webkit-tap-highlight-color:transparent}}';
    document.head.appendChild(css);
  }}

  /* ── 바텀시트 DOM: 최초 1회만 생성 ── */
  if (!document.getElementById('__fort_ov')) {{
    var ov = document.createElement('div');
    ov.id = '__fort_ov';
    ov.className = 'fort-ov';
    ov.innerHTML =
      '<div class="fort-sh" id="__fort_sh">' +
        '<div class="fort-ttl">공유하기</div>' +
        '<div class="fort-grid">' +
          /* 카카오톡 */
          '<button class="fort-btn" id="__fb_kk">' +
            '<div class="fort-ico" style="background:#FEE500">' +
              '<svg width="26" height="26" viewBox="0 0 24 24" fill="#3C1E1E">' +
                '<path d="M12 3C6.477 3 2 6.477 2 10.5c0 2.61 1.548 4.91 3.89 6.27' +
                'l-.99 3.63 4.22-2.79c.95.19 1.89.29 2.88.29 5.523 0 10-3.477 10-7.41' +
                'C22 6.477 17.523 3 12 3z"/>' +
              '</svg>' +
            '</div><span>카카오톡</span>' +
          '</button>' +
          /* 네이버밴드 */
          '<button class="fort-btn" id="__fb_bd">' +
            '<div class="fort-ico" style="background:#03C75A">' +
              '<svg width="26" height="26" viewBox="0 0 40 40" fill="#fff">' +
                '<rect x="4" y="4" width="32" height="32" rx="8"/>' +
                '<rect x="11" y="12" width="6" height="16" fill="#03C75A"/>' +
                '<rect x="23" y="12" width="6" height="16" fill="#03C75A"/>' +
              '</svg>' +
            '</div><span>네이버밴드</span>' +
          '</button>' +
          /* 쓰레드 */
          '<button class="fort-btn" id="__fb_th">' +
            '<div class="fort-ico" style="background:#000">' +
              '<svg width="22" height="22" viewBox="0 0 192 192" fill="#fff">' +
                '<path d="M141.537 88.988a66.667 66.667 0 00-2.518-1.143' +
                'c-1.482-27.307-16.403-42.94-41.457-43.1h-.34' +
                'c-14.986 0-27.449 6.396-35.12 18.036l13.779 9.452' +
                'c5.73-8.695 14.724-10.548 21.348-10.548h.229' +
                'c8.249.053 14.474 2.452 18.503 7.129' +
                'c2.932 3.405 4.893 8.111 5.864 14.05' +
                'c-7.314-1.243-15.224-1.626-23.68-1.14' +
                'c-23.82 1.371-39.134 15.264-38.105 34.568' +
                'c.522 9.792 5.4 18.216 13.735 23.719' +
                'c7.047 4.652 16.124 6.927 25.557 6.412' +
                'c12.458-.683 22.231-5.436 29.049-14.127' +
                'c5.178-6.6 8.453-15.153 9.899-25.93' +
                'c5.937 3.583 10.337 8.298 12.767 13.966' +
                'c4.132 9.635 4.373 25.468-8.546 38.376' +
                'c-11.319 11.308-24.925 16.2-45.488 16.351' +
                'c-22.809-.169-40.06-7.484-51.275-21.742' +
                'C88.809 149.438 83 132.938 82.432 112h-16.57' +
                'c.6 24.74 8.355 44.742 22.637 57.967' +
                'C101.243 182.022 121.22 190.169 144 190.351l.402-.002' +
                'c24.203-.172 42.426-6.856 56.189-20.6' +
                'c18.386-18.366 17.861-41.25 11.755-55.348' +
                'c-4.325-10.083-12.754-18.279-26.809-23.413z"/>' +
            '</svg>' +
            '</div><span>쓰레드</span>' +
          '</button>' +
          /* 인스타그램 */
          '<button class="fort-btn" id="__fb_ig">' +
            '<div class="fort-ico" style="background:linear-gradient(45deg,#f09433,#dc2743,#bc1888)">' +
              '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2">' +
                '<rect x="2" y="2" width="20" height="20" rx="5"/>' +
                '<circle cx="12" cy="12" r="4.5"/>' +
                '<circle cx="17.5" cy="6.5" r="1.2" fill="#fff" stroke="none"/>' +
              '</svg>' +
            '</div><span>인스타그램</span>' +
          '</button>' +
          /* URL복사 */
          '<button class="fort-btn" id="__fb_cp">' +
            '<div class="fort-ico" style="background:#6b7280">' +
              '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2">' +
                '<path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/>' +
                '<path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/>' +
              '</svg>' +
            '</div><span>URL 복사</span>' +
          '</button>' +
        '</div>' +
        '<button class="fort-cancel" id="__fb_cancel">취소</button>' +
      '</div>';
    document.body.appendChild(ov);

    /* ── 닫기 ── */
    function _close() {{
      ov.classList.remove('on');
      document.body.style.overflow = '';
    }}
    ov.addEventListener('click', function(e){{ if(e.target===ov) _close(); }});
    document.getElementById('__fb_cancel').addEventListener('click', _close);

    /* ── 공유 액션 ── */
    function _open(url, w, h) {{
      window.open(url, '_blank', 'width='+w+',height='+h);
      _close();
    }}
    document.getElementById('__fb_kk').addEventListener('click', function() {{
      var url = location.href;
      var isMobile = /android|iphone|ipad|ipod/i.test(navigator.userAgent);
      _close();
      if (isMobile) {{
        var timer = setTimeout(function() {{
          if (navigator.clipboard) {{
            navigator.clipboard.writeText(url).then(function() {{
              alert('📋 링크가 복사되었습니다!\\n카카오톡을 열어 붙여넣어 공유하세요.');
            }}).catch(function() {{ alert('카카오톡 앱을 열어 링크를 공유해 주세요:\\n' + url); }});
          }} else {{
            alert('카카오톡 앱에서 아래 링크를 공유해 주세요:\\n' + url);
          }}
        }}, 1500);
        window.location.href = 'kakaolink://send?msg=' + encodeURIComponent(document.title + '\\n' + url);
      }} else {{
        _open('https://story.kakao.com/share?url='+encodeURIComponent(url), 600, 500);
      }}
    }});
    document.getElementById('__fb_bd').addEventListener('click', function() {{
      _open('https://band.us/plugin/share?body='+encodeURIComponent(document.title+'\\n'+location.href)+'&route='+encodeURIComponent(location.href), 600, 600);
    }});
    document.getElementById('__fb_th').addEventListener('click', function() {{
      _open('https://www.threads.net/intent/post?text='+encodeURIComponent(document.title+'\\n'+location.href), 600, 600);
    }});
    document.getElementById('__fb_ig').addEventListener('click', function() {{
      var cid=window.__fort_cid, fn=window.__fort_fn;
      _close();
      if(typeof saveFortuneCard==='function') saveFortuneCard(cid, fn);
      setTimeout(function(){{ alert('📸 이미지 저장됨!\\n인스타그램 앱에서 올려주세요 📲'); }}, 1500);
    }});
    document.getElementById('__fb_cp').addEventListener('click', function() {{
      var url=location.href;
      function done(){{ _close(); alert('✅ 링크가 복사되었습니다!'); }}
      if(navigator.clipboard) {{ navigator.clipboard.writeText(url).then(done).catch(function(){{ fb(url); done(); }}); }}
      else {{ fb(url); done(); }}
      function fb(t) {{
        var x=document.createElement('textarea'); x.value=t;
        x.style.cssText='position:fixed;top:-9999px;left:-9999px;opacity:0';
        document.body.appendChild(x); x.focus(); x.select();
        document.execCommand('copy'); document.body.removeChild(x);
      }}
    }});

    /* ── 열기 함수: window에 즉시 등록 ── */
    window.fortOpenSheet = function(cardId, fname) {{
      window.__fort_cid = cardId;
      window.__fort_fn  = fname;
      document.getElementById('__fort_ov').classList.add('on');
      document.body.style.overflow = 'hidden';
    }};
    window.fortCloseSheet = _close;
  }}

  /* ── 이미 DOM이 있어도 fortOpenSheet는 항상 window에 보장 ── */
  if (!window.fortOpenSheet) {{
    window.fortOpenSheet = function(cardId, fname) {{
      window.__fort_cid = cardId;
      window.__fort_fn  = fname;
      var o = document.getElementById('__fort_ov');
      if (o) {{ o.classList.add('on'); document.body.style.overflow = 'hidden'; }}
    }};
  }}
}})();
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


# ─────────────────────────────────────────
# 별자리운세 SEO·콘텐츠 개선 헬퍼
# ─────────────────────────────────────────

# CTR 신호 키워드 풀 (점수 구간별)
_Z_SIGNAL_MONEY_UP   = ["금전운 상승 타이밍", "재물운 급상승", "수입 기회 포착", "금전 흐름 반전"]
_Z_SIGNAL_LOVE_UP    = ["연애운 급변", "인연 접촉 신호", "애정운 상승 중", "관계 반전 예고"]
_Z_SIGNAL_WARN       = ["오늘 주의 필요", "신중함이 필요한 날", "충동 결정 주의", "조심해야 할 타이밍"]
_Z_SIGNAL_TOTAL_UP   = ["오늘 총운 최고조", "행운 기회 포착", "운세 상승 흐름 확인", "오늘 놓치면 후회"]
_Z_SIGNAL_MID        = ["오늘 균형 잡힌 하루", "안정적 흐름 확인", "차분한 기운의 날"]

def _zodiac_seo_title(z_kr, today_dot, total, money, health, love):
    """지수 기반 CTR 최적화 제목 생성"""
    # 어떤 신호 쓸지 결정 (가장 두드러진 지표 우선)
    scores = {"money": money, "love": love, "total": total, "health": health}
    top_key = max(scores, key=scores.get)
    top_val = scores[top_key]
    avg = (total + money + love) / 3

    if top_key == "money" and money >= 78:
        signal = random.choice(_Z_SIGNAL_MONEY_UP)
    elif top_key == "love" and love >= 78:
        signal = random.choice(_Z_SIGNAL_LOVE_UP)
    elif total >= 82:
        signal = random.choice(_Z_SIGNAL_TOTAL_UP)
    elif avg <= 58:
        signal = random.choice(_Z_SIGNAL_WARN)
    elif abs(money - love) >= 35:
        signal = f"{'금전운' if money > love else '연애운'} 반전 주목"
    else:
        signal = random.choice(_Z_SIGNAL_MID)

    # 제목 패턴 (날짜 포맷: YYYY년 M월 D일)
    patterns = [
        f"{today_dot} {z_kr} 운세 | {signal}",
        f"{z_kr} 오늘운세 ({today_dot}) – {signal} 확인",
        f"[{today_dot}] {z_kr} 별자리 운세 — {signal}",
        f"{z_kr} {today_dot} 오늘의 운세 · {signal}",
    ]
    return random.choice(patterns), signal


# 섹션별 현실 디테일 문장 풀
_Z_LOVE_DETAIL_UP = [
    "오늘은 예상 못한 연락이 올 수 있습니다. 특히 오후 2시~5시 사이 인간관계 변화 신호가 강합니다.",
    "평소 마음에 두고 있던 사람과 자연스러운 대화 기회가 생길 수 있습니다. 먼저 다가가는 용기가 빛을 발합니다.",
    "SNS나 메신저에서 뜻밖의 메시지가 도착할 수 있습니다. 가볍게 답하되 진심을 담아 보세요.",
    "오늘 저녁 약속이 생긴다면 흘려 넘기지 마세요. 소중한 인연이 이어질 수 있는 자리입니다.",
]
_Z_LOVE_DETAIL_WARN = [
    "감정적으로 예민해지기 쉬운 날입니다. 중요한 대화는 감정이 가라앉은 저녁 이후로 미루세요.",
    "가까운 사람의 말 한마디가 상처로 느껴질 수 있습니다. 오늘은 상대 의도를 먼저 확인해 보세요.",
    "혼자만의 시간이 오히려 관계에 활력을 줄 수 있습니다. 무리해서 연락하기보다 여유를 가져 보세요.",
]
_Z_MONEY_DETAIL_UP = [
    "오늘 소소한 금전 이익이 발생할 수 있습니다. 적은 금액이라도 챙겨두면 나중에 큰 도움이 됩니다.",
    "미뤄두었던 환급금이나 정산 내역을 오늘 확인해 보세요. 놓친 돈이 있을 수 있습니다.",
    "오후 늦게 예상치 못한 수입 관련 연락이 올 수 있습니다. 꼼꼼히 검토하고 결정하세요.",
]
_Z_MONEY_DETAIL_WARN = [
    "오늘은 갑작스러운 지출이 생길 수 있습니다. 특히 오후 3시 이후 충동 구매를 주의하세요.",
    "카드 결제·자동이체 내역을 오늘 한 번 점검하세요. 모르는 사이 새어나가는 돈이 있을 수 있습니다.",
    "투자나 새로운 금전 계약은 오늘보다 2~3일 후로 미루는 것이 유리합니다.",
]
_Z_WORK_DETAIL_UP = [
    "오늘 업무에서 작은 성과가 인정받을 수 있습니다. 평소 해온 노력이 드디어 빛을 발하는 시기입니다.",
    "동료나 상사로부터 예상치 못한 긍정적인 피드백이 올 수 있습니다. 자신감을 갖고 임해 보세요.",
    "새로운 아이디어가 떠오르기 쉬운 날입니다. 메모해 두면 나중에 큰 자산이 됩니다.",
]
_Z_WORK_DETAIL_WARN = [
    "업무 중 세부 사항을 놓치기 쉬운 날입니다. 서두르지 말고 두 번 확인하는 습관을 발휘하세요.",
    "동료와의 의견 충돌이 생길 수 있습니다. 내 입장만 고집하기보다 상대 의견도 충분히 들어보세요.",
    "중요한 발표나 보고는 오늘보다 내일 진행하는 것이 더 좋은 결과를 가져올 수 있습니다.",
]
_Z_AVOID_ACTIONS = [
    ["충동적인 큰 결정", "감정적인 메시지 전송", "불필요한 논쟁 시작"],
    ["섣불리 계약서 사인", "새벽 늦게까지 야식 먹기", "검증 없는 투자 참여"],
    ["기분에 따른 충동 구매", "중요한 약속 취소", "남 험담에 동조하기"],
    ["급하게 사람 판단하기", "수면 부족 강행", "처음 보는 사람에게 돈 빌려주기"],
]
_Z_CHEER = [
    "오늘 하루도 쉽지 않다는 거 알아요. 그래도 당신은 이미 충분히 잘 해내고 있습니다. 오늘 하루도 조금씩, 천천히 나아가세요. ✨",
    "완벽하지 않아도 괜찮아요. 오늘의 작은 선택들이 쌓여 당신만의 길이 됩니다. 그 과정을 믿어보세요. 🌟",
    "힘든 날일수록 자신에게 너그러워지세요. 당신이 생각하는 것보다 훨씬 더 잘 버티고 있습니다. 오늘도 응원합니다. 💫",
    "오늘의 작은 걸음이 미래의 큰 변화를 만듭니다. 조급해하지 말고, 지금 이 순간에 집중해 보세요. 🌙",
    "당신 곁에 좋은 기운이 흐르고 있습니다. 눈에 보이지 않아도 분명히 쌓이고 있으니, 오늘도 힘내세요. ⭐",
]

def _split_fortune_sections(fortune_text):
    """운세 원문을 문단으로 분리해 섹션별로 배분"""
    plain = fortune_text.replace('<br><br>', '\n\n').replace('<br>', '\n')
    paras = [p.strip() for p in plain.split('\n\n') if p.strip()]
    # 문단이 부족하면 단일 문장 단위로 보충
    if len(paras) < 2:
        lines = [l.strip() for l in plain.split('\n') if l.strip()]
        paras = lines
    return paras

def _zodiac_score_badge(pct):
    """점수 → 색상·레벨 반환"""
    if pct >= 80: return "#16a34a", "상승 ↑"
    if pct >= 65: return "#d97706", "보통 →"
    return "#dc2626", "주의 ⚠"

def _zodiac_score_bar(label, emoji, pct):
    color, level = _zodiac_score_badge(pct)
    filled = round(pct / 10)
    bar = '█' * filled + '░' * (10 - filled)
    return (f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">'
            f'<span style="min-width:62px;font-size:12px">{emoji} {label}</span>'
            f'<span style="font-family:monospace;color:{color};font-size:13px;flex:1">{bar}</span>'
            f'<span style="font-size:12px;font-weight:700;color:{color};min-width:30px">{pct}%</span>'
            f'<span style="font-size:11px;color:{color}">{level}</span>'
            f'</div>')


def build_zodiac_post(z, today_str):
    fortune_raw = zodiac_fortune(z['kr'])
    rating      = stars()
    card_id     = f"fc-{z['en']}"

    # 날짜 포맷
    kst_now    = now_kst()
    today_dot  = kst_now.strftime("%Y년 %-m월 %-d일")   # 예: 2026년 4월 13일 (본문 표시용)
    today_sync = kst_now.strftime("%Y년 %m월 %d일")     # 예: 2026년 04월 13일 (index.html 매칭용 zero-pad)

    # 운세 지수
    total, money, health, love = pick_score(z['kr'])

    # SEO 신호 키워드 (제목 표시용)
    _, signal_kw = _zodiac_seo_title(z['kr'], today_dot, total, money, health, love)

    # 제목: index.html fetchFortunePost() 필수 키워드 고정 포함
    # 검색조건: [별자리명, "YYYY년", "MM월", "DD일", "오늘의 운세"] ALL 포함 필수
    title = f"{z['kr']} {today_sync} 오늘의 운세 | {signal_kw}"

    # 행운 아이템·색상·숫자
    lucky_item   = pick_lucky_item(z['kr'])
    lucky_color  = pick_color()
    lucky_number = pick_number()

    # 원문 문단 분리 (섹션 배분용)
    paras = _split_fortune_sections(fortune_raw)
    def _para(idx, fallback=""):
        return paras[idx] if idx < len(paras) else (paras[-1] if paras else fallback)

    # ── 1. 총운 (핵심 요약 2~3줄) ──
    total_color, total_level = _zodiac_score_badge(total)
    summary_html = f'''
<div class="card" style="border-left:5px solid {total_color}">
  <span class="badge" style="background:#f0fdf4;color:{total_color}">🌟 오늘 총운 · {total}% {total_level}</span>
  <p style="margin-top:10px;font-size:15px;line-height:1.9;color:#333;font-weight:500">{_para(0)}</p>
  <p style="margin-top:8px;font-size:14px;line-height:1.85;color:#555">{_para(1)}</p>
</div>'''

    # ── 2. 연애운 ──
    love_color, love_level = _zodiac_score_badge(love)
    love_detail = random.choice(_Z_LOVE_DETAIL_UP if love >= 70 else _Z_LOVE_DETAIL_WARN)
    love_html = f'''
<div class="card">
  <span class="badge" style="background:#fff0f3;color:#e11d48">❤️ 연애운 · {love}% {love_level}</span>
  <p style="margin-top:10px;font-size:14px;line-height:1.85;color:#444">{_para(2)}</p>
  <div style="margin-top:10px;background:#fff0f3;border-radius:10px;padding:12px 14px;
              font-size:13px;color:#9f1239;line-height:1.75;border-left:3px solid #e11d48">
    💡 {love_detail}
  </div>
</div>'''

    # ── 3. 금전운 ──
    money_color, money_level = _zodiac_score_badge(money)
    money_detail = random.choice(_Z_MONEY_DETAIL_UP if money >= 70 else _Z_MONEY_DETAIL_WARN)
    money_html = f'''
<div class="card">
  <span class="badge" style="background:#fefce8;color:#a16207">💰 금전운 · {money}% {money_level}</span>
  <p style="margin-top:10px;font-size:14px;line-height:1.85;color:#444">{_para(3)}</p>
  <div style="margin-top:10px;background:#fefce8;border-radius:10px;padding:12px 14px;
              font-size:13px;color:#92400e;line-height:1.75;border-left:3px solid #d97706">
    💡 {money_detail}
  </div>
</div>'''

    # ── 4. 직장·사업운 ──
    work_score = round((total + health) / 2)
    work_color, work_level = _zodiac_score_badge(work_score)
    work_detail = random.choice(_Z_WORK_DETAIL_UP if work_score >= 70 else _Z_WORK_DETAIL_WARN)
    work_html = f'''
<div class="card">
  <span class="badge" style="background:#eff6ff;color:#1d4ed8">💼 직장·사업운 · {work_score}% {work_level}</span>
  <p style="margin-top:10px;font-size:14px;line-height:1.85;color:#444">{_para(4)}</p>
  <div style="margin-top:10px;background:#eff6ff;border-radius:10px;padding:12px 14px;
              font-size:13px;color:#1e3a8a;line-height:1.75;border-left:3px solid #1d4ed8">
    💡 {work_detail}
  </div>
</div>'''

    # ── 5. 오늘 피해야 할 행동 ──
    avoid_list = random.choice(_Z_AVOID_ACTIONS)
    avoid_items_html = "".join(
        f'<div style="display:flex;align-items:center;gap:8px;padding:7px 0;'
        f'border-bottom:1px solid #fee2e2;font-size:13px;color:#555">'
        f'<span style="color:#dc2626;font-weight:700;flex-shrink:0">✕</span>{item}</div>'
        for item in avoid_list
    )
    avoid_html = f'''
<div class="card" style="border-left:5px solid #dc2626">
  <span class="badge" style="background:#fef2f2;color:#b91c1c">⚠️ 오늘 피해야 할 행동</span>
  <div style="margin-top:10px">{avoid_items_html}</div>
</div>'''

    # ── 6. 응원 토닥 메시지 ──
    cheer_html = f'''
<div style="background:linear-gradient(135deg,#667eea,#764ba2);border-radius:16px;
            padding:22px 20px;margin-bottom:16px;text-align:center">
  <div style="font-size:20px;margin-bottom:8px">{z['emoji']}</div>
  <p style="font-size:14px;color:rgba(255,255,255,0.95);line-height:1.85">
    {random.choice(_Z_CHEER)}
  </p>
</div>'''

    # ── 운세 지수 카드 ──
    score_html = f'''
<div class="card" style="background:#f8f0ff">
  <span class="badge">📊 오늘의 운세 지수 · <strong style="color:#6c3483">{signal_kw}</strong></span>
  <div style="margin-top:12px">
    {_zodiac_score_bar("종합운","🌟",total)}
    {_zodiac_score_bar("금전운","💰",money)}
    {_zodiac_score_bar("건강운","💪",health)}
    {_zodiac_score_bar("애정운","❤️",love)}
  </div>
</div>'''

    # ── 이미지 저장 카드 (총운·연애운·금전운·직장운·피해야할행동 포함) ──
    avoid_short = "".join(
        f'<div style="display:flex;align-items:center;gap:6px;font-size:12px;color:rgba(255,255,255,0.85);padding:4px 0">'
        f'<span style="color:#fca5a5;font-weight:700">✕</span>{item}</div>'
        for item in avoid_list
    )
    image_card_html = f'''
<div id="{card_id}" class="fortune-card">
  <div class="fc-emoji">{z['emoji']}</div>
  <div class="fc-title">{z['kr']}</div>
  <div class="fc-sub">{today_str} · {z['date']}</div>
  <div class="fc-stars">{rating}</div>

  <!-- 총운 -->
  <div style="background:rgba(255,255,255,0.12);border-radius:10px;padding:12px;margin-bottom:8px">
    <div style="font-size:11px;color:rgba(255,255,255,0.7);margin-bottom:6px">🌟 오늘 총운 · {total}%</div>
    <div style="font-size:13px;line-height:1.75;color:rgba(255,255,255,0.95)">{_para(0)}</div>
  </div>

  <!-- 연애운 -->
  <div style="background:rgba(255,255,255,0.12);border-radius:10px;padding:12px;margin-bottom:8px">
    <div style="font-size:11px;color:rgba(255,255,255,0.7);margin-bottom:6px">❤️ 연애운 · {love}%</div>
    <div style="font-size:13px;line-height:1.75;color:rgba(255,255,255,0.95)">{_para(2)}</div>
  </div>

  <!-- 금전운 -->
  <div style="background:rgba(255,255,255,0.12);border-radius:10px;padding:12px;margin-bottom:8px">
    <div style="font-size:11px;color:rgba(255,255,255,0.7);margin-bottom:6px">💰 금전운 · {money}%</div>
    <div style="font-size:13px;line-height:1.75;color:rgba(255,255,255,0.95)">{_para(3)}</div>
  </div>

  <!-- 직장·사업운 -->
  <div style="background:rgba(255,255,255,0.12);border-radius:10px;padding:12px;margin-bottom:8px">
    <div style="font-size:11px;color:rgba(255,255,255,0.7);margin-bottom:6px">💼 직장·사업운 · {work_score}%</div>
    <div style="font-size:13px;line-height:1.75;color:rgba(255,255,255,0.95)">{_para(4)}</div>
  </div>

  <!-- 오늘 피해야 할 행동 -->
  <div style="background:rgba(220,38,38,0.2);border-radius:10px;padding:12px;margin-bottom:12px">
    <div style="font-size:11px;color:rgba(255,255,255,0.7);margin-bottom:6px">⚠️ 오늘 피해야 할 행동</div>
    {avoid_short}
  </div>

  <!-- 행운 아이템 -->
  <div class="fc-lucky">
    <div class="fc-lucky-box"><div class="fc-lucky-lbl">행운 아이템</div><div class="fc-lucky-val" style="font-size:13px">{lucky_item}</div></div>
    <div class="fc-lucky-box"><div class="fc-lucky-lbl">행운 색상</div><div class="fc-lucky-val" style="font-size:13px">{lucky_color}</div></div>
    <div class="fc-lucky-box"><div class="fc-lucky-lbl">행운 숫자</div><div class="fc-lucky-val">{lucky_number}</div></div>
  </div>
  <div class="fc-watermark">todayhoroscopelaboratory.blogspot.com · {today_str}</div>
</div>'''

    # ── SEO 키워드 태그 ──
    kw_list = [
        z['kr'], f"{z['kr']} 오늘운세", f"{z['kr']} 운세",
        f"{z['kr']} 오늘의운세", f"{z['kr']} {today_dot}",
        f"{z['kr']} 별자리운세", f"{z['kr']} 금전운", f"{z['kr']} 연애운",
        f"{z['kr']} 직장운", f"{z['date']} 별자리",
        "오늘의운세", "별자리운세", "무료운세", "별자리오늘",
        "금전운 상승", "연애운 급변", "오늘 주의", "운세 반전",
    ]
    tag_html = "".join(f'<span class="tag">{t}</span>' for t in kw_list)

    content = f"""{style()}
<div class="wrap">
  <!-- 히어로 -->
  <div class="hero">
    <h1>{z['emoji']} {z['kr']} 오늘의 운세</h1>
    <p>{today_str} · {z['date']}</p>
    <div style="margin-top:10px;display:inline-block;background:rgba(255,255,255,0.2);
                padding:4px 14px;border-radius:20px;font-size:13px;font-weight:700">
      {signal_kw}
    </div>
  </div>

  <!-- 1. 총운 -->
  {summary_html}

  <!-- 대표 이미지 -->
  {post_img("zodiac")}

  <!-- 2. 연애운 -->
  {summary_html}

  <!-- 2. 연애운 -->
  {love_html}

  <!-- 3. 금전운 -->
  {money_html}

  <!-- 4. 직장·사업운 -->
  {work_html}

  <!-- 5. 오늘 피해야 할 행동 -->
  {avoid_html}

  <!-- 6. 응원 토닥 메시지 -->
  {cheer_html}

  <!-- 운세 지수 -->
  {score_html}

  <!-- 이미지 저장 카드 -->
  {image_card_html}

  <!-- 공유·저장 버튼 -->
  {share_buttons(card_id, f"{z['kr']}_운세_{today_dot}")}

  <!-- SEO 키워드 -->
  <div class="card"><span class="badge">🔍 관련 키워드</span><div class="tag-cloud">{tag_html}</div></div>
  <div class="meta"><p>{z['kr']} ({z['date']})</p><p>※ 재미로 보는 운세 콘텐츠입니다</p></div>
  {site_link()}
</div>"""
    return title, content, ["별자리운세", z['kr'], "운세", "오늘운세"]


def build_chinese_post(c, today_str):
    fortune = chinese_fortune(c['en'])
    rating  = stars()
    card_id = f"fc-{c['en']}"

    kst_now    = now_kst()
    today_dot  = kst_now.strftime("%Y년 %-m월 %-d일")  # 본문 표시용
    today_sync = kst_now.strftime("%Y년 %m월 %d일")    # index.html 매칭용 zero-pad
    total, money, health, love = pick_score(c['kr'])

    # ── 제목: 신호 키워드 자동 선택 ──
    _SIG_UP   = ["재물운 상승 신호", "금전운 상승 중", "운세 상승 흐름", "행운 상승 감지"]
    _SIG_WARN = ["오늘 주의 필요", "신중함이 필요한 날", "주의 신호 감지", "한 발 물러서기"]
    _SIG_REV  = ["반전의 하루", "예상 밖 반전 운세", "충격적 변화 예고", "흐름이 바뀌는 날"]
    _SIG_MID  = ["안정적인 하루", "균형 잡힌 운세", "차분한 에너지의 날"]
    avg = (total + money) / 2
    if avg >= 80:                signal = random.choice(_SIG_UP)
    elif avg <= 55:              signal = random.choice(_SIG_WARN)
    elif abs(total-money) >= 30: signal = random.choice(_SIG_REV)
    else:                        signal = random.choice(_SIG_MID)

    # 제목: index.html fetchChinesePost() 필수 키워드 고정 포함
    # 검색조건: [띠명, "YYYY년", "MM월", "DD일", "띠운세"] ALL 포함 필수
    title = f"{c['kr']} {today_sync} 오늘의 띠운세 | {signal}"

    # ── 현실 디테일 문장 (지수 기반) ──
    _DET_MONEY_UP   = ["오늘 예상치 못한 소액 수입이 들어올 수 있습니다. 작은 금액이라도 놓치지 마세요.",
                       "미뤄두었던 환급금이나 정산 내역을 오늘 확인해 보세요."]
    _DET_MONEY_WARN = ["오늘은 갑작스러운 지출이 생길 수 있습니다. 특히 오후 3시 이후 충동 구매를 주의하세요.",
                       "카드 결제·자동이체 내역을 오늘 한 번 점검하세요."]
    _DET_HEALTH_UP  = ["오늘은 가벼운 스트레칭이나 산책이 에너지를 끌어올려 줍니다.",
                       "수분 섭취를 늘리면 오후 피로감이 크게 줄어들 것입니다."]
    _DET_HEALTH_WARN= ["피로가 누적되기 쉬운 날입니다. 점심 후 짧은 휴식을 꼭 챙기세요.",
                       "오늘은 과식이나 자극적인 음식을 피하면 소화 불편을 예방할 수 있습니다."]
    _DET_LOVE_UP    = ["오늘 주변 사람에게 먼저 따뜻한 말 한마디를 건네면 관계가 깊어집니다.",
                       "소개나 만남 자리가 생긴다면 적극적으로 참여해 보세요."]
    _DET_LOVE_WARN  = ["오늘은 감정적으로 예민해질 수 있습니다. 중요한 대화는 저녁 이후로 미루세요.",
                       "가까운 사람과의 오해가 생길 수 있습니다. 말보다 먼저 상대 입장을 들어보세요."]
    _DET_CAUTION    = ["오늘은 서류·계약 관련 사항은 꼼꼼히 재확인 후 진행하세요.",
                       "중요한 결정은 오늘보다 하루 이틀 여유를 두고 내리는 것이 유리합니다."]

    detail_lines = [
        random.choice(_DET_MONEY_UP   if money  >= 70 else _DET_MONEY_WARN),
        random.choice(_DET_HEALTH_UP  if health >= 70 else _DET_HEALTH_WARN),
        random.choice(_DET_LOVE_UP    if love   >= 70 else _DET_LOVE_WARN),
        random.choice(_DET_CAUTION),
    ]
    detail_html = "".join(
        f'<div style="display:flex;gap:8px;padding:8px 0;border-bottom:1px solid #f3f0ff;'
        f'font-size:13px;color:#444;line-height:1.7">'
        f'<span style="flex-shrink:0;color:#7c3aed">▸</span><span>{line}</span></div>'
        for line in detail_lines
    )

    # ── 주의점 본문 추출 ──
    caution_kws = ["주의", "조심", "피하", "삼가", "무리하지", "충동", "서두르지"]
    plain_fortune = str(fortune).replace('\n', ' ').strip()
    caution_sentence = next(
        (s.strip() for s in plain_fortune.split('. ')
         if any(k in s for k in caution_kws) and len(s.strip()) > 10), ""
    )
    caution_html = f'''
<div style="background:#fff8e1;border-left:4px solid #f59e0b;border-radius:10px;
            padding:14px 16px;margin-bottom:16px">
  <div style="font-size:12px;font-weight:700;color:#d97706;margin-bottom:6px">⚠️ 오늘의 주의점</div>
  <div style="font-size:14px;color:#555;line-height:1.75">{caution_sentence}</div>
</div>''' if caution_sentence else ""

    # ── 운세 지수 ──
    def _sc(v): return ("#16a34a","상승 ↑") if v>=80 else (("#d97706","보통") if v>=65 else ("#dc2626","주의 ⚠"))
    def _bar(label, emoji, pct):
        c2,lv = _sc(pct); f2=round(pct/10)
        return (f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:9px">'
                f'<span style="min-width:65px;font-size:12px">{emoji} {label}</span>'
                f'<span style="font-family:monospace;color:{c2};font-size:13px">{"█"*f2}{"░"*(10-f2)}</span>'
                f'<span style="font-size:12px;font-weight:700;color:{c2};min-width:28px">{pct}%</span>'
                f'<span style="font-size:11px;color:{c2}">{lv}</span></div>')
    score_html = f'''<div class="card" style="background:#f8f0ff">
  <span class="badge">📊 오늘의 운세 지수 · <strong style="color:#6c3483">{signal}</strong></span>
  <div style="margin-top:12px">
    {_bar("종합운","🌟",total)}{_bar("금전운","💰",money)}{_bar("건강운","💪",health)}{_bar("애정운","❤️",love)}
  </div>
</div>'''

    # ── 출생연도별 (이미지 카드 내부) ──
    current_year = kst_now.year
    years = [y for y in c['year'].split(',') if int(y) <= current_year]
    year_rows_in_card = ""
    for y in years:
        yr_fortune = chinese_fortune(c['en'])
        plain = str(yr_fortune).replace('\n', ' ').strip()
        short = plain[:80] + ('…' if len(plain) > 80 else '')
        year_rows_in_card += (
            f'<div style="display:flex;align-items:flex-start;gap:10px;padding:9px 0;'
            f'border-bottom:1px solid rgba(255,255,255,0.18)">'
            f'<div style="min-width:62px;background:rgba(255,255,255,0.22);color:#fff;'
            f'border-radius:8px;padding:4px 7px;text-align:center;font-size:11px;'
            f'font-weight:700;flex-shrink:0">{y}년생</div>'
            f'<div style="font-size:12px;color:rgba(255,255,255,0.9);line-height:1.65;flex:1">{short}</div>'
            f'</div>'
        )

    # ── SEO 키워드 ──
    years_tags = [f"{y}년생 {c['kr']}" for y in years[:4]]
    kw_list = [
        c['kr'], f"{c['kr']} 오늘운세", f"{c['kr']} 오늘의운세",
        f"{c['kr']} 띠운세", f"{c['kr']} {today_dot}",
        f"{c['kr']} 재물운", f"{c['kr']} 건강운", f"{c['kr']} 애정운",
        "띠운세 오늘", "오늘의운세", "무료운세", f"운세 {today_dot[:4]}",
        "재물운 상승", "오늘 주의", "띠별운세",
    ] + years_tags
    tag_html = "".join(f'<span class="tag">{t}</span>' for t in kw_list)

    content = f"""{style()}
<div class="wrap">
  <div class="hero" style="background:linear-gradient(135deg,#f59e0b,#d97706)">
    <h1>{c['emoji']} {c['kr']} 오늘의 운세</h1>
    <p>{today_str}</p>
    <div style="margin-top:8px;display:inline-block;background:rgba(0,0,0,0.18);
                padding:3px 12px;border-radius:20px;font-size:12px;font-weight:700">{signal}</div>
  </div>

  <!-- 이미지 저장 카드: 메인 운세 + 출생연도별 통합 -->
  <div id="{card_id}" class="fortune-card" style="background:linear-gradient(135deg,#f59e0b,#92400e)">
    <div class="fc-emoji">{c['emoji']}</div>
    <div class="fc-title">{c['kr']}</div>
    <div class="fc-sub">{today_str}</div>
    <div class="fc-stars">{rating}</div>
    <div class="fc-text">{fortune}</div>
    <div style="margin-top:14px;border-top:1px solid rgba(255,255,255,0.3);padding-top:12px">
      <div style="font-size:11px;font-weight:700;color:rgba(255,255,255,0.7);margin-bottom:8px">📅 출생연도별 오늘 운세</div>
      {year_rows_in_card}
    </div>
    <div class="fc-watermark" style="margin-top:14px">todayhoroscopelaboratory.blogspot.com · {today_str}</div>
  </div>

  {share_buttons(card_id, f"{c['kr']}_운세_{today_dot}")}

  <!-- 대표 이미지 -->
  {post_img("chinese")}

  {score_html}
  {caution_html}
  <div class="card">
    <span class="badge">💡 오늘 실전 체크포인트</span>
    <div style="margin-top:8px">{detail_html}</div>
  </div>
  <div class="card"><span class="badge">🔍 관련 키워드</span><div class="tag-cloud">{tag_html}</div></div>
  <div class="meta"><p>{c['kr']} 출생연도: {c['year']}</p><p>※ 재미로 보는 운세 콘텐츠입니다</p></div>
  {site_link()}
</div>"""
    return title, content, ["띠운세", c['kr'], "운세", "오늘운세"]


def zodiac_weekly_fortune(kr_name):
    """주간 운세 CSV에서 가져오기 — zodiac_weekly_1000.csv"""
    if not zodiac_weekly.empty and 'zodiac' in zodiac_weekly.columns:
        m = zodiac_weekly[zodiac_weekly['zodiac'] == kr_name]
        if not m.empty:
            text = m.sample(1).iloc[0]['fortune']
            return str(text).replace('\n\n', '<br><br>').replace('\n', '<br>')
    return sentence()

def zodiac_monthly_fortune(kr_name):
    """월간 운세 CSV에서 가져오기 — zodiac_monthly_1000.csv"""
    if not zodiac_monthly.empty and 'zodiac' in zodiac_monthly.columns:
        m = zodiac_monthly[zodiac_monthly['zodiac'] == kr_name]
        if not m.empty:
            text = m.sample(1).iloc[0]['fortune']
            return str(text).replace('\n\n', '<br><br>').replace('\n', '<br>')
    return sentence()

def chinese_weekly_fortune(en_name):
    """띠 주간 운세 CSV에서 가져오기 — chinese_weekly_1000.csv"""
    if not chinese_weekly.empty and 'animal_zodiac' in chinese_weekly.columns:
        m = chinese_weekly[chinese_weekly['animal_zodiac'] == en_name]
        if not m.empty:
            return m.sample(1).iloc[0]['fortune']
    return sentence()

def chinese_monthly_fortune(en_name):
    """띠 월간 운세 CSV에서 가져오기 — chinese_monthly_1000.csv"""
    if not chinese_monthly.empty and 'animal_zodiac' in chinese_monthly.columns:
        m = chinese_monthly[chinese_monthly['animal_zodiac'] == en_name]
        if not m.empty:
            return m.sample(1).iloc[0]['fortune']
    return sentence()

def build_zodiac_weekly_post(today_str):
    """별자리별 주간운세 12개 개별 발행 — 매주 월요일"""
    week_range = get_week_range()
    today_date = now_kst().date()
    mon_date   = date.fromordinal(today_date.toordinal() - today_date.weekday())
    month_str  = mon_date.strftime("%Y년 %m월")
    results = []
    for z in ZODIACS:
        fortune = zodiac_weekly_fortune(z['kr'])
        rating  = stars()
        card_id = f"zwfc-{z['en']}"
        total, money, health, love = pick_score(z['kr'])

        # 제목 신호 키워드 (간단히)
        scores = {"총운": total, "금전운": money, "건강운": health, "애정운": love}
        top = max(scores, key=scores.get)
        if scores[top] >= 80:
            signal = f"이번 주 {top} 주목"
        elif min(scores.values()) <= 55:
            signal = "이번 주 주의 필요"
        else:
            signal = "이번 주 흐름 확인"
        # 제목: index.html fetchWeeklyPost() 필수 키워드 고정 포함
        # 검색조건: [별자리명, "YYYY년", "MM월", "주간운세"] ALL 포함 필수
        title = f"{z['kr']} {month_str} 주간운세 {week_range} | {signal}"

        kw_list = [
            z['kr'], f"{z['kr']} 주간운세", f"{z['kr']} 이번주운세",
            "별자리 주간운세", f"{z['kr']} {month_str}", "주간운세", "별자리운세"
        ]
        tag_html = "".join(f'<span class="tag">{t}</span>' for t in kw_list)
        score_html = f'''<div class="card" style="background:#f8f0ff">
  <span class="badge">📊 이번 주 운세 지수</span>
  <div style="margin-top:10px">
    {_zodiac_score_bar("종합운","🌟",total)}
    {_zodiac_score_bar("금전운","💰",money)}
    {_zodiac_score_bar("건강운","💪",health)}
    {_zodiac_score_bar("애정운","❤️",love)}
  </div>
</div>'''

        content_html = f"""{style()}
<div class="wrap">
  <div class="hero">
    <h1>📅 {z['emoji']} {z['kr']} 주간운세</h1>
    <p>{week_range} · {z['date']}</p>
    <div style="margin-top:8px;display:inline-block;background:rgba(255,255,255,0.2);padding:3px 12px;border-radius:20px;font-size:12px">{signal}</div>
  </div>
  <div id="{card_id}" class="fortune-card">
    <div class="fc-emoji">{z['emoji']}</div>
    <div class="fc-title">{z['kr']} 주간운세</div>
    <div class="fc-sub">{week_range} · {z['date']}</div>
    <div class="fc-stars">{rating}</div>
    <div class="fc-text">{fortune}</div>
    <div class="fc-watermark">todayhoroscopelaboratory.blogspot.com · {week_range}</div>
  </div>
  {share_buttons(card_id, f"{z['kr']}_주간운세")}

  <!-- 대표 이미지 -->
  {post_img("weekly")}

  {score_html}
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
        fortune = chinese_monthly_fortune(c['en'])
        rating  = stars()
        card_id = f"cmfc-{c['en']}"
        total, money, health, love = pick_score(c['kr'])

        # 제목 신호 키워드
        scores = {"총운": total, "금전운": money, "건강운": health, "애정운": love}
        top = max(scores, key=scores.get)
        if scores[top] >= 80:
            signal = f"이번 달 {top} 상승"
        elif min(scores.values()) <= 55:
            signal = "이번 달 주의 필요"
        else:
            signal = "이번 달 흐름 확인"
        title = f"{c['kr']} {month_str} 월간운세 | {signal}"

        # 기간별: sentence() 제거 → chinese_monthly_fortune 재사용
        periods = [
            ("상순 (1~10일)", chinese_monthly_fortune(c['en'])),
            ("중순 (11~20일)", chinese_monthly_fortune(c['en'])),
            ("하순 (21~말일)", chinese_monthly_fortune(c['en'])),
        ]
        period_html = "".join(
            f'<div class="week-day"><strong>{p}</strong><br><span style="font-size:13px;color:#555">{s[:80]}{"…" if len(str(s))>80 else ""}</span></div>'
            for p, s in periods
        )

        kw_list = [
            c['kr'], f"{c['kr']} 월간운세", f"{c['kr']} 이달운세",
            "띠별 월간운세", f"{c['kr']} {month_str}", "월간운세", "띠운세"
        ]
        tag_html = "".join(f'<span class="tag">{t}</span>' for t in kw_list)
        score_html = f'''<div class="card" style="background:#fffbeb">
  <span class="badge" style="background:#fef3c7;color:#92400e">📊 이번 달 운세 지수</span>
  <div style="margin-top:10px">
    {_zodiac_score_bar("종합운","🌟",total)}
    {_zodiac_score_bar("금전운","💰",money)}
    {_zodiac_score_bar("건강운","💪",health)}
    {_zodiac_score_bar("애정운","❤️",love)}
  </div>
</div>'''

        content_html = f"""{style()}
<div class="wrap">
  <div class="hero" style="background:linear-gradient(135deg,#f59e0b,#d97706)">
    <h1>🌙 {c['emoji']} {c['kr']} 월간운세</h1>
    <p>{month_str}</p>
    <div style="margin-top:8px;display:inline-block;background:rgba(255,255,255,0.2);padding:3px 12px;border-radius:20px;font-size:12px">{signal}</div>
  </div>
  <div id="{card_id}" class="fortune-card" style="background:linear-gradient(135deg,#f59e0b,#92400e)">
    <div class="fc-emoji">{c['emoji']}</div>
    <div class="fc-title">{c['kr']} 월간운세</div>
    <div class="fc-sub">{month_str}</div>
    <div class="fc-stars">{rating}</div>
    <div class="fc-text">{fortune}</div>
    <div class="fc-watermark">todayhoroscopelaboratory.blogspot.com · {month_str}</div>
  </div>
  {share_buttons(card_id, f"{c['kr']}_월간운세")}

  <!-- 대표 이미지 -->
  {post_img("monthly")}

  {score_html}
  <div class="card">
    <span class="badge">📅 {month_str} 기간별 운세</span>
    <div style="margin-top:8px">{period_html}</div>
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

    # kw를 HTML 생성 전에 먼저 정의
    kw = ["별자리운세", "오늘운세", "별자리", today_str,
          "양자리", "황소자리", "쌍둥이자리", "게자리", "사자자리", "처녀자리",
          "천칭자리", "전갈자리", "사수자리", "염소자리", "물병자리", "물고기자리",
          "12별자리운세", "별자리운세전체", "오늘의별자리", "별자리총정리",
          "오늘운세보기", "무료운세", "운세2026"]
    labels = ["별자리운세통합", "운세SNS", "운세", "별자리운세"]

    cards_html = ""
    for z in ZODIACS:
        fortune = zodiac_fortune(z['kr'])
        # 100~200자 범위로 자르기 (이모지 점수바 없음)
        plain = fortune.replace('<br><br>', ' ').replace('<br>', ' ').strip()
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
    <div style="text-align:center;margin-top:8px;font-size:11px;color:#aaa">✨ todayhoroscopelaboratory.blogspot.com · {today_str}</div>
  </div>
  {share_buttons(card_id, f"별자리운세전체_{today_str}")}
  <div style="background:#eef2ff;border-radius:12px;padding:12px;font-size:12px;color:#666;text-align:center;margin-bottom:16px">
    🔮 각 별자리를 클릭하면 상세 운세를 확인할 수 있어요
  </div>
  <div class="card"><span class="badge">🔍 관련 키워드</span>
    <div class="tag-cloud">{''.join(f'<span class="tag">{k}</span>' for k in kw)}</div>
  </div>
  {site_link()}
  <div class="meta">※ 재미로 보는 운세 콘텐츠 · 매일 업데이트</div>
</div>"""

    return title, content_html, labels


# ─────────────────────────────────────────
# ⑦ 운세SNS — 띠 12개 통합 (간결 카드형)
# ─────────────────────────────────────────
def build_sns_chinese_post(today_str):
    """띠 12개를 한 포스트에 SNS 카드형으로"""
    title = f"🐾 오늘의 띠별 운세 전체 {today_str} — 12띠 한눈에"

    # kw를 HTML 생성 전에 먼저 정의
    kw = ["띠운세", "오늘운세", "띠별운세", today_str,
          "쥐띠", "소띠", "호랑이띠", "토끼띠", "용띠", "뱀띠",
          "말띠", "양띠", "원숭이띠", "닭띠", "개띠", "돼지띠",
          "12띠운세", "띠운세전체", "오늘의띠운세", "띠운세총정리",
          "오늘운세보기", "무료운세", "운세2026"]
    labels = ["띠운세통합", "운세SNS", "운세", "띠운세"]

    cards_html = ""
    for c in CHINESE:
        # 1940년 이상, 2030년 이하 연도만, 최대 4개
        years_filtered = [y for y in c['year'].split(',') if 1940 <= int(y) <= 2030][:4]

        year_rows_html = ""
        for y in years_filtered:
            yr_fortune = chinese_fortune(c['en'])
            plain = str(yr_fortune).strip()
            sentences = plain.split('. ')
            short = ''
            for s in sentences:
                candidate = (short + s + '. ').strip()
                if len(candidate) >= 80:
                    short = candidate
                    break
                short = candidate
            if len(short) > 180:
                short = short[:177] + '…'
            if len(short) < 40:
                short = plain[:120] + ('…' if len(plain) > 120 else '')
            year_rows_html += f"""
<div style="display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid #fde68a">
  <div style="min-width:64px;background:#f59e0b;color:#fff;border-radius:8px;padding:4px 8px;
              text-align:center;font-size:12px;font-weight:700;flex-shrink:0">{y}년생</div>
  <div style="font-size:13px;color:#444;line-height:1.7">{short}</div>
</div>"""

        cards_html += f"""
<div style="background:#fff;border-radius:14px;box-shadow:0 2px 8px rgba(0,0,0,.06);
            border-left:4px solid #f59e0b;padding:14px;margin-bottom:12px">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
    <span style="font-size:28px;line-height:1">{c['emoji']}</span>
    <span style="font-weight:900;font-size:15px;color:#92400e">{c['kr']}</span>
  </div>
  {year_rows_html}
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
    <div style="text-align:center;margin-top:8px;font-size:11px;color:#aaa">🐾 todayhoroscopelaboratory.blogspot.com · {today_str}</div>
  </div>
  {share_buttons(card_id, f"띠별운세전체_{today_str}")}
  <div style="background:#fef3c7;border-radius:12px;padding:12px;font-size:12px;color:#666;text-align:center;margin-bottom:16px">
    🐾 각 띠를 클릭하면 출생연도별 상세 운세를 확인할 수 있어요
  </div>
  <div class="card"><span class="badge">🔍 관련 키워드</span>
    <div class="tag-cloud">{''.join(f'<span class="tag">{k}</span>' for k in kw)}</div>
  </div>
  {site_link()}
  <div class="meta">※ 재미로 보는 운세 콘텐츠 · 매일 업데이트</div>
</div>"""

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
