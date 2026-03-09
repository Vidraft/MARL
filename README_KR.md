<div align="center">

# MARL — Model-Agnostic Runtime Middleware for LLMs

**파인튜닝·RAG에 이은 제3의 접근법 — 추론 과정 자체의 구조를 바꾸는 AI 미들웨어**

[![PyPI](https://img.shields.io/pypi/v/marl-middleware?color=6366f1&label=PyPI)](https://pypi.org/project/marl-middleware/)
[![License](https://img.shields.io/badge/License-Apache%202.0-0d9488)](LICENSE)
[![HuggingFace](https://img.shields.io/badge/🤗%20Demo-HuggingFace-ff9d00)](https://huggingface.co/spaces/VIDraft/MARL)
[![FINAL Bench](https://img.shields.io/badge/🏆%20FINAL%20Bench-Global%20%235-16a34a)](https://huggingface.co/spaces/FINAL-Bench/Leaderboard)

`pip install marl-middleware` · `docker run vidraft/marl`

**모든 LLM에 즉시 적용 가능한 다단계 멀티 에이전트 추론 파이프라인**

</div>

---

## MARL이란?

MARL(Model-Agnostic Runtime Middleware)은 **하나의 LLM 호출을 다수의 독립적인 전문가 역할로 분화시키는 다단계 멀티 에이전트 추론 파이프라인**입니다.

기존 LLM 품질 개선 방법은 **파인튜닝(재학습)** 또는 **RAG(검색 증강 생성)** 이 주류였습니다. 그러나 파인튜닝은 수천만 원 이상의 GPU 비용과 수 주의 학습 시간이 필요하고, RAG는 외부 지식을 보강할 뿐 모델의 추론 능력 자체를 개선하지 못합니다.

MARL은 **모델 가중치를 건드리지 않고 런타임에서 추론 과정의 구조를 재설계하는 제3의 접근법**입니다. 어떤 LLM이든 — GPT-5.4, Claude Opus, Gemini, DeepSeek, Llama, 또는 로컬 오픈소스 모델까지 — 코드 한 줄로 MARL을 적용할 수 있으며, 모델을 전환하더라도 효과는 그대로 유지됩니다.

```
┌─ 당신의 앱 ────────────────────────────────────────┐
│  OpenClaw / Cursor / 커스텀 앱 / 모든 LLM 클라이언트 │
│  client = OpenAI(base_url="http://MARL:8080/v1")    │
└────────────────────┬───────────────────────────────┘
                     │ HTTP (OpenAI API 포맷)
                     ▼
┌─ MARL Middleware ──────────────────────────────────┐
│  다단계 멀티 에이전트 추론 파이프라인                  │
│  9개 창발 엔진 · 환각 70%+ 감소                      │
│  FINAL Bench: MA=0.694 vs ER=0.302                  │
└────────────────────┬───────────────────────────────┘
                     │ API 호출
                     ▼
┌─ 모든 LLM ─────────────────────────────────────────┐
│  GPT-5.4 · Claude · Gemini · DeepSeek · Ollama …   │
└─────────────────────────────────────────────────────┘
```

---

## 왜 MARL인가?

### 문제: AI는 틀려도 자신 있게 답하고, 스스로 멈추지 못한다

**메타인지(metacognition)** 란 AI가 자기 답변이 틀렸을 가능성을 인식하고 스스로 교정하는 능력입니다. 세계 최초 AI 메타인지 벤치마크 **FINAL Bench** 연구 결과, GPT-5.2·Claude Opus 4.6·Gemini 3 Pro 등 현존 최고 모델들조차 자기 교정 능력이 심각하게 부족한 것으로 확인되었습니다.

현재 LLM은 자기 회귀(autoregressive) 구조상 한번 답변 생성을 시작하면, 앞의 토큰이 뒤의 토큰을 결정하므로 중간에 "내가 틀렸다"고 멈추고 방향을 바꿀 수 없습니다.

### 해결: 다단계 독립 전문가 파이프라인

MARL은 하나의 질문을 다수의 독립된 전문가 에이전트가 순차적으로 처리합니다. 한 명의 요리사가 혼자 모든 것을 처리하는 것이 아니라, 레시피 기획자가 최적의 접근법을 설계하고, 메인 셰프가 요리하고, 품질 검사관이 검수하고, 미슐랭 심사관이 최종 평가하는 구조입니다.

각 에이전트는 서로 다른 역할과 관점을 가지며, **가설 탐색 → 핵심 해결 → 정합성 감사 → 적대적 검증 → 메타인지 통합** 과정을 거쳐 단일 모델 호출에서는 도출되지 않는 새로운 관점과 자기 교정 능력을 구현합니다.

이 구조는 기존 LLM의 근본적 한계를 두 가지 방식으로 해소합니다:

- **창발적 추론**: 단일 모델 호출에서는 도출되지 않는 새로운 관점이 다단계 상호작용을 통해 나타납니다.
- **구조적 자기 교정**: 기존 LLM은 한번 답변 생성을 시작하면 스스로 방향을 바꾸지 못하지만, MARL은 적대적 검증 단계에서 초안의 오류를 재검토하고, 최종 통합 단계에서 이를 반영한 완전히 새로운 답변을 작성합니다.

---

## 성과

| 지표 | 값 |
|------|-----|
| 환각 감소율 | **70%+** (FINAL Bench 실증) |
| 자기교정 기여율 | **94.8%** (Error Recovery가 전체 개선의 94.8%) |
| FINAL Bench MA vs ER | **0.694 vs 0.302** |
| FINAL Bench 데이터셋 순위 | **HuggingFace 글로벌 인기 5위** |
| 월간 활성 이용자(MAU) | **200만 명** |
| 공개 AI 모델·도구 | **1,500개 이상** |
| HuggingFace STAR AI | **2024 Top 12 선정 (한국 유일)** |
| FACTS Grounding | **Google DeepMind 리더보드 세계 2위** |

---

## 설치

### pip (Linux x86_64 / Python 3.12)

```bash
pip install marl-middleware
```

### Docker (모든 OS — Mac · Windows · Linux)

```bash
docker run -p 8080:8080 vidraft/marl
```

### HuggingFace Space (설치 없이 체험)

> [https://huggingface.co/spaces/VIDraft/MARL](https://huggingface.co/spaces/VIDraft/MARL)

---

## 사용법

### Python SDK

```python
from marl import Marl, MarlConfig

# OpenAI
ml = Marl.from_openai("sk-...", config=MarlConfig(
    mode="emergence", emergence_type="create"
))
result = ml.run("영화 시놉시스 10개 만들어라")
print(result.answer)

# Anthropic
ml = Marl.from_anthropic("sk-ant-...", model="claude-sonnet-4-20250514")

# Ollama (로컬)
ml = Marl.from_ollama("llama3.1")

# Groq (무료)
ml = Marl.from_openai_compatible(
    "https://api.groq.com/openai/v1", "gsk-...", "openai/gpt-oss-120b"
)

# 모든 OpenAI-호환 API (DeepSeek, xAI, Friendli 등)
ml = Marl.from_openai_compatible("https://api.deepseek.com/v1", "key", "deepseek-v3")
```

### 1줄 연동 (모든 LLM 앱)

기존 코드에서 `base_url` **한 줄만 추가**하면 모든 호출이 MARL 파이프라인을 거칩니다:

```python
# Before
client = OpenAI(api_key="sk-...")

# After — 이 한 줄만 추가
client = OpenAI(api_key="sk-...", base_url="http://localhost:8080/v1")
```

---

## 모든 LLM 지원

MARL은 **모델 비종속(Model-Agnostic)** 미들웨어입니다. OpenAI API 포맷을 지원하는 모든 LLM에 즉시 적용됩니다. 특정 모델에 종속되지 않으므로, 더 좋은 모델이 출시되면 즉시 전환할 수 있습니다.

```
OpenAI        — GPT-5.4, GPT-5.2, GPT-4.1, o4-mini, GPT-OSS-120B
Anthropic     — Claude Opus 4.6, Sonnet 4.6, Haiku 4.5
Google        — Gemini 3.1 Pro, Gemini 3 Flash, Gemini 2.5 Pro/Flash
DeepSeek      — DeepSeek-V3, DeepSeek-R1, R2
xAI           — Grok-4, Grok-3
Groq          — gpt-oss-120b, Llama 4, DeepSeek-R1, QwQ-32b (무료)
Meta          — Llama 4 Scout/Maverick
Alibaba       — Qwen3.5 시리즈
Ollama        — 모든 로컬 오픈소스 모델
Custom        — OpenAI API 포맷을 지원하는 모든 엔드포인트
```

> 위 목록은 예시입니다. **OpenAI API 포맷을 지원하는 모든 LLM에 코드 변경 없이 적용됩니다.**

---

## 9개 창발 엔진

MARL은 기본 추론 강화(Insight) 모드 외에 **9개 전문 창발 엔진**을 내장하고 있습니다. 각 엔진은 해당 분야의 전문 지식 매트릭스와 독자적인 창발 규칙(emergence rules)을 기반으로, 단일 LLM에서는 불가능한 도메인 특화 아이디어를 생성합니다.

| 엔진 | 특장점 |
|------|--------|
| 🔧 **Invent** | 기술 융합 기반 발명 아이디어 생성. TRIZ 원리, 바이오 패턴, 모순 해결 전략을 교차 적용하여 특허 수준의 발명 컨셉 도출 |
| ✨ **Create** | 범용 창작 엔진. 클리셰 반전, 패러독스, 장르 융합, 감각 충돌, 문화 융합 등 다차원 자극으로 세상에 없던 아이디어 생성 |
| 🍳 **Recipe** | 요리 창발 엔진. 조리법×텍스처×구조×양념 문법을 교차하여 새로운 요리 컨셉 개발. 맛 화학 검증 내장 |
| 💊 **Pharma** | 신약·화합물 아이디어 발상. 드러그 리포지셔닝, 메커니즘 교차, 전달 혁신, 다중 타겟 설계, 스캐폴드 호핑 |
| 🧬 **Genomics** | 유전체·바이오 창발. 경로 크로스톡, 합성 치사, 표현형 브릿징, 기술 플랫폼 이전 |
| 🧪 **Chemistry** | 화학·소재 창발. 상반 물성 동시 달성, 나노↔거시 스케일 전환, 바이오모방, 폐기물→고부가가치 전환 |
| 🌍 **Ecology** | 생태·환경 창발. 보전 성공 모델 이전, 종 보호 네트워크 효과, 위협→자원 전환, 생태계 서비스 스태킹 |
| ⚖️ **Law** | 법률·규제 창발. 법역 간 프레임워크 이식, 규제 방식 전환, 신기술×기존법 충돌 해결, 법적 도구 혁신 |
| 📄 **Document** | 보고서·공문서 작성 엔진. 구조화된 작문 원칙과 정책 딜레마 기반으로 메타인지적 문서 생성 |

### 모드 전환

`model` 이름에 `::mode`를 붙이면 모드가 전환됩니다:

```
model="gpt-5.4"             →  🔬 Insight (기본 — 팩트체크·전략분석)
model="gpt-5.4::invent"     →  🔧 Invent
model="gpt-5.4::create"     →  ✨ Create
model="gpt-5.4::recipe"     →  🍳 Recipe
model="gpt-5.4::pharma"     →  💊 Pharma
model="gpt-5.4::genomics"   →  🧬 Genomics
model="gpt-5.4::chemistry"  →  🧪 Chemistry
model="gpt-5.4::ecology"    →  🌍 Ecology
model="gpt-5.4::law"        →  ⚖️ Law
model="gpt-5.4::document"   →  📄 Document
```

> `gpt-5.4` 자리에 아무 모델명을 사용할 수 있습니다.

---

## OpenClaw 연동

MARL은 **OpenClaw의 두뇌 역할**을 합니다. OpenClaw이 행동(이메일, 파일, 일정)을 실행하기 전에 MARL이 먼저 깊이 생각합니다.

```bash
# Step 1: MARL 로컬 설치
docker run -p 8080:8080 vidraft/marl

# Step 2: OpenClaw config.json 설정
{
  "llm": {
    "baseURL": "http://localhost:8080/v1",
    "model": "gpt-5.4::create"
  }
}

# Step 3: 채팅에서 자연어로 모드 전환
"MARL 창작 모드로 아이디어 10개 만들어줘"
"MARL 신약 모드로 리포지셔닝 후보 찾아줘"
```

---

## 기술 보호

MARL의 핵심 추론 엔진(다단계 파이프라인, 가중 어텐션 행렬, 에이전트 프롬프트)은 **컴파일된 바이너리(.so)로 제공**되어 독자적 기술을 보호합니다. 동시에 설치, 테스트, 구성, API 연동에 필요한 인터페이스 코드와 데모 환경은 공개하여 누구나 즉시 체험하고 자신의 환경에 통합할 수 있습니다.

---

## 비드래프트 소개

**비드래프트(VIDRAFT)** 는 2030년 이내에 True-AGI 개발을 목표로 2024년 설립된 AI 스타트업입니다. 서울AI허브 입주 기업이며, LLM의 메타인지 강화와 멀티 에이전트 추론 기술을 연구합니다.

| 항목 | 실적 |
|------|------|
| FINAL Bench | 세계 최초 AI 메타인지 벤치마크, HF 글로벌 인기 5위 |
| FINAL Bench Leaderboard | HuggingFace '금주의 스페이스' 선정 |
| HuggingFace 히트맵 리더보드 | 글로벌 4위 |
| STAR AI Top 12 | 2024년 선정 (한국 유일 기업) |
| 의료 AI | Google DeepMind FACTS Grounding 세계 2위 |
| MAU | 200만 명 |
| 누적 방문자 | 3,000만 명 이상 |
| 공개 AI 모델·도구 | 1,500개 이상 |
| NIPA H200 GPU×8 | 국가 AI 인프라 지원 선정 |
| 서울AI허브 | 입주 기업 |
| NH오픈이노베이션 | 2025 선정 |
| 보도 | 서울신문, 아시아경제, IT조선 등 |

---

## 향후 계획

- **MARL 엔터프라이즈 에디션** — 프라이빗 배포, 커스텀 파이프라인, SLA 지원 (2026 상반기)
- **FINAL Bench 기반 검증 논문** — 국제 학술지 투고
- **미국 시장 진출** — 실리콘밸리 파트너십 프로그램 참여
- **OpenClaw ClawHub 등록** — 247K+ 커뮤니티 대상 배포

---

## 링크

| | |
|---|---|
| 🌐 웹사이트 | [https://vidraft.net](https://vidraft.net) |
| 🤗 MARL 체험 | [https://huggingface.co/spaces/VIDraft/MARL](https://huggingface.co/spaces/VIDraft/MARL) |
| 🏆 FINAL Bench | [https://huggingface.co/spaces/FINAL-Bench/Leaderboard](https://huggingface.co/spaces/FINAL-Bench/Leaderboard) |
| 📦 PyPI | [https://pypi.org/project/marl-middleware/](https://pypi.org/project/marl-middleware/) |
| ✉️ 문의 | arxivgpt@gmail.com (김민식 대표) |

---

## 라이선스

Apache License 2.0 — Copyright 2025-2026 VIDRAFT / Vidraft Inc.

---

<div align="center">

**MARL** · Model-Agnostic Runtime Middleware for LLMs

*"모델을 바꾸는 것이 아니라, 모델이 생각하는 방식을 바꿉니다."*

— 김민식, 비드래프트 대표

</div>
