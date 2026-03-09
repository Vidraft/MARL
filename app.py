"""
MARL — Model-Agnostic Runtime Middleware for LLMs
"""
print("=" * 50)
print("  MARL Starting...")
print("=" * 50)

import os, sys, time, traceback

# ── 경로 설정 ──
APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)
print(f"  APP_DIR: {APP_DIR}")
print(f"  CWD: {os.getcwd()}")
print(f"  Files: {os.listdir(APP_DIR)}")

# ── marl 패키지 확인 ──
pkg_dir = os.path.join(APP_DIR, "marl")
if os.path.isdir(pkg_dir):
    print(f"  marl/: {os.listdir(pkg_dir)}")
else:
    print(f"  ⚠️ marl/ directory NOT FOUND at {pkg_dir}")
    # 현재 디렉토리에서도 확인
    cwd_pkg = os.path.join(os.getcwd(), "marl")
    if os.path.isdir(cwd_pkg):
        print(f"  Found at CWD: {cwd_pkg}")
        sys.path.insert(0, os.getcwd())

# ── 의존성 import ──
try:
    import html as html_mod
    print("  ✅ html")
except Exception as e:
    print(f"  ❌ html: {e}")

try:
    import requests
    print(f"  ✅ requests")
except Exception as e:
    print(f"  ❌ requests: {e}")

try:
    import gradio as gr
    print(f"  ✅ gradio {gr.__version__}")
except Exception as e:
    print(f"  ❌ gradio: {e}")
    sys.exit(1)

# ── marl import ──
try:
    from marl import Marl, MarlConfig, MarlResult
    print("  ✅ marl imported")
    MARL_OK = True
except Exception as e:
    print(f"  ❌ marl import failed: {e}")
    traceback.print_exc()
    MARL_OK = False

# ── index.html 로드 ──
INDEX_HTML = ""
for p in [os.path.join(APP_DIR, "index.html"), "index.html",
          "/app/index.html", os.path.join(os.getcwd(), "index.html")]:
    try:
        with open(p, "r", encoding="utf-8") as f:
            INDEX_HTML = f.read()
            print(f"  ✅ index.html from {p}")
            break
    except:
        continue
if not INDEX_HTML:
    print("  ⚠️ index.html not found, inline fallback")
    INDEX_HTML = """<style>
.gradio-container{max-width:100%!important;width:100%!important;padding:0 24px!important}
header{display:none!important}
</style>
<div style="text-align:center;padding:28px 0 16px">
<h1 style="margin:0;font-size:2.2em;font-weight:800;color:#6366f1">MARL</h1>
<p style="color:#475569;font-size:13px;margin:6px 0">Model-Agnostic Runtime Middleware for LLMs</p>
<p style="color:#94a3b8;font-size:11px">Intelligence Amplification · Hallucination Reduction · Zero-Change Middleware</p>
<div style="display:flex;justify-content:center;gap:4px;margin:12px 0;font-size:9px;font-family:monospace">
<span style="background:rgba(13,148,136,.08);color:#0d9488;padding:4px 10px;border-radius:10px">🔍 S1 Hypothesis</span>
<span style="color:#ccc">→</span>
<span style="background:rgba(99,102,241,.08);color:#6366f1;padding:4px 10px;border-radius:10px">⚡ S2 Solver</span>
<span style="color:#ccc">→</span>
<span style="background:rgba(217,119,6,.08);color:#d97706;padding:4px 10px;border-radius:10px">🛡 S3 Auditor</span>
<span style="color:#ccc">→</span>
<span style="background:rgba(225,29,72,.08);color:#e11d48;padding:4px 10px;border-radius:10px">🎯 S4 Verifier</span>
<span style="color:#ccc">→</span>
<span style="background:rgba(139,92,246,.08);color:#8b5cf6;padding:4px 10px;border-radius:10px">🧠 S5 Refiner</span>
</div>
</div>"""

print("=" * 50)

# ════════════════════════════════════════════════════════════════
# Pipeline / Model config
# ════════════════════════════════════════════════════════════════

import re
import random

STAGES = {
    "S1_Hypothesis":  {"label":"S1 · Hypothesis Generator","tag":"Divergent Search","icon":"🔍","color":"#0d9488"},
    "S2_Solver":      {"label":"S2 · Primary Solver","tag":"Forward Pass","icon":"⚡","color":"#6366f1"},
    "S3_Auditor":     {"label":"S3 · Consistency Auditor","tag":"Validation Gate","icon":"🛡️","color":"#d97706"},
    "S4_Verifier":    {"label":"S4 · Adversarial Verifier","tag":"Error Detection","icon":"🎯","color":"#e11d48"},
    "S5_Refiner":     {"label":"S5 · Metacognitive Refiner","tag":"Self-Correction","icon":"🧠","color":"#8b5cf6"},
}
STAGE_ORDER = ["S1_Hypothesis","S2_Solver","S3_Auditor","S4_Verifier","S5_Refiner"]

# ════════════════════════════════════════════════════════════════
# Showcase Examples — displayed during pipeline wait
# ════════════════════════════════════════════════════════════════

SHOWCASE = [
    {"cat":"🎯 함정 질문","q":"0.9999...는 1보다 작은가?",
     "raw":"1에 한없이 가깝지만 1보다 작습니다.","tag":"S1 함정 탐지 → S4 오류 확정",
     "marl":"수학적으로 0.999... = 1 (등비급수·대수적 증명 2가지 제시)"},
    {"cat":"🎯 함정 질문","q":"만리장성은 우주에서 보이는가?",
     "raw":"우주에서 맨눈으로 볼 수 있는 유일한 인공 구조물입니다.",
     "tag":"S4 'NASA 공식 부인' 탐지",
     "marl":"폭 5~8m 장성은 저궤도에서도 맨눈 식별 불가. 영국 풍자화 기원의 도시 전설"},
    {"cat":"🎯 함정 질문","q":"나폴레옹은 키가 작았는가?",
     "raw":"키가 약 157cm로 매우 작았습니다.",
     "tag":"S4 '프랑스 인치 vs 영국 인치 혼동' 탐지",
     "marl":"실제 약 169cm로 당시 프랑스 남성 평균(165cm)보다 큰 편. 영국 프로파간다의 산물"},
    {"cat":"🔬 정밀도 질문","q":"물은 100°C에서 끓는가?",
     "raw":"네, 물은 100°C에서 끓습니다.",
     "tag":"S3 '기압 조건 미명시' 감지",
     "marl":"1기압 기준 100°C. 에베레스트 정상에서는 약 70°C에서 끓음"},
    {"cat":"💀 과신 질문","q":"비타민C가 감기 예방에 효과적인가?",
     "raw":"면역력 강화로 감기 예방에 효과적입니다. (85%)",
     "tag":"S4 'Cochrane 메타분석과 불일치' 탐지",
     "marl":"일반인 예방 효과 미미(8%↓), 고강도 운동 집단에서만 유의미(50%↓)"},
    {"cat":"💀 과신 질문","q":"양자 컴퓨팅이 모든 암호화를 무력화하는가?",
     "raw":"양자 컴퓨터 실용화 시 모든 암호화가 깨집니다.",
     "tag":"S4 '대칭키 vs 비대칭키 구분 누락' 탐지",
     "marl":"RSA·ECC는 취약하나 AES-256은 안전. NIST 양자내성암호 표준 이미 발표"},
    {"cat":"💀 난해한 질문","q":"GPT-5가 AGI인가?",
     "raw":"대부분의 벤치마크에서 인간을 능가하므로 AGI에 근접했습니다.",
     "tag":"S1 '벤치마크 ≠ 범용 지능' 함정 포착",
     "marl":"자기교정 능력(ER=0.302)은 여전히 낮음. '많이 아는 것'과 '모르는 것을 아는 것'은 다른 차원"},
    {"cat":"🧠 창발성 질문","q":"페이커 IP 활용 지원사업 신청서를 작성해줘",
     "raw":"T1과 협업하여 '페이커 에디션' 제품을 기획하면 됩니다.",
     "tag":"S4 'IP 미확보 시 과제 중단 리스크' 탐지",
     "marl":"Plan A(라이선스) + Plan C(대체 디자인) 병행, 유통사 LOI·수요조사 증빙 첨부 전략"},
    {"cat":"🧠 창발성 질문","q":"TAM·SAM·SOM을 작성해줘",
     "raw":"TAM: $500B, SAM: $10B, SOM: $1M (출처 없음)",
     "tag":"S4 'TAM→SAM→SOM 논리적 연결 단절' 탐지",
     "marl":"IDC 보고서 인용 + 세그먼트×ARPU 상향식 산출로 심사위원 검증 가능하게 재구성"},
    {"cat":"🧠 창발성 질문","q":"Python에서 가장 빠른 정렬은?",
     "raw":"퀵소트가 O(n log n)으로 가장 빠릅니다.",
     "tag":"S3 'Python 내장 구현과 괴리' 감지",
     "marl":"sorted()는 TimSort(하이브리드) 사용, 실측에서 순수 QuickSort보다 빠름"},
    {"cat":"🔬 정밀도 질문","q":"에펠탑의 높이는?",
     "raw":"에펠탑의 높이는 324m입니다.",
     "tag":"S4 '안테나 포함/미포함 구분 누락' 탐지",
     "marl":"구조물 300m + 방송 안테나 24m = 총 324m. 맥락에 따라 구분 명시"},
    {"cat":"🔬 정밀도 질문","q":"지구-태양 거리는 빛으로 몇 분?",
     "raw":"약 8분입니다.",
     "tag":"S3 '타원궤도 변동 범위 누락' 감지",
     "marl":"평균 8분 20초. 근일점 8분 10초 ~ 원일점 8분 27초 변동"},
]

MODELS = {
    "Groq": {"env":"GROQ_API_KEY","default":"openai/gpt-oss-120b",
        "list":["openai/gpt-oss-120b","meta-llama/llama-4-scout-17b-16e-instruct",
                "deepseek-r1-distill-llama-70b","llama-3.3-70b-versatile","qwen-qwq-32b"]},
    "OpenAI": {"env":"OPENAI_API_KEY","default":"gpt-5.2",
        "list":["gpt-5.2","gpt-5.2-chat-latest","gpt-5.4","gpt-5.4-pro","gpt-5.2-pro",
                "gpt-5.2-codex","gpt-5","gpt-5-mini","gpt-4o","gpt-4o-mini","gpt-oss-120b"]},
    "Anthropic": {"env":"ANTHROPIC_API_KEY","default":"claude-sonnet-4-6",
        "list":["claude-opus-4-6","claude-sonnet-4-6","claude-haiku-4-5-20251001"]},
    "Google Gemini": {"env":"GOOGLE_API_KEY","default":"gemini-3.1-pro-preview",
        "list":["gemini-3.1-pro-preview","gemini-3-flash","gemini-2.5-flash","gemini-2.5-pro"]},
    "DeepSeek": {"env":"DEEPSEEK_API_KEY","default":"deepseek-chat",
        "list":["deepseek-chat","deepseek-reasoner"]},
    "xAI (Grok)": {"env":"XAI_API_KEY","default":"grok-4",
        "list":["grok-4","grok-4-fast-reasoning","grok-4-1-fast-reasoning","grok-3-beta"]},
    "Friendli": {"env":"FRIENDLI_TOKEN","default":"deppfs281rgffnk","list":["deppfs281rgffnk"]},
    "Ollama (Local)": {"env":"","default":"llama3.1",
        "list":["llama3.1","llama3.1:70b","qwen3.5:32b","deepseek-r1:8b","phi4:14b"]},
    "Custom (OpenAI-compatible)": {"env":"","default":"custom","list":["custom"]},
}
BACKEND_LIST = list(MODELS.keys())

# ════════════════════════════════════════════════════════════════
# MD → HTML
# ════════════════════════════════════════════════════════════════

def _esc(t):
    return html_mod.escape(str(t)) if t else ""

def _hex_rgb(h):
    try: return f"{int(h[1:3],16)},{int(h[3:5],16)},{int(h[5:7],16)}"
    except: return "99,102,241"

def _inline_fmt(text):
    t = text
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
    t = re.sub(r'(\d{1,3})%', r'<span style="font-family:monospace;font-weight:600;color:#6366f1">\1%</span>', t)
    return t

def _md2html(text):
    if not text: return ""
    t = text
    code_blocks = {}
    def _save_code(m):
        k = f"__CODE_{len(code_blocks)}__"
        code = html_mod.escape(m.group(2))
        code_blocks[k] = f'<pre style="background:rgba(15,23,42,.04);border:1px solid #e2e5f0;border-radius:8px;padding:12px;overflow-x:auto;font-family:monospace;font-size:11px;line-height:1.6;margin:8px 0"><code>{code}</code></pre>'
        return k
    t = re.sub(r'```(\w*)\n(.*?)```', _save_code, t, flags=re.DOTALL)
    t = re.sub(r'`([^`]+)`', r'<code style="background:rgba(99,102,241,.08);padding:1px 5px;border-radius:4px;font-family:monospace;font-size:11px">\1</code>', t)

    lines = t.split('\n')
    result = []
    in_list = False
    for line in lines:
        s = line.strip()
        if s in code_blocks:
            if in_list: result.append('</ul>'); in_list = False
            result.append(code_blocks[s]); continue
        hm = re.match(r'^(#{1,4})\s+(.+)$', s)
        if hm:
            if in_list: result.append('</ul>'); in_list = False
            lvl = len(hm.group(1))
            sz = {1:'18px',2:'15px',3:'13px',4:'12px'}[lvl]
            result.append(f'<div style="font-size:{sz};font-weight:700;color:#1e293b;margin:14px 0 6px">{_inline_fmt(html_mod.escape(hm.group(2)))}</div>'); continue
        if re.match(r'^[-*_]{3,}\s*$', s):
            if in_list: result.append('</ul>'); in_list = False
            result.append('<hr style="border:none;border-top:1px solid #e2e5f0;margin:12px 0">'); continue
        lm = re.match(r'^[-*+]\s+(.+)$', s)
        if lm:
            if not in_list: result.append('<ul style="margin:6px 0;padding-left:20px">'); in_list = True
            result.append(f'<li style="margin:3px 0;line-height:1.7">{_inline_fmt(html_mod.escape(lm.group(1)))}</li>'); continue
        nm = re.match(r'^(\d+)[.)]\s+(.+)$', s)
        if nm:
            if in_list: result.append('</ul>'); in_list = False
            result.append(f'<div style="margin:3px 0;padding-left:8px;line-height:1.7"><span style="color:#6366f1;font-weight:600;font-family:monospace;font-size:11px">{nm.group(1)}.</span> {_inline_fmt(html_mod.escape(nm.group(2)))}</div>'); continue
        if in_list: result.append('</ul>'); in_list = False
        if not s: result.append('<div style="height:6px"></div>'); continue
        tm = re.match(r'^\[([A-Z_-]+(?:-\d+)?)\]\s*(.*)', s)
        if tm:
            tag = tm.group(1); rest = _inline_fmt(html_mod.escape(tm.group(2)))
            tc = '#6366f1'
            for px, cl in {'BACKTRACK':'#d97706','FIX':'#e11d48','APPLIED':'#16a34a','TRAP':'#e11d48','HALLUCINATION':'#e11d48','NO-FIXES':'#16a34a'}.items():
                if tag.startswith(px): tc = cl; break
            result.append(f'<div style="margin:6px 0;padding:6px 10px;background:rgba({_hex_rgb(tc)},.06);border-left:3px solid {tc};border-radius:0 6px 6px 0;font-size:12px;line-height:1.7"><span style="font-family:monospace;font-weight:700;color:{tc};font-size:11px">[{html_mod.escape(tag)}]</span> {rest}</div>'); continue
        result.append(f'<p style="margin:4px 0;line-height:1.8">{_inline_fmt(html_mod.escape(s))}</p>')
    if in_list: result.append('</ul>')
    return '\n'.join(result)

# ════════════════════════════════════════════════════════════════
# Answer Cleaner — strip system tags, confidence %, metadata
# ════════════════════════════════════════════════════════════════

def _clean_answer(text):
    """Strip reasoning artifacts from final answer for end-user display."""
    if not text:
        return ""
    t = text

    # Remove "--- Corrections ---" section and everything after
    t = re.split(r'\n-{2,}\s*Corrections\s*-{2,}', t, maxsplit=1)[0]

    lines = t.split('\n')
    clean = []
    for line in lines:
        s = line.strip()
        # Skip system tags: [FIX-n], [TRAP-CHECK], [HALLUCINATION], [APPLIED-n], [BACKTRACK-n], [NO-FIXES-NEEDED]
        if re.match(r'^\[(?:FIX-\d+|TRAP-CHECK|HALLUCINATION|APPLIED-\d+|BACKTRACK-\d+|NO-FIXES-NEEDED)\]', s):
            continue
        # Skip stage labels: "S1 · Hypothesis Generator", "S2 · Primary Solver" etc.
        if re.match(r'^S[1-5]\s*[·\-]', s):
            continue
        # Strip inline confidence: "(confidence: 85%)", "(90% confidence)", "Confidence: 85%"
        line = re.sub(r'\(?\s*[Cc]onfidence[:\s]*\d{1,3}%\s*\)?', '', line)
        line = re.sub(r'\(?\s*\d{1,3}%\s*confidence\s*\)?', '', line)
        # Strip standalone confidence lines: "Confidence: 85%" or "**Confidence:** 90%"
        if re.match(r'^\s*\*{0,2}[Cc]onfidence\*{0,2}\s*[:]\s*\d{1,3}%', line):
            continue
        # Strip "## Confidence Adjustments" section headers
        if re.match(r'^#{1,4}\s*(?:Confidence|Top-\d+\s+Uncertaint)', s):
            continue
        # Strip "★ MANDATORY SELF-CHECK" and similar framework directives
        if re.match(r'^★', s):
            continue
        clean.append(line)

    # Clean up excess blank lines
    result = '\n'.join(clean)
    result = re.sub(r'\n{3,}', '\n\n', result).strip()
    return result


# ════════════════════════════════════════════════════════════════
# HTML Renderers
# ════════════════════════════════════════════════════════════════

def _stage_html(name, content):
    s = STAGES.get(name, {})
    c = s.get("color","#6366f1")
    body = _md2html(content[:3000] if content else "(no output)")
    return f'<div style="border-left:3px solid {c};background:rgba({_hex_rgb(c)},.04);border-radius:0 10px 10px 0;padding:14px 16px;margin:8px 0"><div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span style="font-size:1.1em">{s.get("icon","")}</span><span style="font-family:monospace;font-weight:700;font-size:12px;color:{c}">{s.get("label",name)}</span><span style="font-size:9px;color:#94a3b8;font-family:monospace;background:rgba(0,0,0,.04);padding:2px 8px;border-radius:10px">{s.get("tag","")}</span></div><div style="font-size:12px;line-height:1.7;color:#334155">{body}</div></div>'

def _result_html(content, is_marl=False):
    """Render Raw LLM result (no cleaning needed)."""
    if not content:
        return '<div style="color:#94a3b8;padding:40px;text-align:center;font-size:12px">Waiting...</div>'
    badge = "MARL-Enhanced" if is_marl else "Raw LLM"
    bc = "#6366f1" if is_marl else "#64748b"
    bg = "rgba(99,102,241,.06)" if is_marl else "#f5f6fa"
    body = _md2html(content)
    return f'<div style="padding:16px"><div style="margin-bottom:12px"><span style="font-family:monospace;font-size:9px;font-weight:700;background:{bg};color:{bc};padding:3px 10px;border-radius:10px;text-transform:uppercase;letter-spacing:1px">{badge}</span></div><div style="font-size:13px;line-height:1.8;color:#1e293b;word-break:break-word">{body}</div></div>'

def _marl_result_html(raw_answer, trace_dict):
    """Render MARL result: clean answer + embedded reasoning toggle with S1~S5 trace."""
    clean = _clean_answer(raw_answer)
    if not clean:
        return '<div style="color:#94a3b8;padding:40px;text-align:center;font-size:12px">Waiting...</div>'

    body = _md2html(clean)

    # Build S1~S5 trace HTML for toggle
    trace_parts = ""
    if trace_dict:
        trace_parts = ''.join(_stage_html(n, trace_dict[n]) for n in STAGE_ORDER if n in trace_dict)

    toggle_html = ""
    if trace_parts:
        toggle_html = f'''
<details style="margin-top:16px;border:1px solid #e2e5f0;border-radius:10px;overflow:hidden">
  <summary style="cursor:pointer;padding:10px 16px;background:rgba(99,102,241,.03);font-family:monospace;font-size:11px;font-weight:600;color:#6366f1;user-select:none;display:flex;align-items:center;gap:6px">
    🔍 View Reasoning Process — S1→S2→S3→S4→S5
  </summary>
  <div style="padding:12px 16px;border-top:1px solid #e2e5f0;background:#fafbfc">
    {trace_parts}
  </div>
</details>'''

    return f'''<div style="padding:16px">
  <div style="margin-bottom:12px">
    <span style="font-family:monospace;font-size:9px;font-weight:700;background:rgba(99,102,241,.06);color:#6366f1;padding:3px 10px;border-radius:10px;text-transform:uppercase;letter-spacing:1px">MARL-Enhanced</span>
  </div>
  <div style="font-size:13px;line-height:1.8;color:#1e293b;word-break:break-word">{body}</div>
  {toggle_html}
</div>'''

def _trace_html(trace_dict):
    if not trace_dict:
        return '<div style="color:#94a3b8;padding:30px;text-align:center">Run MARL to see pipeline trace</div>'
    return ''.join(_stage_html(n, trace_dict[n]) for n in STAGE_ORDER if n in trace_dict)

def _pipeline_anim(phase="marl", msg=""):
    """Animated pipeline + rotating showcase Before/After cards."""
    stages = [
        ("S1", "가설 탐색", "🔍", "#0d9488"),
        ("S2", "핵심 해결", "⚡", "#6366f1"),
        ("S3", "정합성 감사", "🛡️", "#d97706"),
        ("S4", "적대적 검증", "🎯", "#e11d48"),
        ("S5", "메타인지 통합", "🧠", "#8b5cf6"),
    ]
    if phase == "raw":
        return f'''<div style="padding:30px 20px;text-align:center">
<div style="font-size:13px;color:#475569;margin-bottom:16px">{_esc(msg) if msg else "Raw LLM 응답 생성 중..."}</div>
<div style="display:inline-block;width:200px;height:4px;background:#e2e5f0;border-radius:4px;overflow:hidden">
<div style="width:40%;height:100%;background:linear-gradient(90deg,#6366f1,#0d9488);border-radius:4px;animation:rawPulse 1.5s ease-in-out infinite"></div>
</div>
<style>@keyframes rawPulse{{0%,100%{{width:30%}}50%{{width:70%}}}}</style>
</div>'''

    # ── Stage pills with sequential glow ──
    pills = []
    arrows = []
    ns = len(stages)
    for i, (sid, name, icon, color) in enumerate(stages):
        delay = i * 1.8
        rgb = _hex_rgb(color)
        pills.append(f'''<div style="display:flex;flex-direction:column;align-items:center;gap:4px;animation:stageGlow {ns*1.8}s ease-in-out infinite;animation-delay:{delay}s;opacity:0.35">
  <div style="width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px;background:rgba({rgb},.1);border:2px solid rgba({rgb},.2)">{icon}</div>
  <div style="font-family:monospace;font-size:10px;font-weight:700;color:{color}">{sid}</div>
  <div style="font-size:9px;color:#94a3b8;white-space:nowrap">{name}</div>
</div>''')
        if i < ns - 1:
            arrows.append(f'<div style="color:#cbd5e1;font-size:14px;margin-top:-16px;animation:arrowPulse {ns*1.8}s ease-in-out infinite;animation-delay:{delay+0.9}s;opacity:0.3">→</div>')

    interleaved = []
    for i, pill in enumerate(pills):
        interleaved.append(pill)
        if i < len(arrows):
            interleaved.append(arrows[i])
    stage_html = "\n".join(interleaved)
    sub = _esc(msg) if msg else "AI가 생각하고, 의심하고, 고쳐서 다시 쓰는 중..."

    # ── Showcase cards — CSS-only rotation ──
    shuffled = list(SHOWCASE)
    random.shuffle(shuffled)
    nc = min(len(shuffled), 8)  # show up to 8 cards
    dur_each = 5  # seconds per card
    total_dur = nc * dur_each

    cards_html = ""
    card_kf = ""
    for idx in range(nc):
        ex = shuffled[idx]
        pct_start = (idx / nc) * 100
        pct_show  = pct_start + 2
        pct_hide  = ((idx + 1) / nc) * 100 - 2
        pct_end   = ((idx + 1) / nc) * 100

        cards_html += f'''<div class="sc-card sc-card-{idx}" style="position:absolute;inset:0;opacity:0;animation:sc{idx} {total_dur}s ease-in-out infinite">
  <div style="display:flex;align-items:center;gap:6px;margin-bottom:10px">
    <span style="font-size:9px;font-weight:700;color:#6366f1;background:rgba(99,102,241,.08);padding:2px 8px;border-radius:6px;font-family:monospace">{_esc(ex['cat'])}</span>
  </div>
  <div style="font-size:13px;font-weight:700;color:#1e293b;margin-bottom:12px;line-height:1.4">"{_esc(ex['q'])}"</div>
  <div style="display:flex;gap:10px">
    <div style="flex:1;padding:10px 12px;background:#fef2f2;border:1px solid #fecaca;border-radius:8px">
      <div style="font-size:9px;font-weight:700;color:#e11d48;margin-bottom:4px;font-family:monospace">❌ Non-MARL</div>
      <div style="font-size:11px;color:#7f1d1d;line-height:1.5">{_esc(ex['raw'])}</div>
    </div>
    <div style="flex:1;padding:10px 12px;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px">
      <div style="font-size:9px;font-weight:700;color:#16a34a;margin-bottom:4px;font-family:monospace">✅ MARL</div>
      <div style="font-size:11px;color:#14532d;line-height:1.5">{_esc(ex['marl'])}</div>
    </div>
  </div>
  <div style="margin-top:8px;font-size:9px;color:#6366f1;font-family:monospace;font-weight:600">🔍 {_esc(ex['tag'])}</div>
</div>\n'''

        card_kf += f"@keyframes sc{idx}{{" \
                   f"0%,{pct_start:.1f}%{{opacity:0;transform:translateY(8px)}}" \
                   f"{pct_show:.1f}%{{opacity:1;transform:translateY(0)}}" \
                   f"{pct_hide:.1f}%{{opacity:1;transform:translateY(0)}}" \
                   f"{pct_end:.1f}%,100%{{opacity:0;transform:translateY(-8px)}}}}\n"

    return f'''<div style="padding:24px 16px;text-align:center">
<div style="display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:nowrap;margin-bottom:16px">
{stage_html}
</div>
<div style="font-size:12px;color:#475569;margin-bottom:6px">{sub}</div>
<div style="display:flex;gap:4px;justify-content:center;margin-bottom:20px">
  <div style="width:6px;height:6px;border-radius:50%;background:#6366f1;animation:dotBounce 1.4s ease-in-out infinite"></div>
  <div style="width:6px;height:6px;border-radius:50%;background:#0d9488;animation:dotBounce 1.4s ease-in-out .2s infinite"></div>
  <div style="width:6px;height:6px;border-radius:50%;background:#8b5cf6;animation:dotBounce 1.4s ease-in-out .4s infinite"></div>
</div>
<div style="text-align:left;max-width:560px;margin:0 auto">
  <div style="font-size:9px;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;font-family:monospace">💡 MARL이 실제로 잡아낸 사례</div>
  <div style="position:relative;min-height:180px">
    {cards_html}
  </div>
</div>
<style>
@keyframes stageGlow{{
  0%,100%{{opacity:0.3;transform:scale(1)}}
  {100/ns:.0f}%{{opacity:1;transform:scale(1.1)}}
  {200/ns:.0f}%{{opacity:0.3;transform:scale(1)}}
}}
@keyframes arrowPulse{{
  0%,100%{{opacity:0.2;color:#cbd5e1}}
  {100/ns:.0f}%{{opacity:1;color:#6366f1}}
  {200/ns:.0f}%{{opacity:0.2;color:#cbd5e1}}
}}
@keyframes dotBounce{{
  0%,100%{{transform:translateY(0)}}
  50%{{transform:translateY(-6px)}}
}}
{card_kf}
</style>
</div>'''

def _status(state, msg, model, color):
    dot = "●" if state == "Running" else "✓"
    return f'<div style="display:flex;align-items:center;gap:10px;padding:10px 16px;background:rgba({_hex_rgb(color)},.06);border:1px solid rgba({_hex_rgb(color)},.15);border-radius:10px;font-family:monospace;font-size:11px"><span style="color:{color};font-weight:700">{dot} {state}</span><span style="color:#475569">{_esc(model)}</span><span style="color:#94a3b8">·</span><span style="color:#64748b">{_esc(msg)}</span></div>'

# ════════════════════════════════════════════════════════════════
# Build Marl
# ════════════════════════════════════════════════════════════════

def _on_backend(backend):
    reg = MODELS.get(backend, {})
    ml, dv, ek = reg.get("list",[]), reg.get("default",""), reg.get("env","")
    return gr.Dropdown(choices=ml, value=dv), gr.Textbox(placeholder=f"ENV: {ek}" if ek else "API Key")

def _build(backend, api_key, model, base_url):
    if not MARL_OK:
        return None, "❌ marl package failed to load. Check Space logs."
    cfg = MarlConfig(include_trace=True, return_final_only=True)
    reg = MODELS.get(backend, {})
    model = model or reg.get("default","")
    ek = reg.get("env","")
    k = api_key or (os.getenv(ek,"") if ek else "")

    try:
        if backend == "Groq":
            if not k: return None, "❌ GROQ_API_KEY required"
            return Marl.from_openai_compatible("https://api.groq.com/openai/v1", k, model, cfg), "✅"
        elif backend == "OpenAI":
            if not k: return None, "❌ OPENAI_API_KEY required"
            return Marl.from_openai(k, model, cfg), "✅"
        elif backend == "Anthropic":
            if not k: return None, "❌ ANTHROPIC_API_KEY required"
            return Marl.from_anthropic(k, model, cfg), "✅"
        elif backend == "Google Gemini":
            k = k or os.getenv("GEMINI_API_KEY","")
            if not k: return None, "❌ GOOGLE_API_KEY required"
            return Marl.from_openai_compatible("https://generativelanguage.googleapis.com/v1beta/openai", k, model, cfg), "✅"
        elif backend == "DeepSeek":
            if not k: return None, "❌ DEEPSEEK_API_KEY required"
            return Marl.from_openai_compatible("https://api.deepseek.com/v1", k, model, cfg), "✅"
        elif backend == "xAI (Grok)":
            if not k: return None, "❌ XAI_API_KEY required"
            return Marl.from_openai_compatible("https://api.x.ai/v1", k, model, cfg), "✅"
        elif backend == "Friendli":
            if not k: return None, "❌ FRIENDLI_TOKEN required"
            return Marl.from_friendli(k, model, cfg), "✅"
        elif backend == "Ollama (Local)":
            return Marl.from_ollama(model, base_url or "http://localhost:11434", cfg), "✅"
        elif backend == "Custom (OpenAI-compatible)":
            if not base_url: return None, "❌ Base URL required"
            return Marl.from_openai_compatible(base_url, api_key or "", model or "default", cfg), "✅"
    except Exception as e:
        return None, f"❌ Build error: {e}"
    return None, "❌ Unsupported"

# ════════════════════════════════════════════════════════════════
# A/B Test (Streaming)
# ════════════════════════════════════════════════════════════════

def run_ab_test(prompt, backend, api_key, model, base_url, budget, mode_sel, etype_sel):
    if not prompt.strip():
        yield ('<div style="color:#e11d48;padding:12px">❌ Enter a prompt</div>',"","","")
        return
    ml, st = _build(backend, api_key, model, base_url)
    if not ml:
        yield (f'<div style="color:#e11d48;padding:12px">{_esc(st)}</div>',"","","")
        return
    ml.config.budget_scale = float(budget)
    # Set mode
    _MODE_MAP = {"🔬 Insight": "insight", "🎨 Emergence": "emergence"}
    _ETYPE_MAP = {"🔧 Invent": "invent", "✨ Create": "create", "🍳 Recipe": "recipe", "💊 Pharma": "pharma", "🧬 Genomics": "genomics", "🧪 Chemistry": "chemistry", "🌍 Ecology": "ecology", "⚖️ Law": "law", "📄 Document": "document"}
    ml.config.mode = _MODE_MAP.get(mode_sel, "insight")
    ml.config.emergence_type = _ETYPE_MAP.get(etype_sel, "invent")
    mode_label = f"{mode_sel}" + (f" · {etype_sel}" if "Emergence" in mode_sel else "")

    # Show both animations simultaneously
    yield (_status("Running",f"{mode_label} · Raw LLM + MARL 동시 실행 중...",model,"#6366f1"),
           _pipeline_anim("raw", "Raw LLM 응답 생성 중..."),
           _pipeline_anim("marl", "MARL 파이프라인 실행 중..."),
           "")

    # ── Parallel execution ──
    from concurrent.futures import ThreadPoolExecutor
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=2) as pool:
        future_raw  = pool.submit(ml.call_fn, prompt, "Answer thoroughly.", 4096, 0.6)
        future_marl = pool.submit(ml.run, prompt)
        raw  = future_raw.result()
        r    = future_marl.result()
    t_total = time.time() - t0

    yield (_status("Complete",f"병렬 완료 {t_total:.1f}s · {len(r.fixes)} corrections",model,"#16a34a"),
           _result_html(raw,False), _marl_result_html(r.answer, r.trace), _trace_html(r.trace))

def run_marl_only(prompt, backend, api_key, model, base_url, budget, mode_sel, etype_sel):
    if not prompt.strip():
        yield ('<div style="color:#e11d48;padding:12px">❌ Enter a prompt</div>',"","","")
        return
    ml, st = _build(backend, api_key, model, base_url)
    if not ml:
        yield (f'<div style="color:#e11d48;padding:12px">{_esc(st)}</div>',"","","")
        return
    ml.config.budget_scale = float(budget)
    _MODE_MAP = {"🔬 Insight": "insight", "🎨 Emergence": "emergence"}
    _ETYPE_MAP = {"🔧 Invent": "invent", "✨ Create": "create", "🍳 Recipe": "recipe", "💊 Pharma": "pharma", "🧬 Genomics": "genomics", "🧪 Chemistry": "chemistry", "🌍 Ecology": "ecology", "⚖️ Law": "law", "📄 Document": "document"}
    ml.config.mode = _MODE_MAP.get(mode_sel, "insight")
    ml.config.emergence_type = _ETYPE_MAP.get(etype_sel, "invent")
    mode_label = f"{mode_sel}" + (f" · {etype_sel}" if "Emergence" in mode_sel else "")
    yield (_status("Running",f"{mode_label} · MARL pipeline...",model,"#6366f1"),
           "",_pipeline_anim("marl", "MARL 파이프라인 실행 중..."),"")
    t0=time.time(); r=ml.run(prompt); t_marl=time.time()-t0
    yield (_status("Complete",f"MARL {t_marl:.1f}s · {len(r.fixes)} corrections",model,"#16a34a"),
           "", _marl_result_html(r.answer, r.trace), _trace_html(r.trace))

# ════════════════════════════════════════════════════════════════
# Gradio App
# ════════════════════════════════════════════════════════════════

def create_app():
    init_m = MODELS["Groq"]["list"]

    with gr.Blocks(title="MARL — Model-Agnostic Runtime Middleware") as app:
        gr.HTML(INDEX_HTML)

        with gr.Tabs():
          with gr.Tab("⚡ Playground"):
            with gr.Row():
                backend = gr.Dropdown(label="Backend", choices=BACKEND_LIST, value="Groq", scale=2)
                api_key = gr.Textbox(label="API Key", type="password", placeholder="ENV: GROQ_API_KEY",
                                     value=os.getenv("GROQ_API_KEY",""), scale=3)
            with gr.Row():
                model = gr.Dropdown(label="Model", choices=init_m, value="openai/gpt-oss-120b",
                                    allow_custom_value=True, scale=3)
                base_url = gr.Textbox(label="Base URL (Custom/Ollama)",
                                       placeholder="http://localhost:11434", scale=2)
                budget = gr.Slider(0.3, 3.0, value=1.0, step=0.1, label="Budget Scale", scale=1)

            with gr.Row():
                mode = gr.Radio(["🔬 Insight", "🎨 Emergence"],
                               value="🔬 Insight", label="Mode", scale=2)
                etype = gr.Radio(["🔧 Invent", "✨ Create", "🍳 Recipe", "💊 Pharma", "🧬 Genomics", "🧪 Chemistry", "🌍 Ecology", "⚖️ Law", "📄 Document"],
                                value="🔧 Invent", label="Emergence Engine", scale=2, visible=False)

            def _on_mode(m):
                return gr.Radio(visible="Emergence" in m)
            mode.change(fn=_on_mode, inputs=[mode], outputs=[etype])

            backend.change(fn=_on_backend, inputs=[backend], outputs=[model, api_key])

            prompt = gr.Textbox(label="Prompt", placeholder="Enter your question or task...", lines=3)

            EXAMPLES = [
                ("🔬", "If launching an AI startup in 2026, what niche markets could reach profitability within 3 years while avoiding red oceans?",
                 "🔬 Insight", "🔧 Invent"),
                ("🔬", "Compare medical school vs AI engineering for a student choosing a career: income, job stability, social value, and work-life balance by 2040",
                 "🔬 Insight", "🔧 Invent"),
                ("🔧", "Invent a device that allows dementia patients to live safely at home alone. Fuse sensors, AI, and UX — under $50/month",
                 "🎨 Emergence", "🔧 Invent"),
                ("🔧", "Design a building exterior material that self-detects cracks and autonomously self-heals",
                 "🎨 Emergence", "🔧 Invent"),
                ("✨", "Create 10 movie loglines that have never existed before. Include genre, one-line synopsis, and box-office hook for each",
                 "🎨 Emergence", "✨ Create"),
                ("✨", "Turn the Korean emotion of 'Han' into a global brand campaign. 3 CF concepts with viral hooks",
                 "🎨 Emergence", "✨ Create"),
                ("🍳", "Develop a recipe that reproduces 90% of Korean beef bulgogi taste and texture using only vegan ingredients",
                 "🎨 Emergence", "🍳 Recipe"),
                ("🍳", "Create 3 Michelin-level dishes from a single instant ramen pack. Extra ingredients must be available at any convenience store",
                 "🎨 Emergence", "🍳 Recipe"),
                ("📄", "Write a 2026 AI industry trend analysis report: market size, key players, government policy, and outlook",
                 "🎨 Emergence", "📄 Document"),
                ("📄", "Analyze why our company turnover rate hit 30% this year and propose a talent retention strategy for the CEO",
                 "🎨 Emergence", "📄 Document"),
                ("💊", "Propose 5 drug repositioning candidates — like how Viagra was originally a heart drug — by applying existing drug targets to completely different diseases",
                 "🎨 Emergence", "💊 Pharma"),
                ("💊", "Design a novel Alzheimer's drug concept by reversing the immune checkpoint mechanism used in cancer immunotherapy",
                 "🎨 Emergence", "💊 Pharma"),
                ("🧬", "Explore synthetic lethality pairs beyond BRCA-PARP: find gene pairs where simultaneous inhibition selectively kills cancer cells",
                 "🎨 Emergence", "🧬 Genomics"),
                ("🧬", "Analyze how gut microbiome modulation of the MAPK pathway affects neurodegenerative diseases via the gut-brain axis",
                 "🎨 Emergence", "🧬 Genomics"),
                ("🧪", "Design a new material that combines graphene-level strength with rubber-level flexibility. Include structure and manufacturing method",
                 "🎨 Emergence", "🧪 Chemistry"),
                ("🧪", "Design a process to transform spent lithium batteries into next-generation solid-state battery materials",
                 "🎨 Emergence", "🧪 Chemistry"),
                ("🌍", "Design a strategy where a single rooftop greening initiative simultaneously achieves carbon capture, water purification, food production, and mental health benefits",
                 "🎨 Emergence", "🌍 Ecology"),
                ("🌍", "Propose 3 business models that transform invasive species from costly problems into valuable resources",
                 "🎨 Emergence", "🌍 Ecology"),
                ("⚖️", "Compare autonomous vehicle accident liability across EU, US, and Korean jurisdictions and design an optimal hybrid regulatory framework",
                 "🎨 Emergence", "⚖️ Law"),
                ("⚖️", "Should AI-generated content have copyright? Collide common law and civil law logic to propose a new legal doctrine",
                 "🎨 Emergence", "⚖️ Law"),
            ]
            gr.HTML('<div style="font-size:10px;font-weight:700;color:#8b90b0;text-transform:uppercase;letter-spacing:1.5px;font-family:var(--mono);margin:12px 0 6px">💡 EXAMPLES — click to auto-fill prompt & mode</div>')
            with gr.Row():
                ex_btns = []
                for i in range(5):
                    icon, text = EXAMPLES[i][0], EXAMPLES[i][1]
                    ex_btns.append(gr.Button(f"{icon} {text[:42]}...", size="sm", scale=1, min_width=60))
            with gr.Row():
                for i in range(5, 10):
                    icon, text = EXAMPLES[i][0], EXAMPLES[i][1]
                    ex_btns.append(gr.Button(f"{icon} {text[:42]}...", size="sm", scale=1, min_width=60))
            with gr.Row():
                for i in range(10, 15):
                    icon, text = EXAMPLES[i][0], EXAMPLES[i][1]
                    ex_btns.append(gr.Button(f"{icon} {text[:42]}...", size="sm", scale=1, min_width=60))
            with gr.Row():
                for i in range(15, 20):
                    icon, text = EXAMPLES[i][0], EXAMPLES[i][1]
                    ex_btns.append(gr.Button(f"{icon} {text[:42]}...", size="sm", scale=1, min_width=60))

            for i, btn in enumerate(ex_btns):
                _, ex_prompt, ex_mode, ex_etype = EXAMPLES[i]
                is_emergence = "Emergence" in ex_mode
                btn.click(fn=lambda p=ex_prompt, m=ex_mode, e=ex_etype, v=is_emergence: (p, m, gr.Radio(value=e, visible=v)),
                          outputs=[prompt, mode, etype])

            with gr.Row():
                ab_btn = gr.Button("⚡ A/B Test · Raw LLM vs MARL", variant="primary", size="lg", scale=3)
                marl_btn = gr.Button("🧠 MARL Only", variant="secondary", size="lg", scale=2)

            status = gr.HTML()

            gr.HTML('<div style="display:flex;gap:12px;margin:12px 0"><div style="flex:1;text-align:center;font-family:JetBrains Mono,monospace;font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#64748b;padding:10px;background:#f5f6fa;border-radius:10px 10px 0 0;border:1px solid #e2e5f0;border-bottom:2px solid #e2e5f0">🤖 A · Raw LLM</div><div style="flex:1;text-align:center;font-family:JetBrains Mono,monospace;font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#6366f1;padding:10px;background:rgba(99,102,241,.04);border-radius:10px 10px 0 0;border:1px solid rgba(99,102,241,.12);border-bottom:2px solid #6366f1">🧠 B · MARL-Enhanced</div></div>')

            with gr.Row():
                raw_out = gr.HTML()
                marl_out = gr.HTML()

            with gr.Accordion("📊 Pipeline Trace — 5-Stage Agent Outputs", open=False):
                trace_out = gr.HTML()

            ins = [prompt, backend, api_key, model, base_url, budget, mode, etype]
            outs = [status, raw_out, marl_out, trace_out]
            ab_btn.click(fn=run_ab_test, inputs=ins, outputs=outs)
            marl_btn.click(fn=run_marl_only, inputs=ins, outputs=outs)

          with gr.Tab("📦 Integration Guide"):
            gr.HTML('''<div style="font-family:Sora,sans-serif;max-width:920px;margin:0 auto;padding:20px;color:#0f172a;line-height:1.7">

<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:24px">
<div style="background:var(--surface,#fff);border:1px solid #e2e5f0;border-radius:16px;padding:20px;box-shadow:0 1px 3px rgba(15,23,42,.04)">
<div style="font-size:8px;font-family:JetBrains Mono,monospace;color:#6366f1;text-transform:uppercase;letter-spacing:2px;font-weight:700;margin-bottom:6px">Quick Start</div>
<pre style="margin:0;font-family:JetBrains Mono,monospace;font-size:14px;color:#6366f1;background:#f5f6fa;padding:10px;border-radius:10px;border:1px solid #e2e5f0"><code>pip install marl-middleware</code></pre>
<div style="margin-top:6px;font-size:9px;color:#94a3b8">Linux x86_64 / Python 3.12 · Other OS → Docker</div>
</div>
<div style="background:var(--surface,#fff);border:1px solid #e2e5f0;border-radius:16px;padding:20px;box-shadow:0 1px 3px rgba(15,23,42,.04)">
<div style="font-size:8px;font-family:JetBrains Mono,monospace;color:#0d9488;text-transform:uppercase;letter-spacing:2px;font-weight:700;margin-bottom:6px">Docker (All Platforms)</div>
<pre style="margin:0;font-family:JetBrains Mono,monospace;font-size:14px;color:#0d9488;background:#f5f6fa;padding:10px;border-radius:10px;border:1px solid #e2e5f0"><code>docker run -p 8080:8080 vidraft/marl</code></pre>
<div style="margin-top:6px;font-size:9px;color:#94a3b8">Mac · Windows · Linux — works everywhere</div>
</div>
</div>

<div style="background:var(--surface,#fff);border:1px solid #e2e5f0;border-radius:16px;padding:20px;margin-bottom:16px;box-shadow:0 1px 3px rgba(15,23,42,.04)">
<div style="font-size:10px;font-family:JetBrains Mono,monospace;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px">⚡ 1-LINE INTEGRATION</div>
<p style="color:#475569;font-size:11px;margin-bottom:10px">Add <b>one line</b> to any OpenAI-compatible app:</p>
<pre style="background:#f5f6fa;padding:14px;border-radius:10px;font-family:JetBrains Mono,monospace;font-size:11px;line-height:1.8;border:1px solid #e2e5f0;overflow-x:auto"><code><span style="color:#94a3b8"># Before</span>
client = OpenAI(api_key=<span style="color:#d97706">"sk-..."</span>)

<span style="color:#94a3b8"># After — just add base_url</span>
client = OpenAI(api_key=<span style="color:#d97706">"sk-..."</span>, <span style="color:#e11d48">base_url=</span><span style="color:#d97706">"http://localhost:8080/v1"</span>)</code></pre>
</div>

<div style="background:var(--surface,#fff);border:1px solid #e2e5f0;border-radius:16px;padding:20px;margin-bottom:16px;box-shadow:0 1px 3px rgba(15,23,42,.04)">
<div style="font-size:10px;font-family:JetBrains Mono,monospace;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px">🎨 9 EMERGENCE MODES</div>
<p style="color:#475569;font-size:11px;margin-bottom:10px">Append <code style="background:rgba(99,102,241,.06);padding:2px 6px;border-radius:4px;color:#6366f1;font-family:JetBrains Mono,monospace;font-size:10px">::mode</code> to any model name:</p>
<div style="overflow-x:auto">
<table style="width:100%;border-collapse:separate;border-spacing:0;font-size:11px;border-radius:10px;overflow:hidden;border:1px solid #e2e5f0">
<tr style="background:#f5f6fa"><th style="text-align:left;padding:8px 10px;font-family:JetBrains Mono,monospace;font-size:8px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px">model</th><th style="text-align:left;padding:8px 10px;font-family:JetBrains Mono,monospace;font-size:8px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px">Mode</th><th style="text-align:left;padding:8px 10px;font-family:JetBrains Mono,monospace;font-size:8px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px">Seeds</th></tr>
<tr><td style="padding:7px 10px;border-top:1px solid #e2e5f0"><code style="color:#6366f1;font-weight:600;font-family:JetBrains Mono,monospace;font-size:10px">gpt-5.2</code></td><td style="padding:7px 10px;border-top:1px solid #e2e5f0">🔬 Insight (default)</td><td style="padding:7px 10px;border-top:1px solid #e2e5f0;color:#94a3b8;font-size:10px">Fact-check · Strategy</td></tr>
<tr style="background:#fafbfe"><td style="padding:7px 10px;border-top:1px solid #e2e5f0"><code style="color:#6366f1;font-weight:600;font-family:JetBrains Mono,monospace;font-size:10px">::invent</code></td><td style="padding:7px 10px;border-top:1px solid #e2e5f0">🔧 Invent</td><td style="padding:7px 10px;border-top:1px solid #e2e5f0;color:#94a3b8;font-size:10px">4,318 tech items</td></tr>
<tr><td style="padding:7px 10px;border-top:1px solid #e2e5f0"><code style="color:#6366f1;font-weight:600;font-family:JetBrains Mono,monospace;font-size:10px">::create</code></td><td style="padding:7px 10px;border-top:1px solid #e2e5f0">✨ Create</td><td style="padding:7px 10px;border-top:1px solid #e2e5f0;color:#94a3b8;font-size:10px">493 seeds (11 categories)</td></tr>
<tr style="background:#fafbfe"><td style="padding:7px 10px;border-top:1px solid #e2e5f0"><code style="color:#6366f1;font-weight:600;font-family:JetBrains Mono,monospace;font-size:10px">::recipe</code></td><td style="padding:7px 10px;border-top:1px solid #e2e5f0">🍳 Recipe</td><td style="padding:7px 10px;border-top:1px solid #e2e5f0;color:#94a3b8;font-size:10px">131 methods · textures</td></tr>
<tr><td style="padding:7px 10px;border-top:1px solid #e2e5f0"><code style="color:#6366f1;font-weight:600;font-family:JetBrains Mono,monospace;font-size:10px">::pharma</code></td><td style="padding:7px 10px;border-top:1px solid #e2e5f0">💊 Pharma</td><td style="padding:7px 10px;border-top:1px solid #e2e5f0;color:#94a3b8;font-size:10px">172 targets · mechanisms</td></tr>
<tr style="background:#fafbfe"><td style="padding:7px 10px;border-top:1px solid #e2e5f0"><code style="color:#6366f1;font-weight:600;font-family:JetBrains Mono,monospace;font-size:10px">::genomics</code></td><td style="padding:7px 10px;border-top:1px solid #e2e5f0">🧬 Genomics</td><td style="padding:7px 10px;border-top:1px solid #e2e5f0;color:#94a3b8;font-size:10px">104 genes · pathways</td></tr>
<tr><td style="padding:7px 10px;border-top:1px solid #e2e5f0"><code style="color:#6366f1;font-weight:600;font-family:JetBrains Mono,monospace;font-size:10px">::chemistry</code></td><td style="padding:7px 10px;border-top:1px solid #e2e5f0">🧪 Chemistry</td><td style="padding:7px 10px;border-top:1px solid #e2e5f0;color:#94a3b8;font-size:10px">135 elements · properties</td></tr>
<tr style="background:#fafbfe"><td style="padding:7px 10px;border-top:1px solid #e2e5f0"><code style="color:#6366f1;font-weight:600;font-family:JetBrains Mono,monospace;font-size:10px">::ecology</code></td><td style="padding:7px 10px;border-top:1px solid #e2e5f0">🌍 Ecology</td><td style="padding:7px 10px;border-top:1px solid #e2e5f0;color:#94a3b8;font-size:10px">105 species · ecosystems</td></tr>
<tr><td style="padding:7px 10px;border-top:1px solid #e2e5f0"><code style="color:#6366f1;font-weight:600;font-family:JetBrains Mono,monospace;font-size:10px">::law</code></td><td style="padding:7px 10px;border-top:1px solid #e2e5f0">⚖️ Law</td><td style="padding:7px 10px;border-top:1px solid #e2e5f0;color:#94a3b8;font-size:10px">59 jurisdictions</td></tr>
<tr style="background:#fafbfe"><td style="padding:7px 10px;border-top:1px solid #e2e5f0"><code style="color:#6366f1;font-weight:600;font-family:JetBrains Mono,monospace;font-size:10px">::document</code></td><td style="padding:7px 10px;border-top:1px solid #e2e5f0">📄 Document</td><td style="padding:7px 10px;border-top:1px solid #e2e5f0;color:#94a3b8;font-size:10px">71 principles</td></tr>
</table>
</div>
<p style="color:#94a3b8;font-size:9px;margin-top:6px;font-family:JetBrains Mono,monospace">Replace gpt-5.2 with any model — claude-sonnet, deepseek-v3, llama3, etc.</p>
</div>

<div style="background:var(--surface,#fff);border:1px solid #e2e5f0;border-radius:16px;padding:20px;margin-bottom:16px;box-shadow:0 1px 3px rgba(15,23,42,.04)">
<div style="font-size:10px;font-family:JetBrains Mono,monospace;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px">🐙 PYTHON SDK</div>
<pre style="background:#f5f6fa;padding:14px;border-radius:10px;font-family:JetBrains Mono,monospace;font-size:11px;line-height:1.8;border:1px solid #e2e5f0;overflow-x:auto"><code><span style="color:#94a3b8"># OpenAI</span>
<span style="color:#6366f1">from</span> marl <span style="color:#6366f1">import</span> Marl, MarlConfig
ml = Marl.from_openai(<span style="color:#d97706">"sk-..."</span>, config=MarlConfig(
    mode=<span style="color:#d97706">"emergence"</span>, emergence_type=<span style="color:#d97706">"create"</span>
))
result = ml.run(<span style="color:#d97706">"Generate 10 movie loglines"</span>)

<span style="color:#94a3b8"># Anthropic</span>
ml = Marl.from_anthropic(<span style="color:#d97706">"sk-ant-..."</span>)

<span style="color:#94a3b8"># Ollama (local)</span>
ml = Marl.from_ollama(<span style="color:#d97706">"llama3.1"</span>)

<span style="color:#94a3b8"># Any OpenAI-compatible</span>
ml = Marl.from_openai_compatible(<span style="color:#d97706">"https://api.groq.com/openai/v1"</span>, <span style="color:#d97706">"key"</span>, <span style="color:#d97706">"gpt-oss-120b"</span>)</code></pre>
</div>

<div style="background:var(--surface,#fff);border:1px solid #e2e5f0;border-radius:16px;padding:20px;margin-bottom:16px;box-shadow:0 1px 3px rgba(15,23,42,.04)">
<div style="font-size:10px;font-family:JetBrains Mono,monospace;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px">🦞 OPENCLAW INTEGRATION</div>
<div style="display:grid;grid-template-columns:auto 1fr;gap:12px;align-items:start">
<div style="background:linear-gradient(135deg,#6366f1,#4f46e5);color:#fff;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;font-family:JetBrains Mono,monospace;flex-shrink:0">1</div>
<div><b style="font-size:11px;color:#0f172a">Install MARL</b><pre style="background:#f5f6fa;padding:8px 12px;border-radius:8px;font-family:JetBrains Mono,monospace;font-size:11px;margin:6px 0;border:1px solid #e2e5f0"><code style="color:#0d9488">docker run -p 8080:8080 vidraft/marl</code></pre></div>
<div style="background:linear-gradient(135deg,#6366f1,#4f46e5);color:#fff;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;font-family:JetBrains Mono,monospace;flex-shrink:0">2</div>
<div><b style="font-size:11px;color:#0f172a">Set config.json</b><pre style="background:#f5f6fa;padding:8px 12px;border-radius:8px;font-family:JetBrains Mono,monospace;font-size:11px;margin:6px 0;border:1px solid #e2e5f0"><code>{ <span style="color:#6366f1">"llm"</span>: { <span style="color:#6366f1">"baseURL"</span>: <span style="color:#d97706">"http://localhost:8080/v1"</span>, <span style="color:#6366f1">"model"</span>: <span style="color:#d97706">"gpt-5.2::create"</span> } }</code></pre></div>
<div style="background:linear-gradient(135deg,#6366f1,#4f46e5);color:#fff;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;font-family:JetBrains Mono,monospace;flex-shrink:0">3</div>
<div><b style="font-size:11px;color:#0f172a">Chat naturally</b><div style="color:#475569;font-size:10px;margin-top:4px">"Analyze this with MARL" · "Use MARL pharma mode for drug repositioning"</div></div>
</div>
</div>

<div style="background:var(--surface,#fff);border:1px solid #e2e5f0;border-radius:16px;padding:20px;margin-bottom:16px;box-shadow:0 1px 3px rgba(15,23,42,.04)">
<div style="font-size:10px;font-family:JetBrains Mono,monospace;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px">🏗️ ARCHITECTURE</div>
<pre style="background:#f5f6fa;padding:14px;border-radius:10px;font-family:JetBrains Mono,monospace;font-size:10px;line-height:1.7;border:1px solid #e2e5f0;overflow-x:auto"><code><span style="color:#0d9488">┌─ Your App ─────────────────────────────────────────┐</span>
│  OpenClaw / Cursor / Custom App / Any LLM Client   │
│  client = OpenAI(<span style="color:#e11d48">base_url=</span><span style="color:#d97706">"http://MARL:8080/v1"</span>)   │
<span style="color:#0d9488">└────────────────────┬───────────────────────────────┘</span>
                     │ HTTP (OpenAI API format)
                     ▼
<span style="color:#6366f1">┌─ MARL Middleware ──────────────────────────────────┐</span>
│  S1 Hypothesis → S2 Solver → S3 Auditor            │
│  → S4 Verifier → S5 Synthesizer                    │
│  <span style="color:#d97706">9 Emergence Engines · 5,538 Seeds</span>                  │
│  <span style="color:#16a34a">FINAL Bench: MA=0.694 vs ER=0.302 (70%+ ↑)</span>        │
<span style="color:#6366f1">└────────────────────┬───────────────────────────────┘</span>
                     │ API call (×5)
                     ▼
<span style="color:#94a3b8">┌─ Any LLM ──────────────────────────────────────────┐</span>
│  OpenAI · Anthropic · Gemini · DeepSeek · Ollama   │
<span style="color:#94a3b8">└────────────────────────────────────────────────────┘</span></code></pre>
</div>

<div style="background:var(--surface,#fff);border:1px solid #e2e5f0;border-radius:16px;padding:20px;margin-bottom:16px;box-shadow:0 1px 3px rgba(15,23,42,.04)">
<div style="font-size:10px;font-family:JetBrains Mono,monospace;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px">📡 SUPPORTED BACKENDS</div>
<div style="overflow-x:auto">
<table style="width:100%;border-collapse:separate;border-spacing:0;font-size:11px;border-radius:10px;overflow:hidden;border:1px solid #e2e5f0">
<tr style="background:#f5f6fa"><th style="text-align:left;padding:8px 10px;font-family:JetBrains Mono,monospace;font-size:8px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px">Backend</th><th style="text-align:left;padding:8px 10px;font-family:JetBrains Mono,monospace;font-size:8px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px">Models</th></tr>
<tr style="background:rgba(99,102,241,.06)"><td style="padding:8px 10px;border-top:1px solid #e2e5f0;font-weight:700;color:#6366f1">⭐ Groq (Default)</td><td style="padding:8px 10px;border-top:1px solid #e2e5f0;font-weight:600">gpt-oss-120b, Llama 4, DeepSeek-R1, QwQ-32b</td></tr>
<tr><td style="padding:8px 10px;border-top:1px solid #e2e5f0">OpenAI</td><td style="padding:8px 10px;border-top:1px solid #e2e5f0">GPT-5.2, GPT-4.1, o4-mini</td></tr>
<tr style="background:#fafbfe"><td style="padding:8px 10px;border-top:1px solid #e2e5f0">Anthropic</td><td style="padding:8px 10px;border-top:1px solid #e2e5f0">Claude Opus 4, Sonnet 4</td></tr>
<tr><td style="padding:8px 10px;border-top:1px solid #e2e5f0">Google Gemini</td><td style="padding:8px 10px;border-top:1px solid #e2e5f0">Gemini 2.5 Pro / Flash</td></tr>
<tr style="background:#fafbfe"><td style="padding:8px 10px;border-top:1px solid #e2e5f0">DeepSeek</td><td style="padding:8px 10px;border-top:1px solid #e2e5f0">V3 / R1</td></tr>
<tr><td style="padding:8px 10px;border-top:1px solid #e2e5f0">xAI</td><td style="padding:8px 10px;border-top:1px solid #e2e5f0">Grok-3 / 4</td></tr>
<tr style="background:#fafbfe"><td style="padding:8px 10px;border-top:1px solid #e2e5f0">Ollama</td><td style="padding:8px 10px;border-top:1px solid #e2e5f0">Llama, Mistral, Phi, Qwen</td></tr>
<tr><td style="padding:8px 10px;border-top:1px solid #e2e5f0">Custom</td><td style="padding:8px 10px;border-top:1px solid #e2e5f0">Any OpenAI-compatible endpoint</td></tr>
</table>
</div>
</div>

<div style="text-align:center;padding:16px;background:#f5f6fa;border:1px solid #e2e5f0;border-radius:10px">
<p style="font-size:11px;color:#6366f1;margin:0;font-weight:700;font-family:JetBrains Mono,monospace">MARL · Model-Agnostic Runtime Middleware</p>
<p style="font-size:9px;color:#94a3b8;margin:4px 0 0;font-family:JetBrains Mono,monospace">pip install marl-middleware · Apache 2.0 · <b style="color:#475569">VIDRAFT.net</b></p>
</div>

</div>''')

        gr.HTML('<div style="text-align:center;padding:20px 0 8px;border-top:1px solid #e2e5f0;margin-top:16px"><p style="font-family:JetBrains Mono,monospace;font-size:8px;color:#94a3b8;letter-spacing:1px"><b style="color:#6366f1">MARL</b> · Model-Agnostic Runtime Middleware · S1→S2→S3→S4→S5 · Apache 2.0 · <b style="color:#475569">VIDRAFT.net</b></p></div>')

    return app

print("  Creating Gradio app...")
try:
    app = create_app()
    print("  ✅ App created successfully")
except Exception as e:
    print(f"  ❌ App creation failed: {e}")
    traceback.print_exc()
    sys.exit(1)

if __name__ == "__main__":
    print("  🚀 Launching on 0.0.0.0:7860 ...")
    try:
        app.launch(server_name="0.0.0.0", server_port=7860, ssr_mode=False)
    except TypeError:
        # ssr_mode not supported in this gradio version
        app.launch(server_name="0.0.0.0", server_port=7860)