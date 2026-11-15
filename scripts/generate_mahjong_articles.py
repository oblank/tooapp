#!/usr/bin/env python3
"""Generate the bilingual Mahjong AI SEO article set.

Renders one static, SEO-ready HTML page per article from the structured,
bilingual content in ``scripts/mahjong_content``. Also regenerates the
articles hub page and rewrites ``sitemap.xml`` so the new pages are indexable.

Usage:
    python3 scripts/generate_mahjong_articles.py
"""

from __future__ import annotations

import html
import json
from pathlib import Path

from mahjong_content import ALL_ARTICLES, CATEGORIES, APP

ROOT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = ROOT / "articles"
SITEMAP = ROOT / "sitemap.xml"
FEED = ROOT / "feed.xml"
SITE = "https://tooapp.com"
PUBLISHED = "2026-11-15"

APP_STORE = "https://apps.apple.com/cn/app/id6758575182"
APP_PAGE = "/apps/mahjong-ai.html"
APP_ICON = "/assets/img/apps/mahjong-ai/icon.jpg"
OG_IMAGE = SITE + APP_ICON

APPLE_SVG = (
    '<svg class="icon-apple" viewBox="0 0 24 24" aria-hidden="true"><path d="M18.71 19.5c-.83 '
    "1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32"
    "-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 "
    "3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 "
    "3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 "
    '1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/></svg>'
)


# ── Page-specific styles (mirrors the existing article page) ──────────────
PAGE_STYLE = """<style>
    .article-hero {
      padding-block: var(--sp-16) var(--sp-12);
      background: linear-gradient(160deg,
        color-mix(in srgb, #FF9F0A 8%, var(--surface)) 0%,
        var(--surface) 100%);
    }
    .article-hero-inner { max-width: 760px; }
    .article-eyebrow {
      font-size: var(--size-sm);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #FF9F0A;
      margin-bottom: var(--sp-4);
    }
    .article-hero-title {
      font-size: clamp(var(--size-2xl), 4vw, var(--size-4xl));
      margin-bottom: var(--sp-6);
    }
    .article-hero-summary {
      font-size: var(--size-md);
      color: var(--text-secondary);
      margin-bottom: var(--sp-8);
      max-width: 58ch;
    }
    .article-meta {
      font-size: var(--size-xs);
      color: var(--text-tertiary);
      margin-bottom: var(--sp-8);
    }
    .article-layout {
      display: grid;
      grid-template-columns: 1fr min(680px, 100%) 1fr;
      gap: var(--sp-8);
      padding-block: var(--sp-16);
    }
    .article-layout > * { grid-column: 2; }
    .prose h2 {
      font-size: var(--size-xl);
      margin-top: var(--sp-12);
      margin-bottom: var(--sp-4);
    }
    .prose h3 {
      font-size: var(--size-lg);
      margin-top: var(--sp-8);
      margin-bottom: var(--sp-3);
    }
    .prose p {
      font-size: var(--size-base);
      color: var(--text-secondary);
      margin-bottom: var(--sp-6);
      max-width: none;
    }
    .prose ul, .prose ol {
      margin-bottom: var(--sp-6);
      padding-left: var(--sp-6);
    }
    .prose li {
      font-size: var(--size-base);
      color: var(--text-secondary);
      margin-bottom: var(--sp-2);
    }
    .prose strong { color: var(--text-primary); }
    .app-callout {
      background: var(--surface-raised);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border-subtle);
      padding: var(--sp-6);
      display: flex;
      gap: var(--sp-4);
      align-items: flex-start;
      margin-block: var(--sp-8);
    }
    .app-callout-icon {
      width: 64px;
      height: 64px;
      border-radius: 14px;
      flex-shrink: 0;
      object-fit: cover;
    }
    .app-callout-body { flex: 1; }
    .app-callout-name {
      font-size: var(--size-lg);
      font-weight: 700;
      margin-bottom: var(--sp-1);
    }
    .app-callout-desc {
      font-size: var(--size-sm);
      color: var(--text-secondary);
      margin-bottom: var(--sp-4);
      max-width: none;
    }
    .app-callout .cta-group { flex-wrap: wrap; }
    .tip-box {
      background: color-mix(in srgb, #FF9F0A 8%, var(--surface));
      border-left: 4px solid #FF9F0A;
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
      padding: var(--sp-4) var(--sp-6);
      margin-block: var(--sp-6);
    }
    .tip-box p { margin-bottom: 0; font-size: var(--size-sm); }
    .tip-label {
      font-size: var(--size-xs);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #FF9F0A;
      margin-bottom: var(--sp-2);
    }
    .breadcrumb {
      font-size: var(--size-xs);
      color: var(--text-tertiary);
      padding-block: var(--sp-4);
      display: flex;
      gap: var(--sp-2);
      align-items: center;
    }
    .breadcrumb a { color: var(--text-secondary); }
    .breadcrumb a:hover { color: var(--blue); }
    .breadcrumb-sep { color: var(--text-tertiary); }
    @media (max-width: 768px) {
      .app-callout { flex-direction: column; }
      .article-layout { grid-template-columns: 1fr; padding-inline: var(--sp-4); }
      .article-layout > * { grid-column: 1; }
    }
  </style>"""


HUB_STYLE = """<style>
    .hub-hero { padding-block: var(--sp-16) var(--sp-10); background: linear-gradient(160deg, color-mix(in srgb, #FF9F0A 8%, var(--surface)) 0%, var(--surface) 100%); }
    .hub-hero-inner { max-width: 760px; }
    .hub-eyebrow { font-size: var(--size-sm); font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #FF9F0A; margin-bottom: var(--sp-4); }
    .hub-title { font-size: clamp(var(--size-2xl), 4vw, var(--size-4xl)); margin-bottom: var(--sp-6); }
    .hub-sub { font-size: var(--size-md); color: var(--text-secondary); max-width: 58ch; }
    .hub-wrap { max-width: 820px; margin-inline: auto; padding-block: var(--sp-12); }
    .hub-group { margin-bottom: var(--sp-10); }
    .hub-group h2 { font-size: var(--size-xl); margin-bottom: var(--sp-4); }
    .hub-list { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-2) var(--sp-6); }
    .hub-list li { padding: var(--sp-2) 0; border-bottom: 1px solid var(--border-subtle); }
    .hub-list a { color: var(--text-secondary); font-size: var(--size-sm); }
    .hub-list a:hover { color: var(--blue); }
    @media (max-width: 640px) { .hub-list { grid-template-columns: 1fr; } }
  </style>"""


def attr(text: str) -> str:
    """Escape text for use inside an HTML attribute."""
    return html.escape(text, quote=True)


def dual(zh: str, en: str, tag: str = "span") -> str:
    """Render an element whose text swaps with the site language toggle."""
    return f'<{tag} data-zh="{attr(zh)}" data-en="{attr(en)}">{zh}</{tag}>'


def header_nav() -> str:
    return """<header class="site-header">
  <div class="container header-inner">
    <a href="/" class="logo" aria-label="Too Apps 首页">
      <span class="logo-mark">Too</span>
      <span class="logo-mark">Apps</span>
    </a>
    <nav class="site-nav" aria-label="主导航">
      <a href="/#apps" data-zh="全部应用" data-en="All Apps">全部应用</a>
      <a href="/articles/" data-zh="麻将文章" data-en="Mahjong Articles">麻将文章</a>
      <a href="/apps/mahjong-ai.html" data-zh="Mahjong AI" data-en="Mahjong AI">Mahjong AI</a>
    </nav>
    <button class="lang-toggle" aria-label="Switch language / 切换语言" type="button">
      <span class="lang-zh" aria-hidden="true">EN</span>
      <span class="lang-en" aria-hidden="true">中文</span>
    </button>
  </div>
</header>"""


FOOTER = """<footer class="site-footer">
  <div class="container footer-inner">
    <div class="footer-brand">
      <a href="/" class="logo" aria-label="Too Apps 首页">
        <span class="logo-mark">Too</span><span class="logo-mark">Apps</span>
      </a>
      <p class="footer-tagline" data-zh="独立开发 · 用心打磨" data-en="Indie crafted · Made with care">独立开发 · 用心打磨</p>
    </div>
    <nav class="footer-nav" aria-label="页脚导航">
      <a href="/" data-zh="首页" data-en="Home">首页</a>
      <a href="/articles/" data-zh="麻将文章" data-en="Mahjong Articles">麻将文章</a>
      <a href="/apps/mahjong-ai.html" data-zh="Mahjong AI" data-en="Mahjong AI">Mahjong AI</a>
      <a href="/apps/noteit.html" data-zh="Noteit" data-en="Noteit">Noteit</a>
      <a href="/apps/rss-reader.html" data-zh="知了" data-en="知了 RSS">知了</a>
    </nav>
    <p class="footer-legal">
      <span data-zh="© 2026 oBlank. 保留所有权利。" data-en="© 2026 Yuhao Deng. All rights reserved.">© 2026 oBlank. 保留所有权利。</span>
    </p>
  </div>
</footer>"""


def app_callout(desc_zh: str, desc_en: str, btn_zh: str, btn_en: str, detail: bool = True) -> str:
    detail_link = (
        f'\n          <a href="{APP_PAGE}" class="btn btn-card-detail" '
        f'data-zh="查看详情" data-en="Learn More">查看详情</a>'
        if detail
        else ""
    )
    return f"""<div class="app-callout">
      <img class="app-callout-icon" src="{APP_ICON}" alt="Mahjong AI app icon" width="64" height="64" loading="lazy">
      <div class="app-callout-body">
        <p class="app-callout-name">Mahjong AI</p>
        <p class="app-callout-desc" data-zh="{attr(desc_zh)}" data-en="{attr(desc_en)}">{desc_zh}</p>
        <div class="cta-group">
          <a href="{APP_STORE}" class="btn btn-store" target="_blank" rel="noopener"
             aria-label="在 App Store 下载 Mahjong AI">
            {APPLE_SVG}
            <span data-zh="{attr(btn_zh)}" data-en="{attr(btn_en)}">{btn_zh}</span>
          </a>{detail_link}
        </div>
      </div>
    </div>"""


def render_article(a: dict) -> str:
    title_zh, title_en = a["title"]
    eyebrow_zh, eyebrow_en = a["eyebrow"]
    sum_zh, sum_en = a["summary"]
    desc_zh, desc_en = a["desc"]
    cat = CATEGORIES[a["cat"]]
    url = f"{SITE}/articles/{a['slug']}.html"
    doc_title = f"{title_zh} | {title_en}"
    meta_desc = f"{desc_zh} | {desc_en}"

    ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title_zh,
        "description": desc_zh,
        "url": url,
        "datePublished": PUBLISHED,
        "dateModified": PUBLISHED,
        "inLanguage": "zh-Hans",
        "articleSection": cat[0],
        "author": {
            "@type": "Person",
            "name": "Yuhao Deng",
            "alternateName": "oBlank",
            "url": f"{SITE}/",
        },
        "publisher": {"@type": "Organization", "name": "Too Apps", "url": f"{SITE}/"},
        "isPartOf": {"@type": "WebSite", "name": "Too Apps", "url": f"{SITE}/"},
    }

    # Body: intro paragraphs, then sections
    body_parts = []
    for zh, en in a["intro"]:
        body_parts.append(f"\n      {dual(zh, en, 'p')}\n")

    for sec in a["sections"]:
        h_zh, h_en = sec["h"]
        body_parts.append(f"\n      <h2 data-zh=\"{attr(h_zh)}\" data-en=\"{attr(h_en)}\">{h_zh}</h2>\n")
        for zh, en in sec["p"]:
            body_parts.append(f"\n      {dual(zh, en, 'p')}\n")

    tip_zh, tip_en = a["tip"]
    body_parts.append(
        f"""
      <div class="tip-box">
        <p class="tip-label" data-zh="实战提示" data-en="Practical Tip">实战提示</p>
        <p data-zh="{attr(tip_zh)}" data-en="{attr(tip_en)}">{tip_zh}</p>
      </div>
"""
    )

    # Recommendation block (shared app pitch, tailored lead-in)
    lead_zh = f"想把上面的内容变成真正的牌技？本文提到的思路，<a href='{APP_PAGE}'>Mahjong AI</a> 都能在实战中帮你落地。"
    lead_en = (
        f"Want to turn these ideas into real skill? <a href='{APP_PAGE}'>Mahjong AI</a> "
        "helps you apply them at the table."
    )
    feats = "".join(
        f'\n        <li data-zh="{attr(f[0])}" data-en="{attr(f[1])}">{f[0]}</li>'
        for f in APP["features"]
    )
    body_parts.append(
        f"""
      <h2 data-zh="推荐工具：Mahjong AI" data-en="Recommended Tool: Mahjong AI">推荐工具：Mahjong AI</h2>

      <p data-zh="{attr(lead_zh)}" data-en="{attr(lead_en)}">{lead_zh}</p>

      <ul>{feats}
      </ul>

      {app_callout(APP["cta_bottom_zh"], APP["cta_bottom_en"], "在 App Store 下载", "Download on App Store")}
"""
    )

    for zh, en in a["concl"]:
        body_parts.append(f"\n      {dual(zh, en, 'p')}\n")

    body = "".join(body_parts)

    return f"""<!DOCTYPE html>
<html lang="zh-Hans" data-lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Primary Meta -->
  <title>{html.escape(doc_title)}</title>
  <meta name="description" content="{attr(meta_desc)}">
  <meta name="author" content="Yuhao Deng · oBlank">

  <!-- Canonical & hreflang -->
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="zh-Hans" href="{url}">
  <link rel="alternate" hreflang="en" href="{url}">
  <link rel="alternate" hreflang="x-default" href="{url}">
  <link rel="alternate" type="application/rss+xml" title="麻将文章 · Mahjong Articles" href="/feed.xml">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{attr(doc_title)}">
  <meta property="og:description" content="{attr(desc_zh)}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:locale" content="zh_CN">
  <meta property="og:locale:alternate" content="en_US">
  <meta property="og:site_name" content="Too Apps">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{attr(doc_title)}">
  <meta name="twitter:description" content="{attr(desc_en)}">
  <meta name="twitter:image" content="{OG_IMAGE}">

  <!-- Theme -->
  <meta name="theme-color" content="#FF9F0A">
  <link rel="icon" type="image/svg+xml" href="/assets/img/favicon.svg">

  <!-- Structured Data -->
  <script type="application/ld+json">
  {json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>

  <link rel="stylesheet" href="/assets/css/site.css">
  {PAGE_STYLE}
</head>
<body>

<!-- ===================== HEADER ===================== -->
{header_nav()}

<!-- ===================== BREADCRUMB ===================== -->
<div class="container">
  <nav class="breadcrumb" aria-label="面包屑导航">
    <a href="/" data-zh="首页" data-en="Home">首页</a>
    <span class="breadcrumb-sep" aria-hidden="true">/</span>
    <a href="/articles/" data-zh="麻将文章" data-en="Mahjong Articles">麻将文章</a>
    <span class="breadcrumb-sep" aria-hidden="true">/</span>
    <span aria-current="page" data-zh="{attr(title_zh)}" data-en="{attr(title_en)}">{title_zh}</span>
  </nav>
</div>

<!-- ===================== ARTICLE HERO ===================== -->
<section class="article-hero" aria-labelledby="article-heading">
  <div class="container article-hero-inner">
    <p class="article-eyebrow" data-zh="{attr(eyebrow_zh)}" data-en="{attr(eyebrow_en)}">{eyebrow_zh}</p>
    <h1 id="article-heading" class="article-hero-title">
      {dual(title_zh, title_en)}
    </h1>
    <p class="article-hero-summary" data-zh="{attr(sum_zh)}" data-en="{attr(sum_en)}">{sum_zh}</p>
    <p class="article-meta" data-zh="作者：oBlank · 2026年11月" data-en="By Yuhao Deng · November 2026">作者：oBlank · 2026年11月</p>

    <!-- Top CTA -->
    {app_callout(APP["cta_top_zh"], APP["cta_top_en"], "免费下载", "Free Download")}
  </div>
</section>

<!-- ===================== ARTICLE BODY ===================== -->
<main>
  <div class="article-layout">
    <article class="prose">{body}
    </article>
  </div>
</main>

<!-- ===================== FOOTER ===================== -->
{FOOTER}

<script src="/assets/js/site.js"></script>
</body>
</html>
"""


def render_hub() -> str:
    url = f"{SITE}/articles/"
    by_cat: dict[str, list[dict]] = {}
    for a in ALL_ARTICLES:
        by_cat.setdefault(a["cat"], []).append(a)

    blocks = []
    for key, (label_zh, label_en) in CATEGORIES.items():
        items = by_cat.get(key)
        if not items:
            continue
        links = "".join(
            f'\n          <li><a href="/articles/{a["slug"]}.html" '
            f'data-zh="{attr(a["title"][0])}" data-en="{attr(a["title"][1])}">{a["title"][0]}</a></li>'
            for a in items
        )
        blocks.append(
            f"""
      <section class="hub-group">
        <h2 data-zh="{attr(label_zh)}" data-en="{attr(label_en)}">{label_zh}</h2>
        <ul class="hub-list">{links}
        </ul>
      </section>"""
        )

    ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "麻将文章 · Mahjong Articles",
        "url": url,
        "inLanguage": "zh-Hans",
        "author": {"@type": "Person", "name": "Yuhao Deng", "alternateName": "oBlank", "url": f"{SITE}/"},
        "publisher": {"@type": "Organization", "name": "Too Apps", "url": f"{SITE}/"},
    }

    body = "".join(blocks)
    return f"""<!DOCTYPE html>
<html lang="zh-Hans" data-lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>麻将文章总览 | Mahjong Articles Hub</title>
  <meta name="description" content="100+ 篇麻将规则、玩法、番种、策略与 AI 教学文章，中英双语。升级你的麻将技术。| 100+ bilingual articles on mahjong rules, variants, scoring, strategy and AI coaching.">
  <meta name="author" content="Yuhao Deng · oBlank">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="zh-Hans" href="{url}">
  <link rel="alternate" hreflang="en" href="{url}">
  <link rel="alternate" hreflang="x-default" href="{url}">
  <link rel="alternate" type="application/rss+xml" title="麻将文章 · Mahjong Articles" href="/feed.xml">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="麻将文章总览 | Mahjong Articles Hub">
  <meta property="og:description" content="100+ 篇中英双语麻将文章：规则、玩法、番种、策略与 AI 教学。">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:locale" content="zh_CN">
  <meta property="og:locale:alternate" content="en_US">
  <meta property="og:site_name" content="Too Apps">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Mahjong Articles Hub">
  <meta name="twitter:description" content="100+ bilingual articles on mahjong rules, variants, scoring and strategy.">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <meta name="theme-color" content="#FF9F0A">
  <link rel="icon" type="image/svg+xml" href="/assets/img/favicon.svg">
  <script type="application/ld+json">
  {json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
  <link rel="stylesheet" href="/assets/css/site.css">
  {HUB_STYLE}
</head>
<body>
{header_nav()}
<div class="container">
  <nav class="breadcrumb" aria-label="面包屑导航">
    <a href="/" data-zh="首页" data-en="Home">首页</a>
    <span class="breadcrumb-sep" aria-hidden="true">/</span>
    <span aria-current="page" data-zh="麻将文章" data-en="Mahjong Articles">麻将文章</span>
  </nav>
</div>
<section class="hub-hero">
  <div class="container hub-hero-inner">
    <p class="hub-eyebrow" data-zh="麻将 · 规则 · 策略 · AI" data-en="Mahjong · Rules · Strategy · AI">麻将 · 规则 · 策略 · AI</p>
    <h1 class="hub-title" data-zh="麻将文章总览" data-en="Mahjong Articles Hub">麻将文章总览</h1>
    <p class="hub-sub" data-zh="从入门规则到地方玩法、番种算法与进阶策略，共 {len(ALL_ARTICLES)} 篇中英双语文章，帮你系统提升麻将技术。" data-en="From beginner rules to regional variants, scoring, and advanced strategy — {len(ALL_ARTICLES)} bilingual articles to level up your game.">
      从入门规则到地方玩法、番种算法与进阶策略，共 {len(ALL_ARTICLES)} 篇中英双语文章，帮你系统提升麻将技术。
    </p>
    {app_callout(APP["cta_top_zh"], APP["cta_top_en"], "免费下载", "Free Download")}
  </div>
</section>
<main class="container hub-wrap">
{body}
</main>
{FOOTER}
<script src="/assets/js/site.js"></script>
</body>
</html>
"""


# ── Sitemap ───────────────────────────────────────────────────────────────
STATIC_URLS = [
    (f"{SITE}/", "2026-10-08", "1.0", "weekly", True),
    (f"{SITE}/en/", "2026-06-23", "0.9", "weekly", True),
    (f"{SITE}/apps/noteit.html", "2026-06-23", "0.8", "monthly", False),
    (f"{SITE}/apps/rss-reader.html", "2026-06-23", "0.8", "monthly", False),
    (f"{SITE}/apps/mahjong-ai.html", "2026-06-23", "0.8", "monthly", False),
    (f"{SITE}/apps/fitpretty.html", "2026-06-23", "0.8", "monthly", False),
    (f"{SITE}/apps/photometa.html", "2026-10-08", "0.8", "monthly", False),
    (f"{SITE}/privacy/", "2026-06-23", "0.4", "yearly", False),
    (f"{SITE}/support/", "2026-06-23", "0.5", "monthly", False),
    (f"{SITE}/articles/ai-journal-app-for-reflection.html", "2026-06-24", "0.7", "weekly", False),
    (f"{SITE}/articles/rss-reader-for-information-overload.html", "2026-06-24", "0.7", "weekly", False),
    (f"{SITE}/articles/mahjong-assistant-practice-guide.html", "2026-06-24", "0.7", "weekly", False),
    (f"{SITE}/articles/fitness-app-for-body-transformation.html", "2026-06-24", "0.7", "weekly", False),
]


def write_sitemap() -> None:
    rows = list(STATIC_URLS)
    rows.insert(9, (f"{SITE}/articles/", PUBLISHED, "0.7", "weekly", False))
    for a in ALL_ARTICLES:
        rows.append((f"{SITE}/articles/{a['slug']}.html", PUBLISHED, "0.6", "monthly", False))

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
        "",
    ]
    for loc, lastmod, priority, freq, is_home in rows:
        parts.append("  <url>")
        parts.append(f"    <loc>{loc}</loc>")
        parts.append(f"    <lastmod>{lastmod}</lastmod>")
        parts.append(f"    <changefreq>{freq}</changefreq>")
        parts.append(f"    <priority>{priority}</priority>")
        if is_home:
            parts.append(f'    <xhtml:link rel="alternate" hreflang="zh-Hans" href="{SITE}/"/>')
            parts.append(f'    <xhtml:link rel="alternate" hreflang="en"      href="{SITE}/en/"/>')
            parts.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>')
        parts.append("  </url>")
        parts.append("")
    parts.append("</urlset>")
    parts.append("")
    SITEMAP.write_text("\n".join(parts), encoding="utf-8")


def write_feed() -> None:
    """Emit an RSS 2.0 feed for the article set (discovery + aggregators)."""
    pub = "Sat, 15 Nov 2026 00:00:00 +0800"
    items = []
    for a in ALL_ARTICLES:
        link = f"{SITE}/articles/{a['slug']}.html"
        desc = f"{a['summary'][0]} — {a['summary'][1]}"
        items.append(
            "    <item>\n"
            f"      <title>{html.escape(a['title'][0])}</title>\n"
            f"      <link>{link}</link>\n"
            f'      <guid isPermaLink="true">{link}</guid>\n'
            f"      <description>{html.escape(desc)}</description>\n"
            f"      <pubDate>{pub}</pubDate>\n"
            "    </item>"
        )
    feed = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        "    <title>麻将文章 · Mahjong Articles — Too Apps</title>\n"
        f"    <link>{SITE}/articles/</link>\n"
        "    <description>中英双语麻将文章：规则、地方玩法、番种算分、策略技巧与 AI 教学。"
        "Bilingual mahjong articles on rules, variants, scoring, strategy and AI.</description>\n"
        "    <language>zh-cn</language>\n"
        f'    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>\n'
        f"    <lastBuildDate>{pub}</lastBuildDate>\n"
        + "\n".join(items)
        + "\n  </channel>\n</rss>\n"
    )
    FEED.write_text(feed, encoding="utf-8")


def main() -> None:
    ARTICLES_DIR.mkdir(exist_ok=True)
    seen = set()
    for a in ALL_ARTICLES:
        slug = a["slug"]
        if slug in seen:
            raise SystemExit(f"duplicate slug: {slug}")
        seen.add(slug)
        (ARTICLES_DIR / f"{slug}.html").write_text(render_article(a), encoding="utf-8")

    (ARTICLES_DIR / "index.html").write_text(render_hub(), encoding="utf-8")
    write_sitemap()
    write_feed()

    print(f"generated {len(ALL_ARTICLES)} articles + hub page + sitemap + feed")


if __name__ == "__main__":
    main()
